# importing the necessary libraries and functions
import numpy as np
import matplotlib.pyplot as plt

from functions import *

# loading in both Q lists for each of the six HoQI's
Q1_1x, Q2_1x, Q1_2x, Q2_2x, Q1_3x, Q2_3x, Q1_1z, Q2_1z, Q1_2z, Q2_2z, Q1_3z, Q2_3z = np.load('Data_Analysis_Part_1/1xQ1.npy'), np.load('Data_Analysis_Part_1/1xQ2.npy'), np.load('Data_Analysis_Part_1/2xQ1.npy'), np.load('Data_Analysis_Part_1/2xQ2.npy'), np.load('Data_Analysis_Part_1/3xQ1.npy'), np.load('Data_Analysis_Part_1/3xQ2.npy'), np.load('Data_Analysis_Part_1/1zQ1.npy'), np.load('Data_Analysis_Part_1/1zQ2.npy'), np.load('Data_Analysis_Part_1/2zQ1.npy'), np.load('Data_Analysis_Part_1/2zQ2.npy'), np.load('Data_Analysis_Part_1/3zQ1.npy'), np.load('Data_Analysis_Part_1/3zQ2.npy')

# transforming the Q lists using single ellipse fitting
Q1_1x_single, Q2_1x_single = transform(Q1_1x, Q2_1x)
Q1_2x_single, Q2_2x_single = transform(Q1_2x, Q2_2x)
Q1_3x_single, Q2_3x_single = transform(Q1_3x, Q2_3x)
Q1_1z_single, Q2_1z_single = transform(Q1_1z, Q2_1z)
Q1_2z_single, Q2_2z_single = transform(Q1_2z, Q2_2z)
Q1_3z_single, Q2_3z_single = transform(Q1_3z, Q2_3z)

# loading the six vector with the direct HoQI displacements
HoQIs = np.load("Data_Analysis_Part_1\\HoQI_fitted_six_vct_list.npy")

# extracting the direct HoQI displacements for the single ellipse fitted Q lists, using the loaded six vector
length_1x_list_single = HoQIs[0:int(3e6), 0]
length_2x_list_single = HoQIs[0:int(3e6), 1]
length_3x_list_single = HoQIs[0:int(3e6), 2]
length_1z_list_single = HoQIs[0:int(3e6), 3]
length_2z_list_single = HoQIs[0:int(3e6), 4]
length_3z_list_single = HoQIs[0:int(3e6), 5]

# defining a time list for the displacement time series (there are in total 3,000,000 data points per HoQI)
time = []
for i in range(0, int(3e6)):
    time.append(i)

# creating a figure in which the six time series of the direct HoQI displacements, one for each HoQI, will be plotted 
figure, axes = plt.subplots(2, 3, figsize=(18, 10))

axes[0, 0].plot(time, length_1x_list_single)
axes[0, 0].set_title('HoQI position (1x) (single)')

axes[0, 1].plot(time, length_2x_list_single)
axes[0, 1].set_title('HoQI position (2x) (single)')

axes[0, 2].plot(time, length_3x_list_single)
axes[0, 2].set_title('HoQI position (3x) (single)')

axes[1, 0].plot(time, length_1z_list_single)
axes[1, 0].set_title('HoQI position (1z) (single)')

axes[1, 1].plot(time, length_2z_list_single)
axes[1, 1].set_title('HoQI position (2z) (single)')

axes[1, 2].plot(time, length_3z_list_single)
axes[1, 2].set_title('HoQI position (3z) (single)')

for ax in axes.flat:
    ax.set_xlabel('time (ms)')
    ax.set_ylabel('position (um)')

plt.tight_layout(w_pad=5.0)
plt.savefig('single_HoQI_position_time_series.png')
plt.show()