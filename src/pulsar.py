#!/user/bin/env python
# -*- coding: utf-8 -*-
# ================================================================================
"""
    File name: pulsar.py
    Date Created: 2024-05-03
    Date Modified: 2024-06-10
    Python version: 3.11+
"""
__author__ = "Josh Wibberley (JMW)"
__copyright__ = "Copyright © 2024 JS Prodüksiyon"
__credits__ = ["Josh Wibberley"]
__license__ = "GNU GPL v3.0"
__version__ = "1.0.1"
__maintainer__ = ["Josh Wibberley"]
__email__ = "jmw@hawke-ai.com"
__status__ = "Development"
__languages__ = ['en','de','tr']  # languages the interface has been translated into.
__nebula__ = '1.8.2'
__build__ = '2024-06-10 16:17'
__debugState__ = False
# ================================================================================
# Check for python version
import sys

MIN_PYTHON = (3,11)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required to run Pulsar.\n" % MIN_PYTHON)

# start application in Administrator mode
if not __debugState__:
    from elevate import elevate
    elevate()

# Now run the actual application
import os, locale
from functools import partial
from nebula import Nebula
from hostsfile import HostsFile
from PySide6 import QtCore, QtGui
from PySide6.QtCore import QTranslator, QLocale, QTranslator, QSize, QLibraryInfo, QCoreApplication
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon, QMainWindow, QDialog, QFileDialog, QDialogButtonBox
from PySide6.QtGui import QIcon, QAction
from utils import (errModal, infoModal, loadSettings, saveSettings, yesNoModal)

# resize screen automatically
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

# windows
from ui.pulsar_about_ui import Ui_AboutDialog
from ui.pulsar_hosts_ui import Ui_configHostsDialog
from ui.pulsar_main_ui import Ui_MainWindow
from ui.pulsar_settings_error_ui import Ui_SettingsErrWin
# from ui.pulsar_status_ui import Ui_ConnStatusWindow
import ui.pulsar_rc

SETTINGS = loadSettings()


### Window Objects ###
class AboutWindow(QDialog):
    def __init__(self, parent=None):
        super(AboutWindow, self).__init__()

        self.ui = Ui_AboutDialog()
        self.ui.setupUi(self)
        self.ui.labelAppVersion.setText(__version__)
        self.ui.labelDeveloperList.setText(','.join(__credits__))
        self.ui.labelBuildDate.setText(__build__)
        self.ui.labelPythonVersion.setText('{}.{}.{}'.format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro))
        self.ui.labelNebulaVersion.setText(__nebula__)


    def openWin(self):
        self.ui.retranslateUi(self)
        self.show()


# class ConnStatusWindow(QMainWindow):
#     def __init__(self, parent=None):
#         super(ConnStatusWindow, self).__init__()

#         self.ui = Ui_ConnStatusWindow()
#         self.ui.setupUi(self)


