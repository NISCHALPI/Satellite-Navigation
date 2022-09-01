import multiprocessing
import xarray
import numpy as np
from georinex import *
import os
from multiprocessing import Queue, Process


# Objective : To read a RINEX observation file for processing


########################################################################################################################
# SECTION 1 : PRELIMINARY OPERATIONS AND FUNCTION DEFINITION
# Function to open the RINEX files

def OPEN(path: str, satID="G"):
    """Opens RINEX file automatically.
       Extracts only GPS satellite"""

    if "MO" in path.upper() or "GO" in path.upper():
        try:
            return rinexheader(path), rinexobs(path, use=satID)

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




########################################################################################################################

# SECTION 2 :  DATA DIRECTORIES CHECKING

# NOTE: If you put your files in the data dir in the programs dir it will automatically
# fnd the data. There must be only two data files - RINEX NAV(valid) AND RINEX OBS FILE FOR SAME

def CHECK_DATADIR() -> tuple:
    # Name of data dirs
    datsDir = os.path.abspath('../data')

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

    return path_to_obs, path_to_nav


########################################################################################################################

# SECTION 3 : MAIN FUNCTION

def main():
    # Extracts data from User
    path_to_obs, path_to_nav = CHECK_DATADIR()

    # open observation and navigation files
    obs_header, obs = OPEN(path_to_obs)

    nav = OPEN(path_to_nav)

    # All measurement in all channel L1, L2, L5 ~ contains both range, phase, doppler, signal strength
    __all_data = np.array(obs.data_vars)

    # Header data needed to postProcess RINEX file
    __header_data = ['RCV CLOCK OFFS APPL', 'APPROX POSITION XYZ', 'TIME OF FIRST OBS', ]






if __name__ == '__main__':
    main()


#############################################################END########################################################
