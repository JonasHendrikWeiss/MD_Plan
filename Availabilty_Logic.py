# the controller behind the availability page of the application
from Panda_To_Storage import import_churchservers_from_dataframe, json_to_pdataframe

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



A = [1,1,1,1,1,1,2,3,4,5,3,5,3,2,3,8]
b = set(A)
print(b)
b.add(1)
c= list(b)
print(c.index(8))
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


def fill_churchserver_selection_button(button_grades, button_servers, list_all_servers):
    list_of_groups = create_list_of_groups(list_all_servers)[0]
    order_of_groups = create_list_of_groups(list_all_servers)[1]




print(create_list_of_groups(List_MD))
pass
print(len(List_MD))