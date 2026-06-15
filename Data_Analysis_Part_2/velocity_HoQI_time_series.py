import numpy as np
import matplotlib.pyplot as plt

from functions import *

window_size_1x_2x = 500
window_size_3x = 210
window_size_1z_2z_3z = 250

Q1_1x, Q2_1x, Q1_2x, Q2_2x, Q1_3x, Q2_3x, Q1_1z, Q2_1z, Q1_2z, Q2_2z, Q1_3z, Q2_3z = np.load('Data_Analysis_Part_1/1xQ1.npy'), np.load('Data_Analysis_Part_1/1xQ2.npy'), np.load('Data_Analysis_Part_1/2xQ1.npy'), np.load('Data_Analysis_Part_1/2xQ2.npy'), np.load('Data_Analysis_Part_1/3xQ1.npy'), np.load('Data_Analysis_Part_1/3xQ2.npy'), np.load('Data_Analysis_Part_1/1zQ1.npy'), np.load('Data_Analysis_Part_1/1zQ2.npy'), np.load('Data_Analysis_Part_1/2zQ1.npy'), np.load('Data_Analysis_Part_1/2zQ2.npy'), np.load('Data_Analysis_Part_1/3zQ1.npy'), np.load('Data_Analysis_Part_1/3zQ2.npy')

Q1_1x_single, Q2_1x_single = transform(Q1_1x, Q2_1x)
Q1_2x_single, Q2_2x_single = transform(Q1_2x, Q2_2x)
Q1_3x_single, Q2_3x_single = transform(Q1_3x, Q2_3x)
Q1_1z_single, Q2_1z_single = transform(Q1_1z, Q2_1z)
Q1_2z_single, Q2_2z_single = transform(Q1_2z, Q2_2z)
Q1_3z_single, Q2_3z_single = transform(Q1_3z, Q2_3z)

Q1_1x_windowed, Q2_1x_windowed = standard_step_window_ellipse_fitting(Q1_1x, Q2_1x, window_size_1x_2x)
Q1_2x_windowed, Q2_2x_windowed = standard_step_window_ellipse_fitting(Q1_2x, Q2_2x, window_size_1x_2x)
Q1_3x_windowed, Q2_3x_windowed = standard_step_window_ellipse_fitting(Q1_3x, Q2_3x, window_size_3x)
Q1_1z_windowed, Q2_1z_windowed = standard_step_window_ellipse_fitting(Q1_1z, Q2_1z, window_size_1z_2z_3z)
Q1_2z_windowed, Q2_2z_windowed = standard_step_window_ellipse_fitting(Q1_2z, Q2_2z, window_size_1z_2z_3z)
Q1_3z_windowed, Q2_3z_windowed = standard_step_window_ellipse_fitting(Q1_3z, Q2_3z, window_size_1z_2z_3z)

HoQIs = np.load("Data_Analysis_Part_1\\HoQI_fitted_six_vct_list.npy")

# length_1x_list_non_fitted = -Q1_Q2_Length(Q1_1x, Q2_1x)
# length_2x_list_non_fitted = Q1_Q2_Length(Q1_2x, Q2_2x)
# length_3x_list_non_fitted = Q1_Q2_Length(Q1_3x, Q2_3x)
# length_1z_list_non_fitted = -Q1_Q2_Length(Q1_1z, Q2_1z)
# length_2z_list_non_fitted = -Q1_Q2_Length(Q1_2z, Q2_2z)
# length_3z_list_non_fitted = -Q1_Q2_Length(Q1_3z, Q2_3z)

length_1x_list_single = HoQIs[0:int(3e6), 0]
length_2x_list_single = HoQIs[0:int(3e6), 1]
length_3x_list_single = HoQIs[0:int(3e6), 2]
length_1z_list_single = HoQIs[0:int(3e6), 3]
length_2z_list_single = HoQIs[0:int(3e6), 4]
length_3z_list_single = HoQIs[0:int(3e6), 5]

length_1x_list_windowed = -Q1_Q2_Length(Q1_1x_windowed, Q2_1x_windowed)[:-150]
length_2x_list_windowed = Q1_Q2_Length(Q1_2x_windowed, Q2_2x_windowed)[:-150]
length_3x_list_windowed = Q1_Q2_Length(Q1_3x_windowed, Q2_3x_windowed)
length_1z_list_windowed = -Q1_Q2_Length(Q1_1z_windowed, Q2_1z_windowed)[:-150]
length_2z_list_windowed = -Q1_Q2_Length(Q1_2z_windowed, Q2_2z_windowed)[:-150]
length_3z_list_windowed = -Q1_Q2_Length(Q1_3z_windowed, Q2_3z_windowed)[:-150]