class ConfigHostsWindow(QDialog):
    def __init__(self, parent=None):
        super(ConfigHostsWindow, self).__init__()

        self.ui = Ui_configHostsDialog()
        self.ui.setupUi(self)
        self.pulsarHostsFile = os.path.dirname(__file__) + os.sep + "pulsarhosts.txt"

        self.ui.buttonBox.button(QDialogButtonBox.Reset).released.connect(self.reset)
        self.ui.hostFilePath.setText(SETTINGS['hosts_file'])
        self.ui.btnSelectFile.released.connect(self.getHostsFile)
        self.ui.txtHostPairs.textChanged.connect(self.selectTextBoxRadio)

    def accept(self) -> None:
        """
        action to be completed on clicking OK
        """
        hostsFileTools = HostsFile()
        nHostsPath = self.ui.hostFilePath.text()

        if nHostsPath == '' and self.ui.txtHostPairs.toPlainText() == '':
            SETTINGS['hosts_file'] = ''
            
        elif self.ui.radioUseFile.isChecked():
            if not hostsFileTools.validateHostsFile(nHostsPath):
                modalTxt = self.tr('The selected file is not a valid hosts file. Please check it and try again.')
                errModal(self, QApplication.translate('ConfigHostsWindow', u'The selected file is not a valid hosts file. Please check it and try again.', None))
                self.ui.hostFilePath.setFocus
                return False
            
            SETTINGS['hosts_file'] = nHostsPath

            if nHostsPath != self.pulsarHostsFile and os.path.exists(self.pulsarHostsFile):
                os.unlink(self.pulsarHostsFile)

        elif self.ui.radioUseTextBox.isChecked():
            if not self.loadFromTextBox():
                return False
            
        # clear stuff and close window
        self.reject()


    def getHostsFile(self) -> None:
        """
        opens the hosts file window
        """
        hostsFileTools = HostsFile()
        file = QFileDialog(self)
        file.setFileMode(QFileDialog.AnyFile)
        file.setViewMode(QFileDialog.Detail)
        if file.exec():
            if not hostsFileTools.validateHostsFile(file.selectedFiles()[0]):
                errModal(self, QApplication.translate('ConfigHostsWindow', u'The selected file is not a valid hosts file. Please check it and try again.', None))
                self.ui.hostFilePath.setText('')
                self.ui.btnSelectFile.setFocus()
                return False

            self.ui.hostFilePath.setText(file.selectedFiles()[0])

            with open(file.selectedFiles()[0], 'r', encoding='utf-8') as file:
                self.ui.txtHostPairs.setPlainText(file.read())

            # this has to be here to override the txtHostPairs.textChanged() event listener
            self.ui.radioUseFile.setChecked(True) 

        self.ui.buttonBox.setFocus()


    def loadFromTextBox(self) -> bool:
        """
        loads the IP/hostname pairs from the text box

        :returns: boolean denoting success
        """
        pairList = self.ui.txtHostPairs.toPlainText()
        hostsFileTools = HostsFile()
        out = ''

        for line in pairList.splitlines():
            if hostsFileTools.validateHostsLine(line):
                out = f'{out}{line}\n'

        if out != '' or out == '\n':
            try:
                with open(self.pulsarHostsFile, 'w', encoding='utf-8') as file:
                    file.write(out)
            except Exception as e:
                print(f'Unable to write Pulsar hosts file: {e}')
                return False

            self.ui.hostFilePath.setText(self.pulsarHostsFile )
            SETTINGS['hosts_file'] = self.pulsarHostsFile
            return True

        else:
            SETTINGS['hosts_file'] = ''
            modalTxt = self.tr('No valid IP Address - Hostname pairs were entered. Hosts cannot be used.<br>Please either check the list and try again or point to a valid file containing the list.')
            errModal(self, QCoreApplication.translate('ConfigHostsWindow', u'No valid IP Address - Hostname pairs were entered. Hosts cannot be used.<br>Please either check the list and try again or point to a valid file containing the list.', None))
            return False


    def reject(self) -> None:
        """
        action to be completed on Cancel button
        """
        self.ui.hostFilePath.setText(SETTINGS['hosts_file'])
        self.ui.txtHostPairs.clear()
        self.ui.radioUseFile.setChecked(True)
        self.hide()


    def reset(self) -> None:
        """
        action to be completed on Reset button
        """
        self.ui.hostFilePath.clear()
        self.ui.txtHostPairs.clear()
        self.ui.radioUseFile.setChecked(True)
        self.ui.hostFilePath.setFocus()


    def selectTextBoxRadio(self) -> None:
        """
        function to select the pairs radio button
        """
        self.ui.radioUseTextBox.setChecked(True)


class SettingsErrorWindow(QMainWindow):
    def __init__(self, parent=None):
        super(SettingsErrorWindow, self).__init__()

        self.ui = Ui_SettingsErrWin()
        self.ui.setupUi(self)
        
        self.parent = parent

    def close(self):
        self.parent.quit()


