# ACTUAL CALCULATION OF POSITION HAPPENS HERE!!
# MADE BY NISCHAL BHATTARAI

# Sources Used:
# http://www.nbmg.unr.edu/staff/pdfs/Blewitt%20Basics%20of%20gps.pdf
# https://www.youtube.com/watch?v=X8uIMepR2uw&list=PLGvhNIiu1ubyEOJga50LJMzVXtbUq6CPo&index=12
# https://gps.alaska.edu/jeff/Classes/GEOS655/Lecture02_GPS_part1_pseudorange.pdf


# IMPORTS
import numpy as np
import sys

sys.path.append('../')
sys.path.append('../parsers')
from threaded.threads.Fthread import Fthread
from parsers.mp_target import Satellite

# Constants
c = 299792458

# TOLERANCE
epsilon = 0.001


def calcualtePseudorange(satelliteCoords, provisionalParam):
    return np.linalg.norm(satelliteCoords - np.array(provisionalParam[0:3])) + c * provisionalParam[3]


def calculateB(gps: list, provisional_parameter: np.array) -> np.array:
    # Initialize
    b = []

    # Fills b with (P - Pcomputed)
    for sat in gps:
        b.append(sat.C1C - calcualtePseudorange(sat.position, provisional_parameter))

    # Converts to  a column vector
    b = np.array(b).reshape(-1, 1)

    ## Assert the shape
    assert b.shape == (len(gps), 1)

    return b


def calculateDesign(gps: list, provisional_parameter: np.array) -> np.array:
    # Initialize Design Matrix
    A = []

    for sat in gps:
        threeColumn = (provisional_parameter[0:3] - sat.position) / calcualtePseudorange(sat.position,
                                                                                         provisional_parameter)
        threeColumn = np.append(threeColumn, c)

        A.append(threeColumn)

    ## NUMPY ARRAY CONVERSION
    A = np.array(A)
    A = A.reshape(-1, 4)

    ## ASSERT
    assert A.shape == (len(gps), 4)

    ## RETURN
    return A


def linear_model(__GPS_SATELLITE: Satellite):
    # Initial Provisional parameter
    provisionalParameter = np.array([0, 0, 0, 0])

    while True:
        # Calculate b given provisional parameter
        b = calculateB(__GPS_SATELLITE, provisionalParameter)


        # Calculate design matrix given
        A = calculateDesign(__GPS_SATELLITE, provisionalParameter)



        # calculate (ATA)-1
        pseudoInv = np.linalg.inv(np.dot(np.transpose(A), A))



        # calculate ATb
        ATB = np.dot(np.transpose(A), b)



        tempCorrection = np.dot(pseudoInv, ATB).flatten()



        if np.linalg.norm(tempCorrection) < epsilon:
            provisionalParameter = provisionalParameter + tempCorrection
            break

        provisionalParameter = provisionalParameter + tempCorrection

        print(provisionalParameter)
