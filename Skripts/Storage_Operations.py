from Zuordnung import ChurchGroup, ChurchService, ChurchServer, TimeSpan, Version
import pandas, pickle
import os
from datetime import datetime


class data_storage():
    def __init__(self, list_churchservers=[], list_services=[], list_groups=[], version_input=Version()):
        self.list_churchservers = list_churchservers
        self.list_services = list_services
        self.list_groups = list_groups
        # A version counter in order to check if the object is up to date
        self.version = version_input

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


def reinitalize_churchservers(list_of_cservers, version):
    reinitalized_list = []
    if version > 1:
        for c in range(len(list_of_cservers)):
            selection = list_of_cservers[c]
            reinitalized_list.append(ChurchServer(lastname=selection.lastname, firstname=selection.firstname,
                                                  abbreviation=selection.abbreviation, group=selection.group,
                                                  unavailable=selection.unavailable, offset=selection.offset,
                                                  group_leader=selection.group_leader))
            selection.group.members.remove(selection) # removes the person from the group so it isn't carried over
            # TODO remove the old and add the new object to all services
    elif version == 1: # Needed because version one had no offset object
        for c in range(len(list_of_cservers)):
            selection = list_of_cservers[c]
            reinitalized_list.append(ChurchServer(lastname=selection.lastname,firstname= selection.firstname,
                                                  abbreviation= selection.abbreviation, group= selection.group,
                                                  unavailable= selection.unavailable))
            selection.group.members.remove(selection) # removes the person from the group so it isn't carried over
    return reinitalized_list
    # When changing this remember to change the version change in storage


def update_objects(storage):
    
    sample_version = Version()
    
    if storage.version.ChurchServer_version != sample_version.ChurchServer_version:
        storage.list_churchservers = reinitalize_churchservers(storage.list_churchservers,
                                                               storage.version.ChurchServer_version)
        # updates the version of the Churchservers that currently existing and then changes the version object
        storage.version.ChurchServer_version = 1
    if storage.version.ChurchService_version != sample_version.ChurchService_version:
        print("test_churchservice")
    if storage.version.ChurchGroup_version != sample_version.ChurchGroup_version:
        print("test_churchgroup")
    if storage.version.Timespan_version != sample_version.Timespan_version:
        print("test_timespan")
    # storage update needs to be done last because it also updates the version number
    if storage.version.Storage_version != sample_version.Storage_version:
        print("test_storage")
        storage = reinitalize_data_storage(storage)
    return storage




def reinitalize_data_storage(storage):
    new_storage = data_storage(list_churchservers=storage.list_churchservers, list_groups=storage.list_groups,
                 list_services=storage.list_services, version_input=storage.version)
    new_storage.version.Storage_version = 1
    # updates only the storage version counter and not all version counters
    return new_storage


if __name__ == "__main__":
    update = update_objects(unpickle_storage())
    pickle_storage(update)