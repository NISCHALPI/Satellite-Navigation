### THE MAIN ASSEMBLY SCRIPT


# IMPORTS
from parsers.superparser import parse
from calculations.linear_model_calculation import linear_model
from transformation.lat_log import Earth
import numpy as np


# Print SV function
def DISPLAY(sv_list: list, name: str = None) -> None:
    """Displays Satellite Info:
    Args: SV_LIST<list> ,  optional = SV_NAME<string>
    OUT: prints satellite info

    if name is not given, prints all satellite info!
    """

    if name is None:
        for __sv in sv_list:
            for attr in __sv.__dict__:
                print(f"{attr} -> {getattr(__sv, attr)}")
            print("\n")
    else:
        # Which satellite
        atIndex = None

        foundSv = True

        for index, sat in enumerate(sv_list):
            if sat.name == name:
                atIndex = index
                break

            foundSv = False

        if foundSv:
            for attr in sv_list[atIndex].__dict__:
                print(f"{attr} -> {getattr(sv_list[atIndex], attr)}")
            print("\n")

        else:
            print(f"SV named {name} not found!")


def main() -> None:
    # Automatically extract data
    # Note: RINEX FILES SHOULD BE IN <data> directory to process
    sat_data = parse()

    print("------------------------------------PARSING COMPLETE------------------------------------------\n")

    print("-------------------------------------------SV-DATA-VIEW------------------------------------------\n")

    DISPLAY(sat_data)

    print("-------------------------------------------END-OF-SV-DATA------------------------------------------\n")

    print("\n-------------------------------------------STARTING-LINEAR- MODEL "
          "MODEL------------------------------------------\n")


    # receiverTime , position into the linear model
    dt, position = linear_model(sat_data)


    # Printing the ECFC-COORDINATES
    print(f"The ECFC coordinates of receiver: ")
    print(f"X-coord = {position[0]} m")
    print(f"Y-coord = {position[1]} m")
    print(f"X-coord = {position[2]} m")

    # Convert it into lat_long
    print("\n-------------------------------------------LINEAR-MODEL-COMPLETED-SUCCESSFULLY"
          "---------------------------\n")

    print("\n-------------------------------------------CONVERTING-WGS-84-ELLIPSOIDAL COORDINATE"
          "---------------------------\n")

    #initialize earth coordinate system
    # initialize radians=False to get everything in degree
    earth = Earth(rads=False)

    # Extract ellipsoidal coordinates
    ellipsoidalCords = earth.CTE(*position)

    print(f"The Ellipsoidal coordinates of receiver: ")
    print(f"Latitude= {ellipsoidalCords[0]} degree")
    print(f"Longitude = {ellipsoidalCords[1]} degree")
    print(f"Height = {ellipsoidalCords[2]} m")

    print("\n--------------------------------------------ANALYSIS-COMPLETED-------------------------\n")


if __name__ == "__main__":
    main()
