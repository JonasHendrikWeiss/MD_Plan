from Zuordnung import *
import pandas
import os


class data_storage():
    def __init__(self, list_churchservers = [], list_services=[]):
        self.list_churchservers = list_churchservers
        self.list_services = list_services


def json_to_pdataframe(dir_path=os.path.dirname(os.path.realpath(__file__)), filname="JSON"):
    # returns a dataframe called pdataframe_json for further use in the program
    pdataframe_json = pandas.read_json(path_or_buf=f"{dir_path}/{filname}", dtype=ChurchServers)
    return pdataframe_json


def import_churchservers_from_dataframe(pdataframe , server_list):
    for x in range(0, pdataframe.size):
        current_cserver = ChurchServers(lastname=pdataframe.at[0, x]["lastname"], firstname=pdataframe.at[0, x]["firstname"],
                                        abbreviation=pdataframe.at[0, x]["abbreviation"],
                                        unavailable = pdataframe.at[0, x]["unavailable"], group= pdataframe.at[0, x]["group"])
        server_list.append(current_cserver)


def list_to_json(list, dir_path=os.path.dirname(os.path.realpath(__file__)),
                 filename="JSON"):
    pandas.DataFrame([list]).to_json(path_or_buf=f"{dir_path}/{filename}")


