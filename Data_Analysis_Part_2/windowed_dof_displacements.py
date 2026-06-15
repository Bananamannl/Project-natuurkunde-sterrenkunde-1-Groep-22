import numpy as np
import matplotlib.pyplot as plt

from functions import *

window_size_1x_2x = 500
window_size_3x = 210
window_size_1z_2z_3z = 250

Q1_1x, Q2_1x, Q1_2x, Q2_2x, Q1_3x, Q2_3x, Q1_1z, Q2_1z, Q1_2z, Q2_2z, Q1_3z, Q2_3z = np.load('Data_Analysis_Part_1/1xQ1.npy'), np.load('Data_Analysis_Part_1/1xQ2.npy'), np.load('Data_Analysis_Part_1/2xQ1.npy'), np.load('Data_Analysis_Part_1/2xQ2.npy'), np.load('Data_Analysis_Part_1/3xQ1.npy'), np.load('Data_Analysis_Part_1/3xQ2.npy'), np.load('Data_Analysis_Part_1/1zQ1.npy'), np.load('Data_Analysis_Part_1/1zQ2.npy'), np.load('Data_Analysis_Part_1/2zQ1.npy'), np.load('Data_Analysis_Part_1/2zQ2.npy'), np.load('Data_Analysis_Part_1/3zQ1.npy'), np.load('Data_Analysis_Part_1/3zQ2.npy')

Q1_1x_windowed, Q2_1x_windowed = standard_step_window_ellipse_fitting(Q1_1x, Q2_1x, window_size_1x_2x)
Q1_2x_windowed, Q2_2x_windowed = standard_step_window_ellipse_fitting(Q1_2x, Q2_2x, window_size_1x_2x)
Q1_3x_windowed, Q2_3x_windowed = standard_step_window_ellipse_fitting(Q1_3x, Q2_3x, window_size_3x)
Q1_1z_windowed, Q2_1z_windowed = standard_step_window_ellipse_fitting(Q1_1z, Q2_1z, window_size_1z_2z_3z)
Q1_2z_windowed, Q2_2z_windowed = standard_step_window_ellipse_fitting(Q1_2z, Q2_2z, window_size_1z_2z_3z)
Q1_3z_windowed, Q2_3z_windowed = standard_step_window_ellipse_fitting(Q1_3z, Q2_3z, window_size_1z_2z_3z)

length_1x_list_windowed = -Q1_Q2_Length(Q1_1x_windowed, Q2_1x_windowed)[:-150]
length_2x_list_windowed = Q1_Q2_Length(Q1_2x_windowed, Q2_2x_windowed)[:-150]
length_3x_list_windowed = Q1_Q2_Length(Q1_3x_windowed, Q2_3x_windowed)
length_1z_list_windowed = -Q1_Q2_Length(Q1_1z_windowed, Q2_1z_windowed)[:-150]
length_2z_list_windowed = -Q1_Q2_Length(Q1_2z_windowed, Q2_2z_windowed)[:-150]
length_3z_list_windowed = -Q1_Q2_Length(Q1_3z_windowed, Q2_3z_windowed)[:-150]

x_list_windowed, y_list_windowed, z_list_windowed, Rx_list_windowed, Ry_list_windowed, Rz_list_windowed  = transformatiematrix(length_1x_list_windowed, length_2x_list_windowed, length_3x_list_windowed, length_1z_list_windowed, length_2z_list_windowed, length_3z_list_windowed)

time = []
for i in range(0, 2999850):
    time.append(i)

figure, axes = plt.subplots(2, 3, figsize=(18, 10))

axes[0, 0].plot(time, length_1x_list_windowed)
axes[0, 0].set_title('HoQI positon (1x)')

axes[0, 1].plot(time, length_2x_list_windowed)
axes[0, 1].set_title('HoQI positon (2x)')

axes[0, 2].plot(time, length_3x_list_windowed)
axes[0, 2].set_title('HoQI positon (3x)')

axes[1, 0].plot(time, length_1z_list_windowed)
axes[1, 0].set_title('HoQI positon (1z)')

axes[1, 1].plot(time, length_2z_list_windowed)
axes[1, 1].set_title('HoQI positon (2z)')

axes[1, 2].plot(time, length_3z_list_windowed)
axes[1, 2].set_title('HoQI positon (3z)')

for ax in axes.flat:
    ax.set_xlabel('time (ms)')
    ax.set_ylabel('HoQI positon (um s$^{-1}$)')

plt.tight_layout(w_pad=5.0)
plt.savefig('windowed_HoQI_postion_time_series.png')
plt.show()

figure, axes = plt.subplots(2, 3, figsize=(18, 10))

axes[0, 0].plot(time, x_list_windowed)
axes[0, 0].set_title('DoF positon (x)')

axes[0, 1].plot(time, y_list_windowed)
axes[0, 1].set_title('DoF positon (y)')

axes[0, 2].plot(time, z_list_windowed)
axes[0, 2].set_title('DoF positon (z)')

axes[1, 0].plot(time, Rx_list_windowed)
axes[1, 0].set_title('DoF positon (Rx)')

axes[1, 1].plot(time, Ry_list_windowed)
axes[1, 1].set_title('DoF positon (Ry)')

axes[1, 2].plot(time, Rz_list_windowed)
axes[1, 2].set_title('DoF positon (Rz)')

for ax in axes.flat:
    ax.set_xlabel('time (ms)')
    ax.set_ylabel('HoQI positon (um s$^{-1}$)')

plt.tight_layout(w_pad=5.0)
plt.savefig('windowed_DoF_position_time_series.png')
plt.show()