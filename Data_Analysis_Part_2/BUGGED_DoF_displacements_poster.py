# importing the necessary libraries and functions
import numpy as np
import matplotlib.pyplot as plt

from functions import *

# introducing the different window sizes
window_size_2x = 500
window_size_1x_3x = 300
window_size_1z_2z_3z = 500

# introducing the different step sizes
step_size_common = 50
step_size_2z = 100

# loading in both Q lists for each of the six HoQI's
Q1_1x, Q2_1x, Q1_2x, Q2_2x, Q1_3x, Q2_3x, Q1_1z, Q2_1z, Q1_2z, Q2_2z, Q1_3z, Q2_3z = np.load('Data_Analysis_Part_1/1xQ1.npy'), np.load('Data_Analysis_Part_1/1xQ2.npy'), np.load('Data_Analysis_Part_1/2xQ1.npy'), np.load('Data_Analysis_Part_1/2xQ2.npy'), np.load('Data_Analysis_Part_1/3xQ1.npy'), np.load('Data_Analysis_Part_1/3xQ2.npy'), np.load('Data_Analysis_Part_1/1zQ1.npy'), np.load('Data_Analysis_Part_1/1zQ2.npy'), np.load('Data_Analysis_Part_1/2zQ1.npy'), np.load('Data_Analysis_Part_1/2zQ2.npy'), np.load('Data_Analysis_Part_1/3zQ1.npy'), np.load('Data_Analysis_Part_1/3zQ2.npy')

# transforming the Q lists using windowed ellipse fitting with step_size = window_size
Q1_1x_windowed, Q2_1x_windowed = variable_step_window_ellipse_fitting(Q1_1x, Q2_1x, window_size_1x_3x, step_size_common)
Q1_2x_windowed, Q2_2x_windowed = variable_step_window_ellipse_fitting(Q1_2x, Q2_2x, window_size_2x, step_size_common)
Q1_3x_windowed, Q2_3x_windowed = variable_step_window_ellipse_fitting(Q1_3x, Q2_3x, window_size_1x_3x, step_size_common)
Q1_1z_windowed, Q2_1z_windowed = variable_step_window_ellipse_fitting(Q1_1z, Q2_1z, window_size_1z_2z_3z, step_size_common)
Q1_2z_windowed, Q2_2z_windowed = variable_step_window_ellipse_fitting(Q1_2z, Q2_2z, window_size_1z_2z_3z, step_size_2z)
Q1_3z_windowed, Q2_3z_windowed = variable_step_window_ellipse_fitting(Q1_3z, Q2_3z, window_size_1z_2z_3z, step_size_common)

# calculating the direct HoQI displacements
lengths = [
    -Q1_Q2_Length(Q1_1x_windowed, Q2_1x_windowed),
    Q1_Q2_Length(Q1_2x_windowed, Q2_2x_windowed),
    Q1_Q2_Length(Q1_3x_windowed, Q2_3x_windowed),
    -Q1_Q2_Length(Q1_1z_windowed, Q2_1z_windowed),
    -Q1_Q2_Length(Q1_2z_windowed, Q2_2z_windowed),
    -Q1_Q2_Length(Q1_3z_windowed, Q2_3z_windowed),
]

min_len = min(len(x) for x in lengths)

(
length_1x_list_windowed,
length_2x_list_windowed,
length_3x_list_windowed,
length_1z_list_windowed,
length_2z_list_windowed,
length_3z_list_windowed
) = [x[:min_len] for x in lengths]

min_len = min(
    len(length_1x_list_windowed),
    len(length_2x_list_windowed),
    len(length_3x_list_windowed),
    len(length_1z_list_windowed),
    len(length_2z_list_windowed),
    len(length_3z_list_windowed),
)

length_1x_list_windowed = length_1x_list_windowed[:min_len]
length_2x_list_windowed = length_2x_list_windowed[:min_len]
length_3x_list_windowed = length_3x_list_windowed[:min_len]
length_1z_list_windowed = length_1z_list_windowed[:min_len]
length_2z_list_windowed = length_2z_list_windowed[:min_len]
length_3z_list_windowed = length_3z_list_windowed[:min_len]

# calculating the displacements in all six degrees of freedom using the 6x6 transformation matrix
x_list_windowed, y_list_windowed, z_list_windowed, Rx_list_windowed, Ry_list_windowed, Rz_list_windowed  = transformatiematrix(length_1x_list_windowed, length_2x_list_windowed, length_3x_list_windowed, length_1z_list_windowed, length_2z_list_windowed, length_3z_list_windowed)

# defining a time list for the displacement time series of the windowed ellipse fitted data
time = np.arange(len(x_list_windowed))

np.save('windowed_x.npy', x_list_windowed)
np.save('windowed_y.npy', y_list_windowed)
np.save('windowed_z.npy', z_list_windowed)

np.save('windowed_Rx.npy', Rx_list_windowed)
np.save('windowed_Ry.npy', Ry_list_windowed)
np.save('windowed_Rz.npy', Rz_list_windowed)

np.save('windowed_time.npy', time)

# doing the same thing for the displacements in all six degrees of freedom
figure, axes = plt.subplots(2, 3, figsize=(18, 10))

axes[0, 0].plot(time, x_list_windowed)
axes[0, 0].set_title('DoF positon (x) (windowed)')

axes[0, 1].plot(time, y_list_windowed)
axes[0, 1].set_title('DoF positon (y) (windowed)')

axes[0, 2].plot(time, z_list_windowed)
axes[0, 2].set_title('DoF positon (z) (windowed)')

axes[1, 0].plot(time, Rx_list_windowed)
axes[1, 0].set_title('DoF positon (Rx) (windowed)')

axes[1, 1].plot(time, Ry_list_windowed)
axes[1, 1].set_title('DoF positon (Ry) (windowed)')

axes[1, 2].plot(time, Rz_list_windowed)
axes[1, 2].set_title('DoF positon (Rz) (windowed)')

for ax in axes.flat:
    ax.set_xlabel('time (ms)')
    ax.set_ylabel('positon (um)')

plt.tight_layout(w_pad=5.0)
plt.savefig('windowed_DoF_position_time_series.png')
plt.show()