time_velocity = []
for i in range(2999999):
    time_velocity.append(i)

time_velocity_windowed = []
for i in range(2999849):
    time_velocity_windowed.append(i)

# velocity_1x_non_fitted, velocity_2x_non_fitted, velocity_3x_non_fitted, velocity_1z_non_fitted, velocity_2z_non_fitted, velocity_3z_non_fitted = [[] for j in range(6)]

# for i in range(0, len(length_1x_list_non_fitted)-1):
#     v_1x_non_fitted = (length_1x_list_non_fitted[i+1] - length_1x_list_non_fitted[i])/0.001
#     v_2x_non_fitted = (length_2x_list_non_fitted[i+1] - length_2x_list_non_fitted[i])/0.001
#     v_3x_non_fitted = (length_3x_list_non_fitted[i+1] - length_3x_list_non_fitted[i])/0.001
#     v_1z_non_fitted = (length_1z_list_non_fitted[i+1] - length_1z_list_non_fitted[i])/0.001
#     v_2z_non_fitted = (length_2z_list_non_fitted[i+1] - length_2z_list_non_fitted[i])/0.001
#     v_3z_non_fitted = (length_3z_list_non_fitted[i+1] - length_3z_list_non_fitted[i])/0.001

#     velocity_1x_non_fitted.append(v_1x_non_fitted)
#     velocity_2x_non_fitted.append(v_2x_non_fitted)
#     velocity_3x_non_fitted.append(v_3x_non_fitted)
#     velocity_1z_non_fitted.append(v_1z_non_fitted)
#     velocity_2z_non_fitted.append(v_2z_non_fitted)
#     velocity_3z_non_fitted.append(v_3z_non_fitted)

velocity_1x_single, velocity_2x_single, velocity_3x_single, velocity_1z_single, velocity_2z_single, velocity_3z_single = [[] for j in range(6)]

for i in range(0, len(length_1x_list_single)-1):
    v_1x_single = (length_1x_list_single[i+1] - length_1x_list_single[i])/0.001
    v_2x_single = (length_2x_list_single[i+1] - length_2x_list_single[i])/0.001
    v_3x_single = (length_3x_list_single[i+1] - length_3x_list_single[i])/0.001
    v_1z_single = (length_1z_list_single[i+1] - length_1z_list_single[i])/0.001
    v_2z_single = (length_2z_list_single[i+1] - length_2z_list_single[i])/0.001
    v_3z_single = (length_3z_list_single[i+1] - length_3z_list_single[i])/0.001

    velocity_1x_single.append(v_1x_single)
    velocity_2x_single.append(v_2x_single)
    velocity_3x_single.append(v_3x_single)
    velocity_1z_single.append(v_1z_single)
    velocity_2z_single.append(v_2z_single)
    velocity_3z_single.append(v_3z_single)

# velocity_1x_windowed, velocity_2x_windowed, velocity_3x_windowed, velocity_1z_windowed, velocity_2z_windowed, velocity_3z_windowed = [[] for j in range(6)]

# for i in range(0, len(length_1x_list_windowed)-1):
#     v_1x_windowed = (length_1x_list_windowed[i+1] - length_1x_list_windowed[i])/0.001
#     v_2x_windowed = (length_2x_list_windowed[i+1] - length_2x_list_windowed[i])/0.001
#     v_3x_windowed = (length_3x_list_windowed[i+1] - length_3x_list_windowed[i])/0.001
#     v_1z_windowed = (length_1z_list_windowed[i+1] - length_1z_list_windowed[i])/0.001
#     v_2z_windowed = (length_2z_list_windowed[i+1] - length_2z_list_windowed[i])/0.001
#     v_3z_windowed = (length_3z_list_windowed[i+1] - length_3z_list_windowed[i])/0.001

#     velocity_1x_windowed.append(v_1x_windowed)
#     velocity_2x_windowed.append(v_2x_windowed)
#     velocity_3x_windowed.append(v_3x_windowed)
#     velocity_1z_windowed.append(v_1z_windowed)
#     velocity_2z_windowed.append(v_2z_windowed)
#     velocity_3z_windowed.append(v_3z_windowed)

# figure, axes = plt.subplots(2, 3, figsize=(18, 10))

# axes[0, 0].plot(time_velocity, velocity_1x_non_fitted)
# axes[0, 0].set_title('velocity 1x (non-fitted)')

# axes[0, 1].plot(time_velocity, velocity_2x_non_fitted)
# axes[0, 1].set_title('velocity 2x (non-fitted)')

