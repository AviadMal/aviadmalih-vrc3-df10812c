# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'questasim_configurator_gui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(929, 899)
        MainWindow.setStyleSheet(u"/*\n"
"color: rgb(0, 0, 0);\n"
"background-color: rgb(0, 0, 0);\n"
" * MacOS Style Sheet for QT Applications\n"
" * Author: Jaime A. Quiroga P.\n"
" * Company: GTRONICK\n"
" * Last updated: 25/12/2020, 23:10.\n"
" * Available at: https://github.com/GTRONICK/QSS/blob/master/MacOS.qss\n"
" */\n"
"QMainWindow {\n"
"    background-color: #e0e0e0;\n"
"}\n"
"\n"
"QPushButton:hover:!pressed\n"
"{\n"
"  border: 1px solid red;\n"
"}\n"
"QPushButton, QToolButton, QCommandLinkButton{\n"
"    padding: 0 5px 0 5px;\n"
"    border-style: solid;\n"
"    border-top-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #c1c9cf, stop:1 #d2d8dd);\n"
"    border-right-color: qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:0, stop:0 #c1c9cf, stop:1 #d2d8dd);\n"
"    border-bottom-color: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 #c1c9cf, stop:1 #d2d8dd);\n"
"    border-left-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #c1c9cf, stop:1 #d2d8dd);\n"
"    border-width: 2px;\n"
"    bor"
                        "der-radius: 8px;\n"
"    color: #616161;\n"
"    font-weight: bold;\n"
"    background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #fbfdfd, stop:0.5 #ffffff, stop:1 #fbfdfd);\n"
"}\n"
"QPushButton::default, QToolButton::default, QCommandLinkButton::default{\n"
"    border: 2px solid transparent;\n"
"    color: #FFFFFF;\n"
"    background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #84afe5, stop:1 #1168e4);\n"
"}\n"
"QPushButton:hover, QToolButton:hover, QCommandLinkButton:hover{\n"
"    color: rgb(46, 61, 153);\n"
"}\n"
"QPushButton:pressed, QToolButton:pressed, QCommandLinkButton:pressed{\n"
"    color: #aeaeae;\n"
"    background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #ffffff, stop:0.5 #fbfdfd, stop:1 #ffffff);\n"
"}\n"
"QPushButton:disabled, QToolButton:disabled, QCommandLinkButton:disabled{\n"
"    color: #616161;\n"
"    background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #dce7eb, stop:0.5 #e0e8"
                        "eb, stop:1 #dee7ec);\n"
"}\n"
"QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QTimeEdit, QDateEdit, QDateTimeEdit {\n"
"    border-width: 2px;\n"
"    border-radius: 8px;\n"
"    border-style: solid;\n"
"    border-top-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 #c1c9cf, stop:1 #d2d8dd);\n"
"    border-right-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #c1c9cf, stop:1 #d2d8dd);\n"
"    border-bottom-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #c1c9cf, stop:1 #d2d8dd);\n"
"    border-left-color: qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:0, stop:0 #c1c9cf, stop:1 #d2d8dd);\n"
"    background-color: #f4f4f4;\n"
"    color: #3d3d3d;\n"
"}\n"
"QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QTimeEdit:focus, QDateEdit:focus, QDateTimeEdit:focus {\n"
"    border-width: 2px;\n"
"    border-radius: 8px;\n"
"    border-style: solid;\n"
"    border-top-color: qlineargradient(sprea"
                        "d:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 #85b7e3, stop:1 #9ec1db);\n"
"    border-right-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #85b7e3, stop:1 #9ec1db);\n"
"    border-bottom-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #85b7e3, stop:1 #9ec1db);\n"
"    border-left-color: qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:0, stop:0 #85b7e3, stop:1 #9ec1db);\n"
"    background-color: #f4f4f4;\n"
"    color: #3d3d3d;\n"
"}\n"
"QLineEdit:disabled, QTextEdit:disabled, QPlainTextEdit:disabled, QSpinBox:disabled, QDoubleSpinBox:disabled, QTimeEdit:disabled, QDateEdit:disabled, QDateTimeEdit:disabled {\n"
"    color: #b9b9b9;\n"
"}\n"
"QSpinBox::up-button, QDoubleSpinBox::up-button, QTimeEdit::up-button, QDateEdit::up-button, QDateTimeEdit::up-button {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"    color: #272727;\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: s"
                        "olid;\n"
"    border-top-right-radius: 3px;\n"
"    padding: 3px;\n"
"}\n"
"QSpinBox::down-button, QDoubleSpinBox::down-button, QTimeEdit::down-button, QDateEdit::down-button, QDateTimeEdit::down-button {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: bottom right;\n"
"    width: 15px;\n"
"    color: #272727;\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid;\n"
"    border-bottom-right-radius: 3px;\n"
"    padding: 3px;\n"
"}\n"
"QSpinBox::up-button:pressed, QDoubleSpinBox::up-button:pressed, QTimeEdit::up-button:pressed, QDateEdit::up-button:pressed, QDateTimeEdit::up-button:pressed {\n"
"    color: #aeaeae;\n"
"    background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #ffffff, stop:0.5 #fbfdfd, stop:1 #ffffff);\n"
"}\n"
"QSpinBox::down-button:pressed, QDoubleSpinBox::down-button:pressed, QTimeEdit::down-button:pressed, QDateEdit::down-button:pressed, QDateTimeEdit::down-button:pressed {\n"
"    color: #aeaeae;\n"
""
                        "    background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #ffffff, stop:0.5 #fbfdfd, stop:1 #ffffff);\n"
"}\n"
"QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover, QTimeEdit::up-button:hover, QDateEdit::up-button:hover, QDateTimeEdit::up-button:hover {\n"
"    color: #FFFFFF;\n"
"    border-top-right-radius: 5px;\n"
"    background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #84afe5, stop:1 #1168e4);\n"
"    \n"
"}\n"
"QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover, QTimeEdit::down-button:hover, QDateEdit::down-button:hover, QDateTimeEdit::down-button:hover {\n"
"    color: #FFFFFF;\n"
"    border-bottom-right-radius: 5px;\n"
"    background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #84afe5, stop:1 #1168e4);\n"
"}\n"
"QSpinBox::up-arrow, QDoubleSpinBox::up-arrow, QTimeEdit::up-arrow, QDateEdit::up-arrow, QDateTimeEdit::up-arrow {\n"
"    image: url(/usr/share/icons/Adwaita/16x16/actions/go-up-symbolic.symbo"
                        "lic.png);\n"
"}\n"
"QSpinBox::down-arrow, QDoubleSpinBox::down-arrow, QTimeEdit::down-arrow, QDateEdit::down-arrow, QDateTimeEdit::down-arrow {\n"
"    image: url(/usr/share/icons/Adwaita/16x16/actions/go-down-symbolic.symbolic.png);\n"
"}\n"
"QProgressBar {\n"
"    max-height: 8px;\n"
"    text-align: center;\n"
"    font: italic bold 11px;\n"
"    color: #3d3d3d;\n"
"    border: 1px solid transparent;\n"
"    border-radius:4px;\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #ddd5d5, stop:0.5 #dad3d3, stop:1 #ddd5d5);\n"
"}\n"
"QProgressBar::chunk {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #467dd1, stop:0.5 #3b88fc, stop:1 #467dd1);\n"
"    border-radius: 4px;\n"
"}\n"
"QProgressBar:disabled {\n"
"    color: #616161;\n"
"}\n"
"QProgressBar::chunk:disabled {\n"
"    background-color: #aeaeae;\n"
"}\n"
"QSlider::groove {\n"
"    border: 1px solid #bbbbbb;\n"
"    background-color: #52595d;\n"
"    border-radius: 4px;\n"
"}\n"
"QSl"
                        "ider::groove:horizontal {\n"
"    height: 6px;\n"
"}\n"
"QSlider::groove:vertical {\n"
"    width: 6px;\n"
"}\n"
"QSlider::handle:horizontal {\n"
"    background: #ffffff;\n"
"    border-style: solid;\n"
"    border-width: 1px;\n"
"    border-color: rgb(207,207,207);\n"
"    width: 12px;\n"
"    margin: -5px 0;\n"
"    border-radius: 7px;\n"
"}\n"
"QSlider::handle:vertical {\n"
"    background: #ffffff;\n"
"    border-style: solid;\n"
"    border-width: 1px;\n"
"    border-color: rgb(207,207,207);\n"
"    height: 12px;\n"
"    margin: 0 -5px;\n"
"    border-radius: 7px;\n"
"}\n"
"QSlider::add-page, QSlider::sub-page {\n"
"    border: 1px transparent;\n"
"    background-color: #52595d;\n"
"    border-radius: 4px;\n"
"}\n"
"QSlider::add-page:horizontal {\n"
"    background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #ddd5d5, stop:0.5 #dad3d3, stop:1 #ddd5d5);\n"
"}\n"
"QSlider::sub-page:horizontal {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #467dd1, stop"
                        ":0.5 #3b88fc, stop:1 #467dd1);\n"
"}\n"
"QSlider::add-page:vertical {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #467dd1, stop:0.5 #3b88fc, stop:1 #467dd1);\n"
"}\n"
"QSlider::sub-page:vertical {\n"
"    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #ddd5d5, stop:0.5 #dad3d3, stop:1 #ddd5d5);\n"
"}\n"
"QSlider::add-page:horizontal:disabled, QSlider::sub-page:horizontal:disabled, QSlider::add-page:vertical:disabled, QSlider::sub-page:vertical:disabled {\n"
"    background: #b9b9b9;\n"
"}\n"
"QComboBox, QFontComboBox {\n"
"    border-width: 2px;\n"
"    border-radius: 8px;\n"
"    border-style: solid;\n"
"    border-top-color: qlineargradient(spread:pad, x1:0.5, y1:1, x2:0.5, y2:0, stop:0 #c1c9cf, stop:1 #d2d8dd);\n"
"    border-right-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #c1c9cf, stop:1 #d2d8dd);\n"
"    border-bottom-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #c1c9cf, stop:1 #d2d8dd);\n"
" "
                        "   border-left-color: qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:0, stop:0 #c1c9cf, stop:1 #d2d8dd);\n"
"    background-color: #f4f4f4;\n"
"    color: #272727;\n"
"    padding-left: 5px;\n"
"}\n"
"QComboBox:editable, QComboBox:!editable, QComboBox::drop-down:editable, QComboBox:!editable:on, QComboBox::drop-down:editable:on {\n"
"    background: #ffffff;\n"
"}\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"    color: #272727;\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid;\n"
"    border-top-right-radius: 3px;\n"
"    border-bottom-right-radius: 3px;\n"
"}\n"
"QComboBox::down-arrow {\n"
"    image: url(/usr/share/icons/Adwaita/16x16/actions/go-down-symbolic.symbolic.png); /*Adawaita icon thene*/\n"
"}\n"
"\n"
"QComboBox::down-arrow:on {\n"
"    top: 1px;\n"
"    left: 1px;\n"
"}\n"
"QComboBox QAbstractItemView {\n"
"    border: 1px solid darkgray;\n"
"    border-radius: "
                        "8px;\n"
"    selection-background-color: #dadada;\n"
"    selection-color: #272727;\n"
"    color: #272727;\n"
"    background: white;\n"
"}\n"
"QLabel, QCheckBox, QRadioButton {\n"
"    color: #272727;\n"
"}\n"
"QCheckBox {\n"
"    padding: 2px;\n"
"}\n"
"QCheckBox:disabled, QRadioButton:disabled {\n"
"    color: #808086;\n"
"    padding: 2px;\n"
"}\n"
"\n"
"QCheckBox:hover {\n"
"    border-radius:4px;\n"
"    border-style:solid;\n"
"    padding-left: 1px;\n"
"    padding-right: 1px;\n"
"    padding-bottom: 1px;\n"
"    padding-top: 1px;\n"
"    border-width:1px;\n"
"    border-color: transparent;\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    image: url(/usr/share/icons/Adwaita/16x16/actions/object-select-symbolic.symbolic.png);\n"
"    height: 15px;\n"
"    width: 15px;\n"
"    border-style:solid;\n"
"    border-width: 1px;\n"
"    border-color: #48a5fd;\n"
"    color: #ffffff;\n"
"    border-radius: 3px;\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #48a5fd, stop:0."
                        "5 #329cfb, stop:1 #48a5fd);\n"
"}\n"
"QCheckBox::indicator:unchecked {\n"
"    \n"
"    height: 15px;\n"
"    width: 15px;\n"
"    border-style:solid;\n"
"    border-width: 1px;\n"
"    border-color: #48a5fd;\n"
"    border-radius: 3px;\n"
"    background-color: #fbfdfa;\n"
"}\n"
"QLCDNumber {\n"
"    color: #616161;;\n"
"}\n"
"QMenuBar {\n"
"    background-color: #ececec;\n"
"}\n"
"QMenuBar::item {\n"
"    color: #616161;\n"
"    spacing: 3px;\n"
"    padding: 1px 4px;\n"
"    background-color: #ececec;\n"
"}\n"
"\n"
"QMenuBar::item:selected {\n"
"    background-color: #dadada;\n"
"    color: #3d3d3d;\n"
"}\n"
"QMenu {\n"
"    background-color: #ececec;\n"
"}\n"
"QMenu::item:selected {\n"
"    background-color: #dadada;\n"
"    color: #3d3d3d;\n"
"}\n"
"QMenu::item {\n"
"    color: #616161;;\n"
"    background-color: #e0e0e0;\n"
"}\n"
"QTabWidget {\n"
"    color:rgb(0,0,0);\n"
"    background-color:#000000;\n"
"}\n"
"QTabWidget::pane {\n"
"    border-color: #050a0e;\n"
"    background-color: #e0e0e0;\n"
"    "
                        "border-width: 1px;\n"
"    border-radius: 4px;\n"
"    position: absolute;\n"
"    top: -0.5em;\n"
"    padding-top: 0.5em;\n"
"}\n"
"\n"
"QTabWidget::tab-bar {\n"
"    alignment: center;\n"
"}\n"
"\n"
"QTabBar::tab {\n"
"    border-bottom: 1px solid #c0c0c0;\n"
"    padding: 3px;\n"
"    color: #272727;\n"
"    background-color: #fefefc;\n"
"    margin-left:0px;\n"
"}\n"
"QTabBar::tab:!last {\n"
"    border-right: 1px solid;\n"
"    border-right-color: #c0c0c0;\n"
"    border-bottom-color: #c0c0c0;\n"
"}\n"
"QTabBar::tab:first {\n"
"    border-top-left-radius: 4px;\n"
"    border-bottom-left-radius: 4px;\n"
"}\n"
"QTabBar::tab:last {\n"
"    border-top-right-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"}\n"
"QTabBar::tab:selected, QTabBar::tab:last:selected, QTabBar::tab:hover {\n"
"    color: #FFFFFF;\n"
"    background-color: qlineargradient(spread:pad, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 #84afe5, stop:1 #1168e4);\n"
"}\n"
"QRadioButton::indicator {\n"
"    height: 14px;\n"
"    width: 14px;\n"
""
                        "    border-style:solid;\n"
