from Zuordnung import ChurchService, ChurchServer
from PySide6.QtWidgets import QListWidgetItem

def add_services_to_combobox(storage, combobox):
    list_services = storage.list_services
    for service_number in range(len(list_services)):
        selected_service = list_services[service_number]
        combobox.addItem(text=selected_service.description, userData=selected_service)

def fill_churchservice_list(storage, list_view):
    list_services = storage.list_services
    list_view.clear()
    for selected_service in range(len(list_services)): # iterates through all services
        print(list_services[selected_service].description)
        service_to_add = QListWidgetItem()
        service_to_add.setText(list_services[selected_service].description)
        service_to_add.setData(0x0100, list_services[selected_service])
        list_view.addItem(service_to_add)



def handle_deletion_of_service(storage, service):
    # just removes a selected service from the list of services
    storage.list_services.remove(service)

def get_available_servers(list_servers, date):
    # Returns all available Servers on a given day in a list
    list_available_servers = []
    for selected_server_number in range(len(list_servers)):
        selected_server = list_servers[selected_server_number]
        if selected_server.is_available(date) == True:
            list_available_servers.append(selected_server)

    return list_available_servers