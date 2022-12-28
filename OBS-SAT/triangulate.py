#!/usr/bin/env python 

#click import 
import click 

# module imports # IMPORTS
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



COMPUTE = {'thread' : True, "process" : False}

@click.command(no_args_is_help=True)
@click.option("-n", "--nav", "path_to_nav", type= click.Path(exists= True, readable= True, resolve_path= True) , help ="Path to RINEX navigation file")
@click.option("-o", "--obs", "path_to_obs", type= click.Path(exists= True, readable= True, resolve_path=True) , help ="Path to RINEX observational file")
@click.option("-c", "--compute", "compute", type = click.Choice(COMPUTE.keys()), help = " Choose a compute mode", default="thread", required= False)
@click.option("-a", "--auto", "auto", is_flag=True, help = "Read data automatically from ./data/ directry")
@click.option("-q", "--quite", "quite", is_flag=True, help = "Only prints reciever coordinate to stdout")
def main(path_to_obs: str =None, path_to_nav: str = None, compute: str = None, auto: bool = None, quite: bool=None) -> None :
    """ Triangulate GPS reciever coordinate using RINEX files! """


    # Parse and read 
    sat_data  = parse(COMPUTE[compute], path_to_obs , path_to_nav, quite)

    # Quite setting 
    if not quite:
        print("------------------------------------PARSING COMPLETE------------------------------------------\n")

        print("-------------------------------------------SV-DATA-VIEW------------------------------------------\n")

        DISPLAY(sat_data)

        print("-------------------------------------------END-OF-SV-DATA------------------------------------------\n")

        print("\n-------------------------------------------STARTING-LINEAR- MODEL "
            "MODEL------------------------------------------\n")

    # receiverTime , position into the linear model
    dt, position = linear_model(sat_data)

    
    if not quite:
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

    if not quite: 
        print(f"The Ellipsoidal coordinates of receiver: ")
        print(f"Latitude= {ellipsoidalCords[0]} degree")
        print(f"Longitude = {ellipsoidalCords[1]} degree")
        print(f"Height = {ellipsoidalCords[2]} m")
        print("\n--------------------------------------------ANALYSIS-COMPLETED-------------------------\n")

    else:
        print(*ellipsoidalCords)
    
   
        







if __name__ == "__main__":
    main()
