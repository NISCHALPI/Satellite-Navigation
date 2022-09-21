import math

from georinex import *
from datetime import datetime




def listGPS(path: str) -> list:
    nav_data = rinexnav3(path, use="G")

    return list(nav_data.sv)
class NoSatelllite(Exception):
    def __init__(self, satellite: str):
        super().__init__("No satellite named " + satellite)


# these are orbital fields or parameters from rinex file
fields = [
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


# decorater for UTC time correction
def total_orbital_parameter(orbital_parameter):
    def total_parameter(*args):

        header_of_rinex = navheader3(args[0])

        header_of_rinex: dict

        orbital_dic = orbital_parameter(*args)

        if 'TIME SYSTEM CORR' in header_of_rinex.keys():
            orbital_dic['TIME SYSTEM CORR'] = header_of_rinex['TIME SYSTEM CORR']

        if 'LEAP SECONDS' in header_of_rinex.keys():
            orbital_dic['LEAP SECONDS'] = int(header_of_rinex['LEAP SECONDS'])

            return orbital_dic
        else:
            return orbital_dic

    return total_parameter


# Getting orbital parameters from RINEX file
@total_orbital_parameter
def get_orbital_parameters(pathtorinex: str, satellite: str) -> dict:
    # load RINEX in georinex to extrat orbital data
    nav = load(pathtorinex)

    if satellite not in nav.sv:
        raise NoSatelllite(satellite)

    time_dim = len(nav.time)

    orbital_dic = {}

    for attrs in fields:
        for i in range(0, time_dim):
            a = nav.sel(sv=satellite).get(attrs).item(i)

            if not math.isnan(a):
                orbital_dic[attrs] = a
                t = 0
                while t < 1:
                    orbital_dic['Toc'] = (to_datetime(nav.time[i])-datetime(1980, 1, 6, 0, 0, 0)).total_seconds()%604800
                    t = t + 1

    orbital_dic['sat'] = nav.sv



    return orbital_dic


if __name__ == "__main__":
    print(get_orbital_parameters('/home/nischal/Desktop/NAV/AMC400USA_R_20220911900_01H_GN.rnx', 'G01'))
