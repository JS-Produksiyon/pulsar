# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pulsar_status.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QPlainTextEdit,
    QPushButton, QSizePolicy, QWidget)
try: 
    import ui.pulsar_rc
except ModuleNotFoundError:
    import pulsar_rc

class Ui_ConnStatusWindow(object):
    def setupUi(self, ConnStatusWindow):
        if not ConnStatusWindow.objectName():
            ConnStatusWindow.setObjectName(u"ConnStatusWindow")
        ConnStatusWindow.resize(640, 480)
        icon = QIcon()
        icon.addFile(u":/icon/resources/pulsar-icon-128.png", QSize(), QIcon.Normal, QIcon.Off)
        ConnStatusWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(ConnStatusWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 10, 611, 16))
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 40, 241, 16))
        self.txtOutput = QPlainTextEdit(self.centralwidget)
        self.txtOutput.setObjectName(u"txtOutput")
        self.txtOutput.setGeometry(QRect(20, 60, 601, 361))
        self.txtOutput.setUndoRedoEnabled(False)
        self.txtOutput.setReadOnly(True)
        self.btnClose = QPushButton(self.centralwidget)
        self.btnClose.setObjectName(u"btnClose")
        self.btnClose.setGeometry(QRect(520, 440, 91, 24))
        ConnStatusWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(ConnStatusWindow)
        self.btnClose.released.connect(ConnStatusWindow.close)

        QMetaObject.connectSlotsByName(ConnStatusWindow)
    # setupUi

    def retranslateUi(self, ConnStatusWindow):
        ConnStatusWindow.setWindowTitle(QCoreApplication.translate("ConnStatusWindow", u"Pulsar :: Connection Status", None))
        self.label.setText(QCoreApplication.translate("ConnStatusWindow", u"Connected to Nebula Mesh Network", None))
        self.label_2.setText(QCoreApplication.translate("ConnStatusWindow", u"Nebula client output:", None))
        self.btnClose.setText(QCoreApplication.translate("ConnStatusWindow", u"Close", None))
    # retranslateUi

