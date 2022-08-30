import multiprocessing

import numpy as np
from georinex import *
import os
from multiprocessing import Queue, Process
from Orbit import absorb


# Objective : To read a RINEX observation file for processing


########################################################################################################################
# SECTION 1 : PRELIMINARY OPERATIONS AND FUNCTION DEFINITION

# Satellite class - stores sat-rcv info obtained from observation file
class Satellite(object):
    """A satellite class for calculations:
    Needs following info  from Nav and Obs file to initialize:
    1: Name
    2: Time of Observation(epoch time) (Found in Observation RINEX file)
    3: Position (position)
    4: Satellite Clock Error(bias) (Found in Navigation file)
    5: Receiver clock offset(rcoff): A bool value to see if receiver clock offset is applied
    6: Pseudo-range (C1C) : Pseudo range for L1 frequency (C/A)
    7: Pseudo-range (C2C) : Pseudo range for L2 frequency (C/A)
    8: Dual-Channeled(channel) : bool to see if receiver is dual channel
    9: Transformation (t_apply) : bool to see if coordinate transformations is applied
    10: Check if all the data is available (sync)

    Critical Method:
    Satellite.sync(self) -> see if all the parameter are available to calculate
    approximate position. Warning!! will pop off if something is missing!! Resync until
    self.snc is True:
    """

    def __init__(self, name: str, time: np.datetime64, position: np.array = None,
                 bias: float = None, rcoff: bool = None, C1C: np.float32 = None, C2C: np.float32 = None, channel:
            bool = None, t_apply: bool = None) -> None:
        self.snc = False
        self.t_apply = t_apply
        self.channel = channel
        self.C2C = C2C
        self.rcoff = rcoff
        self.bias = bias
        self.position = position
        self.time = time
        self.name = name
        self.C1C = C1C

    def sync(self) -> None:
        self.snc = True
        attrs = self.__dict__
        attrs.pop("name")
        attrs.pop("time")

        for keys in attrs.keys():
            if attrs[keys] is None:
                self.snc = False


# Function to open the RINEX files

def OPEN(path: str, satID="G"):
    """Opens RINEX file automatically.
       Extracts only GPS satellite"""

    if "MO" in path.upper() or "GO" in path.upper():
        try:
            return rinexheader(path_to_obs), rinexobs(path, use=satID)

        except:
            print("Cannot open the RINEX file! Check if you have permission to read the file")

            print("Checking the file path!")
            if os.path.exists(path):
                print("File Exists! But cannot read")

            raise "Cannot load the rinex file!"
    elif "GN" in path.upper() or "MN" in path.upper():
        try:
            return rinexnav(path, use=satID)
        except:
            print("Cannot open the RINEX file! Check if you have permission to read the file")

            print("Checking the file path!")
            if os.path.exists(path):
                print("File Exists! But cannot read")

            raise "Cannot load the rinex file!"


# Function to find intersection of epoch of observation between RINEX nav and obs file

def INTERSECTION(obs, nav) -> np.array:
    """Output is all the sv captured and time of intersection in a tuple (sv : np.array, time: np.datetime64) """

    # time of capture -- all time at which satellite is captured by receiver
    __obs_time = np.array(obs.time)

    # All the epoch of observation
    __nav_time = np.array(nav.time)

    # Checks for intersections of Epoch time between two time
    intersection_time = np.intersect1d(__nav_time, __obs_time)

    # FINDS THE SATELLITE THAT HAVE ALL OBS AND NAV DATA NEED FOR POSITIONING
    if np.size(intersection_time) == 0:
        raise "No Intersection time found between Navigation or Observation file!"

    return np.intersect1d(obs.sel(time=intersection_time[0]).sv, nav.sel(time=intersection_time[0]).sv), \
           intersection_time[0]


########################################################################################################################

# SECTION 2 :  DATA DIRECTORIES CHECKING

# NOTE: If you put your files in the data dir in the programs dir it will automatically
# fnd the data. There must be only two data files - RINEX NAV(valid) AND RINEX OBS FILE FOR SAME

# Name of data dirs
datsDir = os.path.abspath('../OBS-SAT/data')

# Path to my data files
path_to_nav = ""
path_to_obs = ""

# Checks if path exists or not
if os.path.exists(datsDir) and len(os.listdir(datsDir)) == 2:
    for file_name in os.listdir(datsDir):
        if 'MO' in file_name.upper() or 'GO' in file_name.upper():
            path_to_obs = os.path.join(datsDir, file_name)
        elif 'GN' in file_name.upper() or 'MN' in file_name.upper():
            path_to_nav = os.path.join(datsDir, file_name)

else:
    print(f"PYTHON DIDN'T FIND ANY DATA FILES IN FOLLOWING DIRECTORY-:\n"
          f"{datsDir}\n\nMANUALLY ENTER THE PATH TO THE DATA FILES!\n")

    path_to_nav = input("ENTER ABSOLUTE PATH TO NAVIGATION RINEX FILE: ")
    path_to_obs = input("ENTER ABSOLUTE PATH TO NAVIGATION RINEX FILE: ")


########################################################################################################################

# SECTION 3 : MAIN FUNCTION

def main():
    # open observation and navigation files
    obs_header, obs = OPEN(path_to_obs)
    nav = OPEN(path_to_nav)

    # All measurement in all channel L1, L2, L5 ~ contains both range, phase, doppler, signal strength
    __all_data = np.array(obs.data_vars)

    # Header data needed to postProcess RINEX file
    __header_data = ['RCV CLOCK OFFS APPL', 'APPROX POSITION XYZ', 'TIME OF FIRST OBS', ]

    # Pseudo range(C/A) ->  C1C= pseudo-range on L1 channel and C2C= pseudo-range on L2 channel
    __data = ["C1C", "C2C", ]

    # Data generated at same epoch (Synchronizing NAV and OBS file)
    common_sv, common_time = INTERSECTION(obs, nav)

    # CREATE SATELLITE OBJECT FILLING ALL THE REQUIRED FIELD | USES MULTIPLE CORES OF CPU


if __name__ == '__main__':
    main()


#############################################################END########################################################

def TARGET(sv: str, time: np.datetime64, data_extract: list, queue: Queue) -> None:
    pass


# args = ( target  --> Gps_satellite , nav ,obs )
def GET_DATA(common_sv: np.array, common_time: np.datetime64, data_extract: list, obs, nav) -> list:
    pass
