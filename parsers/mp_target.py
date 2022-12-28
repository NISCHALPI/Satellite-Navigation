import multiprocessing as mp
import xarray
import numpy as np
from navigation import NAVIGATION

import sys

sys.path.append('../')

# IGNORE THE ERROR | SYS PYTHON_PATH EXPORTED
from threaded.threads.Fthread import Fthread
from threaded.preprocessing import preprocessing


############################################ THE SATELLITE CLASS #######################################################
# Satellite class - stores sat-rcv info obtained from observation file
class Satellite(object):
    """A satellite class for calculations:
    Needs following info  from Nav and Obs file to initialize:
    1: Name
    2: Time of Observation(epoch time) (Found in Observation RINEX file)
    3: Position (position) : np.array
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
        self.dual = channel
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

    def transformation(self, transform: callable):

        try:
            self.position = transform(self.position, self.C1C)
            self.t_apply = True
        except:
            raise "Couldn't apply the earth rotation transformation!"


############################################# FUNCTION AND DATA DEFINITION #############################################

__data = ["C1C", "C2C"]
__data2 = ["C1L", "C2L"]

# Function to find intersection of epoch of observation between RINEX nav and obs file
def __INTERSECTION(obs, nav, quite) -> tuple:
    """Output is all the sv captured and time of intersection in a tuple (sv : np.array, time: np.datetime64) """

    if not quite: 
        print("\nChecking for common epoch in Observation and Navigation file!")
        print("------------------------------------")
    # time of capture -- all time at which satellite is captured by receiver
    __obs_time = np.array(obs.time)

    # All the epoch of observation
    __nav_time = np.array(nav.time)

    # Checks for intersections of Epoch time between two time
    intersection_time = np.intersect1d(__nav_time, __obs_time)

    # FINDS THE SATELLITE THAT HAVE ALL OBS AND NAV DATA NEED FOR POSITIONING
    if np.size(intersection_time) == 0:
        raise "No Intersection time found between Navigation or Observation file!"
    else:
        if not quite:
            print("Intersection Found!")
            
            for time in intersection_time:
                print(time)
                print("\n")

    return np.intersect1d(obs.sel(time=intersection_time[0]).sv, nav.sel(time=intersection_time[0]).sv), \
           intersection_time[0]




# CHECKS IF DATA EXISTS IN INTERSECTION
def __CHECK_NAV(nav_data: xarray.Dataset, sv_list: list or np.array, epoch_time: np.datetime64 or np.array, quite) -> list:
    """Checks if the navigation file has filled parameters for the satellite"""

    if not quite:
        print("Checking data integrity in Navigation File for intersecting epoch!")
        print("------------------------------------")
    filtered_list = []


    for _sv in sv_list:
        isEmpty = np.isnan(nav_data.sel(sv=_sv, time=epoch_time)["M0"].item(0))
        if not isEmpty:
            filtered_list.append(_sv)
    if len(filtered_list) < 4:
        raise """Less than 4 satellite observed! Undetermined Solution: At least 4 required!!!"""
    
    if not quite: 
        for _ in filtered_list:
            print(f"Found complete data for SV = {_}")

        print("------------------------------------")
        print(f"Total SV available: {len(filtered_list)}\n")

    return filtered_list


############################################## MULTIPROCESSING STUFF| DO NOT TOUCH WITHOUT READING MULTIPROCESSING #####
# MULTIPROCESSING TARGET FUNCTION


def __EXTRACT_SV(quite : bool , obs: xarray.Dataset, nav: xarray.Dataset, SV: str, time: np.datetime64, isThread: bool =
False, queue: mp.Queue = None,  ) -> None or Satellite:
    """EXTRACTS DATA FROM SATELLITE GIVEN RINEX NAV AND OBS FILE 
        DESIGNED FOR MULTIPROCESSING!
        
        :argument: OBS-FILE, NAVFILE, SV_NAME, TIME_OF_OBS (EPOCH), IS_DUAL_CHANNEL
        :return :  PUTS SATELLITE  IN MULTIPROCESSING QUEUE | SEE MULTIPROCESSING DOCS 
        """

    global  __data2, __data
    ######################################## OBSERVATION DATA EXTRACT ##############################

    # Objective: Sync the Satellite Class
    sat = Satellite(name=SV, time=time)

    # No Earth rotation transformation applied yet
    sat.t_apply = False

    sat.dual = True


    # Checks for dual channel with respect to __data2 = ["C1C" , "C2C"]
    try:
        for index, attr in enumerate(__data2):
            if not np.isnan(obs[attr].item(0)):
                setattr(sat, __data[index] , obs[attr].item(0))
            else:
                raise "Error! Not a Num"
    except:
        sat.dual = False


    # If not dual with respect to __data2, check  dual with respect to __data1 ["C1C", "C2C"]
    if not sat.dual:
        try:
            for attr in __data:
                if not np.isnan(obs[attr].item(0)):
                    setattr(sat, attr, obs[attr].item(0))
                else:
                    raise "Error! Not a Num"
        except:
            sat.dual = False



    ####################################NAV SECTION DATA EXTRACT ################################################
    if not quite: 
        print(f"Extracting and Processing Navigation Data for {sat.name}")
    # Extracts position and sv clock error

    # Implementer in navigation.py
    position, dt = NAVIGATION(nav, SV, time)

    # Sets position and clock error to satellite class
    sat.position = position
    sat.bias = dt


    ###################################### APPLY PRE-PREOCESSING HERE ##############
    preprocessing(sat, quite)




    # Puts the satellite in the queue
    if isThread:
        return sat
    else:
        queue.put(sat)


# Fix me! Complete Multiprocess
def MULTIPROCESS(obs: xarray.Dataset, nav: xarray.Dataset, quite) -> list:

    # Checks if there is intersection between two RINEX files
    common_sv, common_t = __INTERSECTION(obs, nav, quite)


    # Checks if all the observed satellite have enough data to calculate their position
    common_sv = __CHECK_NAV(nav, common_sv, common_t, quite)

    ######################Multiprocess Process Implementation###################################
    if not quite:
        print("------------------------------------PARSING STARTING------------------------------------------")
        print(f"Spawning {len(common_sv)} process for parsing!")
        print("OUTPUT MAY BE OUT OF SYNC")
        print("------------------------------------")

    # TARGET QUEUE
    queue = mp.Queue()

    # EMPTY PROCESS LIST
    process = []

    # EMPTY SV LIST
    sv_list = []

    # Create targe Process
    for sat in common_sv:
        process.append(
            mp.Process(target=__EXTRACT_SV, args=(quite , obs.sel(sv=sat, time=common_t), nav.sel(sv=sat, time=common_t),
                                                  sat, common_t, False, queue)))

    # Async Process Start
    for proc in process:
        proc.start()

    # Sync the Process
    for proc in process:
        proc.join()

    # Extracts the queue
    while queue.empty() is False:
        sv_list.append(queue.get())

    if not quite:
        print("------------------------------------")
        print("All process completed!\n")

    return sv_list


def MULTITHREAD(obs: xarray.Dataset, nav: xarray.Dataset, quite : bool = False) -> list:
    # Checks if there is intersection between two RINEX files
    common_sv, common_t = __INTERSECTION(obs, nav, quite)


    # Checks if all the observed satellite have enough data to calculate their position
    common_sv = __CHECK_NAV(nav, common_sv, common_t, quite)

    ######################Multithreads Implementation###################################

    # EMPTY PROCESS LIST
    threads = []
    if not quite:
        print("------------------------------------PARSING STARTING------------------------------------------\n")

        print(f"Spawning {len(common_sv)} async thread for parsing!")
        print("OUTPUT MAY BE OUT OF SYNC")
        print("------------------------------------")

    # Create target threads
    for sat in common_sv:
        threads.append(
            Fthread(__EXTRACT_SV, args=(quite , obs.sel(sv=sat, time=common_t), nav.sel(sv=sat, time=common_t),
                                        sat, common_t, True)))

    # Async thread Start
    for trd in threads:
        trd.start()

    # Sync the threads
    for trd in threads:
        trd.join()

    if not quite: 
        print("------------------------------------")
        print("All threads completed!\n")
    
    # Returns the threads
    return [thread.get for thread in threads]
