import numpy as np
import matplotlib as mt
import matplotlib.pyplot as plt 

from functions import *

HoQI_3z_Q1, HoQI_3z_Q2 = np.load('Data_Analysis_Part_1/1xQ1.npy'), np.load('Data_Analysis_Part_1/1xQ2.npy')
HoQI_3z_Q1, HoQI_3z_Q2 = transform(HoQI_3z_Q1[0:300000], HoQI_3z_Q2[0:300000])
length_list_HoQI_3z, optical_phase_list_HoQI_3z, Q_absoluut_list_HoQI_3z = Q1_Q2_Length_opt_phase_norm_Q(HoQI_3z_Q1, HoQI_3z_Q2)

x = HoQI_3z_Q1
y = HoQI_3z_Q2
plt.scatter(x, y, s=3)
plt.figure()
# plt.plot (optical_phase_list_HoQI_3z, Q_absoluut_list_HoQI_3z)
# plt.xlabel ('optical phase')
# plt.ylabel ('norm')
plt.show()