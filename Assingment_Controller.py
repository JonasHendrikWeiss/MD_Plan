import sys

from PySide6.QtCore import QFile, QIODevice
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QListWidgetItem


from Zuordnung import TimeSpan
from Availabilty_Logic import add_grades_to_combobox
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
        add_grades_to_combobox(Assignment_Window.data, Assignment_Window.view.comboBox_Grades)
        Assignment_Window.view.comboBox_Grades.setCurrentIndex(-1)
        Assignment_Window.view.comboBox_Grades.setPlaceholderText("Schuljahre")
        Assignment_Window.view.comboBox_Churchservers.setPlaceholderText("Messdiener")

        # Part of the Code that handles connections

        Assignment_Window.view.comboBox_Grades.activated.connect(
            Assignment_Window.fill_churchserver_selection_button)
        Assignment_Window.view.comboBox_Churchservers.activated.connect(
            Assignment_Window.test_connection)
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


    def fill_churchserver_selection_button(self):
        # Rebuild to do more in Availability Logic
        grade = Assignment_Window.view.comboBox_Grades.currentData()
        combobox_cservers = Assignment_Window.view.comboBox_Churchservers
        combobox_cservers.clear()
        Assignment_Window.add_server_objects(combobox_cservers, grade.members)

    def initiate_saving(self):
        pickle_storage(Assignment_Window.data, filename="data_storage.pkl")
        print(f"Saving {len(Assignment_Window.data.list_churchservers)} MD")




if __name__ == "__main__":
    app = QApplication(sys.argv)
    b = Assignment_Window()
    b.view.show()
    app.exec()
