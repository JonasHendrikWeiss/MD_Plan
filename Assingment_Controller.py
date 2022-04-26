import sys

from PySide6.QtCore import QFile, QIODevice
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QListWidgetItem


from Zuordnung import TimeSpan
from Availabilty_Logic import create_list_of_groups, remove_unavailable_days
from Storage_Operations import pickle_storage,unpickle_storage


class Assignment_Window():
    view = None
    start_date = None
    data = unpickle_storage()
    # import_churchservers_from_dataframe(json_to_pdataframe(), data.list_churchservers)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Import the view from an UI file
        pass

        ui_file_name = "Assignment_Window.ui"
        ui_file = QFile(ui_file_name)
        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
            sys.exit(-1)
        Assignment_Window.view = QUiLoader().load(ui_file)
        ui_file.close()
        Assignment_Window.view.comboBox_Grades.addItems(create_list_of_groups(
            Assignment_Window.data.list_churchservers)[1])
        Assignment_Window.view.comboBox_Grades.setCurrentIndex(-1)
        Assignment_Window.view.comboBox_Grades.setPlaceholderText("Schuljahre")
        Assignment_Window.view.comboBox_Churchservers.setPlaceholderText("Messdiener")

        # Part of the Code that handles connections

        Assignment_Window.view.comboBox_Grades.activated.connect(
            Assignment_Window.fill_churchserver_selection_button)
        Assignment_Window.view.comboBox_Churchservers.activated.connect(
            Assignment_Window.fill_list_with_unavailable)
        Assignment_Window.view.pushButton_save.clicked.connect(Assignment_Window.initiate_saving)

    def return_multi_selection(self):
        # returns all selected Items in a list
        selected_list = []
        for x in range(Assignment_Window.view.listWidget.count()):
            if Assignment_Window.view.listWidget.item(x).isSelected() == True:
                selected_list.append(Assignment_Window.view.listWidget.item(x).data(0x0100))
        return selected_list # 0x0100 is the integer for a Qt.UserRole

    def test_connection(self):  # Function is only used if there is doubt whether a connect is working
        print("Connection works")

    def add_server_objects( selected_object, list_servers):
        # A function to add all Items of a given list as strings to a combobox
        for x in range(len(list_servers)):
            selected_server = list_servers[x]
            selected_object.addItem(selected_server.fullname, userData=selected_server) # adds the Abbreviation as a
            # string and the object as userData

    def add_timespan_object(selected_object, churchserver):
        # Adds all the TimeSpan Objects to the selected object
        for span_number in range(len(churchserver.unavailable)):  # iterates through all possible TimeSpan objects
            item_to_add = QListWidgetItem()  # Adds a temporary custom QListWidgetItem in order to support data
            selected_span = churchserver.unavailable[span_number]
            item_to_add.setText(selected_span.description)
            item_to_add.setData(0x0100, selected_span)  # 0x0100 is the integer for a Qt.UserRole
            selected_object.addItem(item_to_add)

    def select_start_day(self):
        if Assignment_Window.view.comboBox_Churchservers.currentData() != None:
            Assignment_Window.start_date = Assignment_Window.view.calendarWidget.selectedDate().toPython()
            Assignment_Window.view.label_start_day.setText(Assignment_Window.start_date.isoformat())
            Assignment_Window.view.push_button_end_day.setEnabled(True)

    def select_end_day(self):
        selected_end_time = Assignment_Window.view.calendarWidget.selectedDate().toPython()
        selected_server = Assignment_Window.view.comboBox_Churchservers.currentData()
        new_timespan = TimeSpan(Assignment_Window.start_date, selected_end_time)
        selected_server.add_unavailable(new_timespan)  # uses the add unavailable function to look and merge duplicates
        # Resets the view and data so there is nothing carried over to the next operation
        Assignment_Window.fill_list_with_unavailable(Assignment_Window.view.listWidget)
        Assignment_Window.start_date = None
        Assignment_Window.view.label_start_day.setText("Start Abmeldung")
        Assignment_Window.view.push_button_end_day.setEnabled(False)



    def fill_churchserver_selection_button(self):
        # Rebuild to do more in Availability Logic
        grade = Assignment_Window.view.comboBox_Grades.currentText()
        combobox_cservers = Assignment_Window.view.comboBox_Churchservers
        combobox_cservers.clear()
        list_all_servers = Assignment_Window.data.list_churchservers
        temporary_data = create_list_of_groups(list_all_servers)
        index_selected_grade = temporary_data[1].index(grade)
        Assignment_Window.add_server_objects(combobox_cservers, temporary_data[0][index_selected_grade])


    def fill_list_with_unavailable(self):
        selected_server = Assignment_Window.view.comboBox_Churchservers.currentData()
        Assignment_Window.add_timespan_object(Assignment_Window.view.listWidget, selected_server)

        Assignment_Window.view.listWidget.sortItems()

    def unavailable_day(self):
        selected_server = Assignment_Window.view.comboBox_Churchservers.currentData()

        if selected_server == None:
            # Is only relevant if the button is clicked for the first time without making any other selections
            print("No Selection")
            return
        # returns the date of the calendar as a python Datetime object
        selected_datetime=Assignment_Window.view.calendarWidget.selectedDate().toPython()
        new_day = TimeSpan(selected_datetime, selected_datetime)  # Sets the start and end date to the same day
        selected_server.add_unavailable(new_day)  # uses the add unavailable function to look and merge duplicates
        Assignment_Window.fill_list_with_unavailable(Assignment_Window.view.listWidget)


    def initiate_saving(self):
        pickle_storage(Assignment_Window.data, filename="data_storage.pkl")
        print(f"Saving {len(Assignment_Window.data.list_churchservers)} MD")




if __name__ == "__main__":
    app = QApplication(sys.argv)
    b = Assignment_Window()
    b.view.show()
    app.exec()
