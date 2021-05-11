import random
from statistics import mean, median, stdev
from datetime import datetime
from docx import Document


class ChurchServers:
    def __init__(self, name):
        # MD is used as an abbreviation of ChurchServers
        self.name = name
        # Shows if someone is already in the current Messe
        self.is_allocated = True
        # Shows if someone has excused themselves
        self.is_available = False
        # Shows if someone is able to serve at Church
        self.is_advanced = True
        # Grade is simplified into "Child" and "GroupLeader"
        # "Null" is a String to show the grade did not work
        self.grade = "Null"
        self.counter = 0
        # List of datetime objects when a ChurchServer is not available
        self.unavailable = []


class ChurchService:
    def __init__(self, number_md_needed, date_time):
        # numberMD is the number of ChurchServers needed for the Church Service
        self.count = number_md_needed
        self.ListServingMD = []
        # NumberAllocatedMD shows the current amount of Church Servers that are allocated to the Service.
        # If the allocation is finished this number should be equal to number_md_needed
        self.NumberAllocatedMD = len(self.ListServingMD)
        # Adds a time to each ChurchService
        # date_time should be a datetime object
        self.date = date_time


def create_availability(church_server):
    # Placeholder to create a state to check if someone is available
    # currently disabled to reenable change first statement after if to False
    if random.randint(0, 6) == 1:
        church_server.unavailable.append(datetime(2021, 11, 1, 18, 30))
        print(church_server.name)
    else:
        pass


def is_available(church_server, church_service):
    if church_service.date in church_server.unavailable:
        church_server.is_available = False
    else:
        church_server.is_available = True


def is_assigned(check_church_service, church_server):
    # the Function checks if a ChurchServer is already assigned to the Service
    if check_church_service.ListServingMD.count(church_server.name) == 0:
        church_server.is_allocated = False
    else:
        church_server.is_allocated = True


def allocation_md(current_church_service):
    while len(current_church_service.ListServingMD) < current_church_service.count:
        selected_md = random.choice(List_MD)
        is_available(selected_md, current_church_service)
        if selected_md.is_available:
            is_assigned(current_church_service, selected_md)
            if not selected_md.is_allocated:
                current_church_service.ListServingMD.append(selected_md.name)
                selected_md.counter = selected_md.counter + 1
            else:
                pass
        else:
            pass
    else:
        pass

# Functions needed to output the Services to a Docx file


def print_plan_docx(list_services, document_name):
    document = Document()
    document.add_heading("Messdienerplan", 1)
    length = len(List_Services)
    for service_number in range(0, length):
        current_service = list_services[service_number]
        document.add_paragraph(str(current_service.date))
        new_string = "Messe: "
        for x in range(0, current_service.count):
            new_string = new_string + str(current_service.ListServingMD[x]) + " "
        document.add_paragraph(new_string)
    document.save(document_name)


# Definition of lists and variables needed later
List_MD = []
List_Services = []
statistic_list = []
church_service_amount = 100
church_servers_amount = 100

# Generation of ChurchServers
for number_id in range(0, church_servers_amount):
    List_MD.append(ChurchServers("Messdiener" + str(number_id)))
    create_availability(List_MD[number_id])

# Generates church_service_amount of church services
for number_services in range(0, church_service_amount):
    List_Services.append(ChurchService(8, datetime(2021, 11, 1, 18, 30)))

# Allocation of Church Server to Church Services
for selected_church_server in range(0, church_service_amount):
    allocation_md(List_Services[selected_church_server])
    # print(List_Services[selected_church_server].ListServingMD)


# Adds the counter values of each Church Server to a list
for selected_church_server_stats in range(0, church_servers_amount):
    # print(List_MD[selected_church_server_stats].name, List_MD[selected_church_server_stats].counter)
    statistic_list.append(List_MD[selected_church_server_stats].counter)

# statistic Analysis of the allocation of Church Servants

print(List_Services[1])
print(List_MD[1].unavailable)
print("mean", mean(statistic_list))
print("median", median(statistic_list))
print("standard deviation", stdev(statistic_list))
print("max", max(statistic_list))
print("min", min(statistic_list))

print_plan_docx(List_Services, "test.docx")
