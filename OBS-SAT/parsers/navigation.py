import math
import warnings

import georinex as gr
import numpy as np
import xarray
from mp_target import INTERSECTION

obs = gr.rinexobs('/home/bubble/Desktop/Programs/python/OBS-SAT/data/ABPO00MDG_R_20220421000_01H_30S_MO.crx', use='G')
nav = gr.rinexnav('/home/bubble/Desktop/Programs/python/OBS-SAT/data/ABPO00MDG_R_20220421000_01H_GN.rnx', use='G')

common_sv, common_time = INTERSECTION(obs, nav)

# fields to extract
__fields = [
    "SVclockBias",
    "SVclockDrift",
    "SVclockDriftRate",
    "IODE",
    "Crs",
    "DeltaN",
    "M0",
    "Cuc",
    "Eccentricity",
    "Cus",
    "sqrtA",
    "Toe",
    "Cic",
    "Omega0",
    "Cis",
    "Io",
    "Crc",
    "omega",
    "OmegaDot",
    "IDOT",
    "CodesL2",
    "GPSWeek",
    "L2Pflag",
    "SVacc",
    "health",
    "TGD",
    "IODC",
    "TransTime"
]


def CHECK_NAV(nav_data: xarray.Dataset, sv_list: list, epoch_time: np.datetime64) -> list:
    """Checks if the navigation file has filled parameters for the satellite"""
    filtered_list = []

    for _sv in sv_list:
        isEmpty = np.isnan(nav.sel(sv=_sv, time=epoch_time)[__fields[6]].item(0))
        if not isEmpty:
            filtered_list.append(_sv)
    if len(filtered_list) < 4:
        raise """Less than 4 satellite observed! Undetermined Solution: At least 4 required!!!"""

    return filtered_list


def NAVIGATION(nav: xarray.Dataset, sv: str, epoch: np.datetime64) -> dict:
    """Extracts Navigation Data
    ARGS: absolute path to rinex , Name of SV, Epoch time
    """

    try:
        __SV = nav.sel(sv=sv, time=epoch)
    except:
        raise f"Couldn't find the {sv} at that epoch! Please Recheck!"

    __extract = {}

    for attributes in __fields:
        __extract[attributes] = __SV[attributes].item(0)

    print(__extract)

    return __extract

if __name__ == '__main__':
    common_sv = CHECK_NAV(nav, common_sv, common_time)
    NAVIGATION(nav, common_sv[0], common_time)