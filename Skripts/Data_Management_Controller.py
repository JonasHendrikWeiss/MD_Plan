import sys
from PySide6.QtCore import QFile, QIODevice, QRect
from PySide6.QtUiTools import QUiLoader
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QDialog
from PySide6.QtWidgets import QApplication
from Storage_Operations import unpickle_storage
from Zuordnung import ChurchServer, ChurchGroup
from Availability_Controller import Availability_Window, add_grades_to_combobox
from Availabilty_Logic import add_objects_listwidget, add_server_objects
from Assingment_Controller import return_multi_selection, fill_churchservice_list
from datetime import datetime


# TODO add a check if an abbreviation already exists and handle that case

def accept_new_servers():
    data = Data_Management_Window.data
    data.list_churchservers.append(Data_Management_Window.temporary_servers)
    data.list_churchservers.append(Data_Management_Window.temporary_servers)


def accept_edit_server():
    # TODO rebuilt this using a setter function
    dialog = Data_Management_Window.current_dialog
    print(type(Data_Management_Window.temporary_server))
    Data_Management_Window.temporary_server.firstname = dialog.lineEdit_firstname.text()
    Data_Management_Window.temporary_server.lastname = dialog.lineEdit_lastname.text()
    Data_Management_Window.temporary_server.fullname =\
        f"{dialog.lineEdit_firstname.text()} {dialog.lineEdit_lastname.text()}"
    Data_Management_Window.temporary_server.abbreviation = dialog.lineEdit_abbreviation.text()
    Data_Management_Window.temporary_server.group = dialog.comboBox_Grades.currentData()
    # Updates the view if the name is changed
    Data_Management_Window.fill_churchserver_selection_button(dialog)


def accept_new_group():
    selected_start_year = Data_Management_Window.current_dialog.dateEdit.date().toPython().year
    description_grade= Data_Management_Window.current_dialog.lineEdit_name.text()
    Data_Management_Window.data.list_groups.append(ChurchGroup(description_grade, start_year=selected_start_year))

    update_churchserver_comboboxes()


def accept_edit_group():
    print("accepted edit")
    selected_grade = Data_Management_Window.view.comboBox_Grades_2.currentData()
    selected_start_year = Data_Management_Window.current_dialog.dateEdit.date().toPython().year
    description_grade= Data_Management_Window.current_dialog.lineEdit_name.text()
    selected_grade.name = description_grade
    selected_grade.start_year = selected_start_year
    update_churchserver_comboboxes()


def update_churchserver_comboboxes():
    Data_Management_Window.view.comboBox_Grades.clear()
    Data_Management_Window.view.comboBox_Grades_2.clear()
    add_grades_to_combobox(Data_Management_Window.data, Data_Management_Window.view.comboBox_Grades)
    add_grades_to_combobox(Data_Management_Window.data, Data_Management_Window.view.comboBox_Grades_2)

def reset_temporary_data():
    Data_Management_Window.temporary_servers = []
    Data_Management_Window.temporary_server = None


def update_temporary_list():
    new_server_dialog= Data_Management_Window.current_dialog
    new_server_dialog.listWidget.clear()
    add_objects_listwidget(new_server_dialog.listWidget, Data_Management_Window.temporary_servers)


def remove_server_from_list():
    new_server_dialog = Data_Management_Window.current_dialog
    # removes all Servers that are currently selected
    servers_to_remove = return_multi_selection(new_server_dialog.listWidget)
    print(servers_to_remove)
    print(Data_Management_Window.temporary_servers)
    for x in range(len(servers_to_remove)):
        Data_Management_Window.temporary_servers.remove(servers_to_remove[x])
    update_temporary_list()  # Updates the view to match the data
    Data_Management_Window.fill_churchserver_selection_button(new_server_dialog)


