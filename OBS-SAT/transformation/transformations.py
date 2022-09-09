import numpy as np
from time import time


# This script contains all the transformations required to process the RINEX nav and obs file

# CONSTANTS


def transformation_earth_rotation(initial_coordinates: np.array, pseudo_range: np.float32 or float) -> np.array:
    """ This transformation is related due to the rotation of earth-when user receivers the initial satellite
    location is rotated due to earth rotation. To bring everything into ECFC following transformation has
    to be applied --- Accepts 1*3 np.array --- Returns Transformed 1*3 np. Array"""

    omegaE = 7.292115 * 10 ** (-5)  # Earth rotation rate
    c = 299792458  # Precise speed of light

    initial_coordinates = np.array(initial_coordinates).astype(np.float32).reshape((3, 1))

    avg_angular_motion = omegaE * (pseudo_range / c)

    transformation_matrix = np.array([[np.cos(avg_angular_motion), np.sin(avg_angular_motion), 0],
                                      [-np.sin(avg_angular_motion), np.cos(avg_angular_motion), 0],
                                      [0, 0, 1]]).astype(np.float32)

    return np.dot(transformation_matrix, initial_coordinates).reshape((1, 3))
