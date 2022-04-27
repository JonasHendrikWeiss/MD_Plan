import sys

from PySide6.QtCore import QFile, QIODevice
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QListWidgetItem


from Zuordnung import TimeSpan, ChurchService
from Availabilty_Logic import add_grades_to_combobox, add_server_objects_listwidget, add_server_objects
from Storage_Operations import pickle_storage,unpickle_storage
from Assigment_Logic import fill_churchservice_combobox, handle_deletion_of_service

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
        # Fill the Window with initial Data
        # fill the ChurchService combobox initially
        fill_churchservice_combobox(Assignment_Window.data, Assignment_Window.view.comboBox_Services)
        Assignment_Window.view.comboBox_Services.setCurrentIndex(-1)
        Assignment_Window.view.comboBox_Services.setPlaceholderText("Messe")
        # Fill the grade selection combobox
        add_grades_to_combobox(Assignment_Window.data, Assignment_Window.view.comboBox_Grades)
        Assignment_Window.view.comboBox_Grades.setCurrentIndex(-1)
        Assignment_Window.view.comboBox_Grades.setPlaceholderText("Schuljahre")
        Assignment_Window.view.comboBox_Churchservers.setPlaceholderText("Messdiener")

        # Part of the Code that handles connections

        Assignment_Window.view.comboBox_Grades.activated.connect(
            Assignment_Window.fill_churchserver_selection_button)
        Assignment_Window.view.pushButton_save.clicked.connect(Assignment_Window.initiate_saving)
        Assignment_Window.view.pushButton_add_service.clicked.connect(Assignment_Window.create_new_service)
        Assignment_Window.view.pushButton_delete_service.clicked.connect(Assignment_Window.delete_service)
        Assignment_Window.view.comboBox_Services.activated.connect(Assignment_Window.update_service_selection)
        Assignment_Window.view.pushButton_add_cserver.clicked.connect(Assignment_Window.add_server_to_service)
        Assignment_Window.view.pushButton_remove_cservers.clicked.connect(Assignment_Window.remove_server_from_service)

    def return_multi_selection(self):
        # returns all selected Items in a list
        selected_list = []
        for x in range(Assignment_Window.view.listWidget.count()):
            if Assignment_Window.view.listWidget.item(x).isSelected() == True:
                selected_list.append(Assignment_Window.view.listWidget.item(x).data(0x0100))
        return selected_list # 0x0100 is the integer for a Qt.UserRole

    def test_connection(self):  # Function is only used if there is doubt whether a connect is working
        print("Connection works")
        print(type(Assignment_Window.view.timeEdit.time().toPython()))


    def fill_churchserver_selection_button(self):
        # Rebuild to do more in Availability Logic
        grade = Assignment_Window.view.comboBox_Grades.currentData()
        combobox_cservers = Assignment_Window.view.comboBox_Churchservers
        combobox_cservers.clear()
        add_server_objects(combobox_cservers, grade.members)

    def initiate_saving(self):
        pickle_storage(Assignment_Window.data, filename="data_storage.pkl")
        print(f"Saving {len(Assignment_Window.data.list_churchservers)} MD")

    def create_new_service(self):
        time = Assignment_Window.view.timeEdit.time().toPython()
        date = Assignment_Window.view.calendarWidget.selectedDate().toPython()
        number_cs = Assignment_Window.view.spinBox_cserver.value()
        number_leaders = Assignment_Window.view.spinBox_groupleader.value()
        # Creates a new ChurchService with all the collected data
        Assignment_Window.data.list_services.append(ChurchService(number_cs, number_leaders, date, time))
        fill_churchservice_combobox(Assignment_Window.data, Assignment_Window.view.comboBox_Services)

    def delete_service(self):
        selected_service = Assignment_Window.view.comboBox_Services.currentData()
        if selected_service is None:
            return  # Handles the case when there is no service left
        handle_deletion_of_service(Assignment_Window.data, selected_service)
        # fills the churchservice combobox with new data
        fill_churchservice_combobox(Assignment_Window.data, Assignment_Window.view.comboBox_Services)
        Assignment_Window.update_service_selection(Assignment_Window)

    def update_service_selection(self):
        selected_service = Assignment_Window.view.comboBox_Services.currentData()
        # sets the label in order to show the correct description
        if selected_service is None:
            Assignment_Window.view.lable_selected_Service.setText("Ausgewählte Messe")
            return
        Assignment_Window.view.lable_selected_Service.setText(selected_service.description)

        # adds all currently assigned ChurchServers to the listWidget
        Assignment_Window.view.listWidget.clear()
        add_server_objects_listwidget(Assignment_Window.view.listWidget, selected_service.current_churchservers)

    def add_server_to_service(self):
        selected_service = Assignment_Window.view.comboBox_Services.currentData()
        selected_server = Assignment_Window.view.comboBox_Churchservers.currentData()
        if selected_server is None:
            return  # stops the program from adding a None value to the list when nothing is selected
        elif selected_server in selected_service.current_churchservers:
            return  # stops the program from adding a person twice
        selected_service.current_churchservers.append(selected_server)
        # Updates the view in order to correctly display the data
        Assignment_Window.update_service_selection(Assignment_Window)

    def remove_server_from_service(self):
        selected_service = Assignment_Window.view.comboBox_Services.currentData()
        selected_server_list = Assignment_Window.return_multi_selection(Assignment_Window.view.listWidget)
        for selected_server_number in range(len(selected_server_list)):
            selected_server = selected_server_list[selected_server_number] # iterates through all elements of the list
            selected_service.current_churchservers.remove(selected_server) # removes all selected servers
        # Updates the view in order to correctly display the data
        Assignment_Window.update_service_selection(Assignment_Window)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    b = Assignment_Window()
    b.view.show()
    app.exec()
