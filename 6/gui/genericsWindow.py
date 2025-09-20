# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'genericsWindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_genericsWindow(object):
        
    def setupUi(self, genericsWindow):
        if not genericsWindow.objectName():
            genericsWindow.setObjectName(u"genericsWindow")
        genericsWindow.resize(214, 300)
        genericsWindow.setSizeGripEnabled(False)
        self.genericsListWidget = QListWidget(genericsWindow)
        self.genericsListWidget.setObjectName(u"genericsListWidget")
        self.genericsListWidget.setGeometry(QRect(10, 30, 181, 192))
        self.selectPushButton = QPushButton(genericsWindow)
        self.selectPushButton.setObjectName(u"selectPushButton")
        self.selectPushButton.setGeometry(QRect(70, 250, 75, 23))

        self.retranslateUi(genericsWindow)

        QMetaObject.connectSlotsByName(genericsWindow)
    # setupUi

    def retranslateUi(self, genericsWindow):
        genericsWindow.setWindowTitle(QCoreApplication.translate("genericsWindow", u"Generics", None))
        self.selectPushButton.setText(QCoreApplication.translate("genericsWindow", u"Select", None))
    # retranslateUi

