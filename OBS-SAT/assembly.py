### THE MAIN ASSEMBLY SCRIPT


# IMPORTS
from parsers.superparser import parse
from calculations.linear_model_calculation import linear_model


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


    # work on linear model
    print("\n-------------------------------------------STARTING-THREADED-LINEAR "
          "MODEL------------------------------------------\n")
    linear_model(sat_data)

    pass


if __name__ == "__main__":
    main()
    
    
