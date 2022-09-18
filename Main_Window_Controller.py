import sys
from PySide6.QtCore import QFile, QIODevice, QRect
from PySide6.QtUiTools import QUiLoader
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QApplication
from Storage_Operations import data_storage
from Availability_Controller import Availability_Window
from Assingment_Controller import Assignment_Window
from Data_Management_Controller import Data_Management_Window


class Main_Window(QMainWindow):
    def __init__(self):
        super(Main_Window, self).__init__()
        self.initUI()

    def initUI(self):
        # Import the view from an UI file
        uic.loadUi("MainWindow.ui", self)
        self.show()
        self.pushButton_assignment.clicked.connect(Main_Window.start_window_assignment)
        self.pushButton_availability.clicked.connect(Main_Window.start_window_availability)
        self.pushButton_churchservers.clicked.connect(Main_Window.start_window_data_management)
        self.pushButton_settings.clicked.connect(Main_Window.start_window_settings)


    def start_window_assignment(self):
        print("starting availability Window")
        assignment_window = Assignment_Window()
        assignment_window.view.show()

    def start_window_availability(self):
        print("starting assignment Window")
        availability_window = Availability_Window()
        availability_window.view.show()

    def start_window_data_management(self):
        print("starting data management Window")
        data_management_window = Data_Management_Window()
        data_management_window.view.show()

    def start_window_settings(self):
        print("starting settings Window")


if __name__ == "__main__":
    app = QApplication(sys.argv) # Create an instance of QtWidgets.QApplication

    window = Main_Window() # Create an instance of our class
    window.show
    app.exec() # Start the application
