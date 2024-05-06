#!/user/bin/env python
# -*- coding: utf-8 -*-
# ================================================================================
"""
    File name: pulsar.py
    Date Created: 2024-05-03
    Date Modified: 2024-05-06
    Python version: 3.11+
"""
__author__ = "Josh Wibberley (JMW)"
__copyright__ = "Copyright © 2024 JS Prodüksiyon"
__credits__ = ["Josh Wibberley"]
__license__ = "GNU GPL v3.0"
__version__ = "1.0.0"
__maintainer__ = ["Josh Wibberley"]
__email__ = "jmw@hawke-ai.com"
__status__ = "Development"
__languages__ = ['en','de','tr']  # languages the interface has been translated into.
__build__ = ''
# ================================================================================
# Check for python version
import sys

MIN_PYTHON = (3,11)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required to run Pulsar.\n" % MIN_PYTHON)

import os, locale
from nebula import Nebula
from PySide6 import QtCore, QtGui
from PySide6.QtCore import QTranslator, QLocale, QTranslator, QSize, QLibraryInfo, QCoreApplication
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon, QMainWindow, QDialog, QFileDialog
from PySide6.QtGui import QIcon, QAction
from utils import (errModal, infoModal, loadSettings, saveSettings)

# windows
from ui.pulsar_about_ui import Ui_AboutDialog
from ui.pulsar_status_ui import Ui_ConnStatusWindow
from ui.pulsar_main_ui import Ui_MainWindow

SETTINGS = loadSettings()


### Window Objects ###
class AboutWindow(QDialog):
    def __init__(self, parent=None):
        super(AboutWindow, self).__init__()

        self.ui = Ui_AboutDialog()
        self.ui.setupUi(self)

    def openWin(self):
        self.ui.retranslateUi()
        self.show()


class ConnStatusWindow(QMainWindow):
    def __init__(self, parent=None):
        super(ConnStatusWindow, self).__init__()

        self.ui = Ui_ConnStatusWindow()
        self.ui.setupUi(self)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # setup the UI
        self.loadLanguages(parent)
        self.aboutWin = AboutWindow(self)
        self.ui.configFilePath = SETTINGS['config']


        # hide the disconnect button on init
        self.ui.btnDisconnect.hide()

        # Menu Actions
        self.ui.actionAbout_Pulsar.triggered.connect(self.aboutWin.openWin)
        self.ui.actionQuit_2.triggered.connect(parent.quit)

        # link buttons
        # self.ui.btnConnect.released.connect()
        # self.ui.btnDisconnect.released.connect()
        self.ui.btnStatus.released.connect(self.showStatusWin)
        self.ui.btnConfigFileSelect.released.connect(self.getConfigFile)
        self.ui.btnSaveSettings.released.connect(self.saveSettingsBtn)

    def getConfigFile(self) -> None:
        """
        Opens a dialog that allows you to pick a config file and places the content into 
        the file path box
        """
        file = QFileDialog(self)
        file.setFileMode(QFileDialog.AnyFile)
        file.setNameFilter(self.tr('Nebula Config File (*.yml *.yaml)'))
        file.setViewMode(QFileDialog.Detail)
        if file.exec():
            self.ui.configFilePath.setText(file.selectedFiles()[0])


    def loadLanguages(self, parent=None):
        """
        Loads the languages into the combo box and retranslates the UI accordingly
        """
        # add languages to dropdown
        self.ui.cmbLanguages.clear()

        curLocale = QLocale()
        localeLangCode = curLocale.languageToCode(curLocale.language())

        # English is the default language, if we don't have the proper one in the locale
        if SETTINGS['language'] == localeLangCode and localeLangCode not in __languages__:
            SETTINGS['language'] = 'en'
            
        curLocale = QLocale(SETTINGS['language'])

        locale.setlocale(locale.LC_ALL, curLocale.name())

        self.langDict = {}
        langList = []
        
        for lang in __languages__:
            subLocale = QLocale(lang)
            lString = subLocale.nativeLanguageName()
            if 'English' in lString:
                lString = 'English'

            if lang != localeLangCode:
                lString = f"{lString} ({subLocale.languageToString(subLocale.language())})"

            self.langDict[lang] = lString
            langList.append(lString)

        self.ui.cmbLanguages.addItems(sorted(langList, key=locale.strxfrm))
        self.ui.cmbLanguages.setCurrentText(self.langDict[SETTINGS['language']])
        setLanguage(app, SETTINGS['language'])
        self.ui.retranslateUi(self)
        self.aboutWin.ui.retranslateUi(self.aboutWin)
        connWin.ui.retranslateUi(connWin)
        st.menu.retranslateUi()


    def noConfig(self) -> None:
        """
        Set up display for instance when no valid config file is found
        """
        self.ui.btnConnect.setDisabled(True)
        self.show()
        errModal(self, self.tr('No valid Nebula configuration file was found so the connection cannot be made.<br>Please set the path to a valid Nebula configuration file below to continue.'))


    def saveSettingsBtn(self) -> bool:
        """
        Saves the settings when clicking on the button
        """
        configFile = self.ui.configFilePath.text()
        # in Windows we need to make sure that the separators are \ not /
        if sys.platform == 'win32':
            if not os.sep in configFile:
                configFile = configFile.replace('/', os.sep)

        nebulaObj.setConfig(configFile)
        if nebulaObj.validConfig:
            SETTINGS['config'] = configFile
        else:
            errModal(self, 'Invalid Nebula configuration file selected. Please try again!')
            return False
        
        for lang in self.langDict:
            if self.ui.cmbLanguages.currentText() == self.langDict[lang]:
                SETTINGS['language'] = lang

        SETTINGS['tray_start'] = True if self.ui.checkTrayOnly.isChecked() else False
        SETTINGS['auto_connect'] = True if self.ui.checkAutostart.isChecked() else False

        saveSettings(SETTINGS)
        self.loadLanguages(app)
        return True

    def showStatusWin(self) -> None:
        """
        shows the status window
        """
        connWin.show()



