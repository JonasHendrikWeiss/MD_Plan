from PyQt6.QtWidgets import (QWidget, QCalendarWidget, QPushButton, QMenuBar,
                             QLabel, QApplication, QGridLayout, QComboBox, QListWidget)
from PyQt6 import QtGui, QtCore, QtWidgets
import sys
from Availabilty_Logic import create_list_of_groups, get_server_from_abbreviation, get_unavailable_dates, remove_unavailable_days
from Panda_To_Storage import import_churchservers_from_dataframe, json_to_pdataframe, list_to_json, data_storage
from Availabilty_Logic import get_amount_of_elements
# A File to handle the view of the availability page of the application

List_MD = data_storage()
# import all the churchservers from the JSON file
import_churchservers_from_dataframe(json_to_pdataframe(), List_MD.list_churchservers)


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
        Ui_AvailabilityWindow.calendarWidget = QCalendarWidget(self)

        Ui_AvailabilityWindow.comboBox_Grades = QComboBox(self)
        Ui_AvailabilityWindow.comboBox_Churchservers = QComboBox(self)

        push_button_single_day = QPushButton(self, text= "Für einen Tag Abmelden")
        push_button_start_day = QPushButton(self, text= "Start Abmeldung")
        push_button_end_day = QPushButton(self, text="Ende Abmeldung")
        push_button_remove_day = QPushButton(self, text="Abmeldung löschen")
        push_button_save = QPushButton(self, text= "Speichern")


        Ui_AvailabilityWindow.listWidget = QListWidget(self)

        self.setLayout(vbox)

        self.setGeometry(350, 300, 500, 600)
        self.setWindowTitle('Abmeldungen - Messdienerplan')

        vbox.addWidget(Ui_AvailabilityWindow.calendarWidget, 0, 0, 2, 2)
        vbox.addWidget(Ui_AvailabilityWindow.listWidget, 0, 4, 2, 4)
        # Changes the the selection mode to multi selection
        Ui_AvailabilityWindow.listWidget.setSelectionMode(Ui_AvailabilityWindow.listWidget.SelectionMode(3))
        vbox.addWidget(Ui_AvailabilityWindow.comboBox_Grades, 1, 0)
        vbox.addWidget(Ui_AvailabilityWindow.comboBox_Churchservers, 1, 1)
        Ui_AvailabilityWindow.comboBox_Grades.addItems(create_list_of_groups(List_MD.list_churchservers)[2])

        vbox.addWidget(push_button_single_day, 1, 3)
        vbox.addWidget(push_button_start_day, 2, 3)
        vbox.addWidget(push_button_end_day, 2, 4)
        vbox.addWidget(push_button_remove_day, 2, 6, 1, 2)
        vbox.addWidget(push_button_save, 5, 7)



        # TODO Build a Function for returning the List_MD
        self.show()
        # This part of the program handles the connections of all the objects in the view

        Ui_AvailabilityWindow.listWidget.itemSelectionChanged.connect(self.return_multi_selection)
        Ui_AvailabilityWindow.comboBox_Grades.activated.connect(self.fill_churchserver_selection_button)
        Ui_AvailabilityWindow.comboBox_Churchservers.activated.connect(self.fill_list_with_unavailable)
        push_button_single_day.clicked.connect(self.unavailable_day)
        push_button_save.clicked.connect(self.initiate_saving)
        push_button_remove_day.clicked.connect(self.initiate_removal_days)
        # TODO build a error handling for clicking this button before selecting both group and Churchserver


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


    def fill_churchserver_selection_button(self):
        # TODO find out why this funciton doesn't work in Availability Logic
        # Rebuild to do more in Availability Logic
        grade = Ui_AvailabilityWindow.comboBox_Grades.currentText()
        combobox_cservers = Ui_AvailabilityWindow.comboBox_Churchservers
        combobox_cservers.clear()
        list_all_servers = List_MD.list_churchservers
        temporary_data = create_list_of_groups(list_all_servers)
        index_selected_grade = temporary_data[2].index(grade)
        for x in range(len(temporary_data[0][index_selected_grade])):
            combobox_cservers.addItem(temporary_data[0][index_selected_grade][x].abbreviation)



    def fill_list_with_unavailable(self):
        selected_server = get_server_from_abbreviation(Ui_AvailabilityWindow.comboBox_Churchservers.currentText(),
                                                       List_MD)
        print(get_unavailable_dates(selected_server))
        Ui_AvailabilityWindow.listWidget.clear()
        Ui_AvailabilityWindow.listWidget.addItems(get_unavailable_dates(selected_server))
        Ui_AvailabilityWindow.listWidget.sortItems()

    def unavailable_day(self):
        selected_server = get_server_from_abbreviation(Ui_AvailabilityWindow.comboBox_Churchservers.currentText(),
                                                       List_MD)
        if Ui_AvailabilityWindow.calendarWidget.selectedDate().toPyDate().isoformat() not in selected_server.unavailable:
            selected_server.unavailable.append(Ui_AvailabilityWindow.calendarWidget.selectedDate().toPyDate().isoformat())
            Ui_AvailabilityWindow.fill_list_with_unavailable(Ui_AvailabilityWindow.listWidget)
        else:
            print("error")

    def initiate_saving(self):
        print(List_MD.list_churchservers[0].unavailable)
        print(List_MD.list_churchservers[0].abbreviation)
        list_to_json(List_MD.list_churchservers)

    def initiate_removal_days(self):
        # Get the Server that is selected in the Church Server Combobox
        selected_server = get_server_from_abbreviation(Ui_AvailabilityWindow.comboBox_Churchservers.currentText(),
                                                       List_MD)
        current_selection = Ui_AvailabilityWindow.return_multi_selection(Ui_AvailabilityWindow.listWidget)
        remove_unavailable_days(church_server=selected_server,
                                unavailable_days=current_selection)
        Ui_AvailabilityWindow.fill_list_with_unavailable(Ui_AvailabilityWindow.listWidget)


def main():

    app = QApplication(sys.argv)
    ex = Ui_AvailabilityWindow()
    sys.exit(app.exec())


main()