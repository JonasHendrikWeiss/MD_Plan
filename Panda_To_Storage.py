from Zuordnung import *
import pandas
import os


def json_to_pdataframe(path=os.path.dirname(os.path.realpath(__file__)), filname="JSON"):
    # returns a dataframe called pdataframe_json for further use in the program
    pdataframe_json = pandas.read_json(path_or_buf=f"{path}/{filname}", dtype=ChurchServers)
    return pdataframe_json


def import_churchservers_from_dataframe(pdataframe , server_list):
    for x in range(0, pdataframe.size):
        current_cserver = ChurchServers(lastname=pdataframe.at[0, x]["lastname"], firstname=pdataframe.at[0, x]["firstname"],
                                        abbreviation=pdataframe.at[0, x]["abbreviation"])
        current_cserver.unavailable = pdataframe.at[0, x]["unavailable"]
        server_list.append(current_cserver)


# import_churchservers_from_dataframe(json_to_pdataframe())