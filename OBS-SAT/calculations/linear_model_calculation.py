# ACTUAL CALCULATION OF POSITION HAPPENS HERE!!
# MADE BY NISCHAL BHATTARAI

# Sources Used:
# http://www.nbmg.unr.edu/staff/pdfs/Blewitt%20Basics%20of%20gps.pdf

#IMPORTS
import numpy as np
import sys
sys.path.append('../')
from threaded.threads.Fthread import Fthread

# Constants
c = 299792458







def linear_model(__GPS_VISIBLE: list) -> tuple:
    """Args: Preprocessed Satellite Class
       Output: Reciver Clock Bias and Position of Observer (ECFC Coordinats)"""



    # INITIAL ASSUMED POSITION
    initial_points = np.array([0,0,0]).reshape(1,3)

    # INITIAL CLOCK BIAS
    dt = 0


