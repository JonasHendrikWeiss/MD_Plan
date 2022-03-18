from Panda_To_Storage import import_churchservers_from_dataframe, json_to_pdataframe
import pandas
from Zuordnung import ChurchService

def create_new_churchservice(date,number_of_chuchservers, storage_location):
    new_service = ChurchService(number_of_chuchservers, date)
    storage_location.append(new_service)