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
t = np.arange(len(hoqi_1x)) / fs

hoqi_data = [hoqi_1x, hoqi_2x, hoqi_3x, hoqi_1z, hoqi_2z, hoqi_3z]
subplot_titles = ["1x", "2x", "3x", "1z", "2z", "3z"]

fig, axes = plt.subplots(2, 3, figsize=(18, 9))
axes = axes.flatten()

for i, title in enumerate(subplot_titles):
    axes[i].plot(t, hoqi_data[i])
    axes[i].set_title(title)
    axes[i].set_xlabel("Time (s)")
    axes[i].set_ylabel(r"Displacement ($\mu$m)")

fig.suptitle("Time series of HoQI displacements (windowed ellipse fitted)")
plt.tight_layout()
plt.savefig('End_Product_Code/timeseries_windowed_hoqis.png', dpi=300, bbox_inches="tight")
plt.show()