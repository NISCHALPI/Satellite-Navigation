# ACTUAL CALCULATION OF POSITION HAPPENS HERE!!
# MADE BY NISCHAL BHATTARAI

# Sources Used:
# http://www.nbmg.unr.edu/staff/pdfs/Blewitt%20Basics%20of%20gps.pdf

import numpy as np
from threads.Fthread import Fthread

# Constants
c = 299792458


# Create Thread Pool


def __calculate_pseudorange(point: np.array, ref_sat: np.array, clock: np.float32) -> np.float32:
    """"Calculates Pseudorange"""
    return np.linalg.norm(point - ref_sat) + c * clock


def __calculation_matrices(satellite_position: np.array,
                           pseudorange: np.array, points: np.array, dt: np.float32) -> np.array:
    """Calculates the Design Matrix and Residual Observations"""
    num_satellites = pseudorange.size

    threads = [Fthread(func=__calculate_pseudorange, args=(points, sat, dt)) for sat in satellite_position]

    for trd in threads:
        trd.start()
    for trd in threads:
        trd.join()

    _calc_array = [trd.get for trd in threads]

    del threads

    # diff between actual ones and calculated ones
    _b = pseudorange - _calc_array

    # The design matrix calculation

    _A = np.array([np.append(((points - satellite_position[i]) / _calc_array[i]), c)
                   for i in range(num_satellites)])

    return _b.transpose(), _A


def linear_model(*args, **kwargs) -> tuple:
    """Args: Filtered Pseudo-Ranges and Satellite Positions after rotated For ECFC coord
       Output: Position of Observer"""

    _GPS_VISIBLE = kwargs["satellite"]

    initial_points = kwargs["initial_position"]

    dt = 0

    # Initial data we have ::

    # SAT position -- least 4
    # Matrix dim -> n * 4
    sat_pos = np.array([sat.position for sat in _GPS_VISIBLE]).astype(np.float32)

    # pseudo_range for each satellite
    # Matrix dim ->  1 * n
    sat_range = np.array([sat.range for sat in _GPS_VISIBLE]).astype(np.float32)

    while True:
        b, A = __calculation_matrices(sat_pos, sat_range, initial_points, dt)

        correction = np.dot(np.linalg.inv(np.dot(A.transpose(), A)), np.dot(A.transpose(), b)).transpose()

        if np.linalg.norm(correction[:3]) < 0.01:
            break

        dt = correction[-1]

        initial_points += correction[:4]

    return initial_points, dt
