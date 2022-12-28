# Made by Nischal Bhattarai  Contact-Info= nbhattarai@crimson.ua.edu

# Objective : To create a custom class to calculate Orbital Parameters after parsing RINEX file


# Imports
import math

from math import *

from datetime import datetime, timedelta

# constants required (WGS-84)
GM = 3.986005 * 10 ** 14  # units-- m**3/s**2 :: product of gravitational constant G and the mass of the Earth M

omegaE = 7.292115 * 10 ** (-5)  # units-- rad/s :: value of the Earth’s rotation rate

F_relv = -4.442807633 * 10 ** (-10)

#################################################################FUNCTION DEFINITION####################################

# relativistic correction model refer to ICD -GPS
def rel_corr(ecc, ek, sqrtA):
    return F_relv * pow(ecc, sqrtA) * sin(ek)


# Check Week anamoly
def weekanamoly(t1, t2):
    a = t1 - t2
    if a < -302400:
        return 604800 + a
    elif a > 302400:
        return a - 604800
    else:
        return a



#############################################################CALSS DEFINITION ##########################################

#   Error Class
class NoUTC(Exception):
    def __init__(self):
        super().__init__("No UTC correction data given in the RINEX file. Please try another one")


# Orbit and Satellite Position Class
class Orbit(object):

    def __init__(self, kwargs: dict):  # Initilazation of data
        self.Toe = kwargs["Toe"]
        self.Toc = kwargs["Toc"]
        self.a0 = kwargs["SVclockBias"]
        self.a1 = kwargs["SVclockDrift"]
        self.a2 = kwargs["SVclockDriftRate"]
        self.sqrtA = kwargs["sqrtA"]
        self.ecc = kwargs["Eccentricity"]
        self.i0 = kwargs["Io"]
        self.omega0 = kwargs["Omega0"]
        self.omega = kwargs["omega"]
        self.M0 = kwargs["M0"]
        self.del_n = kwargs["DeltaN"]
        self.omegadot = kwargs["OmegaDot"]
        self.i_dot = kwargs["IDOT"]
        self.C_us = kwargs["Cus"]
        self.C_uc = kwargs["Cuc"]
        self.C_is = kwargs["Cis"]
        self.C_ic = kwargs["Cic"]
        self.C_rs = kwargs["Crs"]
        self.C_rc = kwargs["Crc"]
        self.TransTime = kwargs['TransTime']
        self.health = kwargs['health']
        self.gpsweek = kwargs['GPSWeek']
        self.TGD = kwargs['TGD']
        try:

            self.A0 = kwargs['TIME SYSTEM CORR']['GPUT'][0]
            self.A1 = kwargs['TIME SYSTEM CORR']['GPUT'][1]
            self.ref_UTC = kwargs['TIME SYSTEM CORR']['GPUT'][2]
            self.UTC_WN = kwargs['TIME SYSTEM CORR']['GPUT'][3]
            self.leap_seconds = kwargs['LEAP SECONDS']
            self.UTC_CORR = True
        except:
            self.UTC_CORR = False

    def getall(self):

        # Refer to ICD for Formula---

        A = self.sqrtA ** 2

        n0 = sqrt(GM / A ** 3)

        n = n0 + self.del_n

        e = self.ecc

        # Te is time of clock
        tE = self.Toc

        tk = weekanamoly(tE, self.Toe)
        # Correct

        mk = self.M0 + n * tk

        mkdot = n

        ek = mk
        for i in range(0, 10):
            ek = mk + e * sin(ek)

        ekdot = mkdot / (1.0 - e * cos(ek))

        tak = atan2(sqrt(1.0 - e ** 2) * sin(ek), cos(ek) - e)

        tankdot = sin(ek) * ekdot * (1.0 + e * cos(tak)) / (sin(tak) * (1.0 - e * cos(ek)))

        phik = tak + self.omega

        corr_u = self.C_us * sin(2.0 * phik) + self.C_uc * cos(2 * phik)
        corr_r = self.C_rs * sin(2 * phik) + self.C_rc * cos(2 * phik)
        corr_i = self.C_is * sin(2 * phik) + self.C_ic * cos(2 * phik)

        uk = phik + corr_u

        rk = A * (1 - e * cos(ek)) + corr_r

        ik = self.i0 + tk * self.i_dot + corr_i

        # position in orbital plane
        xprimek = rk * cos(uk)
        yprimek = rk * sin(uk)

        omegak = self.omega0 + (self.omegadot - omegaE) * tk - omegaE * self.Toe

        # ECFC coordinates
        x = xprimek * cos(omegak) - (yprimek * sin(omegak) * cos(ik))
        y = xprimek * sin(omegak) + (yprimek * cos(omegak) * cos(ik))
        z = yprimek * sin(ik)

        orbital_element = {'position': [x, y, z]}

        # SV- GPST time correction

        b = weekanamoly(tE, self.Toc)

        dt = (self.a0 + self.a1 * b + self.a2 * b ** 2 + rel_corr(e, ek, self.sqrtA))

        tE = tE - dt + self.TGD

        # Needed for observationl stuff
        orbital_element["SV_CLOCK_ERROR"] = dt
        
        # Animation Parameters
        orbital_element['eccentricity'] = e
        orbital_element['semimajor'] = A
        orbital_element['inclination'] = ik
        orbital_element['acending_node'] = omegak
        orbital_element['periapsis'] = self.omega
        orbital_element['true_anamoly'] = tak
        orbital_element["time_period"] = (2 * math.pi) / n


        # GPST- UTC calculations
        if self.UTC_CORR:
            del_UTC = -1 * self.leap_seconds + self.A0 + self.A1 * (
                    tE - self.ref_UTC + 604800 * (self.gpsweek - self.UTC_WN))  # error term

            del_UTC = tE - del_UTC  # actual gps seconds wrt UTC corrected

            sync_date = datetime(1980, 1, 6, 0, 0, 0)

            del_UTC = timedelta(seconds=del_UTC + 604800 * self.gpsweek)

            UTC_date = sync_date + del_UTC

            orbital_element['UTC'] = UTC_date


        return orbital_element










