from PyQt6.QtWidgets import (QWidget, QCalendarWidget, QPushButton,
                             QLabel, QApplication, QVBoxLayout, QComboBox)
from PyQt6.QtCore import QDate
import sys
from datetime import time



class Interface(QWidget):
    count = 0
    cal = None
    combobox = None
    lable1 = None
    lable2 = None

    def __init__(self):
        super().__init__()
        self.initUI()

    def showDate(self, date):
        self.lbl.setText(date.toString())

    def testfunction(self):
        Interface.count += 1
        Interface.lable2.setText(f" {Interface.cal.selectedDate().toString()}")

    def changefunction(self):
        Interface.lable1.setText(Interface.combobox.currentIndex)


    def initUI(self):
        vbox = QVBoxLayout(self)
        button = QPushButton(self)
        Interface.combobox = QComboBox(self)
        Interface.cal = QCalendarWidget(self)
        Interface.cal.setGridVisible(True)
        Interface.cal.clicked[QDate].connect(self.showDate)
        button.clicked.connect(self.testfunction)

        Interface.combobox.addItem("test")
        Interface.combobox.addItem("best2")
        Interface.combobox.addItem("test3")
        vbox.addWidget(Interface.cal)
        vbox.addWidget(button)
        vbox.addWidget(Interface.combobox)

        self.lbl = QLabel(self)
        date = Interface.cal.selectedDate()
        self.lbl.setText(date.toString())

        Interface.lable2 = QLabel(self)
        Interface.lable1 = QLabel(self)
        Interface.lable3 = QLabel(self)
        Interface.combobox.activated.connect(self.changefunction)
        vbox.addWidget(self.lbl)
        vbox.addWidget(self.lable2)
        vbox.addWidget(self.lable1)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Calendar')
        self.show()





def main():

    app = QApplication(sys.argv)
    ex = Interface()
    sys.exit(app.exec())


main()
