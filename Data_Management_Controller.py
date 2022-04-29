import sys
from PySide6.QtCore import QFile, QIODevice, QRect
from PySide6.QtUiTools import QUiLoader
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QDialog
from PySide6.QtWidgets import QApplication
from Storage_Operations import unpickle_storage
from Zuordnung import ChurchServer
from Availability_Controller import Availability_Window, add_grades_to_combobox
from Availabilty_Logic import add_server_objects_listwidget


def accept_new_servers():
    data = Data_Management_Window.data
    data.list_churchservers.churchserver(Data_Management_Window.temporary_servers)

def reset_temporary_data():
    Data_Management_Window.temporary_servers = []

def update_temporary_list():
    new_server_dialog= Data_Management_Window.churchserver_dialog
    new_server_dialog.listWidget.clear()
    add_server_objects_listwidget(new_server_dialog.listWidget, Data_Management_Window.temporary_servers)


class Data_Management_Window(QMainWindow):
    view = None
    temporary_servers = []
    churchserver_dialog = None
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

        # Connection of buttons in the view
        Data_Management_Window.view.push_button_new_churchserver.clicked.connect(
            Data_Management_Window.open_new_churchserver_dialog)


    def open_new_churchserver_dialog(self):
        ui_file_name = "Dialog_New_Servers.ui"
        ui_file = QFile(ui_file_name)
        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
            sys.exit(-1)
        Data_Management_Window.churchserver_dialog = QUiLoader().load(ui_file)
        new_server_dialog = Data_Management_Window.churchserver_dialog
        ui_file.close()
        new_server_dialog.show()
        add_grades_to_combobox(Data_Management_Window.data, new_server_dialog.comboBox_Grades)
        new_server_dialog.pushButton_new_server.clicked.connect(Data_Management_Window.create_temporary_server)
        new_server_dialog.accepted.connect(accept_new_servers)
        new_server_dialog.rejected.connect(reset_temporary_data)
        new_server_dialog.exec()

    def create_temporary_server(self):
        firstname = Data_Management_Window.churchserver_dialog.lineEdit_firstname.text()
        lastname = Data_Management_Window.churchserver_dialog.lineEdit_lastname.text()
        abbreviation = Data_Management_Window.churchserver_dialog.lineEdit_abbreviation.text()
        grade = Data_Management_Window.churchserver_dialog.comboBox_Grades.currentData()
        Data_Management_Window.temporary_servers.append(ChurchServer(firstname, lastname, abbreviation, grade))
        update_temporary_list()



if __name__ == "__main__":
    app = QApplication(sys.argv) # Create an instance of QtWidgets.QApplication

    window = Data_Management_Window() # Create an instance of our class
    window.view.show()
    app.exec() # Start the application

