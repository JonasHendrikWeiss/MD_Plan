import sys
from PySide6.QtCore import QFile, QIODevice, QRect
from PySide6.QtUiTools import QUiLoader
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QApplication
from Storage_Operations import unpickle_storage

from Availability_Controller import Availability_Window
from Assingment_Controller import Assignment_Window


class Data_Management_Window(QMainWindow):
    view = None
    data = unpickle_storage()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #Import the view from an UI file
        pass

        ui_file_name = "Data_Management.ui"
        ui_file = QFile(ui_file_name)
        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
            sys.exit(-1)
        Data_Management_Window.view = QUiLoader().load(ui_file)
        ui_file.close()


if __name__ == "__main__":
    app = QApplication(sys.argv) # Create an instance of QtWidgets.QApplication

    window = Data_Management_Window() # Create an instance of our class
    window.view.show()
    app.exec() # Start the application