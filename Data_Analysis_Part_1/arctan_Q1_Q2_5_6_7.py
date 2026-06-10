import numpy as np
import matplotlib as mt

from data_extraction_1 import *
from bepaling_Q1_Q2_2 import *

# note that this function uses lists as input arguments
def Q1_Q2_Length(Q1, Q2):
    """
    Q1_Q2_Length( np.array, np.array ) - > np.array
    This function takes two lists of Q1 and Q2 made from the HoQI data, and calculates the optical phase. It then uses the optical phase to calculate the measured length at each timestep. This is then outputed as another np.array.
    """
    # The wavelength of the HoQI laser is 1064 nm, adjusted to e-3 to have the outputed length be in um instead
    w_length = 1064e-3 

    opt_phase = np.unwrap(np.arctan2(Q1, Q2))

    length = (opt_phase * w_length)/(4*np.pi)

    return length

def Q1_Q2_Length_opt_phase_norm_Q(Q1, Q2):
    """
    Q1_Q2_Length( np.array, np.array ) - > np.array
    This function takes two lists of Q1 and Q2 made from the HoQI data, and calculates the optical phase. It then uses the optical phase to calculate the measured length at each timestep. This is then outputed as another np.array.
    """
    # The wavelength of the HoQI laser is 1064 nm, adjusted to e-3 to have the outputed length be in um instead
    w_length = 1064e-3 

    opt_phase = np.unwrap(np.arctan2(Q1, Q2))

    length = (opt_phase * w_length)/(4*np.pi)

    norm = np.sqrt((Q1)**2 + (Q2)**2)

    return length, opt_phase, norm

# testing the function for one HoQI: 
HoQI_3z_Q1, HoQI_3z_Q2 = np.load('Data_Analyse_Dataset_1/3zQ1.npy'), np.load('Data_Analyse_Dataset_1/3zQ2.npy')

length_list_HoQI_3z, optical_phase_list_HoQI_3z, norm_list_HoQI_3z = Q1_Q2_Length_opt_phase_norm_Q(HoQI_3z_Q1, HoQI_3z_Q2)

# print test (if necessary):
# print(displacement_list_HoQI_1[0]-displacement_list_HoQI_1[1])