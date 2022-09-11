import sys

sys.path.append('../')


from transformation.transformations import transformation_earth_rotation
from corrections.pseudorange_filtration_code import Ionospheric_Dual_Channel

# Constants
c = 299792458


def preprocessing(sv) -> None:
    """Threaded preprocessing
    :arguments -> Satellite object
    :return -> None"""

    print(f"Preprocessing {sv.name} satellite's data!")

    # Ionospheric Corrections
    if sv.dual:
        sv.C1C = Ionospheric_Dual_Channel(sv.C1C, sv.C2C)
        print(f"Ionnospheric Corrections Appllied for  {sv.name}")

    delattr(sv, "C2C")

    # Add sat clock error | this is not the reciver clock error!!
    sv.C1C = sv.C1C + c *  sv.bias

    # Earth rotation transformation
    print(f"Earth rotation transformation applied for {sv.name}")
    sv.position = transformation_earth_rotation(sv.position, sv.C1C)

    print("\n")
    sv.t_apply = True