"    border-radius:7px;\n"
"    border-width: 1px;\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    border-color: #48a5fd;\n"
"    background-color: qradialgradient(cx:0.5, cy:0.5, radius:0.4,fx:0.5, fy:0.5, stop:0 #ffffff, stop:0.5 #ffffff, stop:0.6 #48a5fd, stop:1 #48a5fd);\n"
"}\n"
"QRadioButton::indicator:!checked {\n"
"    border-color: #a9b7c6;\n"
"    background-color: #fbfdfa;\n"
"}\n"
"QStatusBar {\n"
"    color:#027f7f;\n"
"}\n"
"\n"
"QDial {\n"
"    background: #16a085;\n"
"}\n"
"\n"
"QToolBox {\n"
"    color: #a9b7c6;\n"
"    background-color: #222b2e;\n"
"}\n"
"QToolBox::tab {\n"
"    color: #a9b7c6;\n"
"    background-color:#222b2e;\n"
"}\n"
"QToolBox::tab:selected {\n"
"    color: #FFFFFF;\n"
"    background-color:#222b2e;\n"
"}\n"
"QScrollArea {\n"
"    color: #FFFFFF;\n"
"    background-color:#e0e0e0;\n"
"}\n"
"\n"
"QScrollBar:horizontal {\n"
"	max-height: 10px;\n"
"	border: 1px transparent grey;\n"
"	margin: 0px 20px 0px 20px;\n"
"	background: transparent;\n"
"}\n"
""
                        "QScrollBar:vertical {\n"
"	max-width: 10px;\n"
"	border: 1px transparent grey;\n"
"	margin: 20px 0px 20px 0px;\n"
"	background: transparent;\n"
"}\n"
"QScrollBar::handle:vertical, QScrollBar::handle:horizontal {\n"
"	background: #52595d;\n"
"	border-style: transparent;\n"
"	border-radius: 4px;\n"
"	min-height: 25px;\n"
"}\n"
"QScrollBar::handle:horizontal:hover, QScrollBar::handle:vertical:hover {\n"
"	background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #467dd1, stop:0.5 #3b88fc, stop:1 #467dd1);\n"
"}\n"
"QScrollBar::add-line, QScrollBar::sub-line {\n"
"    border: 2px transparent grey;\n"
"    border-radius: 4px;\n"
"    subcontrol-origin: margin;\n"
"    background: #b9b9b9;\n"
"}\n"
"QScrollBar::add-line:horizontal {\n"
"    width: 20px;\n"
"    subcontrol-position: right;\n"
"}\n"
"QScrollBar::add-line:vertical {\n"
"    height: 20px;\n"
"    subcontrol-position: bottom;\n"
"}\n"
"QScrollBar::sub-line:horizontal {\n"
"    width: 20px;\n"
"    subcontrol-position: left;\n"
"}\n"
"QScroll"
                        "Bar::sub-line:vertical {\n"
"    height: 20px;\n"
"    subcontrol-position: top;\n"
"}\n"
"QScrollBar::add-line:vertical:pressed, QScrollBar::add-line:horizontal:pressed, QScrollBar::sub-line:horizontal:pressed, QScrollBar::sub-line:vertical:pressed {\n"
"    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #467dd1, stop:0.5 #3b88fc, stop:1 #467dd1);\n"
"}\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal, QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"    background: none;\n"
"}\n"
"QScrollBar::up-arrow:vertical {\n"
"    image: url(/usr/share/icons/Adwaita/16x16/actions/go-up-symbolic.symbolic.png);\n"
"}\n"
"QScrollBar::down-arrow:vertical {\n"
"    image: url(/usr/share/icons/Adwaita/16x16/actions/go-down-symbolic.symbolic.png);\n"
"}\n"
"QScrollBar::left-arrow:horizontal {\n"
"    image: url(/usr/share/icons/Adwaita/16x16/actions/go-previous-symbolic.symbolic.png);\n"
"}\n"
"QScrollBar::right-arrow:horizontal {\n"
"    image: url(/usr/share/icon"
                        "s/Adwaita/16x16/actions/go-next-symbolic.symbolic.png);\n"
