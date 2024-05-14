# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pulsar_settings_error.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton,
    QSizePolicy, QWidget)

class Ui_SettingsErrWin(object):
    def setupUi(self, SettingsErrWin):
        if not SettingsErrWin.objectName():
            SettingsErrWin.setObjectName(u"SettingsErrWin")
        SettingsErrWin.resize(320, 160)
        self.centralwidget = QWidget(SettingsErrWin)
        self.centralwidget.setObjectName(u"centralwidget")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(230, 120, 75, 24))
        self.ErrorMessage = QLabel(self.centralwidget)
        self.ErrorMessage.setObjectName(u"ErrorMessage")
        self.ErrorMessage.setGeometry(QRect(10, 10, 301, 101))
        self.ErrorMessage.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.ErrorMessage.setWordWrap(True)
        SettingsErrWin.setCentralWidget(self.centralwidget)

        self.retranslateUi(SettingsErrWin)
        self.pushButton.released.connect(SettingsErrWin.close)

        QMetaObject.connectSlotsByName(SettingsErrWin)
    # setupUi

    def retranslateUi(self, SettingsErrWin):
        SettingsErrWin.setWindowTitle(QCoreApplication.translate("SettingsErrWin", u"Pulsar - Critical Error!", None))
        self.pushButton.setText(QCoreApplication.translate("SettingsErrWin", u"Close", None))
        self.ErrorMessage.setText(QCoreApplication.translate("SettingsErrWin", u"<html><head/><body><p>The settings file is corrupt. Pulsar is unable to start. </p><p>Please delete <span style=\" font-family:'Courier New';\">settings.yaml</span> to enable Pulsar to start.</p><p>Click the button below to close Pulsar.</p></body></html>", None))
    # retranslateUi

