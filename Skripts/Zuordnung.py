import random
import pandas
from statistics import mean, median, stdev
from datetime import datetime, date, timedelta, time
from docx import Document


List_MD = []
List_Services = []
statistic_list = []


class Version:
    def __init__(self):
        self.ChurchServer_version = 2
        self.ChurchService_version = 1
        self.ChurchGroup_version = 1
        self.Timespan_version = 1
        self.Storage_version = 1


class ChurchServer:
    def __init__(self, lastname, firstname, abbreviation, group="Null", unavailable=[], group_leader=False, offset=0):
        # MD is used as an abbreviation of ChurchServer throughout the code
        # Different Name Attribute of the church server
        self.lastname = lastname
        self.firstname = firstname
        self.fullname = self.get_fullname()
        self.abbreviation = abbreviation
        # Shows if someone is able to serve at Church
        self.group_leader = group_leader
        # Groups are used to organize the ChurchServer and make them more manageable
        # Offset is a value that is used in automatically selecting a CS so a newly created server is not overasigned
        # Values are The average count value a ChurchServer has, +/- 1 exact values need to be determined by testing
        self.offset = int(offset)
        # "Null" is a String to show the group did not work
        if type(group) == type(ChurchGroup("samplegroup")):
            group.add_churchserver(self)
        else:
            self.group = group
        self.counter = 0
        # List of TimeSpan objects when a ChurchServer is not available
        self.unavailable = unavailable
        # remember to change the version counter

    def add_unavailable(self, timespan):
        overlap_list = []
        for selected_unavailable in range(len(self.unavailable)):
            if timespan.check_overlap(self.unavailable[selected_unavailable]):  # Checks if there are any overlaps
                overlap_list.append(self.unavailable[selected_unavailable]) # Mergeable TimeSpans are appended to a list

        for selected_merge in range(len(overlap_list)):
            self.unavailable.remove(overlap_list[selected_merge]) # removes the overlapping element
            timespan = merge_timespan(timespan, overlap_list[selected_merge]) # merges all overlapping elements
        self.unavailable.append(timespan)  # adds the final TimeSpan to the unavailable list

    def is_available(self, checked_date):
        for x in range(len(self.unavailable)):
            if self.unavailable[x].during_timespan(checked_date) is True:
                return False # Returns false if the date is inside of any timespan the ChurchServer is unavailable
        return True

    def get_fullname(self):
        return f"{self.firstname} {self.lastname}"


class ChurchService:
    def __init__(self, number_cs_needed, number_leaders, day, time = time(11,15)):
        # numberMD is the number of ChurchServer needed for the Church Service
        self.count_churchservers = int(number_cs_needed)
        self.count_leaders = int(number_leaders)
        self.count = self.count_churchservers + self.count_leaders
        self.current_churchservers = []
        # NumberAllocatedMD shows the current amount of Church Servers that are allocated to the Service.
        # Adds a time to each ChurchService
        # date_time should be a datetime an_object
        self.time = time
        # self.day is a Datetime an_object as a .isoformat() string
        self.date = day
        # time.strftime('%H:%M') outputs the Hour and minutes of a time
        self.description = f"Messe am {self.date.isoformat()} um {time.strftime('%H:%M')} \n mit {self.count} Messdienern"
        # remember to change the version counter


class TimeSpan:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.order_dates()
        self.description = f"{self.start_date} / {self.end_date}"
        # remember to change the version counter

    def during_timespan(self, checked_date): # Takes a date and returns true if it is in the TimeSpan
        if self.start_date <= checked_date <= self.end_date:
            return True
        else:
            return False

    def check_overlap(self, other):
        # TODO add functionality if day is one of start or end date
        if other.during_timespan(self.start_date - timedelta(days=1)):
            return True
        elif self.during_timespan(other.start_date):
            # This is needed because otherwise one can add a one day TimeSpan to itself
            return True
        elif self.during_timespan(other.start_date - timedelta(days=1)):
            return True
        else:
            return False

    def order_dates(self):
        if self.start_date > self.end_date:
            # Swaps the two values around so the start date is always at the beginning
            self.start_date, self.end_date = self.end_date, self.start_date


def merge_timespan(first_time_span, other_time_span):
    # Merges two TimeSpan Objects into a new one does not delete the old ones
    if first_time_span.check_overlap(other_time_span):  # Checks for shared days so the TimeSpan can be merged
        new_start = min(first_time_span.start_date, other_time_span.start_date)  # the start of the new merge
        new_end = max (first_time_span.end_date, other_time_span.end_date)
        return TimeSpan(new_start, new_end)
    else:
        print("Cannot merge the time span two disjoined events")

# TODO remove all the old unused bits of code in this file and rename it

class ChurchGroup():
    def __init__(self, name, members=[], start_year=datetime.now().year):
        self.name = name
        self.members = list(members)
        self.start_year= start_year
        # remember to change the version counter

    def add_churchserver(self, church_server):
        # adds a churchserver to the ChurchGroup and also adds the link back to the ChurchGroup in the Churchserver
        self.members.append(church_server)
        church_server.group = self


def create_church_servers(filepath, sheet, server_list):
    columns = ["Vorname", "Nachname", "Kürzel", "Schuljahr"]
    table_server = pandas.read_excel(filepath, sheet_name=sheet, header=0, engine="openpyxl",
                                     usecols=columns)
    for x in range(0, table_server.shape[0]):
        server_list.append(ChurchServer(lastname=table_server.at[x, "Nachname"],
                                        firstname=table_server.at[x, "Vorname"],
                                        abbreviation=table_server.at[x, "Kürzel"]))





# Functions needed to output the Services to a Docx file



def statistical_analysis():
    print(List_Services[1])
    print(List_MD[1].unavailable)
    print("mean", mean(statistic_list))
    print("median", median(statistic_list))
    print("standard deviation", stdev(statistic_list))
    print("max", max(statistic_list))
    print("min", min(statistic_list))


# Definition of lists and variables needed later
if __name__ == "__main__":
    print("test")