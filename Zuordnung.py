import random


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


class ChurchService:
    def __init__(self, number_md_needed):
        # numberMD is the number of ChurchServers needed for the Church Service
        self.count = number_md_needed
        self.ListServingMD = []
        # NumberAllocatedMD shows the current amount of Church Servers that are allocated to the Service.
        # If the allocation is finished this number should be equal to number_md_needed
        self.NumberAllocatedMD = len(self.ListServingMD)
        pass


def create_availability(church_server):
    # Placeholder to create a state to check if someone is available
    if random.randint(0, 6) == 1:
        church_server.is_available = False
        # print(church_server.name)
    else:
        church_server.is_available = True


def is_available():
    # Placeholder for later check
    pass


def is_assigned(check_church_service, church_server):
    # the Function checks if a ChurchServer is already assigned to the Service
    if check_church_service.ListServingMD.count(church_server.name) == 0:
        church_server.is_allocated = False
    else:
        church_server.is_allocated = True


def allocation_md(current_church_service):
    while len(current_church_service.ListServingMD) < current_church_service.count:
        random_md = random.choice(List_MD)
        is_available()
        if random_md.is_available:
            is_assigned(current_church_service, random_md)
            if not random_md.is_allocated:
                current_church_service.ListServingMD.append(random_md.name)
            else:
                pass
        else:
            pass
    else:
        pass


List_MD = []


# Generation of ChurchServers
for number_id in range(0, 20):
    List_MD.append(ChurchServers("Messdiener" + str(number_id)))
    create_availability(List_MD[number_id])

Messe1 = ChurchService(8)
Messe2 = ChurchService(8)
Messe3 = ChurchService(8)

allocation_md(Messe1)
allocation_md(Messe2)
allocation_md(Messe3)

print("Messe1")
print(Messe1.ListServingMD)
print("Messe2")
print(Messe2.ListServingMD)
print("Messe3")
print(Messe3.ListServingMD)
