from Zuordnung import ChurchGroup, ChurchService, ChurchServer, TimeSpan
import pandas, pickle
import os
from datetime import datetime


class data_storage():
    def __init__(self, list_churchservers=[], list_services=[], list_groups=[]):
        self.list_churchservers = list_churchservers
        self.list_services = list_services
        self.list_groups = list_groups

    def delete_churchserver(self, churchserver):
        grade_server = churchserver.group
        grade_server.members.remove(churchserver)
        self.list_churchservers.remove(churchserver)

def pickle_storage(storage_object, dir_path=os.path.dirname(os.path.realpath(__file__)), filename="data_storage.pkl"):
    pickle.dump(storage_object, file= open(dir_path+"/"+filename, 'wb'))
    print(dir_path+filename)
    print("pickled everything")


def unpickle_storage(dir_path=os.path.dirname(os.path.realpath(__file__)), filename="data_storage.pkl"):
    try:
        imported_data = pickle.load(file= open(dir_path+"/"+filename, 'rb'))
    except EOFError:
        print("file doesnt exist or is empty")
        imported_data = data_storage()
    return imported_data


def json_to_pdataframe(dir_path=os.path.dirname(os.path.realpath(__file__)), filname="JSON"):
    # returns a dataframe called pdataframe_json for further use in the program
    pdataframe_json = pandas.read_json(path_or_buf=f"{dir_path}/{filname}", dtype=ChurchServer)
    return pdataframe_json


def import_churchservers_from_dataframe(pdataframe, server_list):
    for server in range(0, pdataframe.size):
        temp_list = []  # creates a temporary list for each server
        if pdataframe.at[0, server]["unavailable"]:  # only uses ChurchServer which unavailable lists are not empty
            temp_list = load_TimeSpan(pdataframe.at[0, server]["unavailable"])

        current_cserver = ChurchServer(lastname=pdataframe.at[0, server]["lastname"],
                                       firstname=pdataframe.at[0, server]["firstname"],
                                       abbreviation=pdataframe.at[0, server]["abbreviation"],
                                       unavailable = temp_list,
                                       group= pdataframe.at[0, server]["group"])
        server_list.append(current_cserver)


def list_to_json(data_list, dir_path=os.path.dirname(os.path.realpath(__file__)),
                 filename="JSON"):
    pandas.DataFrame([data_list]).to_json(path_or_buf=f"{dir_path}/{filename}",)
    # if the data increases in size look for double imports because if the dataframe is appended twice data doubles


def load_TimeSpan(unavailable_list):
    # Takes the list of dictionaries that are generated when TimeSpan Objects are Saved and returns a list of TimeSpan
    # objects
    return_list = []
    for selected_entry in range(len(unavailable_list)):
        # stamp_start is the timestamp of the start_date
        stamp_start = int(unavailable_list[selected_entry]["start_date"])
        # converts the timestamp back into a datetime.date
        date_start = datetime.fromtimestamp(stamp_start / 1e3).date()
        # stamp_end is the timestamp of the end_date
        stamp_end = int(unavailable_list[selected_entry]["end_date"])
        date_end = datetime.fromtimestamp(stamp_end / 1e3).date()
        return_list.append(TimeSpan(date_start, date_end)) # creates a TimeSpan Object out of the timestamps
    return return_list


def reinitalize_churchservers(list_of_cservers):
    reinitalized_list = []
    for c in range(len(list_of_cservers)):
        selection = list_of_cservers[c]
        reinitalized_list.append(ChurchServer(selection.lastname, selection.firstname, selection.abbreviation,
                                              selection.group, selection.unavailable))
        selection.group.members.remove(selection) # removes the person from the group so it isn't carried over
    return reinitalized_list