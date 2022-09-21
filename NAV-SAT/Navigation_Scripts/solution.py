from Orbit import absorb, write_orbit
from parse_rinex import NoSatelllite, get_orbital_parameters, listGPS
import os


# checks valid path

def ask_path() -> str:
    global path_to_rinex
    while True:
        try:
            path_to_rinex = input("Enter the absolute path to RINEX file: ")

            if path_to_rinex.lower() == "quit":
                print(f"User Termination! Returned with exit code -1\n")
                exit(-1)
                break

            temp = open(path_to_rinex, 'r')
            temp.close()
            break
        except:
            print('\nInvalid Path! Please try again!')

            continue

    return path_to_rinex


# checks valid sat
def ask_satellite(path_to_rinex: str) -> str:

    global satellite_number

    GPS = listGPS(path_to_rinex)
    print("\nVISIBLE SATELLITE")

    print("----------------------------------------------")
    for gps in GPS:
        print(f"{gps} is available for tracking")

    while True:
        try:

            satellite_number = input("\nEnter the satellite number to track: ")
            data = get_orbital_parameters(path_to_rinex, satellite_number)
            break
        except NoSatelllite:
            print(f'No satellite named {satellite_number} in the given RINEX file.')
            continue

    return satellite_number


if __name__ == '__main__':
    path_to_rinex = ask_path()

    satellite_number = ask_satellite(path_to_rinex)

    # gets ephemeris data
    true_data = absorb(path_to_rinex, satellite_number)

    # writes the data to a file
    write_orbit(true_data, satellite_number)

    cwd = os.getcwd()

    print(f'\nSolution is written to a {satellite_number + "_solution.txt"} in {cwd}')
