
import sys
from PySide6.QtCore import QFile, QIODevice
from PySide6.QtUiTools import QUiLoader
from PyQt6.QtWidgets import (QApplication)

from Storage_Operations import import_churchservers_from_dataframe, json_to_pdataframe, data_storage


class Assignment_Window():
    view = None
    start_date = None
    data = data_storage()
    import_churchservers_from_dataframe(json_to_pdataframe(), data.list_churchservers)


    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        #Import the view from an UI file
        pass

        ui_file_name = "Assignment_Window.ui"
        ui_file = QFile(ui_file_name)
        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
            sys.exit(-1)
        Assignment_Window.view = QUiLoader().load(ui_file)
        ui_file.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    b = Assignment_Window()
    b.view.show()
    app.exec()
