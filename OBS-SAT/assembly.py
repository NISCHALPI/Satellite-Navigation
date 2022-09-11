### THE MAIN ASSEMBLY SCRIPT


# IMPORTS
from parsers.superparser import parse
from threaded.threads.Fthread import Fthread
from calculations.linear_model_calculation import linear_model






def main() -> None:
    # Automatically extract data
    # Note: RINEX FILES SHOULD BE IN <data> directory to process
    sat_data = parse()


    for __sv in sat_data:
        for attr in __sv.__dict__:
             print(f"{attr} -> {getattr(__sv, attr)}")
        print("\n")

    # work on linear model

    linear_model(sat_data)


    pass


if __name__ == "__main__":
    main()
