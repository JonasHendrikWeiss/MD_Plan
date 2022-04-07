
import sys

from PySide6.QtCore import QFile, QIODevice, QRect
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication

from PySide6.QtGui import QPainter
from Zuordnung import TimeSpan
from Availabilty_Logic import create_list_of_groups, get_unavailable_dates, remove_unavailable_days
from Assignment_Logic import create_new_churchservice
from Panda_To_Storage import import_churchservers_from_dataframe, json_to_pdataframe, list_to_json, data_storage

data = data_storage()
# import all the churchservers from the JSON file
import_churchservers_from_dataframe(json_to_pdataframe(), data.list_churchservers)

# TODO replace strings in Churchserver.unavailable with TimeSpan objects and clear all data in the Churchserver objects
class Assignment_Window():
    view = None
    data = data_storage()
    import_churchservers_from_dataframe(json_to_pdataframe(), data.list_churchservers)


    def __init__(self):
        super().__init__()
        print(Assignment_Window.data)
        self.initUI()


    def initUI(self):
        #Import the view from an UI file
        pass

        ui_file_name = "Availability_Window.ui"
        ui_file = QFile(ui_file_name)
        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
            sys.exit(-1)
        Assignment_Window.view = QUiLoader().load(ui_file)
        ui_file.close()
        #Assignment_Window.view.show()

        #This section fills the combobox with data
        Assignment_Window.view.comboBox_Grades.addItems(create_list_of_groups(Assignment_Window.data.list_churchservers)[1])
        Assignment_Window.view.comboBox_Grades.setCurrentIndex(-1)
        Assignment_Window.view.comboBox_Grades.setPlaceholderText("Schuljahre")
        Assignment_Window.view.comboBox_Churchservers.setPlaceholderText("Messdiener")

        # This section is used to add connections to buttons and other parts of the view
        # self. Doesnt work if you want to export things
        Assignment_Window.view.listWidget.itemSelectionChanged.connect(Assignment_Window.return_multi_selection)
        Assignment_Window.view.comboBox_Grades.activated.connect(Assignment_Window.fill_churchserver_selection_button)
        Assignment_Window.view.comboBox_Churchservers.activated.connect(Assignment_Window.fill_list_with_unavailable)
        Assignment_Window.view.push_button_single_day.clicked.connect(Assignment_Window.unavailable_day)
        Assignment_Window.view.push_button_save.clicked.connect(Assignment_Window.initiate_saving)
        Assignment_Window.view.push_button_remove_day.clicked.connect(Assignment_Window.initiate_removal_days)
        Assignment_Window.view.push_button_start_day.clicked.connect(Assignment_Window.print_yes)

        #sys.exit(app.exec())

    
    def return_multi_selection():
        # returns all selected Items in a list
        selected_list = []
        for x in range(Assignment_Window.view.listWidget.count()):
            if Assignment_Window.view.listWidget.item(x).isSelected() == True:
                selected_list.append(Assignment_Window.view.listWidget.item(x).text())
        return selected_list


    def print_yes(self):
        print()
    
    
    def add_server_objects( selected_object, list_servers):
        # A function to add all Items of a given list as strings to a combobox
        for x in range(len(list_servers)):
            selected_server = list_servers[x]
            selected_object.addItem(selected_server.abbreviation, userData=selected_server) # adds the Abbreviation as a
            # string and the object as userData
    
    
    def fill_churchserver_selection_button(self):
        # Rebuild to do more in Availability Logic
        grade = Assignment_Window.view.comboBox_Grades.currentText()
        combobox_cservers = Assignment_Window.view.comboBox_Churchservers
        combobox_cservers.clear()
        list_all_servers = Assignment_Window.data.list_churchservers
        temporary_data = create_list_of_groups(list_all_servers)
        index_selected_grade = temporary_data[1].index(grade)
        Assignment_Window.add_server_objects(combobox_cservers, temporary_data[0][index_selected_grade])
        # Clears the list widget so old data is not carried over to a new church server
        Assignment_Window.view.listWidget.clear()



    
    def fill_list_with_unavailable(self):
        selected_server = Assignment_Window.view.comboBox_Churchservers.currentData()

        print(get_unavailable_dates(selected_server))
        Assignment_Window.view.listWidget.clear()

        Assignment_Window.view.listWidget.addItems(get_unavailable_dates(selected_server))
        Assignment_Window.view.listWidget.sortItems()
    
    def unavailable_day(self):
        selected_server = Assignment_Window.view.comboBox_Churchservers.currentData()


        if selected_server == None:
            # Is only relevant if the button is clicked for the first time without making any other selections
            print("No Selection")
            return
        selected_datetime=Assignment_Window.view.calendarWidget.selectedDate().toPython()
        new_day = TimeSpan(selected_datetime, selected_datetime)  # Sets the start and end date to the same day
        selected_server.add_unavailable(new_day)  # uses the add unavailable function to look and merge duplicates
        Assignment_Window.fill_list_with_unavailable(Assignment_Window.view.listWidget)
    
    def initiate_saving(self):
        list_to_json(Assignment_Window.data.list_churchservers)

    def initiate_removal_days(self):
        # Get the Server that is selected in the Church Server Combobox
        selected_server = Assignment_Window.view.comboBox_Churchservers.currentData()
        current_selection = Assignment_Window.return_multi_selection()
        remove_unavailable_days(church_server=selected_server,
                                unavailable_days=current_selection)
        Assignment_Window.fill_list_with_unavailable(Assignment_Window.view.listWidget)
        #TODO Rebuild this function because it doesnt work after the switch to TimeSpan Objects

if __name__ == "__main__":
    app = QApplication(sys.argv)
    b = Assignment_Window()
    b.view.show()
    app.exec()
