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
sys.path.append('../parsers')
from threaded.threads.Fthread import Fthread
from parsers.mp_target import Satellite

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
    first_three =  (parameter[0:-1] - position) / calculate_pseudorange(position , parameter)

    # return whole row for a given satellite and provisional parameter
    return np.append(first_three , c)



def getParameters(__GPS_VISIBLE: list, provisional_parameter: np.array) -> tuple:
    """
    ARGS: __GPS_SATELLITE class list
    provisional_parameters: provisional parameter

    """
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
        ,np.array(list(map(lambda obj: obj.get, threads_for_design))).reshape(-1,4)




def linear_model(__GPS_VISIBLE: list) -> tuple:
    """Args: Preprocessed Satellite Class
       Output: Reciver Clock Bias and Position of Observer (ECFC Coordinats)"""

    # Accuracy of linear model
    epsilon = 0.001

    # INITIAL CLOCK BIAS
    dtau = 0


    # INITIAL ASSUMED STATE VECTOR
    # Provisional State Vector : shape -> 1 * 4
    initial_points = np.array([0,0,0,dtau], dtype=np.float64)



    # initial pseudorange matrix : dims = m(no of sv) * 1
    # Not yet adjusted with provisional parameters
    # -1 is an infering for no of rows based on size since I know what colum should be (only 1)


    count = 0

    while True:

        delP, designMatrix = getParameters(__GPS_VISIBLE, initial_points)

        # Transpose of design matrix
        designTranspose = designMatrix.transpose()


        # Least square solutions
        sol = np.dot(np.dot(np.linalg.inv(np.dot(designTranspose , designMatrix)) , designTranspose) , delP)



        sol = sol.flatten()



        print(sol)
        initial_points += sol

        if np.linalg.norm(sol) < epsilon:
            break






    return initial_points[-1], initial_points[0:-1]




if __name__ == "__main__":
        list1 = [[17721011.353369, 8651393.403376 , 18066668.984492]]
        list1.append([-7764276.013113 , 24815558.193781, 3355306.117463])
        list1.append([7801883.623771, 19574982.369322, 16200329.385216])
        list1.append([17252169.032178, 19650114.003115, -4997938.841081])
        list1.append([-8926199.493994,11886677.791223, 21992642.490734])
        list1.append([-20869939.195044, 12986675.436728 , 10317360.241586])





