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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QLabel,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QWidget)
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
        self.labelExplanation.setGeometry(QRect(90, 10, 531, 81))
        self.labelExplanation.setWordWrap(True)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 20, 64, 64))
        self.label.setPixmap(QPixmap(u":/icon/resources/pulsar-icon-64.png"))
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(20, 130, 601, 131))
        self.frame.setFrameShape(QFrame.Panel)
        self.frame.setFrameShadow(QFrame.Plain)
        self.label_4 = QLabel(self.frame)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 10, 61, 16))
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 30, 171, 24))
        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 60, 171, 24))
        self.configFilePath = QLineEdit(self.frame)
        self.configFilePath.setObjectName(u"configFilePath")
        self.configFilePath.setGeometry(QRect(160, 30, 341, 24))
        self.btnConfigFileSelect = QPushButton(self.frame)
        self.btnConfigFileSelect.setObjectName(u"btnConfigFileSelect")
        self.btnConfigFileSelect.setGeometry(QRect(510, 30, 75, 24))
        self.comboBox = QComboBox(self.frame)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(160, 60, 341, 24))
        self.btnSaveSettings = QPushButton(self.frame)
        self.btnSaveSettings.setObjectName(u"btnSaveSettings")
        self.btnSaveSettings.setGeometry(QRect(464, 100, 121, 24))
        self.btnConnect = QPushButton(self.centralwidget)
        self.btnConnect.setObjectName(u"btnConnect")
        self.btnConnect.setGeometry(QRect(150, 290, 340, 51))
        font1 = QFont()
        font1.setPointSize(11)
        font1.setBold(True)
        self.btnConnect.setFont(font1)
        self.btnConnect.setStyleSheet(u"color: white;\n"
"background-color: rgb(0, 170, 0);\n"
"border-color: rgb(0, 255, 0);\n"
"")
        self.btnDisconnect = QPushButton(self.centralwidget)
        self.btnDisconnect.setObjectName(u"btnDisconnect")
        self.btnDisconnect.setGeometry(QRect(150, 290, 340, 51))
        self.btnDisconnect.setFont(font1)
        self.btnDisconnect.setStyleSheet(u"color: white;\n"
"background-color: rgb(202, 0, 0);\n"
"border-color: rgb(255, 0, 0);")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(210, 370, 220, 24))
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
        self.menuFile.addSeparator()
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
        self.label.setText("")
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Nebula Configuration File:", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Interface Language:", None))
        self.btnConfigFileSelect.setText(QCoreApplication.translate("MainWindow", u"Open...", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Deutsch (German)", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"English", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"T\u00fcrk\u00e7e (Turkish)", None))

        self.btnSaveSettings.setText(QCoreApplication.translate("MainWindow", u"Save Settings", None))
        self.btnConnect.setText(QCoreApplication.translate("MainWindow", u"Connect to Nebula Mesh Network", None))
        self.btnDisconnect.setText(QCoreApplication.translate("MainWindow", u"Disconnect from Nebula Mesh Network", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Display Connection Status...", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

