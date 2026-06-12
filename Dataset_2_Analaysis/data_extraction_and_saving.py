import numpy as np
import matplotlib.pyplot as plt
from data_2_functions import *

HoQI_data = Data_Extract('Dataset_2_Analaysis/20260501_HoQI_quietdata.txt')

PD1_1x = HoQI_data["SENS_HOQI_1_H_INP_SIN_IN"] 
PD2_1x = HoQI_data["SENS_HOQI_1_H_INP_COS_IN"]
PD3_1x = HoQI_data["SENS_HOQI_1_H_INP_MCOS_IN"]
PD1_2x = HoQI_data["SENS_HOQI_2_H_INP_SIN_IN"]
PD2_2x = HoQI_data["SENS_HOQI_2_H_INP_COS_IN"]
PD3_2x = HoQI_data["SENS_HOQI_2_H_INP_MCOS_IN"]
PD1_3x = HoQI_data["SENS_HOQI_3_H_INP_SIN_IN"]
PD2_3x = HoQI_data["SENS_HOQI_3_H_INP_COS_IN"]
PD3_3x = HoQI_data["SENS_HOQI_3_H_INP_MCOS_IN"]
PD1_1z = HoQI_data["SENS_HOQI_1_V_INP_SIN_IN"]
PD2_1z = HoQI_data["SENS_HOQI_1_V_INP_COS_IN"]
PD3_1z = HoQI_data["SENS_HOQI_1_V_INP_MCOS_IN"]
PD1_2z = HoQI_data["SENS_HOQI_2_V_INP_SIN_IN"]
PD2_2z = HoQI_data["SENS_HOQI_2_V_INP_COS_IN"]
PD3_2z = HoQI_data["SENS_HOQI_2_V_INP_MCOS_IN"]
PD1_3z = HoQI_data["SENS_HOQI_3_V_INP_SIN_IN"]
PD2_3z = HoQI_data["SENS_HOQI_3_V_INP_COS_IN"]
PD3_3z = HoQI_data["SENS_HOQI_3_V_INP_MCOS_IN"]

Q1_1x, Q2_1x = bepaling_Q1_Q2(PD1_1x, PD2_1x, PD3_1x)
Q1_2x, Q2_2x = bepaling_Q1_Q2(PD1_2x, PD2_2x, PD3_2x)
Q1_3x, Q2_3x = bepaling_Q1_Q2(PD1_3x, PD2_3x, PD3_3x)
Q1_1z, Q2_1z = bepaling_Q1_Q2(PD1_1z, PD2_1z, PD3_1z)
Q1_2z, Q2_2z = bepaling_Q1_Q2(PD1_2z, PD2_2z, PD3_2z)
Q1_3z, Q2_3z = bepaling_Q1_Q2(PD1_3z, PD2_3z, PD3_3z)

Q1_list = np.array((Q1_1x, Q1_2x, Q1_3x, Q1_1z, Q1_2z, Q1_3z))
Q2_list = np.array((Q2_1x, Q2_2x, Q2_3x, Q2_1z, Q2_2z, Q2_3z))

np.save('Dataset_2_Analaysis/Data2_Q1.npy', Q1_list)
np.save('Dataset_2_Analaysis/Data2_Q2.npy', Q2_list)
