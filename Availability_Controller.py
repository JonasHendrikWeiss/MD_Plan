
import sys

from PySide6.QtCore import QFile, QIODevice
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication


from Availabilty_Logic import create_list_of_groups, get_server_from_abbreviation, get_unavailable_dates, remove_unavailable_days
from Assignment_Logic import create_new_churchservice
from Panda_To_Storage import import_churchservers_from_dataframe, json_to_pdataframe, list_to_json, data_storage

data = data_storage()
# import all the churchservers from the JSON file
import_churchservers_from_dataframe(json_to_pdataframe(), data.list_churchservers)


class Assignment_Window():
    view = None

    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        #Import the view from an UI file
        app = QApplication(sys.argv)

        ui_file_name = "Availability_Window.ui"
        ui_file = QFile(ui_file_name)
        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
            sys.exit(-1)
        Assignment_Window.view = QUiLoader().load(ui_file)
        ui_file.close()
        Assignment_Window.view.show()

        #This section fills the combobox with data
        Assignment_Window.view.comboBox_Grades.addItems(create_list_of_groups(data.list_churchservers)[1])

        # This section is used to add connections to buttons and other parts of the view
        Assignment_Window.view.listWidget.itemSelectionChanged.connect(self.return_multi_selection)
        Assignment_Window.view.comboBox_Grades.activated.connect(self.fill_churchserver_selection_button)
        Assignment_Window.view.comboBox_Churchservers.activated.connect(self.fill_list_with_unavailable)
        Assignment_Window.view.push_button_single_day.clicked.connect(self.unavailable_day)
        Assignment_Window.view.push_button_save.clicked.connect(self.initiate_saving)
        Assignment_Window.view.push_button_remove_day.clicked.connect(self.initiate_removal_days)
        sys.exit(app.exec())
    # TODO build a error handling for clicking this button before selecting both group and Churchserver

    
    def return_multi_selection(self):
        # returns all selected Items in a list
        selected_list = []
        for x in range(Assignment_Window.view.listWidget.count()):
            if Assignment_Window.view.listWidget.item(x).isSelected() == True:
                selected_list.append(Assignment_Window.view.listWidget.item(x).text())
        return selected_list
    
    
    def add_items(self, list_new_items):
        # A function to add all Items of a given list as strings to a combobox
        for x in range(len(list_new_items)):
            self.additem(str(list_new_items[x]))
    
    
    def fill_churchserver_selection_button(self):
        # Rebuild to do more in Availability Logic
        grade = Assignment_Window.view.comboBox_Grades.currentText()
        combobox_cservers = Assignment_Window.view.comboBox_Churchservers
        combobox_cservers.clear()
        list_all_servers = data.list_churchservers
        temporary_data = create_list_of_groups(list_all_servers)
        index_selected_grade = temporary_data[1].index(grade)
        for x in range(len(temporary_data[0][index_selected_grade])):
            combobox_cservers.addItem(temporary_data[0][index_selected_grade][x].abbreviation)
    
    
    def fill_list_with_unavailable(self):
        selected_server = get_server_from_abbreviation(Assignment_Window.view.comboBox_Churchservers.currentText(),
                                                       data)
        print(get_unavailable_dates(selected_server))
        Assignment_Window.view.listWidget.clear()
        Assignment_Window.view.listWidget.addItems(get_unavailable_dates(selected_server))
        Assignment_Window.view.listWidget.sortItems()
    
    def unavailable_day(self):
        selected_server = get_server_from_abbreviation(Assignment_Window.view.comboBox_Churchservers.currentText(),
                                                       data)
        if Assignment_Window.view.calendarWidget.selectedDate().toPython().isoformat() not in selected_server.unavailable:
            selected_server.unavailable.append(Assignment_Window.view.calendarWidget.selectedDate().toPython().isoformat())
            Assignment_Window.fill_list_with_unavailable(Assignment_Window.view.listWidget)
        else:
            print("error")
    
    def initiate_saving(self):
        print(data.list_churchservers[0].unavailable)
        print(data.list_churchservers[0].abbreviation)
        list_to_json(data.list_churchservers)
    
    def initiate_removal_days(self):
        # Get the Server that is selected in the Church Server Combobox
        selected_server = get_server_from_abbreviation(Assignment_Window.view.comboBox_Churchservers.currentText(),
                                                       data)
        current_selection = Assignment_Window.return_multi_selection(Assignment_Window.view.listWidget)
        remove_unavailable_days(church_server=selected_server,
                                unavailable_days=current_selection)
        Assignment_Window.fill_list_with_unavailable(Assignment_Window.view.listWidget)



Assignment_Window()