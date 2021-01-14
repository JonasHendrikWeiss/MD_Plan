import random


class ChurchServers:
    def __init__(self, name):
        # MD is used as an abbreviation of ChurchServers
        self.name = name
        self.is_allocated = True
        self.is_available = False
        self.is_advanced = True
        self.grade = "Child"


class ChurchService:
    def __init__(self, number_md_needed):
        # numberMD is the number of ChurchServers needed for the Church Service
        self.count = number_md_needed
        self.ListServingMD = []
        # NumberAllocatedMD shows the current amount of Church Servers that are allocated to the Service.
        # If the allocation is finished this number should be equal to number_md_needed
        self.NumberAllocatedMD = len(self.ListServingMD)
        pass


def is_available(church_server):
    if random.randint(0, 8) == 1:
        church_server.is_available = False
    else:
        church_server.is_available = True


def is_assigned(check_church_service, church_server):
    # the Function checks if a ChurchServer is already assigned to the Service
    if check_church_service.ListServingMD.count(church_server.name) == 0:
        church_server.is_allocated = False
        print(church_server.name + "is not available")
    else:
        church_server.is_allocated = True


def allocation_md(current_church_service):
    while len(current_church_service.ListServingMD) < current_church_service.count:
        random_md = random.choice(ListMD)
        is_available(random_md)
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


MD1 = ChurchServers("Messdiener1")
MD1.is_available = False
MD2 = ChurchServers("Messdiener2")
MD2.is_available = False
MD3 = ChurchServers("Messdiener3")
MD4 = ChurchServers("Messdiener4")
MD5 = ChurchServers("Messdiener5")
MD6 = ChurchServers("Messdiener6")
MD7 = ChurchServers("Messdiener7")
MD8 = ChurchServers("Messdiener8")
MD9 = ChurchServers("Messdiener9")

ListMD = [MD1, MD2, MD3, MD4, MD5, MD6, MD7, MD8, MD9]
Messe1 = ChurchService(7)
Messe2 = ChurchService(3)
allocation_md(Messe1)
print(Messe1.ListServingMD)
print(Messe2.ListServingMD)
