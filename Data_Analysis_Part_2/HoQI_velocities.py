import numpy as np
import matplotlib.pyplot as plt

# =========================
# Load saved plot data
# =========================
windowed_ellipse_HoQI_displacement = np.load('End_Product_Code/windowed_ellipse_HoQI_displacement_data.npy')

hoqi_1x = windowed_ellipse_HoQI_displacement[0]
hoqi_2x = windowed_ellipse_HoQI_displacement[1]
hoqi_3x = windowed_ellipse_HoQI_displacement[2]
hoqi_1z = windowed_ellipse_HoQI_displacement[3]
hoqi_2z = windowed_ellipse_HoQI_displacement[4]
hoqi_3z = windowed_ellipse_HoQI_displacement[5]

fs = 1000

vel_1x = np.diff(hoqi_1x) * fs
vel_2x = np.diff(hoqi_2x) * fs
vel_3x = np.diff(hoqi_3x) * fs
vel_1z = np.diff(hoqi_1z) * fs
vel_2z = np.diff(hoqi_2z) * fs
vel_3z = np.diff(hoqi_3z) * fs

t_vel = np.arange(len(vel_1x)) / fs

hoqi_vel_data = [vel_1x, vel_2x, vel_3x, vel_1z, vel_2z, vel_3z]
subplot_titles = ["1x", "2x", "3x", "1z", "2z", "3z"]

fig, axes = plt.subplots(2, 3, figsize=(18, 9))
axes = axes.flatten()

for i, title in enumerate(subplot_titles):
    axes[i].plot(t_vel, hoqi_vel_data[i])
    axes[i].set_title(title)
    axes[i].set_xlabel("Time (s)")
    axes[i].set_ylabel(r"Velocity ($\mu$m/s)")

fig.suptitle("Time series of HoQI velocities (windowed ellipse fitted)")
plt.tight_layout()
plt.savefig('End_Product_Code/timeseries_windowed_hoqi_velocity.png', dpi=300, bbox_inches="tight")
plt.show()