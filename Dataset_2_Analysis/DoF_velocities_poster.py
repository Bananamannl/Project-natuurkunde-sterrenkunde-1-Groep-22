import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# =========================
# Load saved plot data
# =========================
windowed_ellipse_DOF_displacement = np.load('End_Product_Code/windowed_ellipse_DOF_displacement_data.npy', allow_pickle=True)

x  = windowed_ellipse_DOF_displacement[0]
y  = windowed_ellipse_DOF_displacement[1]
z  = windowed_ellipse_DOF_displacement[2]
Rx = windowed_ellipse_DOF_displacement[3]
Ry = windowed_ellipse_DOF_displacement[4]
Rz = windowed_ellipse_DOF_displacement[5]

# Sampling frequency in Hz
fs = 1000

# =========================
# Berekening van snelheden (Velocity)
# =========================
# Numerieke differentiatie: vermenigvuldigen met fs is hetzelfde als delen door dt
x_vel  = np.diff(x) * fs
y_vel  = np.diff(y) * fs
z_vel  = np.diff(z) * fs
Rx_vel = np.diff(Rx) * fs
Ry_vel = np.diff(Ry) * fs
Rz_vel = np.diff(Rz) * fs

# Tijdsvector voor snelheid (1 element korter vanwege np.diff) in milliseconden (ms)
t_vel = (np.arange(len(x_vel)) / fs) * 1000

dof_vel_data = [x_vel, y_vel, z_vel, Rx_vel, Ry_vel, Rz_vel]

# Aangepaste labels voor snelheid (Velocity)
dof_vel_labels = [
    r"Velocity ($\mathrm{\mu}$m/s)", 
    r"Velocity ($\mathrm{\mu}$m/s)", 
    r"Velocity ($\mathrm{\mu}$m/s)",
    r"Velocity ($\mathrm{\mu}$rad/s)", 
    r"Velocity ($\mathrm{\mu}$rad/s)", 
    r"Velocity ($\mathrm{\mu}$rad/s)"
]

# Titels per subplot (exact hetzelfde gehouden)
subplot_titles = ["X", "Y", "Z", "RX", "RY", "RZ"]
colors = ["deepskyblue", "red", "gold", "orange", "limegreen", "violet"]

# =========================
# Plot settings
# =========================
fig, axes = plt.subplots(2, 3, figsize=(18, 9))
axes = axes.flatten()

fig.patch.set_alpha(0)

for i, (label, color, title) in enumerate(zip(dof_vel_labels, colors, subplot_titles)):
    ax = axes[i]
    ax.patch.set_alpha(0)

    ax.plot(
        t_vel,
        dof_vel_data[i],
        color=color,
        linewidth=1.0,
        label=label
    )

    ax.set_title(title, color="white", fontsize=24, fontweight="bold", pad=10)
    ax.set_ylabel(label, color="white", fontsize=20, labelpad=2)
    
    ax.set_xlabel("Time (ms)", color="white", fontsize=16)
    ax.tick_params(axis="both", colors="white", labelsize=12, width=2, length=6, labelbottom=True)

    for spine in ax.spines.values():
        spine.set_color("white")
        spine.set_linewidth(2.5)

    ax.yaxis.set_major_locator(MaxNLocator(nbins=3))
    ax.grid(color="white", alpha=0.25)

# Aangepaste hoofdtitel voor snelheden
fig.suptitle(
    "Time series of DoF velocities (windowed ellipse fitted)",
    fontsize=38,
    fontweight="bold",
    color="white",
    y=0.98
)

plt.tight_layout()

# Opgeslagen onder een nieuwe, logische naam: 'timeseries_windowed_dof_velocity.png'
plt.savefig(
    'End_Product_Code/timeseries_windowed_dof_velocity.png',
    dpi=300,
    bbox_inches="tight",
    transparent=True
)

plt.show()