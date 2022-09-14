# ACTUAL CALCULATION OF POSITION HAPPENS HERE!!
# MADE BY NISCHAL BHATTARAI

# Sources Used:
# http://www.nbmg.unr.edu/staff/pdfs/Blewitt%20Basics%20of%20gps.pdf
# https://www.youtube.com/watch?v=X8uIMepR2uw&list=PLGvhNIiu1ubyEOJga50LJMzVXtbUq6CPo&index=12
# https://gps.alaska.edu/jeff/Classes/GEOS655/Lecture02_GPS_part1_pseudorange.pdf


#IMPORTS
import numpy as np
import sys
sys.path.append('../')
from threaded.threads.Fthread import Fthread

# Constants
c = 299792458

def calculate_pseudorange(position: np.array, parameter: np.array) -> np.float32:
    """Returns computed pseudorange given provisional parameters"""
    return np.linalg.norm(position - parameter[0:-1]) + c * parameter[-1]


def calculate_design(position: np.array, parameter: np.array, pseudorange):
    """Returns row of design matrix  for each satellite given position, provisional paramm"""

    # Set dt = 0 since it doesn't affect design matrix
    parameter[-1] = 0

    # calculate first three element of the row
    first_three =  (parameter[0:-1] - position ) / calculate_pseudorange(position , parameter)

    # return whole row for a given satellite and provisional parameter
    return np.append(first_three , c)



def getParameters(__GPS_VISIBLE: list, provisional_parameter: np.array) -> tuple:

    threads_for_p = []

    threads_for_design = []


    for sv in __GPS_VISIBLE:
        threads_for_p.append(Fthread(calculate_pseudorange, args=(sv.position, provisional_parameter)))
        threads_for_design.append(Fthread(calculate_design, args=(sv.position, provisional_parameter, sv.C1C)))

    for thread in threads_for_p:
        thread.start()

    for thread in threads_for_design:
        thread.start()


    for thread in threads_for_p:
        thread.join()

    for thread in threads_for_design:
        thread.join()

    return np.array(list(map(lambda obj: obj.get, threads_for_p))).reshape(-1,1) \
        ,np.array(list(map(lambda obj: obj.get, threads_for_design)))




def linear_model(__GPS_VISIBLE: list) -> tuple:
    """Args: Preprocessed Satellite Class
       Output: Reciver Clock Bias and Position of Observer (ECFC Coordinats)"""

    # Accuracy of linear model

    # INITIAL CLOCK BIAS
    dtau = 0


    # INITIAL ASSUMED STATE VECTOR
    # Provisional State Vector : shape -> 1 * 4
    initial_points = np.array([0,0,0,dtau])



    # initial pseudorange matrix : dims = m(no of sv) * 1
    # Not yet adjusted with provisional parameters
    # -1 is an infering for no of rows based on size since I know what colum should be (only 1)
    delP, designMatrix = getParameters(__GPS_VISIBLE, initial_points)


    designTranspose = designMatrix.transpose()



    sol = np.matmul(np.linalg.inv(np.matmul(designTranspose, designMatrix)), np.matmul(designTranspose , delP))

    print(sol)









