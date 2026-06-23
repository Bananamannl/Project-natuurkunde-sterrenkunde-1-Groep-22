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

np.save('windowed_x.npy', x_list_windowed)
np.save('windowed_y.npy', y_list_windowed)
np.save('windowed_z.npy', z_list_windowed)
np.save('windowed_Rx.npy', Rx_list_windowed)
np.save('windowed_Ry.npy', Ry_list_windowed)
np.save('windowed_Rz.npy', Rz_list_windowed)

# defining time list for the velocity time series of the windowed ellipse fitted data
time = np.arange(len(x_list_windowed))

# velocity calculation (np.gradient)
vx = np.gradient(x_list_windowed, 1)
vy = np.gradient(y_list_windowed, 1)
vz = np.gradient(z_list_windowed, 1)

vRx = np.gradient(Rx_list_windowed, 1)
vRy = np.gradient(Ry_list_windowed, 1)
vRz = np.gradient(Rz_list_windowed, 1)

np.save('windowed_vx.npy', vx)
np.save('windowed_vy.npy', vy)
np.save('windowed_vz.npy', vz)
np.save('windowed_vRx.npy', vRx)
np.save('windowed_vRy.npy', vRy)
np.save('windowed_vRz.npy', vRz)
np.save('windowed_time.npy', time)

# plotting velocities
figure, axes = plt.subplots(2, 3, figsize=(18, 10))

axes[0, 0].plot(time, vx)
axes[0, 0].set_title('DoF velocity (x) (windowed)')

axes[0, 1].plot(time, vy)
axes[0, 1].set_title('DoF velocity (y) (windowed)')

axes[0, 2].plot(time, vz)
axes[0, 2].set_title('DoF velocity (z) (windowed)')

axes[1, 0].plot(time, vRx)
axes[1, 0].set_title('DoF velocity (Rx) (windowed)')

axes[1, 1].plot(time, vRy)
axes[1, 1].set_title('DoF velocity (Ry) (windowed)')

axes[1, 2].plot(time, vRz)
axes[1, 2].set_title('DoF velocity (Rz) (windowed)')

for ax in axes.flat:
    ax.set_xlabel('time (ms)')
    ax.set_ylabel('velocity')

plt.tight_layout(w_pad=5.0)
plt.savefig('windowed_DoF_velocity_time_series.png')
plt.show()