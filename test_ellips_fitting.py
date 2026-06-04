from data_extraction_1 import *
from bepaling_Q1_Q2_2 import *
from ellips_fitting_and_reshaping_4_5 import *

data_20260421 = Data_Extract('20260421_HoQIs.txt')
tijd = data_20260421["T"]
PD2_1x = data_20260421["SENS_HOQI_1_H_INP_COS_IN"]
PD3_1x = data_20260421["SENS_HOQI_1_H_INP_MCOS_IN"]
PD1_1x = data_20260421["SENS_HOQI_1_H_INP_SIN_IN"] 

Q1, Q2 = bepaling_Q1_Q2(PD1_1x, PD2_1x, PD3_1x)
Q1_kopie = Q1.copy()
Q2_kopie = Q2.copy()
print(Q1_kopie)
#plt.figure()
#plt.scatter(Q1, Q2, s=3)
#plt.scatter(Q1_new, Q2_new, s=5)
#plt.axis("equal")
#plt.grid()
#plt.show()