# Primary driver is the System Tray Icon
class systemTray():
    """
    System Tray Icon
    """
    def __init__(self, parent, nebula=None) -> None:
        self.connected = False
        self.iconOn = QIcon(os.path.dirname(__file__) + '/ui/resources/pulsar-icon-16.png', size=QSize(16, 16))
        self.iconOn.addFile(os.path.dirname(__file__) + '/ui/resources/pulsar-icon-24.png', size=QSize(24, 24))
        self.iconOn.addFile(os.path.dirname(__file__) + '/ui/resources/pulsar-icon-32.png', size=QSize(32, 32))
        self.iconOff = QIcon(os.path.dirname(__file__) + '/ui/resources/pulsar-icon-gray-16.png', size=QSize(16, 16))
        self.iconOff.addFile(os.path.dirname(__file__) + '/ui/resources/pulsar-icon-gray-24.png', size=QSize(24, 24))
        self.iconOff.addFile(os.path.dirname(__file__) + '/ui/resources/pulsar-icon-gray-32.png', size=QSize(32, 32))
        self.trayObj = QSystemTrayIcon()
        self.trayObj.setIcon(self.iconOff)
        self.trayObj.setVisible(True)
        self.menu = systemTrayMenu(self)
        self.menu.quit.triggered.connect(parent.quit)
        self.menu.connItem.triggered.connect(self.nebulaConnect)
        self.menu.disconnItem.triggered.connect(self.nebulaDisconnect)
        self.menu.settingsWin.triggered.connect(self.showMainWin)
        self.menu.statusWin.triggered.connect(self.showStatusWin)
        self.trayObj.setContextMenu(self.menu)
        self.nebulaObj = nebula

    def connectStatusIcon(self) -> None:
        """
        Change icon depending on connection status
        """
        if self.connected:
            self.trayObj.setIcon(self.iconOn)
        elif not self.connected:
            self.trayObj.setIcon(self.iconOff)

    def nebulaConnect(self) -> None:
        """
        Enable connection 
        """
        if not self.connected:
            self.connected = True
            self.connectStatusIcon()

    def nebulaDisconnect(self) -> None:
        """
        Disable connection
        """
        if self.connected:
            self.connected = False
            self.connectStatusIcon()

    def retranslateUi(self) -> None:
        """
        Retranslates the interface
        """

    def showMainWin(self) -> None:
        """
        Display main window
        """
        mainWin.show()

    def showStatusWin(self) -> None:
        """
        Display Connection Status window
        """
        connWin.show()

class systemTrayMenu(QMenu):
    """
    Menu for the system Tray Icon
    """
    def __init__(self, parent=None):
        super(systemTrayMenu, self).__init__()
        
        self.connItem = QAction(self.tr('Connect to Nebula'))
        self.addAction(self.connItem)
        self.disconnItem = QAction(self.tr('Disconnect from Nebula'))
        self.addAction(self.disconnItem)
        self.addSeparator()
        self.statusWin = QAction(self.tr('Status...')) 
        self.addAction(self.statusWin)
        self.settingsWin = QAction(self.tr('Settings...'))
        self.addAction(self.settingsWin)
        self.addSeparator()
        self.quit = QAction(self.tr('Quit'))
        self.addAction(self.quit)
        self.retranslateUi()

    def retranslateUi(self):
        """
        translate the menu
        """
        self.connItem.setText(QCoreApplication.translate("SystemTray", u"Connect to Nebula", None))
        self.disconnItem.setText(QCoreApplication.translate("SystemTray", u"Disconnect from Nebula", None))
        self.statusWin.setText(QCoreApplication.translate("SystemTray", u"Status...", None))
        self.settingsWin.setText(QCoreApplication.translate("SystemTray", u"Settings...", None))
        self.quit.setText(QCoreApplication.translate("SystemTray", u"Quit", None))


def setLanguage(app, language) -> bool:
    """
    set interface language

    """
    if type(app) == QApplication:
        translator = QTranslator(app)
        translator.load(language, 'qtbase', '_', QLibraryInfo.path(QLibraryInfo.TranslationsPath))
        app.installTranslator(translator)
        translator = QTranslator(app)
        app.removeTranslator(translator)
        translator.load(os.path.dirname(__file__) + os.sep + 'translations' + os.sep + 'culmt_{}.qm'.format(language))
        app.installTranslator(translator)
        return True
    else:
        return False


if __name__ == '__main__':
    nebulaObj = Nebula()

    app = QApplication(sys.argv)
    app.setStyle('fusion')
    app.setQuitOnLastWindowClosed(False)

    setLanguage(app, SETTINGS['language'])

    st = systemTray(app)
    mainWin = MainWindow(app)
    connWin = ConnStatusWindow()
    
    if not os.path.exists(SETTINGS['config']):
        mainWin.noConfig()


    app.exec()
    