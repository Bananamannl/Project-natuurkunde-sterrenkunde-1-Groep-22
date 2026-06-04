import numpy as np
# functie om uit PD1, PD2 en PD3 een lijst te maken Q1 en een lijst Q2.
def bepaling_Q1_Q2(PD1, PD2, PD3):  
    Q1 = np.array(PD1)-np.array(PD2)
    Q2 = np.array(PD1)-np.array(PD3)
    return Q1, Q2