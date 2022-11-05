import sys

from PySide6.QtCore import QFile, QIODevice
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QListWidgetItem

from Print_Handeling import print_to_docx
from Zuordnung import TimeSpan, ChurchService
from Availabilty_Logic import add_grades_to_combobox, add_objects_listwidget, add_server_objects
from Storage_Operations import pickle_storage, unpickle_storage, reinitalize_churchservers, data_storage
from Assigment_Logic import fill_churchservice_list, handle_deletion_of_service, get_available_servers


def return_multi_selection(an_object):
    # returns all selected Items in a list
    selected_list = []
    for x in range(an_object.count()):
        if an_object.item(x).isSelected() == True:
            selected_list.append(an_object.item(x).data(0x0100))
    return selected_list # 0x0100 is the integer for a Qt.UserRole


class Assignment_Window():
    print_selection = None
    view = None
    start_date = None
    data = unpickle_storage()
    pass
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
        # Fill the grade selection combobox
        add_grades_to_combobox(Assignment_Window.data, Assignment_Window.view.comboBox_Grades)
        Assignment_Window.view.comboBox_Grades.setCurrentIndex(-1)
        Assignment_Window.view.comboBox_Grades.setPlaceholderText("Schuljahre")

        # Part of the Code that handles connections

        Assignment_Window.view.comboBox_Grades.activated.connect(
            Assignment_Window.fill_churchserver_selection_button)
        Assignment_Window.view.listWidget_service_selection.clicked.connect(Assignment_Window.update_service_selection)
        Assignment_Window.view.pushButton_save.clicked.connect(Assignment_Window.initiate_saving)
        Assignment_Window.view.pushButton_add_service.clicked.connect(Assignment_Window.create_new_service)
        Assignment_Window.view.pushButton_delete_service.clicked.connect(Assignment_Window.delete_service)

        Assignment_Window.view.pushButton_add_cserver.clicked.connect(Assignment_Window.add_server_to_service)
        Assignment_Window.view.pushButton_remove_cservers.clicked.connect(Assignment_Window.remove_server_from_service)
        Assignment_Window.view.pushButton_fill_service.clicked.connect(Assignment_Window.test_connection)
        Assignment_Window.view.checkBox_show_all_servers.clicked.connect(
            Assignment_Window.fill_churchserver_selection_button)
        Assignment_Window.view.pushButton_print.clicked.connect(Assignment_Window.open_print_dialog)
        # Fills the service selection button on startup
        fill_churchservice_list(Assignment_Window.data, Assignment_Window.view.listWidget_service_selection)



    def test_connection(self):  # Function is only used if there is doubt whether a connect is working
        print("Connection works")
        print(type(Assignment_Window.view.timeEdit.time().toPython()))


    def fill_churchserver_selection_button(self):
        # Rebuild to do more in Availability Logic
        grade = Assignment_Window.view.comboBox_Grades.currentData()
        if grade is None:
            return
        churchserver_selection_list = Assignment_Window.view.listWidget_server_selection
        # selected_service is only used if checkbox_state is checked
        selected_service = Assignment_Window.view.listWidget_service_selection.currentItem()
        if selected_service is None:
            Assignment_Window.view.error_label.setText("Wähle eine Messe aus")
            return
        else:
            selected_service = selected_service.data(0x0100)
            Assignment_Window.view.error_label.clear()
        checkbox_state = Assignment_Window.view.checkBox_show_all_servers.isChecked()

        if checkbox_state is False and selected_service is not None:
            list_available = get_available_servers(grade.members, selected_service.date)
            add_objects_listwidget(churchserver_selection_list, list_available)
        else:
            add_objects_listwidget(churchserver_selection_list, grade.members)


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
        Assignment_Window.view.listWidget_server_in_service.clear()
        fill_churchservice_list(Assignment_Window.data, Assignment_Window.view.listWidget_service_selection)


    def delete_service(self):
        selected_service = Assignment_Window.view.listWidget_service_selection.currentItem().data(0x0100)
        # .data(0x0100) selects the userData of the selected view Item
        print(selected_service)
        if selected_service is None:
            return  # Handles the case when there is no service left
        Assignment_Window.view.listWidget_server_selection.clear()
        handle_deletion_of_service(Assignment_Window.data, selected_service)
        # fills the churchservice combobox with new data
        fill_churchservice_list(Assignment_Window.data, Assignment_Window.view.listWidget_service_selection)
        Assignment_Window.update_service_selection(Assignment_Window)

    def update_service_selection(self):
        if Assignment_Window.view.listWidget_service_selection.currentItem() is None:
            Assignment_Window.view.lable_selected_Service.setText("Ausgewählte Messe")
            return
        selected_service = Assignment_Window.view.listWidget_service_selection.currentItem().data(0x0100)
        # sets the label in order to show the correct description
        Assignment_Window.view.lable_selected_Service.setText(selected_service.description)

        # adds all currently assigned ChurchServers to the listWidget
        add_objects_listwidget(Assignment_Window.view.listWidget_server_in_service, selected_service.current_churchservers)
        Assignment_Window.fill_churchserver_selection_button(self)

    def add_server_to_service(self):
        selected_service = Assignment_Window.view.listWidget_service_selection.currentItem().data(0x0100)
        selection = return_multi_selection(Assignment_Window.view.listWidget_server_selection)
        for number in range(len(selection)):
            selected_server = selection[number]
            if selected_server is None:
                pass  # stops the program from adding a None value to the list when nothing is selected
            elif selected_server in selected_service.current_churchservers:
                return  # stops the program from adding a person twice
            selected_service.current_churchservers.append(selected_server)
        # Updates the view in order to correctly display the data
        Assignment_Window.update_service_selection(Assignment_Window)

    def remove_server_from_service(self):
        selected_service = Assignment_Window.view.listWidget_service_selection.currentItem().data(0x0100)
        selected_server_list = return_multi_selection(Assignment_Window.view.listWidget_server_in_service)
        for selected_server_number in range(len(selected_server_list)):
            selected_server = selected_server_list[selected_server_number] # iterates through all elements of the list
            print(selected_server)
            print(selected_service.current_churchservers)
            selected_service.current_churchservers.remove(selected_server) # removes all selected servers
        # Updates the view in order to correctly display the data
        Assignment_Window.update_service_selection(Assignment_Window)


# TODO Build a reset function to reset the UI after certain actions like deleting or adding church services

    def open_print_dialog(self):
        # Open the view of the dialog
        ui_file_name = "Dialog_Print.ui"
        ui_file = QFile(ui_file_name)
        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
            sys.exit(-1)
        Assignment_Window.current_dialog = QUiLoader().load(ui_file)
        print_dialog = Assignment_Window.current_dialog
        ui_file.close()
        print_dialog.show()
        print_dialog.listWidget_print.clicked.connect(Assignment_Window.update_selecion)
        fill_churchservice_list(Assignment_Window.data, print_dialog.listWidget_print)
        print_dialog.accepted.connect(Assignment_Window.start_print)
        print_dialog.rejected.connect(print("No"))
        print_dialog.exec()


    def update_selecion():
        Assignment_Window.print_selection = return_multi_selection(Assignment_Window.current_dialog.listWidget_print)


    def start_print():
        print_to_docx(list_to_print=Assignment_Window.print_selection, name_output=Assignment_Window.current_dialog.lineEdit_Name.text())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    b = Assignment_Window()
    b.view.show()
    app.exec()
