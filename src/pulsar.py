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

import os
from nebula import Nebula
from PySide6 import QtCore, QtGui
from PySide6.QtCore import QTranslator, QLocale, QTranslator, QSize
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon, QMainWindow, QDialog
from PySide6.QtGui import QIcon, QAction
from utils import (errModal, infoModal, loadSettings, saveSettings)

# windows
from ui.pulsar_about_ui import Ui_AboutDialog
from ui.pulsar_status_ui import Ui_ConnStatusWindow
from ui.pulsar_main_ui import Ui_MainWindow

SETTINGS = loadSettings()


# Windows
class AboutWindow(QDialog):
    def __init__(self, parent=None):
        super(AboutWindow, self).__init__()

        self.ui = Ui_AboutDialog()
        self.ui.setupUi(self)


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
    
        # hide the disconnect button on init
        self.ui.btnDisconnect.hide()

    def noConfig(self):
        """
        Set up display for instance when no valid config file is found
        """
        self.ui.btnConnect.setDisabled(True)
        self.show()
        errModal(self, self.tr('No valid Nebula configuration file was found so the connection cannot be made.<br>Please set the path to a valid Nebula configuration file below to continue.'))


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



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('fusion')
    app.setQuitOnLastWindowClosed(False)

    st = systemTray(app)
    mainWin = MainWindow()
    connWin = ConnStatusWindow()
    
    if not os.path.exists(SETTINGS['config']):
        mainWin.noConfig()


    app.exec()
    