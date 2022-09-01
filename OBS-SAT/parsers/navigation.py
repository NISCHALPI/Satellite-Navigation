from datetime import datetime
import georinex as gr
import numpy as np
import xarray
from Orbit import Orbit
from pandas import Timestamp




# DATE TIME CALCULATOR
def to_datetime(time: np.datetime64) -> datetime:
    """Converts np.datetime64 to datetime.datetime"""
    return Timestamp(time).to_pydatetime()


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


################################################HELPER FUNCTION#########################################################
def NAVIGATION(nav: xarray.Dataset, sv: str, epoch: np.datetime64) -> tuple:
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


    __extract['Toc'] = ( to_datetime(epoch) - datetime(1980, 1, 6, 0, 0, 0))\
                           .total_seconds()%604800


    __orbit = Orbit(__extract)

    data = __orbit.getall()

    return np.array(data['position']), data['SV_CLOCK_ERROR']



#################################################END###################################################################
