from Zuordnung import ChurchService, ChurchServer

def add_services_to_combobox(storage, combobox):
    list_services = storage.list_services
    for service_number in range(len(list_services)):
        selected_service = list_services[service_number]
        combobox.addItem(text=selected_service.description, userData=selected_service)

def fill_churchservice_combobox(storage, combobox_service):
    list_services = storage.list_services
    combobox_service.clear()
    for selected_service in range(len(list_services)):
        print(list_services[selected_service].description)
        combobox_service.addItem(list_services[selected_service].description,
        userData=list_services[selected_service])

def handle_deletion_of_service(storage, service):
    # just removes a selected service from the list of services
    storage.list_services.remove(service)