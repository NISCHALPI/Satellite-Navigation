import numpy as np
import random as rand


def get_testdata() -> list:
    ## RECEIVER POS IN EARTH
    recv_pos = np.array([4097216.55, 4292119.18, -2065771.1988])

    ###SAT HYPOTHETICAL LOCATION

    # ALTITUDE OF SV
    r = (20200 + 6365) * 1000

    sat_loc = []

    for i in range(4):
        # Random Coordinates
        theta = rand.uniform(0, np.pi)
        phi = rand.uniform(0, 2 * np.pi)

        # Coords
        x = r * np.sin(theta) * np.cos(phi)
        y = r * np.sin(theta) * np.sin(phi)
        z = r * np.cos(theta)

        coordinates = np.array([x, y, z])

        pseudorange = np.linalg.norm(coordinates - recv_pos)

        sat_loc.append((coordinates , pseudorange))

    return sat_loc
