# the controller behind the availability page of the application
from Storage_Operations import import_churchservers_from_dataframe, json_to_pdataframe
import pandas

def get_amount_of_elements(list):
    set_of_list = set(list)
    return len(set_of_list)

List_MD = []
List_grades = []
# import all the churchservers from the JSON file
import_churchservers_from_dataframe(json_to_pdataframe(), List_MD)




def create_list_of_groups(list_all_servers):
    set_of_groups = set([])
    list_of_groups = []
    for server in range(len(list_all_servers)):
        set_of_groups.add(list_all_servers[server].group)
    order_of_groups = list(set_of_groups)
    # maps the list and turns all items into integers to sort them by value more easily
    order_of_groups = list(map(int, order_of_groups))
    order_of_groups.sort()
    # Turns the integers back into strings
    order_of_groups = list(map(str, order_of_groups))
    for group_amount in range(len(set_of_groups)):
        list_of_groups.append([])
    for server in range(len(list_all_servers)):
        list_of_groups[order_of_groups.index(list_all_servers[server].group)].append(list_all_servers[server])

    return list_of_groups, order_of_groups
    # str_order_of_groups was removed because it was the same as order of groups


def create_dataframe_of_groups(list_all_servers):
    #Takes a list and turns it into a pandas.DataFrame
    return pandas.DataFrame(create_list_of_groups(list_all_servers)[0])



def get_unavailable_dates(selected_churchserver):
    # returns a list with the descriptions of unavailable days
    description_list=[]
    for c in range(len(selected_churchserver.unavailable)):
        description_list.append(selected_churchserver.unavailable[c])
    return description_list


def remove_unavailable_days(church_server, unavailable_days):
    # Removes all TimeSpan Objects from a list from the unavailable list of the ChurchServer
    for selected_date in range(len(unavailable_days)):
        church_server.unavailable.remove(unavailable_days[selected_date])

