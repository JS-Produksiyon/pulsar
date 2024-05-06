# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pulsar_main.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QLabel, QLineEdit, QMainWindow, QMenu,
    QMenuBar, QPushButton, QSizePolicy, QWidget)
try: 
    import ui.pulsar_rc
except ModuleNotFoundError:
    import pulsar_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(640, 480)
        icon = QIcon()
        icon.addFile(u":/icon/resources/pulsar-icon-128.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.actionConnect = QAction(MainWindow)
        self.actionConnect.setObjectName(u"actionConnect")
        self.actionDisconnect = QAction(MainWindow)
        self.actionDisconnect.setObjectName(u"actionDisconnect")
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName(u"actionQuit")
        self.actionConnection_Status = QAction(MainWindow)
        self.actionConnection_Status.setObjectName(u"actionConnection_Status")
        self.actionConnection_Status.setEnabled(False)
        self.actionConnection_Status.setVisible(False)
        self.actionQuit_2 = QAction(MainWindow)
        self.actionQuit_2.setObjectName(u"actionQuit_2")
        self.actionUser_Guide = QAction(MainWindow)
        self.actionUser_Guide.setObjectName(u"actionUser_Guide")
        self.actionAbout_Pulsar = QAction(MainWindow)
        self.actionAbout_Pulsar.setObjectName(u"actionAbout_Pulsar")
        self.actionLicense = QAction(MainWindow)
        self.actionLicense.setObjectName(u"actionLicense")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.labelExplanation = QLabel(self.centralwidget)
        self.labelExplanation.setObjectName(u"labelExplanation")
        self.labelExplanation.setGeometry(QRect(90, 10, 531, 111))
        self.labelExplanation.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.labelExplanation.setWordWrap(True)
        self.labelIcon = QLabel(self.centralwidget)
        self.labelIcon.setObjectName(u"labelIcon")
        self.labelIcon.setGeometry(QRect(10, 20, 64, 64))
        self.labelIcon.setText(u"")
        self.labelIcon.setPixmap(QPixmap(u":/icon/resources/pulsar-icon-64.png"))
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(20, 130, 601, 171))
        self.frame.setFrameShape(QFrame.Panel)
        self.frame.setFrameShadow(QFrame.Plain)
        self.labelSettings = QLabel(self.frame)
        self.labelSettings.setObjectName(u"labelSettings")
        self.labelSettings.setGeometry(QRect(10, 10, 171, 16))
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.labelSettings.setFont(font)
        self.labelConfigFile = QLabel(self.frame)
        self.labelConfigFile.setObjectName(u"labelConfigFile")
        self.labelConfigFile.setGeometry(QRect(10, 30, 171, 24))
        self.labelLanguage = QLabel(self.frame)
        self.labelLanguage.setObjectName(u"labelLanguage")
        self.labelLanguage.setGeometry(QRect(10, 60, 171, 24))
        self.configFilePath = QLineEdit(self.frame)
        self.configFilePath.setObjectName(u"configFilePath")
        self.configFilePath.setGeometry(QRect(190, 30, 311, 24))
        self.btnConfigFileSelect = QPushButton(self.frame)
        self.btnConfigFileSelect.setObjectName(u"btnConfigFileSelect")
        self.btnConfigFileSelect.setGeometry(QRect(510, 30, 75, 24))
        self.cmbLanguages = QComboBox(self.frame)
        self.cmbLanguages.setObjectName(u"cmbLanguages")
        self.cmbLanguages.setGeometry(QRect(190, 60, 311, 24))
        self.btnSaveSettings = QPushButton(self.frame)
        self.btnSaveSettings.setObjectName(u"btnSaveSettings")
        self.btnSaveSettings.setGeometry(QRect(460, 130, 121, 24))
        self.checkTrayOnly = QCheckBox(self.frame)
        self.checkTrayOnly.setObjectName(u"checkTrayOnly")
        self.checkTrayOnly.setGeometry(QRect(190, 90, 301, 20))
        self.checkTrayOnly.setChecked(True)
        self.checkAutostart = QCheckBox(self.frame)
        self.checkAutostart.setObjectName(u"checkAutostart")
        self.checkAutostart.setGeometry(QRect(190, 110, 301, 20))
        self.btnConnect = QPushButton(self.centralwidget)
        self.btnConnect.setObjectName(u"btnConnect")
        self.btnConnect.setEnabled(True)
        self.btnConnect.setGeometry(QRect(150, 330, 340, 51))
        self.btnConnect.setFont(font)
        self.btnConnect.setStyleSheet(u"QPushButton#btnConnect {\n"
"	color: white;\n"
"	background-color: rgb(0, 170, 0);\n"
"	border-color: rgb(0, 255, 0);\n"
"	border-radius: 10px;\n"
"}\n"
"QPushButton#btnConnect:pressed {\n"
"	background-color: rgb(0, 255, 0)\n"
"}\n"
"QPushButton#btnConnect:disabled {\n"
"	background-color: rgb(0, 85, 0);\n"
"}")
        self.btnDisconnect = QPushButton(self.centralwidget)
        self.btnDisconnect.setObjectName(u"btnDisconnect")
        self.btnDisconnect.setGeometry(QRect(150, 330, 340, 51))
        self.btnDisconnect.setFont(font)
        self.btnDisconnect.setStyleSheet(u"QPushButton#btnDisconnect {\n"
"	color: white;\n"
"	background-color: rgb(202, 0, 0);\n"
"	border-color: rgb(255, 0, 0);\n"
"	border-radius: 10px;\n"
"}\n"
"QPushButton#btnDisconnect:pressed {\n"
"	background-color: rgb(255,0,0);\n"
"}")
        self.btnStatus = QPushButton(self.centralwidget)
        self.btnStatus.setObjectName(u"btnStatus")
        self.btnStatus.setEnabled(False)
        self.btnStatus.setGeometry(QRect(210, 400, 220, 24))
        self.btnQuit = QPushButton(self.centralwidget)
        self.btnQuit.setObjectName(u"btnQuit")
        self.btnQuit.setGeometry(QRect(260, 400, 120, 24))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 640, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionConnect)
        self.menuFile.addAction(self.actionDisconnect)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionConnection_Status)
        self.menuFile.addAction(self.actionQuit_2)
        self.menuHelp.addAction(self.actionUser_Guide)
        self.menuHelp.addAction(self.actionLicense)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout_Pulsar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Pulsar :: Nebula Mesh Network GUI", None))
        self.actionConnect.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
