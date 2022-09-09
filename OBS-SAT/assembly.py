### THE MAIN ASSEMBLY SCRIPT


# IMPORTS

from parsers.superparser import parse
from transformation.transformations import transformation_earth_rotation
from corrections.pseudorange_filtration_code import Ionospheric_Dual_Channel
from calculations.linear_model_calculation import linear_model
from calculations.threads.Fthread import Fthread


def main():
    # Automatically extract data
    # Note: RINEX FILES SHOULD BE IN <data> directory to process
    sat_data = parse()



    # These preprocessing should be threaded

    # Get Ionospheric-Free correction
    if sat_data[0].dual:
        for __sv in sat_data:
            __sv.C1C = Ionospheric_Dual_Channel(__sv.C1C, __sv.C2C)

    # Apply earth rotation transformation to the data

    # apply transformation



    pass


if __name__ == "__main__":
    main()
