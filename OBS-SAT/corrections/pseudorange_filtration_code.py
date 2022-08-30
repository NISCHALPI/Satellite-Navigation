
import numpy as np

# Constant definitions


c = 299792458  # Precise speed of light


# Function to eliminate Ionospheric delay - Only works on L1-L2 dual channel carrier measurement
# Drawback: Significant Noise in Measurement
def Ionospheric_Dual_Channel(l1_range: np.float32, l2_range: np.float32) -> np.float32:
    """Dual channel ionospheric free-combination to eliminate ionospheric pseudo-range ambiguity
    Args: L1 Range - L2 Range : type=np.float32
    Out: Corrected Range : type=np.float32"""

    l1_coefficient = 2.546
    l2_coefficient = -1.546

    return l1_coefficient * l1_range + l2_coefficient * l2_range

# Since No Weather Data is Provided, the Tropospheric Delay is Ignored

# Multipath is Ignored - No DGPS data

# Can correct:
# -Relativistic Error -- Nav file
# -Ionosphere Error only if Receiver is Dual Channel -- this file
# -SAT time offset -- Nav file
# -Check for Receiver time offset --Parse Rinex

