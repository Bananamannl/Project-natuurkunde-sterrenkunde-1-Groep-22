from functions import *
import numpy as np
import matplotlib.pyplot as plt
from windowed_ellipse_fitting import *


Q1, Q2 = np.load("Data_Analysis_Part_1\\3zQ1.npy"), np.load("Data_Analysis_Part_1\\3zQ2.npy")
# Q1, Q2 = standard_step_window_ellipse_fitting(Q1[10000:15000], Q2[10000:15000], window_size=250)
Q1, Q2 = transform(Q1[10000:15000], Q2[10000:15000])

# plt.plot(Q1, Q2)
norm_lijst = []
for i in range (len(Q1)):
    norm = np.sqrt((Q1[i])**2 + (Q2[i])**2)
    norm_lijst.append(norm)

kleiner_dan_1 = 0
groter_dan_1 = 0
for j in range(0, len(norm_lijst)):
    if norm_lijst[j] < 1:
        kleiner_dan_1 += 1
    else:
        groter_dan_1 += 1

print(kleiner_dan_1)
print(groter_dan_1)

opt_fase = Q1_Q2_Opt_Fase(Q1, Q2)

positions = np.load("Data_Analysis_Part_1\HoQI_fitted_six_vct_list.npy")
x_HoQI = positions[10000:int(15000), 0]

plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.plot(opt_fase, x_HoQI)
plt.xlabel('phase')
plt.ylabel('HoQI_13z')

plt.subplot(1, 2, 2)
plt.plot(opt_fase, norm_lijst)
plt.xlabel('phase')
plt.ylabel('norm_3z')

plt.tight_layout()
plt.show()