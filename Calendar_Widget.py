from PyQt6.QtWidgets import (QWidget, QCalendarWidget, QPushButton,
                             QLabel, QApplication, QVBoxLayout, QComboBox)
from PyQt6.QtCore import QDate
import sys
from Zuordnung import create_church_servers, ChurchServers
from datetime import time
List_MD = []
create_church_servers("Liste_Messdiener_Computer.xlsx", "Kinder", List_MD)

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

    def unavaiable_day(self):
        selected = Interface.combobox.currentText()
        for b in range(len(List_MD)):
            if selected == List_MD[b].abbreviation:
                break
        List_MD[b].unavailable.append(Interface.cal.selectedDate())
        Interface.lable2.setText(f"{List_MD[b].abbreviation} kann am {Interface.cal.selectedDate().toString()} nicht")


    def select_churchserver(self):
        selected = Interface.combobox.currentText()
        for b in range(len(List_MD)):
            if selected == List_MD[b].abbreviation:
                break
        Interface.lable1.setText(f"{selected} mit Nummer {b}")


    def initUI(self):
        vbox = QVBoxLayout(self)
        button = QPushButton(self)
        Interface.combobox = QComboBox(self)
        Interface.cal = QCalendarWidget(self)
        Interface.cal.setGridVisible(True)
        Interface.cal.clicked[QDate].connect(self.showDate)
        button.clicked.connect(self.unavaiable_day)
        for x in range(len(List_MD)):
            Interface.combobox.addItem(List_MD[x].abbreviation)


        vbox.addWidget(Interface.cal)
        vbox.addWidget(button)
        vbox.addWidget(Interface.combobox)

        self.lbl = QLabel(self)
        date = Interface.cal.selectedDate()
        self.lbl.setText(date.toString())

        Interface.lable2 = QLabel(self)
        Interface.lable1 = QLabel(self)
        Interface.lable3 = QLabel(self)
        Interface.combobox.activated.connect(self.select_churchserver)
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
