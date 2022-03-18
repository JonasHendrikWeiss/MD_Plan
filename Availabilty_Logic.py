# the controller behind the availability page of the application
from Panda_To_Storage import import_churchservers_from_dataframe, json_to_pdataframe
import pandas

def get_amount_of_elements(list):
    set_of_list = set(list)
    return len(set_of_list)

List_MD = []
List_grades = []
# import all the churchservers from the JSON file
import_churchservers_from_dataframe(json_to_pdataframe(), List_MD)

for x in range(len(List_MD)):
    List_grades.append(List_MD[x].group)

print(get_amount_of_elements(List_grades))


 # TODO Rebuild this as a dataframe
def create_list_of_groups(list_all_servers):
    set_of_groups = set([])
    list_of_groups = []
    str_order_of_groups = []
    for server in range(len(list_all_servers)):
        set_of_groups.add(list_all_servers[server].group)
    order_of_groups = list(set_of_groups)
    for x in range(len(order_of_groups)):
        str_order_of_groups.append(str(order_of_groups[x]))
    for group_amount in range(len(set_of_groups)):
        list_of_groups.append([])
    for server in range(len(list_all_servers)):
        list_of_groups[order_of_groups.index(list_all_servers[server].group)].append(list_all_servers[server])
    return list_of_groups, order_of_groups, str_order_of_groups


def create_dataframe_of_groups(list_all_servers):
    #Takes a list and turns it into a pandas.DataFrame
    return pandas.DataFrame(create_list_of_groups(list_all_servers)[0])


def get_server_from_abbreviation(abbreviation, storage_object):
    # Takes an abbreviation and a List of all ChurchServers and returns the first ChurchServer with a matching
    # abbreviation
    for b in range(len(storage_object.list_churchservers)):
        if abbreviation == storage_object.list_churchservers[b].abbreviation:
            return storage_object.list_churchservers[b]


def get_unavailable_dates(selected_churchserver):
    return selected_churchserver.unavailable


def remove_unavailable_days(church_server, unavailable_days):
    # Removes all days from a list from the unavailable list of the ChurchServer
    # Try is used to get rid of the error thrown when unavailable Days is not in the unavailable days.
    for selected_date in range(len(unavailable_days)):
        church_server.unavailable.remove(unavailable_days[selected_date])

