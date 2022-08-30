import georinex as gr
import xarray
from superparser import INTERSECTION, Satellite



__data = ["C1C", "C2C"]

obs = gr.rinexobs('/home/bubble/Desktop/Programs/python/OBS-SAT/data/ABPO00MDG_R_20220421000_01H_30S_MO.crx', use='G')
nav = gr.rinexnav('/home/bubble/Desktop/Programs/python/OBS-SAT/data/ABPO00MDG_R_20220421000_01H_GN.rnx', use='G')

common_sv, common_time = INTERSECTION(obs, nav)


############################################## MULTIPROCESSING STUFF| DO NOT TOUCH WITHOUT READING MULTIPROCESSING #####


# Dual channel Detector
def DUAL_CHANNEL(_obs: xarray.Dataset) -> bool:
    """
    ARGS: _obs
    RETURN: Bool : True if "C1C" and "C2C" exists | False otherwise

    """

    # ALL THE OBSERVATION DATA
    keys = list(_obs.data_vars.keys())

    for attrs in __data:
        if attrs not in keys:
            return False
    return True



# MULTIPROCESSING TARGET FUNCTION
def EXTRACT_SV(SV: str, time, isDual: bool, data_extract=None) -> None:

    # Read the global variable
    if data_extract is None:
        data_extract = __data
######################################## OBSERVATION DATA EXTRACT ##############################
    # Objective: Sync the Satellite Class
    sat = Satellite(name=SV, time=time)

    # Get the specific sv data
    sv_data = obs.sel(sv=SV, time=time)

    # No Earth rotation transformation applied yet
    sat.t_apply = False

    # Dual channel data Extract and Setting
    if not isDual:
        """If not dual channel, set C1C only"""
        setattr(sat, data_extract[0], sv_data[data_extract[0]].values)
        setattr(sat, "channel", False)
    else:
        "Otherwise set C1C and C2C"
        for attrs in __data:
            setattr(sat, attrs, sv_data[attrs].values)

####################################NAV SECTION DATA EXTRACT ################################################



    for attrs in sat.__dict__:
        print(f"{attrs} -> {getattr(sat , attrs)}")





if __name__ == '__main__':
    dual = DUAL_CHANNEL(obs)
    EXTRACT_SV(common_sv[0], common_time, dual)
