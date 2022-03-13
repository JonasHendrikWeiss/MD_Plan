from PyQt6.QtWidgets import (QWidget, QCalendarWidget, QPushButton,
                             QLabel, QApplication, QVBoxLayout, QComboBox)
from PyQt6.QtCore import QDate
import sys
from Panda_To_Storage import *
from Zuordnung import create_church_servers, ChurchServers
from datetime import time
List_MD = []
# import all the churchservers from the JSON file
import_churchservers_from_dataframe(json_to_pdataframe(), List_MD)


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
        List_MD[b].unavailable.append(Interface.cal.selectedDate().toPyDate().isoformat())
        Interface.lable2.setText(f"{List_MD[b].abbreviation} kann am {Interface.cal.selectedDate().toString()} nicht")
        list_to_json(list=List_MD)


    def select_churchserver(self):
        selected = Interface.combobox.currentText()
        for b in range(len(List_MD)):
            if selected == List_MD[b].abbreviation:
                break
        Interface.lable1.setText(f"{selected} mit Nummer {b}")


    def initUI(self):
        vbox = QVBoxLayout(self)
        button = QPushButton(self, text="Abmeldung")
        Interface.combobox = QComboBox(self)
        Interface.cal = QCalendarWidget(self)
        Interface.cal.setGridVisible(True)
        Interface.cal.clicked[QDate].connect(self.showDate)
        # If the button is clicked it starts the unavailable day  function,
        # which makes a ChurchServer unavailable on a given day
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
        #vbox.addWidget(button_write_plan)
        #vbox.addWidget(button_availability)
        #vbox.addWidget(button_manage_cservers)
        #vbox.addWidget(button_settings)
        self.show()





def main():

    app = QApplication(sys.argv)
    ex = Interface()
    sys.exit(app.exec())


main()