class MainWindow(QMainWindow):
    def __init__(self, parent=None, nebula=None):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # setup the UI
        self.aboutWin = AboutWindow(self)
        self.configHostsWin = ConfigHostsWindow(self)
        self.st = systemTray(app, nebula)
        self.loadLanguages(parent)
        self.ui.configFilePath.setText(SETTINGS['config'])
        if SETTINGS['tray_start']:
            self.ui.checkTrayOnly.setChecked(True)
        else:
            self.ui.checkTrayOnly.setChecked(False)

        if SETTINGS['auto_connect']:
            self.ui.checkAutostart.setChecked(True)
        else:
            self.ui.checkAutostart.setChecked(False)

        if SETTINGS['use_hosts']:
            self.ui.checkUseHosts.setChecked(True)
        else:
            self.ui.checkUseHosts.setChecked(False)

        # hide the disconnect button on init
        self.ui.btnDisconnect.hide()
        self.ui.btnStatus.hide()

        # Menu Actions
        self.ui.actionConnect.triggered.connect(self.st.nebulaConnect)
        self.ui.actionDisconnect.triggered.connect(self.st.nebulaDisconnect)
        # self.ui.actionConnection_Status.triggered.connect(self.showStatusWin)
        self.ui.actionQuit_2.triggered.connect(partial(self.quitPulsar, parent))
        self.ui.actionUser_Guide.triggered.connect(self.openManual)
        self.ui.actionLicense.triggered.connect(self.openLicense)
        self.ui.actionAbout_Pulsar.triggered.connect(self.aboutWin.openWin)

        # link buttons
        self.ui.btnConnect.released.connect(self.st.nebulaConnect)
        self.ui.btnDisconnect.released.connect(self.st.nebulaDisconnect)
        # self.ui.btnStatus.released.connect(self.showStatusWin)
        self.ui.btnConfigFileSelect.released.connect(self.getConfigFile)
        self.ui.btnConfigureHosts.released.connect(self.configHostsWin.show)
        self.ui.btnSaveSettings.released.connect(self.saveSettingsBtn)
        self.ui.btnQuit.released.connect(partial(self.quitPulsar, parent))

        # set focus
        if self.st.connected:
            self.ui.btnDisconnect.setFocus()
        else:
            self.ui.btnConnect.setFocus()

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
        localeLangCode = curLocale.languageToCode(curLocale.language())

        locale.setlocale(locale.LC_ALL, curLocale.name())

        self.switchLanguage(parent, SETTINGS['language'])
        self.ui.retranslateUi(self)
        self.aboutWin.ui.retranslateUi(self.aboutWin)
        self.configHostsWin.ui.retranslateUi(self.configHostsWin)
        # connWin.ui.retranslateUi(connWin)
        self.st.retranslateUi(self.st)
        self.st.setToolTip(self.st.connToolTip if self.st.connected else self.st.disconnToolTip)
        self.st.menu.retranslateUi(self.st.menu)

        langTxt = [self.tr('Deutsch (German)'), self.tr('English'), self.tr('Türkçe (Turkish)')]

        self.langDict = {'de': QCoreApplication.translate('MainWindow', u'Deutsch (German)', None),
                         'en': QCoreApplication.translate('MainWindow', u'English', None),
                         'tr': QCoreApplication.translate('MainWindow', u'Türkçe (Turkish)', None)}
        langList = []

        for lang in self.langDict:
            langList.append(self.langDict[lang])

        self.ui.cmbLanguages.addItems(sorted(langList, key=locale.strxfrm))
        self.ui.cmbLanguages.setCurrentText(self.langDict[SETTINGS['language']])


    def noConfig(self) -> None:
        """
        Set up display for instance when no valid config file is found
        """
        self.ui.btnConnect.setDisabled(True)
        self.ui.configFilePath.setFocus()
        self.show()
        modalTxt = self.tr('No valid Nebula configuration file was found so the connection cannot be made.<br>Please set the path to a valid Nebula configuration file below to continue.')
        infoModal(self, 
                  QCoreApplication.translate('MainWindow', u'No valid Nebula configuration file was found so the connection cannot be made.<br>Please set the path to a valid Nebula configuration file below to continue.', None))


    def openLicense(self) -> None:
        """
        Opens URL to license
        """
        url = QtCore.QUrl('https://github.com/JS-Produksiyon/pulsar/blob/main/LICENSE')
        if not QtGui.QDesktopServices.openUrl(url):
            modalTxt = self.tr('Unable to open link to license.')
            errModal(self, QCoreApplication.translate('MainWindow', u'Unable to open link to license.', None))


    def openManual(self) -> None:
        """
        Opens URL to user manual
        """
        url = QtCore.QUrl('https://github.com/JS-Produksiyon/pulsar/blob/main/README.md')
        if not QtGui.QDesktopServices.openUrl(url):
            modalTxt = self.tr('Unable to open link to user guide.')
            errModal(self, QCoreApplication.translate('MainWindow', 'Unable to open link to user guide.', None))


    def quitPulsar(self, parent) -> None:
        """
        Checks if Pulsar is connected and pops up a query if still connected
        """
        if not self.st.connected:
            parent.quit()
        else:
            msg = self.tr("Pulsar is still connected to the Nebula mesh network.<br>Are you sure you want to quit the program?")
            msg = QCoreApplication.translate("MainWindow", u"Pulsar is still connected to the Nebula mesh network.<br>Are you sure you want to quit the program?", None)
            q = yesNoModal(self, msg)
            
            if q:
                self.st.nebulaDisconnect()
                parent.quit()


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
            if self.ui.btnConnect.isEnabled() == False:
                self.ui.btnConnect.setEnabled(True)
        else:
            if self.ui.btnConnect.isEnabled() == True:
                self.ui.btnConnect.setEnabled(False)
            errModal(self, 'Invalid Nebula configuration file selected. Please try again!')
            return False
        
        for lang in self.langDict:
            if self.ui.cmbLanguages.currentText() == self.langDict[lang]:
                SETTINGS['language'] = lang

        if SETTINGS['hosts_file'] == '':
            self.ui.checkUseHosts.setChecked(False)

        SETTINGS['tray_start'] = True if self.ui.checkTrayOnly.isChecked() else False
        SETTINGS['auto_connect'] = True if self.ui.checkAutostart.isChecked() else False
        SETTINGS['use_hosts'] = True if self.ui.checkUseHosts.isChecked() else False
        
        saveSettings(SETTINGS)
        self.loadLanguages(app)
        return True

    def switchLanguage(self, app, language='en') -> bool:
        """
        set interface language

        """
        if type(app) == QApplication:
            translator = QTranslator(app)
            translator.load(language, 'qtbase', '_', QLibraryInfo.path(QLibraryInfo.TranslationsPath))
            app.installTranslator(translator)
            translator = QTranslator(app)
            app.removeTranslator(translator)
            translator.load(os.path.dirname(__file__) + os.sep + 'translations' + os.sep + 'pulsar_{}.qm'.format(language))
            app.installTranslator(translator)
            return True
        else:
            return False

    # def showStatusWin(self) -> None:
    #     """
    #     shows the status window
    #     """
    #     connWin.show()