"}\n"
"")
        self.actionSaveConfig = QAction(MainWindow)
        self.actionSaveConfig.setObjectName(u"actionSaveConfig")
        self.actiondsd = QAction(MainWindow)
        self.actiondsd.setObjectName(u"actiondsd")
        self.actiondfd = QAction(MainWindow)
        self.actiondfd.setObjectName(u"actiondfd")
        self.actionLoadConfig = QAction(MainWindow)
        self.actionLoadConfig.setObjectName(u"actionLoadConfig")
        self.actionSave_As_Config = QAction(MainWindow)
        self.actionSave_As_Config.setObjectName(u"actionSave_As_Config")
        self.actionCangeDir = QAction(MainWindow)
        self.actionCangeDir.setObjectName(u"actionCangeDir")
        self.actionConstant_Override = QAction(MainWindow)
        self.actionConstant_Override.setObjectName(u"actionConstant_Override")
        self.actionBuild_design = QAction(MainWindow)
        self.actionBuild_design.setObjectName(u"actionBuild_design")
        self.actionSuper_Env = QAction(MainWindow)
        self.actionSuper_Env.setObjectName(u"actionSuper_Env")
        self.actionCreate_Env = QAction(MainWindow)
        self.actionCreate_Env.setObjectName(u"actionCreate_Env")
        self.actionCreate_Project = QAction(MainWindow)
        self.actionCreate_Project.setObjectName(u"actionCreate_Project")
        self.actionArtifactory = QAction(MainWindow)
        self.actionArtifactory.setObjectName(u"actionArtifactory")
        self.actionCheck_Bugs = QAction(MainWindow)
        self.actionCheck_Bugs.setObjectName(u"actionCheck_Bugs")
        self.actionReport_Bugs_Featuers = QAction(MainWindow)
        self.actionReport_Bugs_Featuers.setObjectName(u"actionReport_Bugs_Featuers")
        self.cloneRepo = QAction(MainWindow)
        self.cloneRepo.setObjectName(u"cloneRepo")
        self.gitGraph = QAction(MainWindow)
        self.gitGraph.setObjectName(u"gitGraph")
        self.gitGraphDsigen = QAction(MainWindow)
        self.gitGraphDsigen.setObjectName(u"gitGraphDsigen")
        self.actionRUVM = QAction(MainWindow)
        self.actionRUVM.setObjectName(u"actionRUVM")
        self.actionAdd = QAction(MainWindow)
        self.actionAdd.setObjectName(u"actionAdd")
        self.actionRemove = QAction(MainWindow)
        self.actionRemove.setObjectName(u"actionRemove")
        self.actionDark = QAction(MainWindow)
        self.actionDark.setObjectName(u"actionDark")
        self.actionDefault = QAction(MainWindow)
        self.actionDefault.setObjectName(u"actionDefault")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.MainGUI = QTabWidget(self.centralwidget)
        self.MainGUI.setObjectName(u"MainGUI")
        font = QFont()
        font.setFamily(u"Arial")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.MainGUI.setFont(font)
        self.MainGUI.setFocusPolicy(Qt.NoFocus)
        self.MainGUI.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.MainGUI.setStyleSheet(u"")
        self.main_tab = QWidget()
        self.main_tab.setObjectName(u"main_tab")
        self.run_option_gp = QGroupBox(self.main_tab)
        self.run_option_gp.setObjectName(u"run_option_gp")
        self.run_option_gp.setGeometry(QRect(420, 290, 281, 161))
        self.run_option_gp.setFont(font)
        self.run_option_gp.setStyleSheet(u"")
        self.verbosity_combo_bt = QComboBox(self.run_option_gp)
        self.verbosity_combo_bt.addItem("")
        self.verbosity_combo_bt.addItem("")
        self.verbosity_combo_bt.addItem("")
        self.verbosity_combo_bt.addItem("")
        self.verbosity_combo_bt.addItem("")
        self.verbosity_combo_bt.addItem("")
        self.verbosity_combo_bt.setObjectName(u"verbosity_combo_bt")
        self.verbosity_combo_bt.setGeometry(QRect(90, 25, 171, 23))
        self.verbosity_combo_bt.setFont(font)
        self.seed_line = QLineEdit(self.run_option_gp)
        self.seed_line.setObjectName(u"seed_line")
        self.seed_line.setGeometry(QRect(90, 55, 171, 23))
        self.seed_line.setFont(font)
        self.run_time_line = QLineEdit(self.run_option_gp)
        self.run_time_line.setObjectName(u"run_time_line")
        self.run_time_line.setGeometry(QRect(90, 85, 171, 23))
        self.run_time_line.setFont(font)
        self.label_6 = QLabel(self.run_option_gp)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(20, 80, 61, 31))
        self.label_6.setFont(font)
        self.label_3 = QLabel(self.run_option_gp)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(20, 20, 71, 31))
        self.label_3.setFont(font)
        self.label_5 = QLabel(self.run_option_gp)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(20, 50, 61, 31))
        self.label_5.setFont(font)
        self.stages = QGroupBox(self.main_tab)
        self.stages.setObjectName(u"stages")
        self.stages.setGeometry(QRect(10, 290, 161, 241))
        self.stages.setFont(font)
        self.stages.setStyleSheet(u"")
        self.stages.setFlat(False)
        self.stages.setCheckable(False)
        self.post_compile_bt = QCheckBox(self.stages)
        self.post_compile_bt.setObjectName(u"post_compile_bt")
        self.post_compile_bt.setGeometry(QRect(20, 156, 120, 21))
        self.post_compile_bt.setFont(font)
        self.simulate_bt = QCheckBox(self.stages)
        self.simulate_bt.setObjectName(u"simulate_bt")
        self.simulate_bt.setGeometry(QRect(20, 210, 120, 21))
        self.simulate_bt.setFont(font)
        self.opt_bt = QCheckBox(self.stages)
        self.opt_bt.setObjectName(u"opt_bt")
        self.opt_bt.setGeometry(QRect(20, 183, 120, 21))
        self.opt_bt.setFont(font)
        self.pre_comp_bt = QCheckBox(self.stages)
        self.pre_comp_bt.setObjectName(u"pre_comp_bt")
        self.pre_comp_bt.setGeometry(QRect(20, 25, 120, 21))
        self.pre_comp_bt.setFont(font)
        self.pre_comp_bt.setStyleSheet(u"")
        self.compile_env_bt = QCheckBox(self.stages)
        self.compile_env_bt.setObjectName(u"compile_env_bt")
        self.compile_env_bt.setGeometry(QRect(20, 129, 120, 21))
        self.compile_env_bt.setFont(font)
        self.comp_design_bt = QCheckBox(self.stages)
        self.comp_design_bt.setObjectName(u"comp_design_bt")
        self.comp_design_bt.setGeometry(QRect(20, 52, 120, 21))
        self.comp_design_bt.setFont(font)
        self.comp_vips_bt = QCheckBox(self.stages)
        self.comp_vips_bt.setObjectName(u"comp_vips_bt")
        self.comp_vips_bt.setGeometry(QRect(20, 103, 120, 21))
        self.comp_vips_bt.setFont(font)
        self.comp_dpi_bt = QCheckBox(self.stages)
        self.comp_dpi_bt.setObjectName(u"comp_dpi_bt")
        self.comp_dpi_bt.setGeometry(QRect(20, 77, 120, 21))
        self.comp_dpi_bt.setFont(font)
        self.run_modes_gp = QGroupBox(self.main_tab)
        self.run_modes_gp.setObjectName(u"run_modes_gp")
        self.run_modes_gp.setGeometry(QRect(190, 290, 211, 241))
        self.run_modes_gp.setFont(font)
        self.run_modes_gp.setStyleSheet(u"")
        self.run_modes_gp.setFlat(False)
        self.run_modes_gp.setCheckable(False)
        self.code_cov_bt = QCheckBox(self.run_modes_gp)
        self.code_cov_bt.setObjectName(u"code_cov_bt")
        self.code_cov_bt.setGeometry(QRect(20, 80, 181, 21))
        self.code_cov_bt.setFont(font)
        self.debug_mode_bt = QCheckBox(self.run_modes_gp)
        self.debug_mode_bt.setObjectName(u"debug_mode_bt")
        self.debug_mode_bt.setGeometry(QRect(20, 50, 121, 21))
        self.debug_mode_bt.setFont(font)
        self.gui_bt = QCheckBox(self.run_modes_gp)
        self.gui_bt.setObjectName(u"gui_bt")
        self.gui_bt.setGeometry(QRect(20, 20, 171, 21))
        self.gui_bt.setFont(font)
        self.gui_bt.setStyleSheet(u"")
        self.dummy_dut_bt = QCheckBox(self.run_modes_gp)
        self.dummy_dut_bt.setObjectName(u"dummy_dut_bt")
        self.dummy_dut_bt.setGeometry(QRect(20, 110, 181, 21))
        self.dummy_dut_bt.setFont(font)
        self.debug_break_cb = QCheckBox(self.run_modes_gp)
        self.debug_break_cb.setObjectName(u"debug_break_cb")
        self.debug_break_cb.setGeometry(QRect(20, 140, 171, 17))
        font1 = QFont()
        font1.setFamily(u"Arial")
        font1.setPointSize(8)
        self.debug_break_cb.setFont(font1)
        self.debug_config_db = QCheckBox(self.run_modes_gp)
        self.debug_config_db.setObjectName(u"debug_config_db")
        self.debug_config_db.setGeometry(QRect(20, 170, 171, 17))
        self.debug_config_db.setFont(font1)
        self.load_config_gp = QGroupBox(self.main_tab)
        self.load_config_gp.setObjectName(u"load_config_gp")
        self.load_config_gp.setGeometry(QRect(90, 166, 721, 101))
        self.load_config_gp.setStyleSheet(u"")
        self.config_name_push_bt = QPushButton(self.load_config_gp)
        self.config_name_push_bt.setObjectName(u"config_name_push_bt")
        self.config_name_push_bt.setGeometry(QRect(5, 10, 110, 25))
        self.config_name_line = QLineEdit(self.load_config_gp)
        self.config_name_line.setObjectName(u"config_name_line")
        self.config_name_line.setGeometry(QRect(120, 10, 591, 23))
        self.config_name_line.setFont(font)
        self.tb_bt = QPushButton(self.load_config_gp)
        self.tb_bt.setObjectName(u"tb_bt")
        self.tb_bt.setGeometry(QRect(5, 40, 110, 25))
        self.tb_line = QLineEdit(self.load_config_gp)
        self.tb_line.setObjectName(u"tb_line")
        self.tb_line.setGeometry(QRect(120, 40, 591, 23))
        self.tb_line.setFont(font)
        self.test_line = QLineEdit(self.load_config_gp)
        self.test_line.setObjectName(u"test_line")
        self.test_line.setGeometry(QRect(120, 70, 590, 23))
        self.test_line.setFont(font)
        self.test_bt = QPushButton(self.load_config_gp)
        self.test_bt.setObjectName(u"test_bt")
        self.test_bt.setGeometry(QRect(5, 70, 110, 25))
        self.general_gp = QGroupBox(self.main_tab)
        self.general_gp.setObjectName(u"general_gp")
        self.general_gp.setGeometry(QRect(720, 290, 151, 161))
        self.general_gp.setFont(font)
        self.general_gp.setStyleSheet(u"")
        self.general_gp.setFlat(False)
        self.general_gp.setCheckable(False)
        self.clear_work_bt = QCheckBox(self.general_gp)
        self.clear_work_bt.setObjectName(u"clear_work_bt")
        self.clear_work_bt.setGeometry(QRect(10, 30, 120, 21))
        self.clear_work_bt.setFont(font)
        self.new_trans_bt = QCheckBox(self.general_gp)
        self.new_trans_bt.setObjectName(u"new_trans_bt")
        self.new_trans_bt.setGeometry(QRect(10, 60, 120, 21))
        self.new_trans_bt.setFont(font)
        self.save_wave_bt = QCheckBox(self.general_gp)
        self.save_wave_bt.setObjectName(u"save_wave_bt")
        self.save_wave_bt.setGeometry(QRect(10, 90, 120, 21))
        self.save_wave_bt.setFont(font)
        self.close_gui_bt = QCheckBox(self.general_gp)
        self.close_gui_bt.setObjectName(u"close_gui_bt")
        self.close_gui_bt.setGeometry(QRect(10, 120, 120, 21))
        self.close_gui_bt.setFont(font)
        self.Dark = QSlider(self.main_tab)
        self.Dark.setObjectName(u"Dark")
        self.Dark.setGeometry(QRect(710, 110, 131, 22))
        self.Dark.setOrientation(Qt.Horizontal)
        self.ok_cancel_buttun = QDialogButtonBox(self.main_tab)
        self.ok_cancel_buttun.setObjectName(u"ok_cancel_buttun")
        self.ok_cancel_buttun.setGeometry(QRect(150, 506, 351, 61))
        self.ok_cancel_buttun.setFont(font)
        self.ok_cancel_buttun.setStyleSheet(u"")
        self.ok_cancel_buttun.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.load_tool_bt = QPushButton(self.main_tab)
        self.load_tool_bt.setObjectName(u"load_tool_bt")
        self.load_tool_bt.setEnabled(True)
        self.load_tool_bt.setGeometry(QRect(90, 10, 110, 25))
        self.visualizer_bt = QCheckBox(self.main_tab)
        self.visualizer_bt.setObjectName(u"visualizer_bt")
        self.visualizer_bt.setGeometry(QRect(130, 40, 91, 21))
        self.visualizer_bt.setFont(font)
        self.vrun_bt = QCheckBox(self.main_tab)
        self.vrun_bt.setObjectName(u"vrun_bt")
        self.vrun_bt.setGeometry(QRect(220, 40, 71, 21))
        self.vrun_bt.setFont(font)
        self.questasim_bt = QCheckBox(self.main_tab)
        self.questasim_bt.setObjectName(u"questasim_bt")
        self.questasim_bt.setGeometry(QRect(30, 40, 91, 21))
        self.questasim_bt.setFont(font)
        self.vrc_ver_combo_bt = QComboBox(self.main_tab)
        self.vrc_ver_combo_bt.setObjectName(u"vrc_ver_combo_bt")
        self.vrc_ver_combo_bt.setGeometry(QRect(800, 50, 51, 22))
        self.vrc_ver_combo_bt.setFont(font)
        self.qvip_ver_combo_bt = QComboBox(self.main_tab)
        self.qvip_ver_combo_bt.setObjectName(u"qvip_ver_combo_bt")
        self.qvip_ver_combo_bt.setGeometry(QRect(360, 50, 69, 22))
        self.qvip_ver_combo_bt.setFont(font)
        self.qvip_ver_combo_bt.setStyleSheet(u"")
        self.visualizer_ver_combo_bt = QComboBox(self.main_tab)
        self.visualizer_ver_combo_bt.setObjectName(u"visualizer_ver_combo_bt")
        self.visualizer_ver_combo_bt.setGeometry(QRect(600, 50, 69, 22))
        self.visualizer_ver_combo_bt.setFont(font)
        self.label_17 = QLabel(self.main_tab)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setGeometry(QRect(690, 20, 91, 31))
        self.label_17.setFont(font)
        self.label_14 = QLabel(self.main_tab)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setGeometry(QRect(460, 20, 101, 31))
        self.label_14.setFont(font)
        self.label_15 = QLabel(self.main_tab)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setGeometry(QRect(570, 20, 101, 31))
        self.label_15.setFont(font)
        self.label_16 = QLabel(self.main_tab)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setGeometry(QRect(780, 20, 101, 31))
        self.label_16.setFont(font)
        self.label_13 = QLabel(self.main_tab)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(350, 20, 101, 31))
        self.label_13.setFont(font)
        self.questa_ver_combo_bt = QComboBox(self.main_tab)
        self.questa_ver_combo_bt.setObjectName(u"questa_ver_combo_bt")
        self.questa_ver_combo_bt.setGeometry(QRect(480, 50, 69, 22))
        self.questa_ver_combo_bt.setFont(font)
        self.vrun_ver_combo_bt = QComboBox(self.main_tab)
        self.vrun_ver_combo_bt.setObjectName(u"vrun_ver_combo_bt")
        self.vrun_ver_combo_bt.setGeometry(QRect(700, 50, 69, 22))
        self.vrun_ver_combo_bt.setFont(font)
        self.label = QLabel(self.main_tab)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(230, 105, 441, 31))
        font2 = QFont()
        font2.setFamily(u"Arial")
        font2.setPointSize(18)
        font2.setBold(False)
        font2.setItalic(False)
        font2.setWeight(50)
        self.label.setFont(font2)
        self.label.setStyleSheet(u"")
        self.MainGUI.addTab(self.main_tab, "")
        self.dpi_tab = QWidget()
        self.dpi_tab.setObjectName(u"dpi_tab")
        self.dpi_tab.setToolTipDuration(-1)
        self.add_dpi_button = QPushButton(self.dpi_tab)
        self.add_dpi_button.setObjectName(u"add_dpi_button")
        self.add_dpi_button.setGeometry(QRect(300, 280, 75, 23))
        self.add_dpi_button.setToolTipDuration(5000)
        self.add_dpi_button.setAutoFillBackground(False)
        self.add_dpi_button.setStyleSheet(u"")
        self.clear_button = QPushButton(self.dpi_tab)
        self.clear_button.setObjectName(u"clear_button")
        self.clear_button.setGeometry(QRect(480, 280, 75, 23))
        self.clear_button.setToolTipDuration(5000)
        self.dpi_list_label = QLabel(self.dpi_tab)
        self.dpi_list_label.setObjectName(u"dpi_list_label")
        self.dpi_list_label.setGeometry(QRect(300, 40, 251, 21))
        self.dpi_list_label.setToolTipDuration(1000)
        self.dpi_list_label.setLayoutDirection(Qt.LeftToRight)
        self.dpi_list_label.setAutoFillBackground(False)
        self.dpi_list_label.setAlignment(Qt.AlignCenter)
        self.dpi_list = QListWidget(self.dpi_tab)
        self.dpi_list.setObjectName(u"dpi_list")
        self.dpi_list.setGeometry(QRect(300, 70, 256, 192))
        self.dpi_build_errors_label = QLabel(self.dpi_tab)
        self.dpi_build_errors_label.setObjectName(u"dpi_build_errors_label")
        self.dpi_build_errors_label.setGeometry(QRect(70, 320, 781, 461))
        self.dpi_build_errors_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.dpi_build_errors_label.setWordWrap(True)
        self.dpi_help_push_button = QPushButton(self.dpi_tab)
        self.dpi_help_push_button.setObjectName(u"dpi_help_push_button")
        self.dpi_help_push_button.setGeometry(QRect(300, 40, 31, 23))
        self.dpi_load_template_push_button = QPushButton(self.dpi_tab)
        self.dpi_load_template_push_button.setObjectName(u"dpi_load_template_push_button")
        self.dpi_load_template_push_button.setGeometry(QRect(40, 20, 111, 23))
        font3 = QFont()
        font3.setPointSize(6)
        font3.setBold(True)
        font3.setWeight(75)
        self.dpi_load_template_push_button.setFont(font3)
        self.MainGUI.addTab(self.dpi_tab, "")
        self.advance_tab = QWidget()
        self.advance_tab.setObjectName(u"advance_tab")
        self.general_gp_4 = QGroupBox(self.advance_tab)
        self.general_gp_4.setObjectName(u"general_gp_4")
        self.general_gp_4.setGeometry(QRect(30, 10, 301, 181))
        self.general_gp_4.setFont(font)
        self.general_gp_4.setStyleSheet(u"")
        self.work_dir_line = QLineEdit(self.general_gp_4)
        self.work_dir_line.setObjectName(u"work_dir_line")
        self.work_dir_line.setGeometry(QRect(110, 30, 171, 23))
        self.work_dir_line.setFont(font)
        self.pre_compile_lable_3 = QLabel(self.general_gp_4)
        self.pre_compile_lable_3.setObjectName(u"pre_compile_lable_3")
        self.pre_compile_lable_3.setGeometry(QRect(30, 30, 81, 16))
        self.pre_compile_lable_3.setFont(font)
        self.modelsimini_line = QLineEdit(self.general_gp_4)
        self.modelsimini_line.setObjectName(u"modelsimini_line")
        self.modelsimini_line.setGeometry(QRect(110, 60, 171, 23))
        self.modelsimini_line.setFont(font)
        self.pre_compile_lable_4 = QLabel(self.general_gp_4)
        self.pre_compile_lable_4.setObjectName(u"pre_compile_lable_4")
        self.pre_compile_lable_4.setGeometry(QRect(30, 60, 81, 16))
        self.pre_compile_lable_4.setFont(font)
        self.wave_line = QLineEdit(self.general_gp_4)
        self.wave_line.setObjectName(u"wave_line")
        self.wave_line.setGeometry(QRect(110, 90, 171, 23))
        self.wave_line.setFont(font)
        self.pre_compile_lable_6 = QLabel(self.general_gp_4)
        self.pre_compile_lable_6.setObjectName(u"pre_compile_lable_6")
        self.pre_compile_lable_6.setGeometry(QRect(30, 90, 81, 16))
        self.pre_compile_lable_6.setFont(font)
        self.compile_commanda_gp = QGroupBox(self.advance_tab)
        self.compile_commanda_gp.setObjectName(u"compile_commanda_gp")
        self.compile_commanda_gp.setGeometry(QRect(370, 10, 461, 181))
        self.compile_commanda_gp.setFont(font)
        self.compile_commanda_gp.setStyleSheet(u"")
        self.pre_compile_line = QLineEdit(self.compile_commanda_gp)
        self.pre_compile_line.setObjectName(u"pre_compile_line")
        self.pre_compile_line.setGeometry(QRect(130, 30, 291, 23))
        self.pre_compile_line.setFont(font)
        self.pre_compile_lable = QLabel(self.compile_commanda_gp)
        self.pre_compile_lable.setObjectName(u"pre_compile_lable")
        self.pre_compile_lable.setGeometry(QRect(26, 30, 81, 21))
        self.pre_compile_lable.setFont(font)
        self.compile_design_line = QLineEdit(self.compile_commanda_gp)
        self.compile_design_line.setObjectName(u"compile_design_line")
        self.compile_design_line.setGeometry(QRect(130, 60, 291, 23))
        self.compile_design_line.setFont(font)
        self.compile_env_line = QLineEdit(self.compile_commanda_gp)
        self.compile_env_line.setObjectName(u"compile_env_line")
        self.compile_env_line.setGeometry(QRect(130, 120, 291, 23))
        self.compile_env_line.setFont(font)
        self.post_compile_line = QLineEdit(self.compile_commanda_gp)
        self.post_compile_line.setObjectName(u"post_compile_line")
        self.post_compile_line.setGeometry(QRect(130, 150, 291, 23))
        self.post_compile_line.setFont(font)
        self.post_compile_lable = QLabel(self.compile_commanda_gp)
        self.post_compile_lable.setObjectName(u"post_compile_lable")
        self.post_compile_lable.setGeometry(QRect(28, 150, 81, 16))
        self.post_compile_lable.setFont(font)
        self.compile_vips_line = QLineEdit(self.compile_commanda_gp)
        self.compile_vips_line.setObjectName(u"compile_vips_line")
        self.compile_vips_line.setGeometry(QRect(130, 90, 291, 23))
        self.compile_vips_line.setFont(font)
        self.compile_vip_lable = QLabel(self.compile_commanda_gp)
        self.compile_vip_lable.setObjectName(u"compile_vip_lable")
        self.compile_vip_lable.setGeometry(QRect(26, 90, 81, 16))
        self.compile_vip_lable.setFont(font)
        self.compile_design_push_bt = QPushButton(self.compile_commanda_gp)
        self.compile_design_push_bt.setObjectName(u"compile_design_push_bt")
        self.compile_design_push_bt.setGeometry(QRect(5, 60, 121, 20))
        self.compile_design_push_bt.setFont(font)
        self.compile_design_push_bt.setStyleSheet(u"background-color: rgb(224, 224, 224);\n"
"font: 8pt \"Arial\";\n"
"border-color: rgb(224, 224, 224);")
        self.compile_env_push_bt = QPushButton(self.compile_commanda_gp)
        self.compile_env_push_bt.setObjectName(u"compile_env_push_bt")
        self.compile_env_push_bt.setGeometry(QRect(0, 120, 111, 20))
        self.compile_env_push_bt.setFont(font)
        self.compile_env_push_bt.setStyleSheet(u"background-color: rgb(224, 224, 224);\n"
"font: 8pt \"Arial\";\n"
"border-color: rgb(224, 224, 224);")
        self.opt_args_gp = QGroupBox(self.advance_tab)
        self.opt_args_gp.setObjectName(u"opt_args_gp")
        self.opt_args_gp.setGeometry(QRect(30, 220, 801, 321))
        self.opt_args_gp.setFont(font)
        self.opt_args_gp.setStyleSheet(u"")
        self.opt_libs_line = QLineEdit(self.opt_args_gp)
        self.opt_libs_line.setObjectName(u"opt_libs_line")
        self.opt_libs_line.setGeometry(QRect(130, 30, 651, 23))
        self.opt_libs_line.setFont(font)
        self.opt_defualt_lable = QLabel(self.opt_args_gp)
        self.opt_defualt_lable.setObjectName(u"opt_defualt_lable")
        self.opt_defualt_lable.setGeometry(QRect(30, 130, 91, 16))
        self.opt_defualt_lable.setFont(font)
        self.opt_debug_lable = QLabel(self.opt_args_gp)
        self.opt_debug_lable.setObjectName(u"opt_debug_lable")
        self.opt_debug_lable.setGeometry(QRect(30, 180, 81, 16))
        self.opt_debug_lable.setFont(font)
        self.label_11 = QLabel(self.opt_args_gp)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(30, 230, 121, 16))
        self.label_11.setFont(font)
        self.opt_defualt_line = QLineEdit(self.opt_args_gp)
        self.opt_defualt_line.setObjectName(u"opt_defualt_line")
        self.opt_defualt_line.setGeometry(QRect(130, 130, 651, 23))
        self.opt_defualt_line.setFont(font)
        self.opt_debug_line = QLineEdit(self.opt_args_gp)
        self.opt_debug_line.setObjectName(u"opt_debug_line")
        self.opt_debug_line.setGeometry(QRect(130, 180, 651, 23))
        self.opt_debug_line.setFont(font)
        self.opt_codecov_line = QLineEdit(self.opt_args_gp)
        self.opt_codecov_line.setObjectName(u"opt_codecov_line")
        self.opt_codecov_line.setGeometry(QRect(130, 230, 651, 23))
        self.opt_codecov_line.setFont(font)
        self.opt_visualizer_lable = QLabel(self.opt_args_gp)
        self.opt_visualizer_lable.setObjectName(u"opt_visualizer_lable")
        self.opt_visualizer_lable.setGeometry(QRect(30, 280, 121, 16))
        self.opt_visualizer_lable.setFont(font)
        self.opt_visualizer_line = QLineEdit(self.opt_args_gp)
        self.opt_visualizer_line.setObjectName(u"opt_visualizer_line")
        self.opt_visualizer_line.setGeometry(QRect(130, 280, 651, 23))
        self.opt_visualizer_line.setFont(font)
        self.libraries_push_bt = QPushButton(self.opt_args_gp)
        self.libraries_push_bt.setObjectName(u"libraries_push_bt")
        self.libraries_push_bt.setGeometry(QRect(2, 30, 101, 20))
        self.libraries_push_bt.setStyleSheet(u"background-color: rgb(224, 224, 224);\n"
"font: 8pt \"Arial\";\n"
"border-color: rgb(224, 224, 224);")
        self.opt_genenv_line = QLineEdit(self.opt_args_gp)
        self.opt_genenv_line.setObjectName(u"opt_genenv_line")
        self.opt_genenv_line.setGeometry(QRect(130, 80, 651, 23))
        self.opt_genenv_line.setFont(font)
        self.opt_gen_env_lable = QLabel(self.opt_args_gp)
        self.opt_gen_env_lable.setObjectName(u"opt_gen_env_lable")
        self.opt_gen_env_lable.setGeometry(QRect(30, 80, 91, 16))
        self.opt_gen_env_lable.setFont(font)
        self.sim_args_gp = QGroupBox(self.advance_tab)
        self.sim_args_gp.setObjectName(u"sim_args_gp")
        self.sim_args_gp.setGeometry(QRect(30, 560, 801, 241))
        self.sim_args_gp.setFont(font)
        self.sim_args_gp.setStyleSheet(u"")
        self.vsim_defualt_line = QLineEdit(self.sim_args_gp)
        self.vsim_defualt_line.setObjectName(u"vsim_defualt_line")
        self.vsim_defualt_line.setGeometry(QRect(130, 30, 651, 23))
        self.vsim_defualt_line.setFont(font)
        self.vsim_defualt_lable = QLabel(self.sim_args_gp)
        self.vsim_defualt_lable.setObjectName(u"vsim_defualt_lable")
        self.vsim_defualt_lable.setGeometry(QRect(30, 30, 81, 16))
        self.vsim_defualt_lable.setFont(font)
        self.vsim_debug_lable = QLabel(self.sim_args_gp)
        self.vsim_debug_lable.setObjectName(u"vsim_debug_lable")
        self.vsim_debug_lable.setGeometry(QRect(30, 70, 91, 16))
        self.vsim_debug_lable.setFont(font)
        self.vsim_codecov_lable = QLabel(self.sim_args_gp)
        self.vsim_codecov_lable.setObjectName(u"vsim_codecov_lable")
        self.vsim_codecov_lable.setGeometry(QRect(30, 110, 81, 16))
        self.vsim_codecov_lable.setFont(font)
        self.vsim_debug_line = QLineEdit(self.sim_args_gp)
        self.vsim_debug_line.setObjectName(u"vsim_debug_line")
        self.vsim_debug_line.setGeometry(QRect(130, 70, 651, 23))
        self.vsim_debug_line.setFont(font)
        self.vsim_codecov_line = QLineEdit(self.sim_args_gp)
        self.vsim_codecov_line.setObjectName(u"vsim_codecov_line")
        self.vsim_codecov_line.setGeometry(QRect(130, 110, 651, 23))
        self.vsim_codecov_line.setFont(font)
        self.vsim_visualizer_lable = QLabel(self.sim_args_gp)
        self.vsim_visualizer_lable.setObjectName(u"vsim_visualizer_lable")
        self.vsim_visualizer_lable.setGeometry(QRect(30, 190, 121, 16))
        self.vsim_visualizer_lable.setFont(font)
        self.vsim_visualizer_line = QLineEdit(self.sim_args_gp)
        self.vsim_visualizer_line.setObjectName(u"vsim_visualizer_line")
        self.vsim_visualizer_line.setGeometry(QRect(130, 190, 651, 23))
        self.vsim_visualizer_line.setFont(font)
        self.vsim_dpi_label = QLabel(self.sim_args_gp)
        self.vsim_dpi_label.setObjectName(u"vsim_dpi_label")
        self.vsim_dpi_label.setGeometry(QRect(30, 150, 81, 16))
        self.vsim_dpi_label.setFont(font)
        self.vsim_dpi_label.setToolTipDuration(-1)
        self.vsim_dpi_textbox = QLineEdit(self.sim_args_gp)
        self.vsim_dpi_textbox.setObjectName(u"vsim_dpi_textbox")
        self.vsim_dpi_textbox.setGeometry(QRect(130, 150, 651, 23))
        self.vsim_dpi_textbox.setFont(font)
        self.vsim_dpi_textbox.setToolTipDuration(-1)
        self.MainGUI.addTab(self.advance_tab, "")
        self.regression_tab = QWidget()
        self.regression_tab.setObjectName(u"regression_tab")
        self.reg_modes = QGroupBox(self.regression_tab)
        self.reg_modes.setObjectName(u"reg_modes")
        self.reg_modes.setGeometry(QRect(30, 130, 211, 201))
        self.reg_modes.setFont(font)
        self.reg_modes.setStyleSheet(u"")
        self.reg_modes.setFlat(False)
        self.reg_modes.setCheckable(False)
        self.triage_bt = QCheckBox(self.reg_modes)
        self.triage_bt.setObjectName(u"triage_bt")
        self.triage_bt.setGeometry(QRect(20, 70, 151, 21))
        self.triage_bt.setFont(font)
        self.grid_bt = QCheckBox(self.reg_modes)
        self.grid_bt.setObjectName(u"grid_bt")
        self.grid_bt.setGeometry(QRect(20, 45, 151, 21))
        self.grid_bt.setFont(font)
        self.trend_bt = QCheckBox(self.reg_modes)
        self.trend_bt.setObjectName(u"trend_bt")
        self.trend_bt.setGeometry(QRect(20, 20, 151, 21))
        self.trend_bt.setFont(font)
        self.delete_vrmdata_bt = QCheckBox(self.reg_modes)
        self.delete_vrmdata_bt.setObjectName(u"delete_vrmdata_bt")
        self.delete_vrmdata_bt.setGeometry(QRect(20, 145, 151, 21))
        self.delete_vrmdata_bt.setFont(font)
        self.mail_bt = QCheckBox(self.reg_modes)
        self.mail_bt.setObjectName(u"mail_bt")
        self.mail_bt.setGeometry(QRect(20, 95, 151, 21))
        self.mail_bt.setFont(font)
        self.report_bt = QCheckBox(self.reg_modes)
        self.report_bt.setObjectName(u"report_bt")
        self.report_bt.setGeometry(QRect(20, 120, 151, 21))
        self.report_bt.setFont(font)
        self.rerun_bt = QCheckBox(self.reg_modes)
        self.rerun_bt.setObjectName(u"rerun_bt")
        self.rerun_bt.setGeometry(QRect(20, 170, 151, 21))
        self.rerun_bt.setFont(font)
        self.reg_option_gp = QGroupBox(self.regression_tab)
        self.reg_option_gp.setObjectName(u"reg_option_gp")
        self.reg_option_gp.setGeometry(QRect(270, 130, 201, 191))
        self.reg_option_gp.setFont(font)
        self.reg_option_gp.setStyleSheet(u"")
        self.jobs = QLabel(self.reg_option_gp)
        self.jobs.setObjectName(u"jobs")
        self.jobs.setGeometry(QRect(15, 50, 101, 31))
        self.jobs.setFont(font)
        self.jobs_combo_bt = QComboBox(self.reg_option_gp)
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.addItem("")
        self.jobs_combo_bt.setObjectName(u"jobs_combo_bt")
        self.jobs_combo_bt.setGeometry(QRect(50, 54, 51, 22))
        self.jobs_combo_bt.setFont(font)
        self.RankPushBut = QPushButton(self.reg_option_gp)
        self.RankPushBut.setObjectName(u"RankPushBut")
        self.RankPushBut.setGeometry(QRect(10, 25, 51, 20))
        self.load_config_gp_4 = QGroupBox(self.regression_tab)
        self.load_config_gp_4.setObjectName(u"load_config_gp_4")
        self.load_config_gp_4.setGeometry(QRect(30, 20, 791, 101))
        self.load_config_gp_4.setStyleSheet(u"")
        self.testplan_bt = QPushButton(self.load_config_gp_4)
        self.testplan_bt.setObjectName(u"testplan_bt")
        self.testplan_bt.setGeometry(QRect(35, 30, 110, 25))
        self.testplan_line = QLineEdit(self.load_config_gp_4)
        self.testplan_line.setObjectName(u"testplan_line")
        self.testplan_line.setGeometry(QRect(150, 30, 590, 23))
        self.testplan_line.setFont(font)
        self.reg_modes_2 = QGroupBox(self.regression_tab)
        self.reg_modes_2.setObjectName(u"reg_modes_2")
        self.reg_modes_2.setGeometry(QRect(30, 340, 831, 451))
        self.reg_modes_2.setFont(font)
        self.reg_modes_2.setStyleSheet(u"")
        self.reg_modes_2.setFlat(False)
        self.reg_modes_2.setCheckable(False)
        self.verticalLayout = QVBoxLayout(self.reg_modes_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.TestNamePushButton = QPushButton(self.regression_tab)
        self.TestNamePushButton.setObjectName(u"TestNamePushButton")
        self.TestNamePushButton.setGeometry(QRect(110, 336, 190, 20))
        self.TestNamePushButton.setStyleSheet(u"background-color: rgb(224, 224, 224);\n"
"font: 8pt \"Arial\";\n"
"border-color: rgb(224, 224, 224);")
        self.generics_options_groupbox = QGroupBox(self.regression_tab)
        self.generics_options_groupbox.setObjectName(u"generics_options_groupbox")
        self.generics_options_groupbox.setGeometry(QRect(510, 130, 241, 201))
        self.generics_options_groupbox.setFont(font)
        self.generics_options_groupbox.setStyleSheet(u"")
        self.add_generics_sets_button = QPushButton(self.generics_options_groupbox)
        self.add_generics_sets_button.setObjectName(u"add_generics_sets_button")
        self.add_generics_sets_button.setGeometry(QRect(10, 170, 111, 23))
        self.add_generics_sets_button.setFont(font3)
        self.clear_generics_table_button = QPushButton(self.generics_options_groupbox)
        self.clear_generics_table_button.setObjectName(u"clear_generics_table_button")
        self.clear_generics_table_button.setGeometry(QRect(140, 170, 81, 23))
        self.clear_generics_table_button.setFont(font3)
        self.regressionGenericsTableWidget = QTableWidget(self.regression_tab)
        if (self.regressionGenericsTableWidget.columnCount() < 1):
            self.regressionGenericsTableWidget.setColumnCount(1)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setTextAlignment(Qt.AlignCenter);
        self.regressionGenericsTableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        self.regressionGenericsTableWidget.setObjectName(u"regressionGenericsTableWidget")
        self.regressionGenericsTableWidget.setGeometry(QRect(540, 180, 181, 111))
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.regressionGenericsTableWidget.sizePolicy().hasHeightForWidth())
        self.regressionGenericsTableWidget.setSizePolicy(sizePolicy)
        self.regressionGenericsTableWidget.setFrameShape(QFrame.Box)
        self.regressionGenericsTableWidget.setFrameShadow(QFrame.Plain)
        self.regressionGenericsTableWidget.setLineWidth(1)
        self.regressionGenericsTableWidget.setMidLineWidth(1)
        self.regressionGenericsTableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.regressionGenericsTableWidget.horizontalHeader().setStretchLastSection(True)
        self.regressionGenericsTableWidget.verticalHeader().setStretchLastSection(True)
        self.definesPushButton = QPushButton(self.regression_tab)
        self.definesPushButton.setObjectName(u"definesPushButton")
        self.definesPushButton.setGeometry(QRect(520, 150, 221, 23))
        font4 = QFont()
        font4.setFamily(u"Arial")
        font4.setPointSize(8)
        font4.setBold(False)
        font4.setItalic(False)
        font4.setUnderline(True)
        font4.setWeight(50)
        self.definesPushButton.setFont(font4)
        self.definesPushButton.setAutoFillBackground(False)
        self.definesPushButton.setStyleSheet(u"background-color: rgb(224, 224, 224);\n"
"font: 8pt \"Arial\";\n"
"border-color: rgb(224, 224, 224);")
        self.MainGUI.addTab(self.regression_tab, "")
        self.generics_options_groupbox.raise_()
        self.reg_modes.raise_()
        self.reg_option_gp.raise_()
        self.load_config_gp_4.raise_()
        self.reg_modes_2.raise_()
        self.TestNamePushButton.raise_()
        self.regressionGenericsTableWidget.raise_()
        self.definesPushButton.raise_()

        self.gridLayout.addWidget(self.MainGUI, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 929, 18))
        self.menufile = QMenu(self.menubar)
        self.menufile.setObjectName(u"menufile")
        self.menuLink = QMenu(self.menubar)
        self.menuLink.setObjectName(u"menuLink")
        self.menuGit = QMenu(self.menubar)
        self.menuGit.setObjectName(u"menuGit")
        MainWindow.setMenuBar(self.menubar)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.menubar.addAction(self.menufile.menuAction())
        self.menubar.addAction(self.menuLink.menuAction())
        self.menubar.addAction(self.menuGit.menuAction())
        self.menufile.addSeparator()
        self.menufile.addAction(self.actionLoadConfig)
        self.menufile.addAction(self.actionSaveConfig)
        self.menufile.addAction(self.actionCangeDir)
        self.menufile.addAction(self.actionConstant_Override)
        self.menufile.addAction(self.actionBuild_design)
        self.menuLink.addAction(self.actionCreate_Env)
        self.menuLink.addAction(self.actionCreate_Project)
        self.menuLink.addAction(self.actionArtifactory)
        self.menuLink.addAction(self.actionRUVM)
        self.menuGit.addAction(self.gitGraph)
        self.menuGit.addAction(self.gitGraphDsigen)
        self.menuGit.addAction(self.cloneRepo)
        self.menuGit.addAction(self.actionReport_Bugs_Featuers)
        self.menuGit.addAction(self.actionCheck_Bugs)

        self.retranslateUi(MainWindow)

        self.MainGUI.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionSaveConfig.setText(QCoreApplication.translate("MainWindow", u"Save Config", None))
        self.actiondsd.setText(QCoreApplication.translate("MainWindow", u"dsd", None))
        self.actiondfd.setText(QCoreApplication.translate("MainWindow", u"dfd", None))
        self.actionLoadConfig.setText(QCoreApplication.translate("MainWindow", u"Load Config", None))
        self.actionSave_As_Config.setText(QCoreApplication.translate("MainWindow", u"Save As Config", None))
        self.actionCangeDir.setText(QCoreApplication.translate("MainWindow", u"Change Dir", None))
        self.actionConstant_Override.setText(QCoreApplication.translate("MainWindow", u"Constant Override", None))
        self.actionBuild_design.setText(QCoreApplication.translate("MainWindow", u"Build Design", None))
        self.actionSuper_Env.setText(QCoreApplication.translate("MainWindow", u"Super Env", None))
        self.actionCreate_Env.setText(QCoreApplication.translate("MainWindow", u"Create Env", None))
