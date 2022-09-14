# This module does fast conversion between ECFC-coordinate to Ellipsoidal Coordinate

# Modules needed
import numpy as np

# CONSTANTS
# WGS 84 - Ellipsoidal parameters in meters - See docs on : https://en.wikipedia.org/wiki/Earth_ellipsoid

CONST_EQUATORS = 6378137
CONST_POLES = 6356752.3142


# Class for a Reference Planet
class Planet(object):
    """This is a class for a reference Planet. It takes eccentricity and semi-major axis as init
    parameter.

    Use the class method to convert [a,b] - > [ecc, a], access method by Planet.elliptical_parameter(*args)
    -> np.array.

    Use Ellipsoidal to Cartesian(ETC) and Cartesian to Ellipsoidal(CTE) methods of
    this class.

    Calculations and Return types are in Radians by default. Pass rads= False to do calculations in
    degree and return types in degrees"""

    @classmethod
    def elliptical_parameter(cls, a: np.float32, b: np.float32) -> np.array:
        """ args : semi-major, semi-minor
            out : np.array(eccentricity, semi-major)"""

        ecc = np.sqrt((1 - (b ** 2 / a ** 2)))

        return np.array([ecc, a], dtype=np.float32)

    def __init__(self, ecc: np.float32, a: np.float32, **kwargs) -> None:
        """Initialization of Reference coordinate system. Needed to define an ellipsoidal coordinate system."""
        self.e = ecc
        self.a = a
        try:
            self.rads = kwargs["rads"]
        except:
            self.rads = True

    def __N(self, lat: np.float32) -> np.float32:
        """Calculation of N"""
        den = np.sqrt(1 - (np.power(self.e, 2) * np.power(np.sin(lat), 2)))

        return np.float32(self.a / den)

    # Conversion between Ellipsoid to Cartesian ECFC
    def ETC(self, lat: np.float32, long: np.float32, h: np.float32) -> np.array:
        """Conversion between Ellipsoidal  to Cartesian ECFC coordinates"""
        if not self.rads:
            lat = np.deg2rad(lat)
            long = np.deg2rad(long)

        n = self.__N(lat)

        # calculations
        x = (n + h) * np.cos(lat) * np.cos(long)
        y = (n + h) * np.cos(lat) * np.sin(long)
        z = (n * (1 - np.power(self.e, 2)) + h) * np.sin(lat)

        return np.array([x, y, z], dtype=np.float32)

    # Iteration Eq1
    def __iter1(self, p: np.float32, lat: np.float32) -> np.float32:
        return np.float32(p / np.cos(lat)) - self.__N(lat)

    # Iteration Eq2
    def __iter2(self, p: np.float32, z: np.float32, h: np.float32, lat: np.float32) -> np.float32:
        n = self.__N(lat)
        calc = 1 / (1 - (self.e ** 2 * (n / (n + h))))

        return np.arctan((z / p) * calc)

        # Conversion between Cartesian to Ellipsoidal

    def CTE(self, x: np.float32, y: np.float32, z: np.float32) -> np.array:
        # calculation of longitude is straight forward
        long = np.arctan(y / x)

        # Definition of p is
        p = np.sqrt(x ** 2 + y ** 2)

        # Initial Latitude
        lat = np.float32(0)

        # Iterative Algorithm
        while True:
            temp = lat
            h = self.__iter1(p, lat)
            lat = self.__iter2(p, z, h, lat)

            if np.abs(lat - temp) < 1e-3:
                break

        if not self.rads:
            return np.array([np.rad2deg(lat), np.rad2deg(long), h], dtype=np.float32)

        return np.array([lat, long, h], dtype=np.float32)


class Earth(Planet):
    """It is a basically a planet class initialized with WGS 84 parameters-- See <class Planet> docs for
     more info!"""

    def __init__(self, **kwargs):
        # WGS-84 EARTH ELLIPTICAL PARAMETERS in meter
        args = super().elliptical_parameter(np.float32(CONST_EQUATORS), np.float32(CONST_POLES))

        super().__init__(*args, **kwargs)


x = Earth(rads=False)


# Test vector: https://www.oc.nps.edu/oc2902w/coord/llhxyz.htm
if __name__ == "__main__":

    coords = np.array([12, 11, 229584], dtype=np.float32)

    print(x.CTE(*coords))