# Primary driver is the System Tray Icon
class systemTray(QSystemTrayIcon):
    """
    System Tray Icon
    """
    def __init__(self, parent, nebula=None) -> None:
        super(systemTray, self).__init__()

        self.hostsFile = HostsFile()

        self.connected = False
        self.connToolTip = self.tr('Pulsar connected')
        self.disconnToolTip = self.tr('Pulsar not connected')
        self.retranslateUi(self)

        self.iconOn = QIcon()
        self.iconOn.addFile(u':/icon/resources/pulsar-icon-16.png', size=QSize(16, 16))
        self.iconOn.addFile(u':/icon/resources/pulsar-icon-24.png', size=QSize(24, 24))
        self.iconOn.addFile(u':/icon/resources/pulsar-icon-32.png', size=QSize(32, 32))
        self.iconOff = QIcon()
        self.iconOff.addFile(u':/icon/resources/pulsar-icon-gray-16.png', size=QSize(16, 16))
        self.iconOff.addFile(u':/icon/resources/pulsar-icon-gray-24.png', size=QSize(24, 24))
        self.iconOff.addFile(u':/icon/resources/pulsar-icon-gray-32.png', size=QSize(32, 32))
        self.setIcon(self.iconOff)
        self.setToolTip('Pulsar')
        self.setVisible(True)
        self.menu = systemTrayMenu(self)
        self.menu.quit.triggered.connect(partial(self.quitPulsar, parent))
        self.menu.connItem.triggered.connect(self.nebulaConnect)
        self.menu.disconnItem.triggered.connect(self.nebulaDisconnect)
        self.menu.settingsWin.triggered.connect(self.showMainWin)
        # self.menu.statusWin.triggered.connect(self.showStatusWin)
        self.setContextMenu(self.menu)
        self.nebulaObj = nebula

    def connectStatusIcon(self) -> None:
        """
        Change icon depending on connection status
        """
        if self.connected:
            self.setIcon(self.iconOn)
        elif not self.connected:
            self.setIcon(self.iconOff)

    def nebulaConnect(self) -> None:
        """
        Enable connection 
        """
        if not self.connected:
            if not __debugState__:
                if SETTINGS['use_hosts']:
                    self.hostsFile.loadFromFile(SETTINGS['hosts_file'])
                self.nebulaObj.connect()
                

            self.connected = True
            self.connectStatusIcon()
            mainWin.ui.btnDisconnect.show()
            self.setToolTip(self.connToolTip)

    def nebulaDisconnect(self) -> None:
        """
        Disable connection
        """
        if self.connected:
            self.connected = False
            self.connectStatusIcon()
            mainWin.ui.btnDisconnect.hide()
            self.setToolTip(self.disconnToolTip)
            if not __debugState__:
                self.nebulaObj.disconnect()
                if SETTINGS['use_hosts']:
                    self.hostsFile.restoreHostsFile()

    def quitPulsar(self,parent):
        if self.connected and not __debugState__:
            self.nebulaDisconnect()

        parent.quit()

    def retranslateUi(self, systemTray):
        self.connToolTip = self.tr('Pulsar connected')
        self.connToolTip = QCoreApplication.translate('systemTray', u'Pulsar connected', None)
        self.disconnToolTip = self.tr('Pulsar not connected')
        self.disconnToolTip = QCoreApplication.translate('systemTray', u'Pulsar not connected', None)

    def showMainWin(self) -> None:
        """
        Display main window
        """
        mainWin.show()

    # def showStatusWin(self) -> None:
    #     """
    #     Display Connection Status window
    #     """
    #     connWin.show()

