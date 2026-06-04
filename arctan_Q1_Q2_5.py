import numpy as np
import matplotlib as mt

from data_extraction_1 import *
from Bepaling_Q1_Q2_2 import *


def Q1_Q2_length(Q1, Q2):
    """
    Q1_Q2_length( np.array, np.array ) - > np.array
    This function takes two lists of Q1 and Q2 made from the HoQI data, and calculates the optical phase. It then uses the optical phase to calculate the measured length at each timestep. This is then outputed as another np.array.
    """
    w_length = 1064e-9 # The wavelength of the HoQI laser is 1064 nm

    opt_phase = np.atan2(Q1, Q2)

    length = (opt_phase * w_length)/(4*np.pi)

    return length

## Testing the function
