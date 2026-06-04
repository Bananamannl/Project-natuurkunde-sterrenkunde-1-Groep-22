import numpy as np
from data_extraction_1 import Data_Extract

data_20260421 = Data_Extract('20260421_HoQIs.txt')
tijd = data_20260421["T"]

PD1_1x = data_20260421["SENS_HOQI_1_H_INP_SIN_IN"] 
PD2_1x = data_20260421["SENS_HOQI_1_H_INP_COS_IN"]
PD3_1x = data_20260421["SENS_HOQI_1_H_INP_MCOS_IN"]
PD1_2x = data_20260421["SENS_HOQI_2_H_INP_SIN_IN"]
PD2_2x = data_20260421["SENS_HOQI_2_H_INP_COS_IN"]
PD3_2x = data_20260421["SENS_HOQI_2_H_INP_MCOS_IN"]
PD1_3x = data_20260421["SENS_HOQI_3_H_INP_SIN_IN"]
PD2_3x = data_20260421["SENS_HOQI_3_H_INP_COS_IN"]
PD3_3x = data_20260421["SENS_HOQI_3_H_INP_MCOS_IN"]
PD1_1z = data_20260421["SENS_HOQI_1_V_INP_SIN_IN"]
PD2_1z = data_20260421["SENS_HOQI_1_V_INP_COS_IN"]
PD3_1z = data_20260421["SENS_HOQI_1_V_INP_MCOS_IN"]
PD1_2z = data_20260421["SENS_HOQI_2_V_INP_SIN_IN"]
PD2_2z = data_20260421["SENS_HOQI_2_V_INP_COS_IN"]
PD3_2z = data_20260421["SENS_HOQI_2_V_INP_MCOS_IN"]
PD1_3z = data_20260421["SENS_HOQI_3_V_INP_SIN_IN"]
PD2_3z = data_20260421["SENS_HOQI_3_V_INP_COS_IN"]
PD3_3z = data_20260421["SENS_HOQI_3_V_INP_MCOS_IN"]

# functie om uit PD1, PD2 en PD3 een lijst te maken Q1 en een lijst Q2.
def bepaling_Q1_Q2(PD1, PD2, PD3):  
    Q1 = np.array(PD1)-np.array(PD2)
    Q2 = np.array(PD1)-np.array(PD3)
    return Q1, Q2

def Q_lijsten():
    Q1_1x, Q2_1x = bepaling_Q1_Q2(PD1_1x, PD2_1x, PD3_1x)
    Q1_2x, Q2_2x = bepaling_Q1_Q2(PD1_2x, PD2_2x, PD3_2x)
    Q1_3x, Q2_3x = bepaling_Q1_Q2(PD1_3x, PD2_3x, PD3_3x)
    Q1_1z, Q2_1z = bepaling_Q1_Q2(PD1_1z, PD2_1z, PD3_1z)
    Q1_2z, Q2_2z = bepaling_Q1_Q2(PD1_2z, PD2_2z, PD3_2z)
    Q1_3z, Q2_3z = bepaling_Q1_Q2(PD1_3z, PD2_3z, PD3_3z)
    
    return Q1_1x, Q2_1x, Q1_2x, Q2_2x, Q1_3x, Q2_3x, Q1_1z, Q2_1z, Q1_2z, Q2_2z, Q1_3z, Q2_3z

#sla de eerste 3 op zodat we ze niet steeds hoeven op te halen
#Q1_2x, Q2_2x = bepaling_Q1_Q2(PD1_2x, PD2_2x, PD3_2x)
#Q1_2x_kopie = Q1_2x.copy()
#Q2_2x_kopie = Q2_2x.copy()
#np.save("2xQ1.npy", Q1_2x_kopie)
#np.save("2xQ2.npy", Q2_2x_kopie)
