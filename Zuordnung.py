import random


class ChurchServants:
    def __init__(self, name):
        # MD is used as an abbreviation of ChurchServants
        self.name = name

        pass


class ChurchService:
    def __init__(self, number_md):
        # numberMD is the number of ChurchServants needed for the Church Service
        self.count = number_md
        self.ListServingMD = []
        pass


def allocation_md(current_churchservice):
    for x in range(0, current_churchservice.count):
        random_md = random.choice(ListMD)
        current_churchservice.ListServingMD.append(random_md.name)


MD1 = ChurchServants("Messdiener1")
MD2 = ChurchServants("Messdiener2")
MD3 = ChurchServants("Messdiener3")
MD4 = ChurchServants("Messdiener4")
MD5 = ChurchServants("Messdiener5")
MD6 = ChurchServants("Messdiener6")
MD7 = ChurchServants("Messdiener7")
MD8 = ChurchServants("Messdiener8")
MD9 = ChurchServants("Messdiener9")

ListMD = [MD1, MD2, MD3, MD4, MD5, MD6, MD7, MD8, MD9]
Messe1 = ChurchService(4)

allocation_md(Messe1)
print(Messe1.ListServingMD)
