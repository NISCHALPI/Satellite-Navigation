### THE MAIN ASSEMBLY SCRIPT


# IMPORTS
from calculations.threads.Fthread import Fthread
from parsers.superparser import parse
from transformation.transformations import transformation_earth_rotation
from corrections.pseudorange_filtration_code import Ionospheric_Dual_Channel
from calculations.linear_model_calculation import linear_model
from calculations.threads.Fthread import Fthread




def threaded_preprocessing(sv) -> None:
    """Threaded preprocessing
    :arguments -> Satellite object
    :return -> None"""

    # Ionospheric Corrections
    if sv.dual:
        sv.C1C = Ionospheric_Dual_Channel(sv.C1C, sv.C2C)

    # Earth rotation transformation

    sv.C1C = transformation_earth_rotation(sv.position, sv.C1C)

    sv.t_apply = True





def main() -> None:
    # Automatically extract data
    # Note: RINEX FILES SHOULD BE IN <data> directory to process
    sat_data = parse()



    threads = [Fthread(threaded_preprocessing, (sv,)) for sv in sat_data ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    del thread

    for __sv in sat_data:
        for attr in __sv.__dict__:
            print(f"{attr} -> {getattr(__sv, attr)}")
        print("\n")



    pass


if __name__ == "__main__":
    main()
