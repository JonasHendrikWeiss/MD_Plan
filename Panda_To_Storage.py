from Zuordnung import ChurchServers, create_church_servers, create_availability
import pandas
import os

List_MD = []
create_church_servers("Liste_Messdiener_Computer.xlsx", "Kinder", List_MD)

for x in range(len(List_MD)):
    create_availability(List_MD[x])

#storage_table = pandas.read_table(List_MD)



dir_path = os.path.dirname(os.path.realpath(__file__))
storage_frame.to_json(path_or_buf= f"{dir_path}/JSON")
print("test")

