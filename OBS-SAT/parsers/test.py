import georinex as gr
import xarray

from superparser import INTERSECTION, Satellite

__data = ["C1C", "C2C", "C1L", "C2L"]

obs = gr.rinexobs('/home/bubble/Desktop/Programs/python/OBS-SAT/data/ABPO00MDG_R_20220421000_01H_30S_MO.crx', use='G')
nav = gr.rinexnav('/home/bubble/Desktop/Programs/python/OBS-SAT/data/ABPO00MDG_R_20220421000_01H_GN.rnx', use='G')

common_sv, common_time = INTERSECTION(obs, nav)




# Dual channel Detector
def DUAL_CHANNEL(_obs: xarray.Dataset) -> tuple:
    """
    ARGS: _obs
    RETURN: (signature, bool) for signature:
                                            -1 for None  | None has dual channel
                                            0 for C1C   | C1C has dual channel
                                            1 for C1L   | C1L has dual channel
    """

    # ALL THE OBSERVATION DATA
    keys = list(_obs.data_vars.keys())

    return_bool = False

    return_bool = __data[0] in keys and __data[1] in keys

    if return_bool:
        return 0, return_bool
    else:
        return_bool = __data[2] in keys and __data[3] in keys

        if return_bool:
            return 1, return_bool
        else:
            return -1, return_bool


def TARGET(SV: str, time, signature: int, dual: bool, data_extract=None) -> None:

    # Read the global variable
    if data_extract is None:
        data_extract = __data

    # Objective: Sync the Satellite Class
    sat = Satellite(name=SV, time=time)

    # Get the specific sv data
    sv_data = obs.sel(sv=SV, time=time)

    # Dual channel data Extract and Setting
    if not dual:
        setattr(sat, data_extract[0], sv_data[data_extract[0]].values)
        setattr(sat, "channel", False)


    else:
        setattr(sat, "channel", True)

        if signature == 0:
            for attributes in data_extract[:2]:
                setattr(sat, attributes, sv_data[attributes].values)

        elif signature == 1:
            for attributes in data_extract[2:]:
                if attributes == "C2L":
                    setattr(sat, "C2C", sv_data[attributes].values)
                else:
                    setattr(sat, "C2C", sv_data[attributes].values)


    for attributes in sat.__dict__:
        print(f"{attributes} -> {getattr(sat, attributes)}")


if __name__ == '__main__':
    sig, dual = DUAL_CHANNEL(obs)

    #TARGET(common_sv[0], common_time, sig, dual)
