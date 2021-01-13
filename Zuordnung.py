import random

class Messdiener:
    def __init__(self,name):
    #MD is used as an abbreviation of Messdiener
        self.name = name

        pass


class Messe:
    def __init__(self, numberMessdiener):
        # numberMessdiener is the number of Messdiener needed for the Messe
        self.Anzahl = numberMessdiener
        pass



MD1 = Messdiener("Messdiener1")
MD2 = Messdiener("Messdiener2")
MD3 = Messdiener("Messdiener3")
MD4 = Messdiener("Messdiener4")
MD5 = Messdiener("Messdiener5")
MD6 = Messdiener("Messdiener6")
MD7 = Messdiener("Messdiener7")
MD8 = Messdiener("Messdiener8")
MD9 = Messdiener("Messdiener9")
ListeMD=[MD1, MD2, MD3, MD4, MD5, MD6, MD7, MD8, MD9]
Messe1= Messe(4)


def allocation_md(messe_aktuell):
    for x in range (0,messe_aktuell.Anzahl):
        random_md = random.choice(ListeMD)
        print(random_md.name)

allocation_md(Messe1)