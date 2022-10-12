### THE MAIN ASSEMBLY SCRIPT


# IMPORTS
from parsers.superparser import parse
from calculations.linear_model_calculation import linear_model
from transformation.lat_log import Earth
from test_data import get_testdata


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

    sat_data = sat_data[0:4]

    test_data = get_testdata()

    index = 0

    for loc, pseudo in test_data:
        sat_data[index].C1C = pseudo
        sat_data[index].position = loc
        sat_data[index].bias = 0
        index += 1

    ## dt, position = linear_model(sat_data)
    linear_model(sat_data)


if __name__ == "__main__":
    main()
