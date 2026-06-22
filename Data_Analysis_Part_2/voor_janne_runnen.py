import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from pathlib import Path

# =========================
# Load Q1/Q2 data
# =========================
DATA_FOLDER = Path(
    r"C:\Users\timob\OneDrive - UvA\Project 1\GitHub Map\Project-natuurkunde-sterrenkunde-1-Groep-22\Data_Analysis_Part_2\Q_lijsten_poster"
)

Q1_1x = np.load(DATA_FOLDER / "1xQ1.npy")
Q2_1x = np.load(DATA_FOLDER / "1xQ2.npy")

Q1_3x = np.load(DATA_FOLDER / "3xQ1.npy")
Q2_3x = np.load(DATA_FOLDER / "3xQ2.npy")

Q1_1z = np.load(DATA_FOLDER / "1zQ1.npy")
Q2_1z = np.load(DATA_FOLDER / "1zQ2.npy")

Q1_3z = np.load(DATA_FOLDER / "3zQ1.npy")
Q2_3z = np.load(DATA_FOLDER / "3zQ2.npy")

# =========================
# Same data repeated 3 times
# =========================
Q1_lists = [
    [Q1_1x, Q1_1x, Q1_1x],
    [Q1_3x, Q1_3x, Q1_3x],
    [Q1_1z, Q1_1z, Q1_1z],
    [Q1_3z, Q1_3z, Q1_3z],
]

Q2_lists = [
    [Q2_1x, Q2_1x, Q2_1x],
    [Q2_3x, Q2_3x, Q2_3x],
    [Q2_1z, Q2_1z, Q2_1z],
    [Q2_3z, Q2_3z, Q2_3z],
]

# =========================
# Titles
# =========================
column_titles = [
    "Original",
    "Transformed",
    "Windowed fit"
]

row_titles = [
    r"$1_x$",
    r"$3_x$",
    r"$1_z$",
    r"$3_z$"
]

# =========================
# Colors
# =========================
column_colors = [
    "red",
    "deepskyblue",
    "limegreen"
]

# =========================
# Plot settings
# =========================
fig, axes = plt.subplots(
    4,
    3,
    figsize=(14, 16),
    sharex=False,
    sharey=False
)

fig.patch.set_alpha(0)

for row in range(4):
    for col in range(3):
        ax = axes[row, col]
        ax.patch.set_alpha(0)

        Q1 = Q1_lists[row][col]
        Q2 = Q2_lists[row][col]

        ax.scatter(
            Q1,
            Q2,
            color=column_colors[col],
            s=2,
            alpha=0.8
        )

        # Vierkante plots
        ax.set_aspect("equal", adjustable="box")
        ax.set_box_aspect(1)

        # Witte assen, ticks en grid
        ax.tick_params(
            axis="both",
            colors="white",
            labelsize=14,
            width=2,
            length=6
        )

        for spine in ax.spines.values():
            spine.set_color("white")
            spine.set_linewidth(2.5)

        ax.grid(color="white", alpha=0.25)

        ax.xaxis.set_major_locator(MaxNLocator(nbins=3))
        ax.yaxis.set_major_locator(MaxNLocator(nbins=3))

        # Alleen kolomtitels bovenste rij
        if row == 0:
            ax.set_title(
                column_titles[col],
                fontsize=24,
                fontweight="bold",
                color="white"
            )

        # Alleen rijtitels links
        if col == 0:
            ax.set_ylabel(
                row_titles[row],
                color="white",
                fontsize=28,
                fontweight="bold",
                rotation=0,
                labelpad=45,
                va="center"
            )

# Grote figuurtitel
fig.suptitle(
    r"$Q_1$-$Q_2$ ellipse plots",
    fontsize=34,
    fontweight="bold",
    color="white"
)

plt.tight_layout(rect=[0, 0, 1, 0.96])

plt.savefig(
    "Q1_Q2_style_test_transparent.png",
    dpi=300,
    bbox_inches="tight",
    transparent=True
)

plt.show()