class systemTrayMenu(QMenu):
    """
    Menu for the system Tray Icon
    """
    def __init__(self, parent=None):
        super(systemTrayMenu, self).__init__()
        
        self.parent = parent
        self.connItem = QAction(self.tr('Connect to Nebula'))
        self.addAction(self.connItem)
        self.disconnItem = QAction(self.tr('Disconnect from Nebula'))
        self.addAction(self.disconnItem)
        self.addSeparator()
        self.settingsWin = QAction(self.tr('Show Pulsar Window'))
        self.addAction(self.settingsWin)
        # self.statusWin = QAction(self.tr('Show Connection Status')) 
        # self.addAction(self.statusWin)
        self.addSeparator()
        self.quit = QAction(self.tr('Quit'))
        self.addAction(self.quit)
        self.retranslateUi(self)

    def retranslateUi(self, MainWindow):
        """
        translate the menu
        """
        strings = [self.tr("Connect to Nebula"), self.tr("Disconnect from Nebula"), self.tr("Show Pulsar Window"), self.tr("Quit")]
        self.connItem.setText(QCoreApplication.translate("systemTrayMenu", u"Connect to Nebula", None))
        self.disconnItem.setText(QCoreApplication.translate("systemTrayMenu", u"Disconnect from Nebula", None))
        # self.statusWin.setText(QCoreApplication.translate("systemTrayMenu", u"Show Connection Status", None))
        self.settingsWin.setText(QCoreApplication.translate("systemTrayMenu", u"Show Pulsar Window", None))
        self.quit.setText(QCoreApplication.translate("systemTrayMenu", u"Quit", None))


if __name__ == '__main__':
    nebulaObj = Nebula(keep_alive=SETTINGS['keep_alive'], log_level=SETTINGS['log_level'])
    __nebula__ = nebulaObj.version()

    app = QApplication(sys.argv)
    app.setStyle('fusion')
    app.setQuitOnLastWindowClosed(False)

    if SETTINGS == False:
        settingsError = SettingsErrorWindow(app)
        settingsError.show()
    
    else:
        # connWin = ConnStatusWindow()
        mainWin = MainWindow(app, nebulaObj)
        
        if not os.path.exists(SETTINGS['config']):
            mainWin.noConfig()
        else:
            nebulaObj.setConfig(SETTINGS['config'])
            nebulaObj.usePing = SETTINGS['use_ping']
            nebulaObj.pingInterval = int(SETTINGS['ping_interval'])
        
        if not SETTINGS['tray_start']:
            mainWin.show()

        if SETTINGS['auto_connect']:
            mainWin.st.nebulaConnect()

    sys.exit(app.exec())
    