def delete_server():
    # Data_Management_Window.data.delete_churchserver(Data_Management_Window.temporary_server)
    # The function will be added later after I build the reinitialize button in the settings tab
    grade_server = Data_Management_Window.temporary_server.group
    grade_server.members.remove(Data_Management_Window.temporary_server)
    Data_Management_Window.data.list_churchservers.remove(Data_Management_Window.temporary_server)
    # gets back into the main program without calling accept_edit_server
    Data_Management_Window.current_dialog.reject()
    # updates the view to match the data
    Data_Management_Window.fill_churchserver_selection_button(grade_server)


class Data_Management_Window(QMainWindow):
    view = None
    temporary_servers = []
    temporary_server = None
    current_dialog = None
    data = unpickle_storage()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #Import the view from an UI file
        ui_file_name = "Data_Management.ui"
        ui_file = QFile(ui_file_name)
        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
            sys.exit(-1)
        Data_Management_Window.view = QUiLoader().load(ui_file)
        ui_file.close()
        # Fill the grade selection combobox
        add_grades_to_combobox(Data_Management_Window.data, Data_Management_Window.view.comboBox_Grades)
        add_grades_to_combobox(Data_Management_Window.data, Data_Management_Window.view.comboBox_Grades_2)
        Data_Management_Window.view.comboBox_Grades.setCurrentIndex(-1)
        Data_Management_Window.view.comboBox_Grades.setPlaceholderText("Schuljahre")
        Data_Management_Window.view.comboBox_Churchservers.setPlaceholderText("Messdiener")
        Data_Management_Window.view.push_button_modify_churchserver.setEnabled(False)

        # Connection of buttons in the view
        Data_Management_Window.view.push_button_new_churchserver.clicked.connect(
            Data_Management_Window.open_new_churchserver_dialog)
        Data_Management_Window.view.push_button_new_churchgroup.clicked.connect(
            Data_Management_Window.open_new_churchgroup_dialog)
        Data_Management_Window.view.push_button_modify_churchserver.clicked.connect(
            Data_Management_Window.open_edit_churchserver_dialog)
        Data_Management_Window.view.push_button_modify_churchgroup.clicked.connect(
            Data_Management_Window.open_edit_churchgroup_dialog)
        Data_Management_Window.view.comboBox_Grades.activated.connect(
            Data_Management_Window.fill_churchserver_selection_button)
        Data_Management_Window.view.comboBox_Churchservers.activated.connect(
            Data_Management_Window.activate_modify_button)

    def open_new_churchserver_dialog(self):
        # Open the view of the dialog
        ui_file_name = "Dialog_New_Servers.ui"
        ui_file = QFile(ui_file_name)
        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
            sys.exit(-1)
        Data_Management_Window.current_dialog = QUiLoader().load(ui_file)
        new_server_dialog = Data_Management_Window.current_dialog
        ui_file.close()
        new_server_dialog.show()

        add_grades_to_combobox(Data_Management_Window.data, new_server_dialog.comboBox_Grades)
        new_server_dialog.pushButton_new_server.clicked.connect(Data_Management_Window.create_temporary_server)
        new_server_dialog.pushButton_delete_server.clicked.connect(remove_server_from_list)
        new_server_dialog.accepted.connect(accept_new_servers)
        new_server_dialog.rejected.connect(reset_temporary_data)
        new_server_dialog.exec()

    def open_edit_churchserver_dialog(self):
        # Open the view of the dialog
        ui_file_name = "Dialog_Edit_Server.ui"
        ui_file = QFile(ui_file_name)
        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
            sys.exit(-1)
        Data_Management_Window.current_dialog = QUiLoader().load(ui_file)
        edit_server_dialog = Data_Management_Window.current_dialog
        ui_file.close()
        edit_server_dialog.show()
        Data_Management_Window.temporary_server = Data_Management_Window.view.comboBox_Churchservers.currentData()
        add_grades_to_combobox(Data_Management_Window.data, edit_server_dialog.comboBox_Grades)
        edit_server_dialog.pushButton_delete_server.clicked.connect(delete_server)
        edit_server_dialog.accepted.connect(accept_edit_server)
        edit_server_dialog.rejected.connect(reset_temporary_data)
        # Inputs the Current Data into the lineEdits
        edit_server_dialog.lineEdit_firstname.setText(Data_Management_Window.temporary_server.firstname)
        edit_server_dialog.lineEdit_lastname.setText(Data_Management_Window.temporary_server.lastname)
        edit_server_dialog.lineEdit_abbreviation.setText(Data_Management_Window.temporary_server.abbreviation)
        edit_server_dialog.comboBox_Grades.setCurrentIndex(
            edit_server_dialog.comboBox_Grades.findData(Data_Management_Window.temporary_server.group))


        edit_server_dialog.exec()

    def open_edit_churchgroup_dialog(self):
        # Open the view of the dialog
        ui_file_name = "Dialog_Edit_Group.ui"
        ui_file = QFile(ui_file_name)
        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
            sys.exit(-1)
        Data_Management_Window.current_dialog = QUiLoader().load(ui_file)
        edit_server_dialog = Data_Management_Window.current_dialog
        ui_file.close()
        edit_server_dialog.show()

        selected_grade = Data_Management_Window.view.comboBox_Grades_2.currentData()
        add_objects_listwidget(edit_server_dialog.listWidget, selected_grade.members)
        # converts the integer startyear attribute into a datetime an_object in order to add it to the view
        edit_server_dialog.dateEdit.setDate(datetime.strptime(str(selected_grade.start_year), "%Y").date())
        edit_server_dialog.lineEdit_name.setText(selected_grade.name)

        edit_server_dialog.accepted.connect(accept_edit_group)
        edit_server_dialog.rejected.connect(reset_temporary_data)
        edit_server_dialog.exec()

    def open_new_churchgroup_dialog(self):
        # Open the view of the dialog
        ui_file_name = "Dialog_New_Group.ui"
        ui_file = QFile(ui_file_name)
        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
            sys.exit(-1)
        Data_Management_Window.current_dialog = QUiLoader().load(ui_file)
        edit_server_dialog = Data_Management_Window.current_dialog
        ui_file.close()
        edit_server_dialog.show()
        edit_server_dialog.dateEdit.setDate(datetime.now())
        edit_server_dialog.lineEdit_name.setText("4")

        edit_server_dialog.accepted.connect(accept_new_group)
        edit_server_dialog.rejected.connect(reset_temporary_data)

        edit_server_dialog.exec()




    def create_temporary_server(self):
        firstname = Data_Management_Window.current_dialog.lineEdit_firstname.text()
        lastname = Data_Management_Window.current_dialog.lineEdit_lastname.text()
        abbreviation = Data_Management_Window.current_dialog.lineEdit_abbreviation.text()
        grade = Data_Management_Window.current_dialog.comboBox_Grades.currentData()
        Data_Management_Window.temporary_servers.append(ChurchServer(firstname, lastname, abbreviation, grade))
        update_temporary_list()

    def fill_churchserver_selection_button(self):
        # Rebuild to do more in Availability Logic
        grade = Data_Management_Window.view.comboBox_Grades.currentData()
        if grade is None:
            return
        combobox_cservers = Data_Management_Window.view.comboBox_Churchservers
        # selected_service is only used if checkbox_state is checked
        combobox_cservers.clear()
        add_server_objects(combobox_cservers, grade.members)
        Data_Management_Window.view.push_button_modify_churchserver.setEnabled(False)

    def activate_modify_button(self):
        Data_Management_Window.view.push_button_modify_churchserver.setEnabled(True)



if __name__ == "__main__":
    app = QApplication(sys.argv) # Create an instance of QtWidgets.QApplication

    window = Data_Management_Window() # Create an instance of our class
    window.view.show()
    app.exec() # Start the application

