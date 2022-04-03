from PyQt6.QtWidgets import (QWidget, QCalendarWidget, QPushButton, QSpinBox,
                             QLabel, QApplication, QGridLayout, QComboBox, QListWidget)
from PyQt6 import QtGui, QtCore, QtWidgets
import sys
from Availabilty_Logic import create_list_of_groups, get_server_from_abbreviation, get_unavailable_dates, remove_unavailable_days
from Assignment_Logic import create_new_churchservice
from Panda_To_Storage import import_churchservers_from_dataframe, json_to_pdataframe, list_to_json, data_storage

data = data_storage()
# import all the churchservers from the JSON file
import_churchservers_from_dataframe(json_to_pdataframe(), data.list_churchservers)


class Assingment_Window(QWidget):
    spinbox_server = None
    calendarWidget = None
    comboBox_Grades = None
    comboBox_Churchservers = None
    comboBox_Service = None
    listWidget = None
    output_label = None

    def __init__(self):
        super().__init__()
        self.initUI()



    def initUI(self):
        vbox = QGridLayout(self)

        Assingment_Window.calendarWidget = QCalendarWidget(self)
        Assingment_Window.spinbox_server = QSpinBox(self)
        Assingment_Window.comboBox_Grades = QComboBox(self)
        Assingment_Window.comboBox_Churchservers = QComboBox(self)
        Assingment_Window.comboBox_Service = QComboBox(self)
        Assingment_Window.output_label = QLabel(self, text= "LABEL")

        push_button_fill = QPushButton(self, text="Messe mit Messdiener füllen")
        push_button_add_service = QPushButton(self, text= "Messe hinzufügen")
        push_button_remove_service = QPushButton(self, text= "Messe löschen")
        push_button_remove_cserver = QPushButton(self, text="Messdiener entfernen")
        push_button_save = QPushButton(self, text= "Speichern")
        push_button_add_server = QPushButton(self, text= "Messdiener hinzufügen")

        Assingment_Window.spinbox_server.setValue(8)

        Assingment_Window.listWidget = QListWidget(self)

        self.setLayout(vbox)

        self.setGeometry(350, 300, 500, 600)
        self.setWindowTitle('Plan schreiben - Messdienerplan')

        # Changes the the selection mode to multi selection
        Assingment_Window.listWidget.setSelectionMode(Assingment_Window.listWidget.SelectionMode(3))
        # Moves Widgets to the correct position
        vbox.addWidget(Assingment_Window.calendarWidget, 0, 0, 2, 2)
        vbox.addWidget(Assingment_Window.listWidget, 0, 4, 2, 4)
        vbox.addWidget(Assingment_Window.comboBox_Service, 1, 0, 1,2 )
        vbox.addWidget(Assingment_Window.comboBox_Grades, 2, 4)
        vbox.addWidget(Assingment_Window.comboBox_Churchservers, 2, 5)
        vbox.addWidget(Assingment_Window.output_label, 0, 2, 2, 3)
        vbox.addWidget(push_button_add_service, 1, 3)
        vbox.addWidget(push_button_remove_service, 3, 3)
        vbox.addWidget(push_button_fill, 4, 3)
        vbox.addWidget(Assingment_Window.spinbox_server, 2, 3)

        vbox.addWidget(push_button_remove_cserver, 4, 7)
        vbox.addWidget(push_button_add_server, 5, 7,)
        vbox.addWidget(push_button_save, 6, 7)
        self.show()

        # This section is used to add connections to buttons and other parts of the view
        push_button_add_service.clicked.connect(self.init_new_service)
        push_button_remove_service.clicked.connect(self.delete_selected_service)

    def fill_combobox_with_services(self):
        Assingment_Window.comboBox_Service.clear()
        for x in range(len(data.list_services)):
            Assingment_Window.comboBox_Service.addItem(data.list_services[x].description)

    def init_new_service(self):
        selected_date = Assingment_Window.calendarWidget.selectedDate().toPyDate().isoformat()
        create_new_churchservice(date=selected_date, number_of_chuchservers=Assingment_Window.spinbox_server.value(),
                                 storage_location=data.list_services)
        self.fill_combobox_with_services()

    def delete_selected_service(self):
        selected_service_str = Assingment_Window.comboBox_Service.currentText()
        Assingment_Window.output_label.setText(selected_service_str)

        




def main():

    app = QApplication(sys.argv)
    ex = Assingment_Window()
    sys.exit(app.exec())


main()