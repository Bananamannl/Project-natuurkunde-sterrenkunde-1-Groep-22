import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# =========================
# Load saved plot data
# =========================
data = np.load(r"Data_Analysis_Part_2\image_format_test.npy", allow_pickle=True).item()

x = data["x"]
y_true = data["y_true"]
y_pred_passive = data["y_pred_passive"]
y_pred_active = data["y_pred_active"]
labels = [r"$x_0$", r"$y_0$", r"$a$", r"$b$", r"$\theta$"]
center_shift = data["center_shift"]
passive_train_size = data["passive_train_size"]

# =========================
# Plot settings
# =========================
fig, axes = plt.subplots(
    len(labels),
    1,
    figsize=(16, 10),
    sharex=True
)

# Maak figure en axes transparant
fig.patch.set_alpha(0)

for i, label in enumerate(labels):
    ax = axes[i]
    ax.patch.set_alpha(0)

    # Windowed ellipse fit: blauw
    ax.plot(
        x,
        y_true[:, i],
        color="limegreen",
        linewidth=1.0,
        label="Windowed fit"
    )

    # Static/passive model: rood
    ax.plot(
        x,
        y_pred_passive[:, i],
        color="red",
        linewidth=1.1,
        label="Static model"
    )

    # Active model: blauw, maar dashed zodat je hem onderscheidt
    ax.plot(
        x,
        y_pred_active[:, i],
        color="deepskyblue",
        linewidth=1.0,
        alpha=0.9,
        label="Active model"
    )

    ax.axvspan(
        center_shift,
        center_shift + passive_train_size,
        color="white",
        alpha=0.12,
        label="Training data" if i == 0 else None
    )

    # Witte labels, ticks, assen en grid
    ax.set_ylabel(label, color="white", fontsize=24)
    ax.tick_params(axis="both", colors="white")

    for spine in ax.spines.values():
        spine.set_color("white")
        spine.set_linewidth(2.5)

    ax.yaxis.set_major_locator(MaxNLocator(nbins=3))
    ax.grid(color="white", alpha=0.25)

    ax.tick_params(axis="both", colors="white", labelsize=14, width=2, length=6)

    if i == 0:
        ax.set_title(
            "Ellipse parameter predictions for static and active kNN model",
            fontsize=34,
            fontweight="bold",
            color="white"
        )

axes[-1].set_xlabel("Time (ms)", color="white", fontsize=24)

# Legenda wit maken
lines, legend_labels = axes[0].get_legend_handles_labels()

legend = fig.legend(
    lines,
    legend_labels,
    loc="upper right",
    bbox_to_anchor=(1.11, 0.90),
    frameon=False,
    fontsize= 24
)

for text in legend.get_texts():
    text.set_color("white")

plt.tight_layout(rect=[0, 0, 0.88, 0.96])

plt.savefig(
    "replotted_image_format_test_transparent.png",
    dpi=300,
    bbox_inches="tight",
    transparent=True
)

plt.show()