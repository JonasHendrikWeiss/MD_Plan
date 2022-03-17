from PyQt6.QtWidgets import (QWidget, QCalendarWidget, QPushButton, QMenuBar,
                             QLabel, QApplication, QGridLayout, QComboBox, QListWidget)
from PyQt6 import QtGui, QtCore, QtWidgets
import sys
from Availabilty_Logic import create_list_of_groups
from Panda_To_Storage import import_churchservers_from_dataframe, json_to_pdataframe
from Availabilty_Logic import get_amount_of_elements
# A File to handle the view of the availability page of the application

List_MD = []
# import all the churchservers from the JSON file
import_churchservers_from_dataframe(json_to_pdataframe(), List_MD)


class Ui_AvailabilityWindow(QWidget):

    calendarWidget = None
    comboBox_Grades = None
    comboBox_Churchservers = None
    listWidget = None

    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        vbox = QGridLayout(self)
        calendarWidget = QCalendarWidget(self)

        comboBox_Grades = QComboBox(self)
        comboBox_Churchservers = QComboBox(self)

        push_button_single_day = QPushButton(self, text= "Für einen Tag Abmelden")
        push_button_start_day = QPushButton(self, text= "Start Abmeldung")
        push_button_end_day = QPushButton(self, text="Ende Abmeldung")
        push_button_remove_day = QPushButton(self, text="Abmeldung löschen")
        push_button_save = QPushButton(self, text= "Speichern")


        Ui_AvailabilityWindow.listWidget = QListWidget(self)

        self.setLayout(vbox)

        self.setGeometry(350, 300, 500, 600)
        self.setWindowTitle('Abmeldungen - Messdienerplan')

        vbox.addWidget(calendarWidget, 0, 0, 2, 2)
        #calendarWidget.setSelectionMode(QItemSelectionModel())
        vbox.addWidget(Ui_AvailabilityWindow.listWidget, 0, 4, 2, 4)
        Ui_AvailabilityWindow.listWidget.addItem("test1")
        Ui_AvailabilityWindow.listWidget.addItem("test2")
        Ui_AvailabilityWindow.listWidget.addItem("test3")
        # Changes the the selection mode to multi selection
        Ui_AvailabilityWindow.listWidget.setSelectionMode(Ui_AvailabilityWindow.listWidget.SelectionMode(3))
        vbox.addWidget(comboBox_Grades, 1, 0)
        vbox.addWidget(comboBox_Churchservers, 1, 1)
        comboBox_Grades.addItems(create_list_of_groups(List_MD)[2])

        vbox.addWidget(push_button_single_day, 1, 3)
        vbox.addWidget(push_button_start_day, 2, 3)
        vbox.addWidget(push_button_end_day, 2, 4)
        vbox.addWidget(push_button_remove_day, 2, 6, 1, 2)
        vbox.addWidget(push_button_save, 5, 7)

        Ui_AvailabilityWindow.listWidget.itemSelectionChanged.connect(self.return_multi_selection)

        self.show()


    def return_multi_selection(self):
        # returns all selected Items in a list
        selected_list = []
        for x in range(Ui_AvailabilityWindow.listWidget.count()):
            if Ui_AvailabilityWindow.listWidget.item(x).isSelected() == True:
                selected_list.append(Ui_AvailabilityWindow.listWidget.item(x).text())
        return selected_list


    def add_items(self, list_new_items):
        # A function to add all Items of a given list as strings to a combobox
        for x in range(len(list_new_items)):
            self.additem(str(list_new_items[x]))



def main():

    app = QApplication(sys.argv)
    ex = Ui_AvailabilityWindow()
    sys.exit(app.exec())


main()