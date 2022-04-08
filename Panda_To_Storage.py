from Zuordnung import *
import pandas
import os
from datetime import datetime


class data_storage():
    def __init__(self, list_churchservers = [], list_services=[]):
        self.list_churchservers = list_churchservers
        self.list_services = list_services


def json_to_pdataframe(dir_path=os.path.dirname(os.path.realpath(__file__)), filname="JSON"):
    # returns a dataframe called pdataframe_json for further use in the program
    pdataframe_json = pandas.read_json(path_or_buf=f"{dir_path}/{filname}", dtype=ChurchServers)
    return pdataframe_json


def import_churchservers_from_dataframe(pdataframe, server_list):
    for server in range(0, pdataframe.size):
        temp_list = []  # creates a temporary list for each server
        if pdataframe.at[0, server]["unavailable"]:  # only uses ChurchServers which unavailable lists are not empty
            for selected_entry in range(len(pdataframe.at[0, server]["unavailable"])):
                # stamp_start is the timestamp of the start_date
                stamp_start = int(pdataframe.at[0, server]["unavailable"][selected_entry]["start_date"])
                # converts the timestamp back into a datetime.date
                date_start = datetime.fromtimestamp(stamp_start / 1e3).date()
                # stamp_end is the timestamp of the end_date
                stamp_end = int(pdataframe.at[0, server]["unavailable"][selected_entry]["end_date"])
                date_end = datetime.fromtimestamp(stamp_end / 1e3).date()
                temp_list.append(TimeSpan(date_start, date_end)) # creates a TimeSpan Object out of the timestamps

        current_cserver = ChurchServers(lastname=pdataframe.at[0, server]["lastname"],
                                        firstname=pdataframe.at[0, server]["firstname"],
                                        abbreviation=pdataframe.at[0, server]["abbreviation"],
                                        unavailable = temp_list,
                                        group= pdataframe.at[0, server]["group"])
        server_list.append(current_cserver)


def list_to_json(list, dir_path=os.path.dirname(os.path.realpath(__file__)),
                 filename="JSON"):
    pandas.DataFrame([list]).to_json(path_or_buf=f"{dir_path}/{filename}",)
    # if it crashed at [] around list. Removed it because the size of the data was increasing

def load_TimeSpan(dictionary, list): # loads TimeSpan Objects to a list
    for selected_entry in range(len(dictionary)):
        # stamp_start is the timestamp of the start_date
        stamp_start = int(dictionary["start_date"])
        # converts the timestamp back into a datetime.date
        date_start = datetime.fromtimestamp(stamp_start / 1e3).date()
        # stamp_end is the timestamp of the end_date
        stamp_end = int(dictionary[selected_entry]["end_date"])
        date_end = datetime.fromtimestamp(stamp_end / 1e3).date()
        list.append(TimeSpan(date_start, date_end)) # creates a TimeSpan Object out of the timestamps
    return list
