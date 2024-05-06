# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pulsar_about.ui'
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
    QLabel, QSizePolicy, QWidget)
try: 
    import ui.pulsar_rc
except ModuleNotFoundError:
    import pulsar_rc


class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        if not AboutDialog.objectName():
            AboutDialog.setObjectName(u"AboutDialog")
        AboutDialog.resize(400, 300)
        icon = QIcon()
        icon.addFile(u":/icon/resources/pulsar-icon-128.png", QSize(), QIcon.Normal, QIcon.Off)
        AboutDialog.setWindowIcon(icon)
        self.buttonBox = QDialogButtonBox(AboutDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(90, 260, 301, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Close)
        self.label = QLabel(AboutDialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 10, 32, 32))
        self.label.setPixmap(QPixmap(u":/icon/resources/pulsar-icon-32.png"))
        self.label_2 = QLabel(AboutDialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(50, 10, 251, 16))
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setText(u"Pulsar")
        self.label_3 = QLabel(AboutDialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(50, 30, 341, 16))
        self.label_4 = QLabel(AboutDialog)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 60, 300, 16))
        font1 = QFont()
        font1.setPointSize(9)
        font1.setBold(False)
        self.label_4.setFont(font1)
        self.label_5 = QLabel(AboutDialog)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(10, 80, 300, 16))
        self.label_5.setFont(font1)
        self.label_6 = QLabel(AboutDialog)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(10, 80, 300, 16))
        self.label_6.setFont(font1)
        self.label_7 = QLabel(AboutDialog)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(10, 110, 95, 16))
        font2 = QFont()
        font2.setPointSize(9)
        font2.setBold(False)
        font2.setItalic(True)
        self.label_7.setFont(font2)
        self.labelDeveloperList = QLabel(AboutDialog)
        self.labelDeveloperList.setObjectName(u"labelDeveloperList")
        self.labelDeveloperList.setGeometry(QRect(120, 110, 261, 16))
        self.labelDeveloperList.setFont(font1)
        self.labelDeveloperList.setText(u"JMW")
        self.label_8 = QLabel(AboutDialog)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(10, 130, 95, 16))
        self.label_8.setFont(font2)
        self.labelAppVersion = QLabel(AboutDialog)
        self.labelAppVersion.setObjectName(u"labelAppVersion")
        self.labelAppVersion.setGeometry(QRect(120, 130, 261, 16))
        self.labelAppVersion.setFont(font1)
        self.labelAppVersion.setText(u"1.0")
        self.labelBuildDate = QLabel(AboutDialog)
        self.labelBuildDate.setObjectName(u"labelBuildDate")
        self.labelBuildDate.setGeometry(QRect(120, 150, 261, 16))
        self.labelBuildDate.setFont(font1)
        self.labelBuildDate.setText(u"2025-05-05")
        self.label_9 = QLabel(AboutDialog)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(10, 150, 95, 16))
        self.label_9.setFont(font2)
        self.label_10 = QLabel(AboutDialog)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(10, 170, 95, 16))
        self.label_10.setFont(font2)
        self.labelPythonVersion = QLabel(AboutDialog)
        self.labelPythonVersion.setObjectName(u"labelPythonVersion")
        self.labelPythonVersion.setGeometry(QRect(120, 170, 261, 16))
        self.labelPythonVersion.setFont(font1)
        self.labelPythonVersion.setText(u"3.11")
        self.labelNebulaVersion = QLabel(AboutDialog)
        self.labelNebulaVersion.setObjectName(u"labelNebulaVersion")
        self.labelNebulaVersion.setGeometry(QRect(120, 190, 261, 16))
        self.labelNebulaVersion.setFont(font1)
        self.labelNebulaVersion.setText(u"1.8")
        self.label_11 = QLabel(AboutDialog)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(10, 190, 95, 16))
        self.label_11.setFont(font2)

        self.retranslateUi(AboutDialog)
        self.buttonBox.accepted.connect(AboutDialog.accept)
        self.buttonBox.rejected.connect(AboutDialog.reject)

        QMetaObject.connectSlotsByName(AboutDialog)
    # setupUi

    def retranslateUi(self, AboutDialog):
        AboutDialog.setWindowTitle(QCoreApplication.translate("AboutDialog", u"About Pulsar", None))
        self.label.setText("")
        self.label_3.setText(QCoreApplication.translate("AboutDialog", u"A Graphical User Interface for the Nebula Mesh Network", None))
        self.label_4.setText(QCoreApplication.translate("AboutDialog", u"Developed by JS Prod\u00fcksiyon Ltd. \u015eti. ", None))
        self.label_5.setText("")
        self.label_6.setText(QCoreApplication.translate("AboutDialog", u"Released under the GNU GPL v3.0 license.", None))
        self.label_7.setText(QCoreApplication.translate("AboutDialog", u"Developers:", None))
        self.label_8.setText(QCoreApplication.translate("AboutDialog", u"Version:", None))
        self.label_9.setText(QCoreApplication.translate("AboutDialog", u"Build:", None))
        self.label_10.setText(QCoreApplication.translate("AboutDialog", u"Python Version:", None))
        self.label_11.setText(QCoreApplication.translate("AboutDialog", u"Nebula Version:", None))
    # retranslateUi

