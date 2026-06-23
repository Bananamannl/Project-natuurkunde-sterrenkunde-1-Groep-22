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
t = np.arange(len(x)) / fs

dof_data   = [x,  y,  z,  Rx, Ry, Rz]
dof_labels = [
    r"Displacement ($\mathrm{\mu}$m)", 
    r"Displacement ($\mathrm{\mu}$m)", 
    r"Displacement ($\mathrm{\mu}$m)",
    r"Displacement ($\mathrm{\mu}$rad)", 
    r"Displacement ($\mathrm{\mu}$rad)", 
    r"Displacement ($\mathrm{\mu}$rad)"
]

# Titels per subplot toegevoegd
subplot_titles = ["X", "Y", "Z", "RX", "RY", "RZ"]
colors = ["deepskyblue", "red", "gold", "orange", "limegreen", "violet"]

# =========================
# Plot settings (sharex=True is hier weggehaald)
# =========================
fig, axes = plt.subplots(2, 3, figsize=(18, 9))
axes = axes.flatten()

fig.patch.set_alpha(0)

for i, (label, color, title) in enumerate(zip(dof_labels, colors, subplot_titles)):
    ax = axes[i]
    ax.patch.set_alpha(0)

    ax.plot(
        t,
        dof_data[i],
        color=color,
        linewidth=1.0,
        label=label
    )

    ax.set_title(title, color="white", fontsize=24, fontweight="bold", pad=10)
    
    ax.set_ylabel(label, color="white", fontsize=20, labelpad=2)
    
    # Dit zet nu verplicht op ELKE subplot de x-as label en zorgt dat de ticks zichtbaar zijn
    ax.set_xlabel("Time (ms)", color="white", fontsize=16)
    ax.tick_params(axis="both", colors="white", labelsize=12, width=2, length=6, labelbottom=True)

    for spine in ax.spines.values():
        spine.set_color("white")
        spine.set_linewidth(2.5)

    ax.yaxis.set_major_locator(MaxNLocator(nbins=3))
    ax.grid(color="white", alpha=0.25)

# Hoofdtitel 
fig.suptitle(
    "Time series of DoF displacements (windowed ellipse fitted)",
    fontsize=38,
    fontweight="bold",
    color="white",
    y=0.98
)

# tight_layout zorgt dat alles mooi past binnen de nieuwe formaten
plt.tight_layout()

plt.savefig(
    'End_Product_Code/timeseries_windowed_dof.png',
    dpi=300,
    bbox_inches="tight",
    transparent=True
)

plt.show()