# axes[0, 2].plot(time_velocity, velocity_3x_non_fitted)
# axes[0, 2].set_title('velocity 3x (non-fitted)')

# axes[1, 0].plot(time_velocity, velocity_1z_non_fitted)
# axes[1, 0].set_title('velocity 1z (non-fitted)')

# axes[1, 1].plot(time_velocity, velocity_2z_non_fitted)
# axes[1, 1].set_title('velocity 2z (non-fitted)')

# axes[1, 2].plot(time_velocity, velocity_3z_non_fitted)
# axes[1, 2].set_title('velocity 3z (non-fitted)')

# for ax in axes.flat:
#     ax.set_xlabel('time (ms)')
#     ax.set_ylabel('velocity (um s$^{-1}$)')

# plt.tight_layout(w_pad=5.0)
# plt.savefig('velocity_non_fitted_time_series.png')
# plt.show()

figure, axes = plt.subplots(2, 3, figsize=(18, 10))

axes[0, 0].plot(time_velocity, velocity_1x_single)
axes[0, 0].set_title('velocity 1x (single)')

axes[0, 1].plot(time_velocity, velocity_2x_single)
axes[0, 1].set_title('velocity 2x (single)')

axes[0, 2].plot(time_velocity, velocity_3x_single)
axes[0, 2].set_title('velocity 3x (single)')

axes[1, 0].plot(time_velocity, velocity_1z_single)
axes[1, 0].set_title('velocity 1z (single)')

axes[1, 1].plot(time_velocity, velocity_2z_single)
axes[1, 1].set_title('velocity 2z (single)')

axes[1, 2].plot(time_velocity, velocity_3z_single)
axes[1, 2].set_title('velocity 3z (single)')

for ax in axes.flat:
    ax.set_xlabel('time (ms)')
    ax.set_ylabel('velocity (um s$^{-1}$)')

plt.tight_layout(w_pad=5.0)
plt.savefig('velocity_single_time_series.png')
plt.show()

# figure, axes = plt.subplots(2, 3, figsize=(18, 10))

# axes[0, 0].plot(time_velocity_windowed, velocity_1x_windowed)
# axes[0, 0].set_title('velocity 1x (windowed)')

# axes[0, 1].plot(time_velocity_windowed, velocity_2x_windowed)
# axes[0, 1].set_title('velocity 2x (windowed)')

# axes[0, 2].plot(time_velocity_windowed, velocity_3x_windowed)
# axes[0, 2].set_title('velocity 3x (windowed)')

# axes[1, 0].plot(time_velocity_windowed, velocity_1z_windowed)
# axes[1, 0].set_title('velocity 1z (windowed)')

# axes[1, 1].plot(time_velocity_windowed, velocity_2z_windowed)
# axes[1, 1].set_title('velocity 2z (windowed)')

# axes[1, 2].plot(time_velocity_windowed, velocity_3z_windowed)
# axes[1, 2].set_title('velocity 3z (windowed)')

# for ax in axes.flat:
#     ax.set_xlabel('time (ms)')
#     ax.set_ylabel('velocity (um s$^{-1}$)')

# plt.tight_layout(w_pad=5.0)
# plt.savefig('velocity_windowed_time_series.png')
# plt.show()

time = []
for i in range(3000000):
    time.append(i)

time_windowed = []
for i in range(2999850):
    time_windowed.append(i)

# at each run, change this accordingly to select the desired HoQI
# Q1, Q2 = Q1_1x, Q2_1x
# Q1, Q2 = Q1_1x_single, Q2_1x_single
Q1, Q2 = Q1_1x_windowed, Q2_1x_windowed

# velocity = velocity_1x_windowed
title = '1x (windowed)'

t_start = int(1.625e6)
t_end = int(1.628e6)

figure = plt.figure()
ax = figure.add_subplot(projection='3d')
# ax.plot(Q1[t_start:t_end], Q2[t_start:t_end], velocity[t_start:t_end], lw=0.8, alpha=0.8)
# ax.plot(Q1[t_start:t_end], Q2[t_start:t_end], time[t_start:t_end], lw=0.8, alpha=0.8)
ax.plot(Q1[t_start:t_end], Q2[t_start:t_end], time_windowed[t_start:t_end], lw=0.8, alpha=0.8)
ax.set_xlabel('Q1')
ax.set_ylabel('Q2')
# ax.set_zlabel('velocity (um s$^{-1}$)')
ax.set_zlabel('time (ms)')
ax.zaxis.labelpad = 20
ax.set_title(f'HoQI {title}')
plt.savefig('Q1_Q2_3D_cilinder.png')
plt.show()