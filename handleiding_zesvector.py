import numpy as np
import matplotlib.pyplot as plt

zesvector_matrix = np.load("fitted_six_vct_list.npy")

tijd_lijst = []
for tijd in range(0, 3000000, 1):
    tijd_lijst.append(tijd)

x_lijst_gefit = zesvector_matrix[0:int(3e6), 0]
y_lijst_gefit = zesvector_matrix[0:int(3e6), 1]
z_lijst_gefit = zesvector_matrix[0:int(3e6), 2]
Rx_lijst_gefit = zesvector_matrix[0:int(3e6), 3]
Ry_lijst_gefit = zesvector_matrix[0:int(3e6), 4]
Rz_lijst_gefit = zesvector_matrix[0:int(3e6), 5]

plt.plot(tijd_lijst, x_lijst_gefit)
plt.xlabel("x (um)")
plt.ylabel("tijd (ms)")
plt.show()