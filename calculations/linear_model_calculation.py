# ACTUAL CALCULATION OF POSITION HAPPENS HERE!!
# MADE BY NISCHAL BHATTARAI

# Sources Used:
# http://www.nbmg.unr.edu/staff/pdfs/Blewitt%20Basics%20of%20gps.pdf
# https://www.youtube.com/watch?v=X8uIMepR2uw&list=PLGvhNIiu1ubyEOJga50LJMzVXtbUq6CPo&index=12
# https://gps.alaska.edu/jeff/Classes/GEOS655/Lecture02_GPS_part1_pseudorange.pdf


# IMPORTS
import numpy as np
import sys



# Constants
c = 299792458

# TOLERANCE
epsilon = 0.00001


def __calcualtePseudorange(satelliteCoords, provisionalParam):
    return np.linalg.norm(satelliteCoords - np.array(provisionalParam[0:3])) + c * provisionalParam[3]


def __calculateB(gps: list, provisional_parameter: np.array) -> np.array:
    """

    :param gps: GPS satellite list
    :param provisional_parameter: Provisional Parameters as numPy array
    :return: the b matrix , P - Pcalc in Taylor Series
    """
    # Initialize
    b = []

    # Fills b with (P - Pcomputed)
    for sat in gps:
        b.append(sat.C1C - __calcualtePseudorange(sat.position, provisional_parameter))

    # Converts to  a column vector
    b = np.array(b).reshape(-1, 1)

    ## Assert the shape
    assert b.shape == (len(gps), 1)

    return b


def __calculateDesign(gps: list, provisional_parameter: np.array) -> np.array:

    """

    :param gps: GPS satellite list
    :param provisional_parameter: Provisional Parameters as numPy array
    :return: The design matrix
    """


    # Initialize Design Matrix
    A = []

    for sat in gps:
        threeColumn = (provisional_parameter[0:3] - sat.position) / __calcualtePseudorange(sat.position,
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


def linear_model(__GPS_SATELLITE: list) -> tuple:

    """
    :param __GPS_SATELLITE: Gps satellite list( Satellite )
    :return: dt (time offset of receiver ) , coordinates( coordinates of receiver )
    """

    # Initial Provisional parameter
    provisionalParameter = np.array([0, 0, 0, 0])

    # While Loop Iteration
    while True:
        # Calculate b given provisional parameter
        b = __calculateB(__GPS_SATELLITE, provisionalParameter)



        # Calculate design matrix given
        A = __calculateDesign(__GPS_SATELLITE, provisionalParameter)



        # calculate (ATA)-1
        pseudoInv = np.linalg.inv(np.dot(np.transpose(A), A))



        # calculate ATb
        ATB = np.dot(np.transpose(A), b)



        tempCorrection = np.dot(pseudoInv, ATB).flatten()


        # The Break Condition
        if np.linalg.norm(tempCorrection) < epsilon:
            provisionalParameter = provisionalParameter + tempCorrection
            break

        # The Update Condition
        provisionalParameter = provisionalParameter + tempCorrection


    return provisionalParameter[3] , provisionalParameter[0:3]