#if QT_CONFIG(shortcut)
        self.actionConnect.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+C", None))
#endif // QT_CONFIG(shortcut)
        self.actionDisconnect.setText(QCoreApplication.translate("MainWindow", u"Disconnect", None))
#if QT_CONFIG(shortcut)
        self.actionDisconnect.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+D", None))
#endif // QT_CONFIG(shortcut)
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
        self.actionConnection_Status.setText(QCoreApplication.translate("MainWindow", u"Connection Status...", None))
#if QT_CONFIG(shortcut)
        self.actionConnection_Status.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionQuit_2.setText(QCoreApplication.translate("MainWindow", u"Quit Pulsar", None))
#if QT_CONFIG(shortcut)
        self.actionQuit_2.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Q", None))
#endif // QT_CONFIG(shortcut)
        self.actionUser_Guide.setText(QCoreApplication.translate("MainWindow", u"User Guide", None))
        self.actionAbout_Pulsar.setText(QCoreApplication.translate("MainWindow", u"About Pulsar", None))
        self.actionLicense.setText(QCoreApplication.translate("MainWindow", u"License", None))
        self.labelExplanation.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">Pulsar</span> is a GUI client that makes it possible for Windows or MacOS computers to connect to a Nebula mesh network. For Pulsar to work, a valid Nebula configuration <code>.yaml</code> file location must be supplied in the box below. The Nebula CA file, and the client key and certificate files must either be saved relative to the configuration file, or else be defined with a full path. The client will only connect to the Nebula Mesh Network if all files are present.</p></body></html>", None))
        self.labelSettings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.labelConfigFile.setText(QCoreApplication.translate("MainWindow", u"Nebula Configuration File:", None))
        self.labelLanguage.setText(QCoreApplication.translate("MainWindow", u"Interface Language:", None))
        self.btnConfigFileSelect.setText(QCoreApplication.translate("MainWindow", u"Open...", None))
        self.btnSaveSettings.setText(QCoreApplication.translate("MainWindow", u"Save Settings", None))
        self.checkTrayOnly.setText(QCoreApplication.translate("MainWindow", u"Start in Tray Only", None))
        self.checkAutostart.setText(QCoreApplication.translate("MainWindow", u"Connect to Nebula Network on Startup", None))
        self.btnConnect.setText(QCoreApplication.translate("MainWindow", u"Connect to Nebula Mesh Network", None))
        self.btnDisconnect.setText(QCoreApplication.translate("MainWindow", u"Disconnect from Nebula Mesh Network", None))
        self.btnStatus.setText(QCoreApplication.translate("MainWindow", u"Display Connection Status...", None))
        self.btnQuit.setText(QCoreApplication.translate("MainWindow", u"Quit Pulsar", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

