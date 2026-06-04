import numpy as np
import matplotlib as mt

from data_extraction_1 import *
from bepaling_Q1_Q2_2 import *


def Q1_Q2_Length(Q1, Q2):
    """
    Q1_Q2_Length( np.array, np.array ) - > np.array
    This function takes two lists of Q1 and Q2 made from the HoQI data, and calculates the optical phase. It then uses the optical phase to calculate the measured length at each timestep. This is then outputed as another np.array.
    """
    w_length = 1064e-9 # The wavelength of the HoQI laser is 1064 nm

    opt_phase = np.arctan2(Q1, Q2)

    length = (opt_phase * w_length)/(4*np.pi)

    return length

## Testing the function

# First HoQI PD1, PD2, PD3: 
# SENS_HOQI_1_H_INP_SIN_IN SENS_HOQI_1_H_INP_COS_IN SENS_HOQI_1_H_INP_MCOS_IN
HoQI_1_Q1, HoQI_1_Q2 = np.load('3zQ1.npy'), np.load('3zQ2.npy')

displacement_list_HoQI_1 = Q1_Q2_Length(HoQI_1_Q1, HoQI_1_Q2)*10**6

#print(HoQI_data['SENS_HOQI_1_H_INP_SIN_IN'])
print(displacement_list_HoQI_1[0]-displacement_list_HoQI_1[1])