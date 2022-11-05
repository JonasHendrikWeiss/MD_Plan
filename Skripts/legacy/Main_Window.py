from PyQt6.QtWidgets import (QWidget, QCalendarWidget, QPushButton,
                             QLabel, QApplication, QVBoxLayout, QComboBox)
from PyQt6.QtCore import QDate
import sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        vbox = QVBoxLayout(self)
        button_write_plan = QPushButton(self, text="Messdienerplan")
        button_availability = QPushButton(self, text="Abmeldungen")
        button_manage_cservers = QPushButton(self, text="Messdiener Verwalten")
        button_settings = QPushButton(self, text="Einstellungen")
        self.resize(251, 304)
        """
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(40, 20, 171, 41))
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(40, 80, 171, 41))
        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(40, 140, 171, 41))
        self.pushButton_4 = QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(40, 200, 171, 41))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 251, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)"""



        vbox.addWidget(button_write_plan)
        vbox.addWidget(button_availability)
        vbox.addWidget(button_manage_cservers)
        vbox.addWidget(button_settings)
        self.lbl = QLabel(self)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Hauptmenü - Messdienerplan')
        self.show()





def main():

    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec())


main()



"""
# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindowUPYQBp.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
                            QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
                           QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
                           QRadialGradient)
from PySide2.QtWidgets import *


class Ui_MainWindow(an_object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(251, 304)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(40, 20, 171, 41))
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(40, 80, 171, 41))
        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(40, 140, 171, 41))
        self.pushButton_4 = QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(40, 200, 171, 41))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 251, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Messdienerplan - Hauptmen\u00fc", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Messdienerplan schreiben", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Abmeldungen", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Messdiener Verwalten", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"Einstellungen", None))
    # retranslateUi
    
    """