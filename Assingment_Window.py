from PyQt6.QtWidgets import (QWidget, QCalendarWidget, QPushButton, QMenuBar,
                             QLabel, QApplication, QGridLayout, QComboBox, QListWidget)
from PyQt6 import QtGui, QtCore, QtWidgets
import sys
from Availabilty_Logic import create_list_of_groups, get_server_from_abbreviation, get_unavailable_dates, remove_unavailable_days
from Panda_To_Storage import import_churchservers_from_dataframe, json_to_pdataframe, list_to_json, data_storage

List_MD = data_storage()
# import all the churchservers from the JSON file
import_churchservers_from_dataframe(json_to_pdataframe(), List_MD.list_churchservers)


class Assingment_Window(QWidget):

    calendarWidget = None
    comboBox_Grades = None
    comboBox_Churchservers = None
    comboBox_Service = None
    listWidget = None

    def __init__(self):
        super().__init__()
        self.initUI()



    def initUI(self):
        vbox = QGridLayout(self)
        Assingment_Window.calendarWidget = QCalendarWidget(self)

        Assingment_Window.comboBox_Grades = QComboBox(self)
        Assingment_Window.comboBox_Churchservers = QComboBox(self)
        Assingment_Window.comboBox_Service = QComboBox(self)

        push_button_fill = QPushButton(self, text="Messe mit Messdiener füllen")
        push_button_add_service = QPushButton(self, text= "Messe hinzufügen")
        push_button_remove_service = QPushButton(self, text= "Messe löschen")
        push_button_remove_cserver = QPushButton(self, text="Messdiener entfernen")
        push_button_save = QPushButton(self, text= "Speichern")
        push_button_add_server = QPushButton(self, text= "Messdiener hinzufügen")

        Assingment_Window.listWidget = QListWidget(self)

        self.setLayout(vbox)

        self.setGeometry(350, 300, 500, 600)
        self.setWindowTitle('Plan schreiben - Messdienerplan')

        vbox.addWidget(Assingment_Window.calendarWidget, 0, 0, 2, 2)
        vbox.addWidget(Assingment_Window.listWidget, 0, 4, 2, 4)
        # Changes the the selection mode to multi selection
        Assingment_Window.listWidget.setSelectionMode(Assingment_Window.listWidget.SelectionMode(3))
        vbox.addWidget(Assingment_Window.comboBox_Service, 1, 0, 1,2 )
        vbox.addWidget(Assingment_Window.comboBox_Grades, 2, 4)
        vbox.addWidget(Assingment_Window.comboBox_Churchservers, 2, 5)

        vbox.addWidget(push_button_add_service, 1, 3)
        vbox.addWidget(push_button_remove_service, 2, 3)
        vbox.addWidget(push_button_fill, 3, 3)

        vbox.addWidget(push_button_remove_cserver, 4, 7)
        vbox.addWidget(push_button_add_server, 5, 7,)
        vbox.addWidget(push_button_save, 6, 7)


        self.show()


def main():

    app = QApplication(sys.argv)
    ex = Assingment_Window()
    sys.exit(app.exec())


main()