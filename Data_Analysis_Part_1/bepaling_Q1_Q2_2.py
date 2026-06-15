import numpy as np

# function to convert the PD lists of a certain HoQI into a Q1 list and a Q2 list
def bepaling_Q1_Q2(PD1, PD2, PD3):  
    Q1 = np.array(PD1)-np.array(PD2)
    Q2 = np.array(PD1)-np.array(PD3)
    return Q1, Q2
