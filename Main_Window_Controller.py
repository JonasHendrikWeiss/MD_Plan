import sys
from PySide6.QtCore import QFile, QIODevice, QRect
from PySide6.QtUiTools import QUiLoader
from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QApplication
from Panda_To_Storage import data_storage, import_churchservers_from_dataframe, json_to_pdataframe

from Availability_Controller import Assignment_Window

data= data_storage()
import_churchservers_from_dataframe(json_to_pdataframe(), data.list_churchservers)

class Main_Window(QMainWindow):

    def __init__(self):
        super(Main_Window, self).__init__()
        self.initUI()



    def initUI(self):
        #Import the view from an UI file
        uic.loadUi("MainWindow.ui", self)
        self.show()
        self.pushButton.clicked.connect(Main_Window.start_window)





    def start_window(self):
        print("est")
        a = Assignment_Window()
        a.view.show()
        #Mainrunner.window.show()
        #Mainrunner.app1.exec()


app = QApplication(sys.argv) # Create an instance of QtWidgets.QApplication

window = Main_Window() # Create an instance of our class
window.show
app.exec() # Start the application