#if QT_CONFIG(statustip)
        self.actionCreate_Env.setStatusTip(QCoreApplication.translate("MainWindow", u"Create verification environment under UVM framework", None))
#endif // QT_CONFIG(statustip)
        self.actionCreate_Project.setText(QCoreApplication.translate("MainWindow", u"Create Project", None))
        self.actionArtifactory.setText(QCoreApplication.translate("MainWindow", u"Artifactory", None))
        self.actionCheck_Bugs.setText(QCoreApplication.translate("MainWindow", u"Check Bug", None))
#if QT_CONFIG(statustip)
        self.actionCheck_Bugs.setStatusTip(QCoreApplication.translate("MainWindow", u"Git checkout environment to a relevant bug", None))
#endif // QT_CONFIG(statustip)
        self.actionReport_Bugs_Featuers.setText(QCoreApplication.translate("MainWindow", u"Report Bug", None))
#if QT_CONFIG(tooltip)
        self.actionReport_Bugs_Featuers.setToolTip(QCoreApplication.translate("MainWindow", u"Report a bug with a Git commit ID to TFS", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.actionReport_Bugs_Featuers.setStatusTip(QCoreApplication.translate("MainWindow", u"Report a bug with a Git commit ID to TFS", None))
#endif // QT_CONFIG(statustip)
        self.cloneRepo.setText(QCoreApplication.translate("MainWindow", u"Clone Repo", None))
#if QT_CONFIG(statustip)
        self.cloneRepo.setStatusTip(QCoreApplication.translate("MainWindow", u"Git clone a repository", None))
#endif // QT_CONFIG(statustip)
        self.gitGraph.setText(QCoreApplication.translate("MainWindow", u"Git Graph", None))
#if QT_CONFIG(statustip)
        self.gitGraph.setStatusTip(QCoreApplication.translate("MainWindow", u"Load web tool for current Git repository", None))
#endif // QT_CONFIG(statustip)
        self.gitGraphDsigen.setText(QCoreApplication.translate("MainWindow", u"Git Graph Design", None))
#if QT_CONFIG(statustip)
        self.gitGraphDsigen.setStatusTip(QCoreApplication.translate("MainWindow", u"Load web tool for design's Git repository", None))
#endif // QT_CONFIG(statustip)
        self.actionRUVM.setText(QCoreApplication.translate("MainWindow", u"RUVM", None))
#if QT_CONFIG(statustip)
        self.actionRUVM.setStatusTip(QCoreApplication.translate("MainWindow", u"Load Mentor tool for RAL to create register package from Excel", None))
#endif // QT_CONFIG(statustip)
        self.actionAdd.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.actionRemove.setText(QCoreApplication.translate("MainWindow", u"Remove", None))
        self.actionDark.setText(QCoreApplication.translate("MainWindow", u"Dark Mode", None))
        self.actionDefault.setText(QCoreApplication.translate("MainWindow", u"Default", None))
#if QT_CONFIG(statustip)
        self.MainGUI.setStatusTip("")
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.MainGUI.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
#if QT_CONFIG(accessibility)
        self.MainGUI.setAccessibleName("")
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.MainGUI.setAccessibleDescription("")
#endif // QT_CONFIG(accessibility)
        self.run_option_gp.setTitle(QCoreApplication.translate("MainWindow", u"Run Option", None))
        self.verbosity_combo_bt.setItemText(0, QCoreApplication.translate("MainWindow", u"UVM_LOW", None))
        self.verbosity_combo_bt.setItemText(1, QCoreApplication.translate("MainWindow", u"UVM_DEBUG", None))
        self.verbosity_combo_bt.setItemText(2, QCoreApplication.translate("MainWindow", u"UVM_FULL", None))
        self.verbosity_combo_bt.setItemText(3, QCoreApplication.translate("MainWindow", u"UVM_HIGH", None))
        self.verbosity_combo_bt.setItemText(4, QCoreApplication.translate("MainWindow", u"UVM_MEDIUM", None))
        self.verbosity_combo_bt.setItemText(5, QCoreApplication.translate("MainWindow", u"UVM_NONE", None))

        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Run Time:", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Verbosity:", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Seed:", None))
#if QT_CONFIG(whatsthis)
        self.stages.setWhatsThis(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>xdfxx</p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.stages.setTitle(QCoreApplication.translate("MainWindow", u"Stages", None))
        self.post_compile_bt.setText(QCoreApplication.translate("MainWindow", u"Post Compile", None))
        self.simulate_bt.setText(QCoreApplication.translate("MainWindow", u"Simulation", None))
        self.opt_bt.setText(QCoreApplication.translate("MainWindow", u"Optimize", None))
        self.pre_comp_bt.setText(QCoreApplication.translate("MainWindow", u"Pre Compile", None))
        self.compile_env_bt.setText(QCoreApplication.translate("MainWindow", u"Compile Env", None))
        self.comp_design_bt.setText(QCoreApplication.translate("MainWindow", u"Compile Design", None))
        self.comp_vips_bt.setText(QCoreApplication.translate("MainWindow", u"Compile VIPS", None))
        self.comp_dpi_bt.setText(QCoreApplication.translate("MainWindow", u"Compile DPI", None))
        self.run_modes_gp.setTitle(QCoreApplication.translate("MainWindow", u"Run Modes", None))
        self.code_cov_bt.setText(QCoreApplication.translate("MainWindow", u"Code Coverage Mode", None))
        self.debug_mode_bt.setText(QCoreApplication.translate("MainWindow", u"Debug Mode", None))
#if QT_CONFIG(tooltip)
        self.gui_bt.setToolTip(QCoreApplication.translate("MainWindow", u"When activated - run in application mode, otherwise in batch mode", None))
#endif // QT_CONFIG(tooltip)
        self.gui_bt.setText(QCoreApplication.translate("MainWindow", u"GUI Mode", None))
        self.dummy_dut_bt.setText(QCoreApplication.translate("MainWindow", u"Dummy DUT", None))
#if QT_CONFIG(tooltip)
        self.debug_break_cb.setToolTip(QCoreApplication.translate("MainWindow", u"Break at each UVM_ERROR appearance in simulation", None))
#endif // QT_CONFIG(tooltip)
        self.debug_break_cb.setText(QCoreApplication.translate("MainWindow", u"Break at UVM_ERROR", None))
#if QT_CONFIG(tooltip)
        self.debug_config_db.setToolTip(QCoreApplication.translate("MainWindow", u"Print calls to config_db get and set", None))
#endif // QT_CONFIG(tooltip)
        self.debug_config_db.setText(QCoreApplication.translate("MainWindow", u"Show config db info", None))
        self.load_config_gp.setTitle("")
        self.config_name_push_bt.setText(QCoreApplication.translate("MainWindow", u"Config Name", None))
        self.tb_bt.setText(QCoreApplication.translate("MainWindow", u"TB Name", None))
        self.test_bt.setText(QCoreApplication.translate("MainWindow", u"Select Test", None))
        self.general_gp.setTitle(QCoreApplication.translate("MainWindow", u"General", None))
        self.clear_work_bt.setText(QCoreApplication.translate("MainWindow", u"Clear Work", None))
        self.new_trans_bt.setText(QCoreApplication.translate("MainWindow", u"New Terminal", None))
        self.save_wave_bt.setText(QCoreApplication.translate("MainWindow", u"Save Wave", None))
        self.close_gui_bt.setText(QCoreApplication.translate("MainWindow", u"Close GUI", None))
#if QT_CONFIG(whatsthis)
        self.load_tool_bt.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
#if QT_CONFIG(accessibility)
        self.load_tool_bt.setAccessibleName("")
#endif // QT_CONFIG(accessibility)
#if QT_CONFIG(accessibility)
        self.load_tool_bt.setAccessibleDescription("")
#endif // QT_CONFIG(accessibility)
        self.load_tool_bt.setText(QCoreApplication.translate("MainWindow", u"Load Tool", None))
        self.visualizer_bt.setText(QCoreApplication.translate("MainWindow", u"Visualizer", None))
        self.vrun_bt.setText(QCoreApplication.translate("MainWindow", u"VRUN", None))
        self.questasim_bt.setText(QCoreApplication.translate("MainWindow", u"Questasim", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"VRUN Version:", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Questa Version:", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Visualizer Version:", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"VRC Version:", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"QVIP Version:", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Verification Runner Configurator", None))
        self.MainGUI.setTabText(self.MainGUI.indexOf(self.main_tab), QCoreApplication.translate("MainWindow", u"Main", None))
#if QT_CONFIG(tooltip)
        self.add_dpi_button.setToolTip(QCoreApplication.translate("MainWindow", u"Add Python or C++ files to be built into shared objects", None))
#endif // QT_CONFIG(tooltip)
        self.add_dpi_button.setText(QCoreApplication.translate("MainWindow", u"Add", None))
#if QT_CONFIG(tooltip)
        self.clear_button.setToolTip(QCoreApplication.translate("MainWindow", u"Clear all selected files from list", None))
#endif // QT_CONFIG(tooltip)
        self.clear_button.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
#if QT_CONFIG(tooltip)
        self.dpi_list_label.setToolTip(QCoreApplication.translate("MainWindow", u"List of Python / C++ files to be built into shared objects", None))
#endif // QT_CONFIG(tooltip)
        self.dpi_list_label.setText(QCoreApplication.translate("MainWindow", u"Project's DPI Files:", None))
#if QT_CONFIG(tooltip)
        self.dpi_list.setToolTip(QCoreApplication.translate("MainWindow", u"List of Python / C++ files to be built into shared objects", None))
#endif // QT_CONFIG(tooltip)
        self.dpi_build_errors_label.setText("")
#if QT_CONFIG(tooltip)
        self.dpi_help_push_button.setToolTip(QCoreApplication.translate("MainWindow", u"Click here to read the instructions on how to incorporate DPIs in your SystemVerilog project", None))
#endif // QT_CONFIG(tooltip)
        self.dpi_help_push_button.setText(QCoreApplication.translate("MainWindow", u"?", None))
#if QT_CONFIG(tooltip)
        self.dpi_load_template_push_button.setToolTip(QCoreApplication.translate("MainWindow", u"Click here to load a Python file template under Pysv framework", None))
#endif // QT_CONFIG(tooltip)
        self.dpi_load_template_push_button.setText(QCoreApplication.translate("MainWindow", u"Load Template", None))
        self.MainGUI.setTabText(self.MainGUI.indexOf(self.dpi_tab), QCoreApplication.translate("MainWindow", u"DPI", None))
#if QT_CONFIG(tooltip)
        self.MainGUI.setTabToolTip(self.MainGUI.indexOf(self.dpi_tab), QCoreApplication.translate("MainWindow", u"Python and C++ DPI configurations", None))
#endif // QT_CONFIG(tooltip)
        self.general_gp_4.setTitle(QCoreApplication.translate("MainWindow", u"General", None))
        self.pre_compile_lable_3.setText(QCoreApplication.translate("MainWindow", u"Work Dir", None))
        self.pre_compile_lable_4.setText(QCoreApplication.translate("MainWindow", u"Modelsimini", None))
        self.pre_compile_lable_6.setText(QCoreApplication.translate("MainWindow", u"Wave", None))
        self.compile_commanda_gp.setTitle(QCoreApplication.translate("MainWindow", u"Compile Commands", None))
        self.pre_compile_lable.setText(QCoreApplication.translate("MainWindow", u"Pre Compile", None))
        self.post_compile_lable.setText(QCoreApplication.translate("MainWindow", u"Post Compile", None))
        self.compile_vip_lable.setText(QCoreApplication.translate("MainWindow", u"Compile VIPs", None))
#if QT_CONFIG(tooltip)
        self.compile_design_push_bt.setToolTip(QCoreApplication.translate("MainWindow", u"Generate vrc_compile_design.do (Currently, we only support Xilinx)", None))
#endif // QT_CONFIG(tooltip)
        self.compile_design_push_bt.setText(QCoreApplication.translate("MainWindow", u"Compile Design", None))
#if QT_CONFIG(tooltip)
        self.compile_env_push_bt.setToolTip(QCoreApplication.translate("MainWindow", u"Genereate vrc_compile_env.do", None))
#endif // QT_CONFIG(tooltip)
        self.compile_env_push_bt.setText(QCoreApplication.translate("MainWindow", u"Compile Env", None))
        self.opt_args_gp.setTitle(QCoreApplication.translate("MainWindow", u"Optimization Arguments", None))
        self.opt_defualt_lable.setText(QCoreApplication.translate("MainWindow", u"Default Args:", None))
        self.opt_debug_lable.setText(QCoreApplication.translate("MainWindow", u"Debug Args:", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Codecov Args", None))
        self.opt_visualizer_lable.setText(QCoreApplication.translate("MainWindow", u"Visualizer Args", None))
        self.opt_visualizer_line.setText("")
#if QT_CONFIG(tooltip)
        self.libraries_push_bt.setToolTip(QCoreApplication.translate("MainWindow", u"Get libraries from elaborate.do of the design", None))
#endif // QT_CONFIG(tooltip)
        self.libraries_push_bt.setText(QCoreApplication.translate("MainWindow", u"Libraries", None))
        self.opt_gen_env_lable.setText(QCoreApplication.translate("MainWindow", u"GenEnv Libs", None))
        self.sim_args_gp.setTitle(QCoreApplication.translate("MainWindow", u"Simulation Arguments", None))
        self.vsim_defualt_lable.setText(QCoreApplication.translate("MainWindow", u"Default Args", None))
        self.vsim_debug_lable.setText(QCoreApplication.translate("MainWindow", u"Debug Args:", None))
        self.vsim_codecov_lable.setText(QCoreApplication.translate("MainWindow", u"Codecov Args", None))
        self.vsim_visualizer_lable.setText(QCoreApplication.translate("MainWindow", u"Visualizer Args", None))
        self.vsim_visualizer_line.setText("")
#if QT_CONFIG(tooltip)
        self.vsim_dpi_label.setToolTip(QCoreApplication.translate("MainWindow", u"DPI simulation commands (e.g. -sv_lib mySharedObject)", None))
#endif // QT_CONFIG(tooltip)
        self.vsim_dpi_label.setText(QCoreApplication.translate("MainWindow", u"DPI Args", None))
#if QT_CONFIG(tooltip)
        self.vsim_dpi_textbox.setToolTip(QCoreApplication.translate("MainWindow", u"DPI simulation commands (e.g. -sv_lib mySharedObject)", None))
#endif // QT_CONFIG(tooltip)
        self.MainGUI.setTabText(self.MainGUI.indexOf(self.advance_tab), QCoreApplication.translate("MainWindow", u"Advanced", None))
        self.reg_modes.setTitle(QCoreApplication.translate("MainWindow", u"Reg Modes", None))
#if QT_CONFIG(tooltip)
        self.triage_bt.setToolTip(QCoreApplication.translate("MainWindow", u"Create a file that combines wlf & ucdb ", None))
#endif // QT_CONFIG(tooltip)
        self.triage_bt.setText(QCoreApplication.translate("MainWindow", u"Triage", None))
#if QT_CONFIG(tooltip)
        self.grid_bt.setToolTip(QCoreApplication.translate("MainWindow", u"Runs tests in parallel", None))
#endif // QT_CONFIG(tooltip)
        self.grid_bt.setText(QCoreApplication.translate("MainWindow", u"Grid", None))
#if QT_CONFIG(tooltip)
        self.trend_bt.setToolTip(QCoreApplication.translate("MainWindow", u"Creates coverage graphs", None))
#endif // QT_CONFIG(tooltip)
        self.trend_bt.setText(QCoreApplication.translate("MainWindow", u"Trend", None))
#if QT_CONFIG(tooltip)
        self.delete_vrmdata_bt.setToolTip(QCoreApplication.translate("MainWindow", u"Delete old vrmdata directories", None))
#endif // QT_CONFIG(tooltip)
        self.delete_vrmdata_bt.setText(QCoreApplication.translate("MainWindow", u"Delete Prev vrmdata", None))
#if QT_CONFIG(tooltip)
        self.mail_bt.setToolTip(QCoreApplication.translate("MainWindow", u"Send mail to user when regression is done", None))
#endif // QT_CONFIG(tooltip)
        self.mail_bt.setText(QCoreApplication.translate("MainWindow", u"Mail", None))
#if QT_CONFIG(tooltip)
        self.report_bt.setToolTip(QCoreApplication.translate("MainWindow", u"Creates sim/vrunhtmlreport directory with html coverage report", None))
#endif // QT_CONFIG(tooltip)
        self.report_bt.setText(QCoreApplication.translate("MainWindow", u"Coverage Report", None))
#if QT_CONFIG(tooltip)
        self.rerun_bt.setToolTip(QCoreApplication.translate("MainWindow", u"Rerun failed tests in debug mode after regression is done", None))
#endif // QT_CONFIG(tooltip)
        self.rerun_bt.setText(QCoreApplication.translate("MainWindow", u"Rerun", None))
        self.reg_option_gp.setTitle(QCoreApplication.translate("MainWindow", u"Reg Option", None))
        self.jobs.setText(QCoreApplication.translate("MainWindow", u"Jobs", None))
        self.jobs_combo_bt.setItemText(0, QCoreApplication.translate("MainWindow", u"1", None))
        self.jobs_combo_bt.setItemText(1, QCoreApplication.translate("MainWindow", u"2", None))
        self.jobs_combo_bt.setItemText(2, QCoreApplication.translate("MainWindow", u"3", None))
        self.jobs_combo_bt.setItemText(3, QCoreApplication.translate("MainWindow", u"4", None))
        self.jobs_combo_bt.setItemText(4, QCoreApplication.translate("MainWindow", u"5", None))
        self.jobs_combo_bt.setItemText(5, QCoreApplication.translate("MainWindow", u"6", None))
        self.jobs_combo_bt.setItemText(6, QCoreApplication.translate("MainWindow", u"7", None))
        self.jobs_combo_bt.setItemText(7, QCoreApplication.translate("MainWindow", u"8", None))
        self.jobs_combo_bt.setItemText(8, QCoreApplication.translate("MainWindow", u"9", None))
        self.jobs_combo_bt.setItemText(9, QCoreApplication.translate("MainWindow", u"10", None))
        self.jobs_combo_bt.setItemText(10, QCoreApplication.translate("MainWindow", u"11", None))
        self.jobs_combo_bt.setItemText(11, QCoreApplication.translate("MainWindow", u"12", None))
        self.jobs_combo_bt.setItemText(12, QCoreApplication.translate("MainWindow", u"13", None))
        self.jobs_combo_bt.setItemText(13, QCoreApplication.translate("MainWindow", u"14", None))
        self.jobs_combo_bt.setItemText(14, QCoreApplication.translate("MainWindow", u"15", None))
        self.jobs_combo_bt.setItemText(15, QCoreApplication.translate("MainWindow", u"16", None))
        self.jobs_combo_bt.setItemText(16, QCoreApplication.translate("MainWindow", u"17", None))
        self.jobs_combo_bt.setItemText(17, QCoreApplication.translate("MainWindow", u"18", None))
        self.jobs_combo_bt.setItemText(18, QCoreApplication.translate("MainWindow", u"19", None))
        self.jobs_combo_bt.setItemText(19, QCoreApplication.translate("MainWindow", u"20", None))
        self.jobs_combo_bt.setItemText(20, QCoreApplication.translate("MainWindow", u"21", None))
        self.jobs_combo_bt.setItemText(21, QCoreApplication.translate("MainWindow", u"22", None))
        self.jobs_combo_bt.setItemText(22, QCoreApplication.translate("MainWindow", u"23", None))
        self.jobs_combo_bt.setItemText(23, QCoreApplication.translate("MainWindow", u"24", None))
        self.jobs_combo_bt.setItemText(24, QCoreApplication.translate("MainWindow", u"25", None))
        self.jobs_combo_bt.setItemText(25, QCoreApplication.translate("MainWindow", u"26", None))
        self.jobs_combo_bt.setItemText(26, QCoreApplication.translate("MainWindow", u"27", None))
        self.jobs_combo_bt.setItemText(27, QCoreApplication.translate("MainWindow", u"28", None))
        self.jobs_combo_bt.setItemText(28, QCoreApplication.translate("MainWindow", u"29", None))
        self.jobs_combo_bt.setItemText(29, QCoreApplication.translate("MainWindow", u"30", None))
        self.jobs_combo_bt.setItemText(30, QCoreApplication.translate("MainWindow", u"31", None))
        self.jobs_combo_bt.setItemText(31, QCoreApplication.translate("MainWindow", u"31", None))
        self.jobs_combo_bt.setItemText(32, QCoreApplication.translate("MainWindow", u"32", None))
        self.jobs_combo_bt.setItemText(33, QCoreApplication.translate("MainWindow", u"33", None))
        self.jobs_combo_bt.setItemText(34, QCoreApplication.translate("MainWindow", u"34", None))
        self.jobs_combo_bt.setItemText(35, QCoreApplication.translate("MainWindow", u"35", None))
        self.jobs_combo_bt.setItemText(36, QCoreApplication.translate("MainWindow", u"36", None))
        self.jobs_combo_bt.setItemText(37, QCoreApplication.translate("MainWindow", u"37", None))
        self.jobs_combo_bt.setItemText(38, QCoreApplication.translate("MainWindow", u"38", None))
        self.jobs_combo_bt.setItemText(39, QCoreApplication.translate("MainWindow", u"39", None))
        self.jobs_combo_bt.setItemText(40, QCoreApplication.translate("MainWindow", u"40", None))
        self.jobs_combo_bt.setItemText(41, QCoreApplication.translate("MainWindow", u"41", None))
        self.jobs_combo_bt.setItemText(42, QCoreApplication.translate("MainWindow", u"42", None))
        self.jobs_combo_bt.setItemText(43, QCoreApplication.translate("MainWindow", u"43", None))
        self.jobs_combo_bt.setItemText(44, QCoreApplication.translate("MainWindow", u"44", None))
        self.jobs_combo_bt.setItemText(45, QCoreApplication.translate("MainWindow", u"45", None))
        self.jobs_combo_bt.setItemText(46, QCoreApplication.translate("MainWindow", u"46", None))
        self.jobs_combo_bt.setItemText(47, QCoreApplication.translate("MainWindow", u"47", None))
        self.jobs_combo_bt.setItemText(48, QCoreApplication.translate("MainWindow", u"48", None))
        self.jobs_combo_bt.setItemText(49, QCoreApplication.translate("MainWindow", u"49", None))
        self.jobs_combo_bt.setItemText(50, QCoreApplication.translate("MainWindow", u"50", None))

#if QT_CONFIG(tooltip)
        self.jobs_combo_bt.setToolTip(QCoreApplication.translate("MainWindow", u"Number of cores for the regression run (i.e. number of tests that will run in parallel)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.RankPushBut.setToolTip(QCoreApplication.translate("MainWindow", u"Creates a test list with the top tests that contributed to the coverage report", None))
#endif // QT_CONFIG(tooltip)
        self.RankPushBut.setText(QCoreApplication.translate("MainWindow", u"Rank", None))
        self.load_config_gp_4.setTitle("")
#if QT_CONFIG(tooltip)
        self.testplan_bt.setToolTip(QCoreApplication.translate("MainWindow", u"Choose xml file with coverage links", None))
#endif // QT_CONFIG(tooltip)
        self.testplan_bt.setText(QCoreApplication.translate("MainWindow", u"Test Plan", None))
        self.testplan_line.setText("")
        self.reg_modes_2.setTitle(QCoreApplication.translate("MainWindow", u"Test List Name :", None))
        self.TestNamePushButton.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
#if QT_CONFIG(tooltip)
        self.generics_options_groupbox.setToolTip(QCoreApplication.translate("MainWindow", u"Choose generics sets for regressions", None))
#endif // QT_CONFIG(tooltip)
        self.generics_options_groupbox.setTitle(QCoreApplication.translate("MainWindow", u"Generics", None))
        self.add_generics_sets_button.setText(QCoreApplication.translate("MainWindow", u"Choose generics set", None))
#if QT_CONFIG(tooltip)
        self.clear_generics_table_button.setToolTip(QCoreApplication.translate("MainWindow", u"Clear generics list", None))
#endif // QT_CONFIG(tooltip)
        self.clear_generics_table_button.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        ___qtablewidgetitem = self.regressionGenericsTableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Regression", None));
#if QT_CONFIG(tooltip)
        ___qtablewidgetitem.setToolTip(QCoreApplication.translate("MainWindow", u"Regression number and generic set used in that regression", None));
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.definesPushButton.setToolTip(QCoreApplication.translate("MainWindow", u"Choose project's defines file", None))
#endif // QT_CONFIG(tooltip)
        self.definesPushButton.setText(QCoreApplication.translate("MainWindow", u"Choose defines file", None))
        self.MainGUI.setTabText(self.MainGUI.indexOf(self.regression_tab), QCoreApplication.translate("MainWindow", u"Regression", None))
        self.menufile.setTitle(QCoreApplication.translate("MainWindow", u"Config", None))
        self.menuLink.setTitle(QCoreApplication.translate("MainWindow", u"Link", None))
        self.menuGit.setTitle(QCoreApplication.translate("MainWindow", u"TFS/GIT", None))
    # retranslateUi

