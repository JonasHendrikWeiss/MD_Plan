
import sys

from PySide6.QtCore import QFile, QIODevice
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QListWidgetItem

from PySide6.QtGui import QPainter
from Zuordnung import TimeSpan
from Availabilty_Logic import add_server_objects, remove_unavailable_days, add_grades_to_combobox
from Storage_Operations import unpickle_storage, pickle_storage, list_to_json, data_storage
from datetime import datetime


class Availability_Window():
    view = None
    start_date = None
    data = unpickle_storage()
    # import_churchservers_from_dataframe(json_to_pdataframe(), data.list_churchservers)


    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        #Import the view from an UI file
        ui_file_name = "Availability_Window.ui"
        ui_file = QFile(ui_file_name)
        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
            sys.exit(-1)
        Availability_Window.view = QUiLoader().load(ui_file)
        ui_file.close()
        #Assignment_Window.view.show()

        # This section fills the combobox with data
        add_grades_to_combobox(Availability_Window.data, Availability_Window.view.comboBox_Grades)

        Availability_Window.view.comboBox_Grades.setCurrentIndex(-1)
        Availability_Window.view.comboBox_Grades.setPlaceholderText("Schuljahre")
        Availability_Window.view.comboBox_Churchservers.setPlaceholderText("Messdiener")

        # This section is used to add connections to buttons and other parts of the view
        # self. Doesnt work if you want to export things
        Availability_Window.view.listWidget.itemSelectionChanged.connect(Availability_Window.return_multi_selection)
        Availability_Window.view.comboBox_Grades.activated.connect(
            Availability_Window.fill_churchserver_selection_button)
        Availability_Window.view.comboBox_Churchservers.activated.connect(
            Availability_Window.fill_list_with_unavailable)
        Availability_Window.view.push_button_single_day.clicked.connect(Availability_Window.unavailable_day)
        Availability_Window.view.push_button_save.clicked.connect(Availability_Window.initiate_saving)
        Availability_Window.view.push_button_remove_day.clicked.connect(Availability_Window.initiate_removal_days)
        Availability_Window.view.push_button_start_day.clicked.connect(Availability_Window.select_start_day)
        Availability_Window.view.push_button_end_day.clicked.connect(Availability_Window.select_end_day)

    def return_multi_selection():
        # returns all selected Items in a list
        selected_list = []
        for x in range(Availability_Window.view.listWidget.count()):
            if Availability_Window.view.listWidget.item(x).isSelected() == True:
                selected_list.append(Availability_Window.view.listWidget.item(x).data(0x0100))
        return selected_list # 0x0100 is the integer for a Qt.UserRole

    def test_connection(self):  # Function is only used if there is doubt whether a connect is working
        print("Connection works")



    def add_timespan_object(selected_object, churchserver):
        # Adds all the TimeSpan Objects to the selected an_object
        for span_number in range(len(churchserver.unavailable)):  # iterates through all possible TimeSpan objects
            item_to_add = QListWidgetItem() # Adds a temporary custom QListWidgetItem in order to support data
            selected_span = churchserver.unavailable[span_number]
            item_to_add.setText(selected_span.description)
            item_to_add.setData(0x0100, selected_span)  # 0x0100 is the integer for a Qt.UserRole
            selected_object.addItem(item_to_add)

    def select_start_day(self):
        if Availability_Window.view.comboBox_Churchservers.currentData() != None:
            Availability_Window.start_date = Availability_Window.view.calendarWidget.selectedDate().toPython()
            Availability_Window.view.label_start_day.setText(Availability_Window.start_date.isoformat())
            Availability_Window.view.push_button_end_day.setEnabled(True)

    def select_end_day(self):
        selected_end_time = Availability_Window.view.calendarWidget.selectedDate().toPython()
        selected_server = Availability_Window.view.comboBox_Churchservers.currentData()
        new_timespan = TimeSpan(Availability_Window.start_date, selected_end_time)
        selected_server.add_unavailable(new_timespan)  # uses the add unavailable function to look and merge duplicates
        # Resets the view and data so there is nothing carried over to the next operation
        Availability_Window.fill_list_with_unavailable(Availability_Window.view.listWidget)
        Availability_Window.start_date = None
        Availability_Window.view.label_start_day.setText("Start Abmeldung")
        Availability_Window.view.push_button_end_day.setEnabled(False)


    
    def fill_churchserver_selection_button(self):
        # Rebuild to do more in Availability Logic
        grade = Availability_Window.view.comboBox_Grades.currentData()
        combobox_cservers = Availability_Window.view.comboBox_Churchservers
        combobox_cservers.clear()
        add_server_objects(combobox_cservers, grade.members)
        # Clears the list widget so old data is not carried over to a new church server
        Availability_Window.clear_on_changed_server()
    
    def fill_list_with_unavailable(self):
        selected_server = Availability_Window.view.comboBox_Churchservers.currentData()

        #print(get_unavailable_dates(selected_server))
        Availability_Window.clear_on_changed_server()
        Availability_Window.add_timespan_object(Availability_Window.view.listWidget, selected_server)

        Availability_Window.view.listWidget.sortItems()
    
    def unavailable_day(self):
        selected_server = Availability_Window.view.comboBox_Churchservers.currentData()

        if selected_server == None:
            # Is only relevant if the button is clicked for the first time without making any other selections
            print("No Selection")
            return
        # returns the date of the calendar as a python Datetime an_object
        selected_datetime=Availability_Window.view.calendarWidget.selectedDate().toPython()
        new_day = TimeSpan(selected_datetime, selected_datetime)  # Sets the start and end date to the same day
        selected_server.add_unavailable(new_day)  # uses the add unavailable function to look and merge duplicates
        Availability_Window.fill_list_with_unavailable(Availability_Window.view.listWidget)
    
    def initiate_saving(self):
        pickle_storage(Availability_Window.data, filename="data_storage.pkl")
        print(f"Saving {len(Availability_Window.data.list_churchservers)} MD")

    def initiate_removal_days(self):
        # Get the Server that is selected in the Church Server Combobox
        selected_server = Availability_Window.view.comboBox_Churchservers.currentData()
        current_selection = Availability_Window.return_multi_selection()
        remove_unavailable_days(church_server=selected_server,
                                unavailable_days=current_selection)
        Availability_Window.fill_list_with_unavailable(Availability_Window.view.listWidget)

    def clear_on_changed_server():
        # Clears all Data in the view and some other values so a new ChurchServer has no data of the old one
        Availability_Window.view.listWidget.clear()
        Availability_Window.start_date = None
        Availability_Window.view.label_start_day.setText("Start Abmeldung")
        Availability_Window.view.push_button_end_day.setEnabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    b = Availability_Window()
    b.view.show()
    app.exec()


