# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pulsar_hosts.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QLabel, QLineEdit, QPlainTextEdit, QPushButton,
    QSizePolicy, QWidget)
try: 
    import ui.pulsar_rc
except ModuleNotFoundError:
    import pulsar_rc

class Ui_configHostsDialog(object):
    def setupUi(self, configHostsDialog):
        if not configHostsDialog.objectName():
            configHostsDialog.setObjectName(u"configHostsDialog")
        configHostsDialog.resize(425, 340)
        icon = QIcon()
        icon.addFile(u":/icon/resources/pulsar-icon-128.png", QSize(), QIcon.Normal, QIcon.Off)
        configHostsDialog.setWindowIcon(icon)
        self.buttonBox = QDialogButtonBox(configHostsDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(110, 300, 301, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.label = QLabel(configHostsDialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 10, 411, 21))
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.label_2 = QLabel(configHostsDialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 30, 401, 71))
        self.label_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.label_2.setWordWrap(True)
        self.label_3 = QLabel(configHostsDialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 110, 49, 24))
        self.hostFilePath = QLineEdit(configHostsDialog)
        self.hostFilePath.setObjectName(u"hostFilePath")
        self.hostFilePath.setGeometry(QRect(70, 110, 261, 24))
        self.pushButton = QPushButton(configHostsDialog)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(340, 110, 75, 24))
        self.label_4 = QLabel(configHostsDialog)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 140, 401, 24))
        self.txtHostPairs = QPlainTextEdit(configHostsDialog)
        self.txtHostPairs.setObjectName(u"txtHostPairs")
        self.txtHostPairs.setGeometry(QRect(10, 170, 401, 121))

        self.retranslateUi(configHostsDialog)
        self.buttonBox.accepted.connect(configHostsDialog.accept)
        self.buttonBox.rejected.connect(configHostsDialog.reject)

        QMetaObject.connectSlotsByName(configHostsDialog)
    # setupUi

    def retranslateUi(self, configHostsDialog):
        configHostsDialog.setWindowTitle(QCoreApplication.translate("configHostsDialog", u"Pulsar :: Configure Network Hosts", None))
        self.label.setText(QCoreApplication.translate("configHostsDialog", u"Configure Nebula Network Hosts", None))
        self.label_2.setText(QCoreApplication.translate("configHostsDialog", u"If you wish to be able to navigate to various hosts on the Nebula network using domain names instead of IP addresses, you can either point to a text file (<code>.txt</code>) containing IP address-hostname pairs, or else enter the pairs in the box below.", None))
        self.label_3.setText(QCoreApplication.translate("configHostsDialog", u"File:", None))
        self.pushButton.setText(QCoreApplication.translate("configHostsDialog", u"Open...", None))
        self.label_4.setText(QCoreApplication.translate("configHostsDialog", u"IP Address - Hostname Pairs:", None))
    # retranslateUi

