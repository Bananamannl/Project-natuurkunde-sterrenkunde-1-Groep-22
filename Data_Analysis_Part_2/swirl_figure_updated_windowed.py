import numpy as np
import matplotlib.pyplot as plt

# =========================
# Load windowed ellipse fitted Q and HoQI displacement data
# =========================
Q1_list_windowed = np.load('End_Product_Code/windowed_ellipse_Q1_data.npy')
Q2_list_windowed = np.load('End_Product_Code/windowed_ellipse_Q2_data.npy')
displacement_windowed = np.load('End_Product_Code/windowed_ellipse_HoQI_displacement_data.npy')

Q1_1x_w, Q1_2x_w, Q1_3x_w, Q1_1z_w, Q1_2z_w, Q1_3z_w = [Q1_list_windowed[i] for i in range(6)]
Q2_1x_w, Q2_2x_w, Q2_3x_w, Q2_1z_w, Q2_2z_w, Q2_3z_w = [Q2_list_windowed[i] for i in range(6)]

# =========================
# Load single ellipse fitted Q and HoQI displacement data
# =========================
Q1_list_single = np.load('End_Product_Code/single_ellipse_Q1_data.npy')
Q2_list_single = np.load('End_Product_Code/single_ellipse_Q2_data.npy')
displacement_single = np.load('End_Product_Code/single_ellipse_HoQI_displacement_data.npy')

Q1_1x_s, Q1_2x_s, Q1_3x_s, Q1_1z_s, Q1_2z_s, Q1_3z_s = [Q1_list_single[i] for i in range(6)]
Q2_1x_s, Q2_2x_s, Q2_3x_s, Q2_1z_s, Q2_2z_s, Q2_3z_s = [Q2_list_single[i] for i in range(6)]

# =========================
# Load non-fitted Q and HoQI displacement data
# =========================
Q1_list_raw = np.load('End_Product_Code/raw_Q1_data.npy')
Q2_list_raw = np.load('End_Product_Code/raw_Q2_data.npy')

Q1_1x_r = Q1_list_raw[0]
Q2_1x_r = Q2_list_raw[0]

# =========================
# Velocity calculation
# =========================
fs = 1000  # Hz

vel_1x_w = np.diff(displacement_windowed[0]) * fs
vel_1x_s = np.diff(displacement_single[0]) * fs

# =========================
# Select the desired time interval
# =========================
t_start = int(1823e3)
t_end   = int(1827e3)

# =========================
# Windowed ellipse fitted plot
# =========================
time_w = np.arange(len(Q1_1x_w)) * fs  # in ms

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

ax.plot(Q1_1x_w[t_start:t_end], Q2_1x_w[t_start:t_end], time_w[t_start:t_end], lw=0.8, alpha=0.8)

ax.set_xlabel('Q1')
ax.set_ylabel('Q2')
ax.set_zlabel('time (ms)')
ax.set_title('HoQI 1x (windowed ellipse fitted)')

plt.tight_layout()
plt.savefig('Swirl_figure_windowed_highx_highv.png')
plt.show()

# =========================
# Single ellipse fitted plot
# =========================
time_s = np.arange(len(Q1_1x_s)) * fs  # in ms

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

ax.plot(Q1_1x_s[t_start:t_end], Q2_1x_s[t_start:t_end], time_s[t_start:t_end], lw=0.8, alpha=0.8)

ax.set_xlabel('Q1')
ax.set_ylabel('Q2')
ax.set_zlabel('time (ms)')
ax.set_title('HoQI 1x (single ellipse fitted)')

plt.tight_layout()
plt.savefig('Swirl_figure_single_highx_highv.png')
plt.show()

# =========================
# Non-fitted plot
# =========================
time_r = np.arange(len(Q1_1x_r)) * fs  # in ms

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

ax.plot(Q1_1x_r[t_start:t_end], Q2_1x_r[t_start:t_end], time_r[t_start:t_end], lw=0.8, alpha=0.8)

ax.set_xlabel('Q1')
ax.set_ylabel('Q2')
ax.set_zlabel('time (ms)')
ax.set_title('HoQI 1x (non-fitted)')

plt.tight_layout()
plt.savefig('Swirl_figure_non_highx_highv.png')
plt.show()