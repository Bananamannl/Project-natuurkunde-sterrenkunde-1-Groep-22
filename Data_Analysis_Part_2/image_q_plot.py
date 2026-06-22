import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
# from functions import transform
# from windowed_ellipse_fitting import *
from pathlib import Path

# =========================
# Load Q1/Q2 data
# =========================
# Voorbeeld: vul hier jouw bestanden in
Q1_1x, Q2_1x = np.load(r"C:\Users\timob\OneDrive - UvA\Project 1\GitHub Map\Project-natuurkunde-sterrenkunde-1-Groep-22\Data_Analysis_Part_2\Q_lijsten_poster\1xQ1.npy"), np.load(r"C:\Users\timob\OneDrive - UvA\Project 1\GitHub Map\Project-natuurkunde-sterrenkunde-1-Groep-22\Data_Analysis_Part_2\Q_lijsten_poster\1xQ2.npy")
Q1_3x, Q2_3x = np.load(r"C:\Users\timob\OneDrive - UvA\Project 1\GitHub Map\Project-natuurkunde-sterrenkunde-1-Groep-22\Data_Analysis_Part_2\Q_lijsten_poster\3xQ1.npy"), np.load(r"C:\Users\timob\OneDrive - UvA\Project 1\GitHub Map\Project-natuurkunde-sterrenkunde-1-Groep-22\Data_Analysis_Part_2\Q_lijsten_poster\3xQ2.npy")
Q1_1z, Q2_1z = np.load(r"C:\Users\timob\OneDrive - UvA\Project 1\GitHub Map\Project-natuurkunde-sterrenkunde-1-Groep-22\Data_Analysis_Part_2\Q_lijsten_poster\1zQ1.npy"), np.load(r"C:\Users\timob\OneDrive - UvA\Project 1\GitHub Map\Project-natuurkunde-sterrenkunde-1-Groep-22\Data_Analysis_Part_2\Q_lijsten_poster\1zQ2.npy")
Q1_3z, Q2_3z = np.load(r"C:\Users\timob\OneDrive - UvA\Project 1\GitHub Map\Project-natuurkunde-sterrenkunde-1-Groep-22\Data_Analysis_Part_2\Q_lijsten_poster\3zQ1.npy"), np.load(r"C:\Users\timob\OneDrive - UvA\Project 1\GitHub Map\Project-natuurkunde-sterrenkunde-1-Groep-22\Data_Analysis_Part_2\Q_lijsten_poster\3zQ2.npy")


# # =========================
# # Save folder
# # =========================
# SAVE_FOLDER = Path(
#     r"C:\Users\timob\OneDrive - UvA\Project 1\GitHub Map\Project-natuurkunde-sterrenkunde-1-Groep-22\Data_Analysis_Part_2\Q_lijsten_poster"
# )

# # =========================
# # Original loaded HoQI data
# # =========================
# hoqi_data = {
#     "1x": (Q1_1x, Q2_1x),
#     "3x": (Q1_3x, Q2_3x),
#     "1z": (Q1_1z, Q2_1z),
#     "3z": (Q1_3z, Q2_3z),
# }

# # =========================
# # Window sizes per HoQI type
# # =========================
# window_sizes = {
#     "1x": 500,
#     "3x": 500,
#     "1z": 300,
#     "3z": 300,
# }

# # =========================
# # Transform + windowed fitting
# # =========================
# processed_arrays = {}

# for hoqi_name, (Q1, Q2) in hoqi_data.items():

#     # Transformed data
#     Q1_transformed, Q2_transformed = transform(Q1, Q2)

#     processed_arrays[f"Q1_{hoqi_name}_transformed"] = Q1_transformed
#     processed_arrays[f"Q2_{hoqi_name}_transformed"] = Q2_transformed

#     # Kies juiste window size
#     window_size = window_sizes[hoqi_name]

#     # Windowed ellipse data
#     Q1_windowed, Q2_windowed = variable_step_window_ellipse_fitting(
#         Q1,
#         Q2,
#         window_size=window_size,
#         step_size=50
#     )

#     processed_arrays[f"Q1_{hoqi_name}_windowed"] = Q1_windowed
#     processed_arrays[f"Q2_{hoqi_name}_windowed"] = Q2_windowed

# # =========================
# # Save processed arrays
# # Comment dit blok uit als alles al opgeslagen is
# # =========================
# for array_name, array in processed_arrays.items():
#     np.save(SAVE_FOLDER / f"{array_name}.npy", array)
#     print(f"Saved: {array_name}.npy")



SAVE_FOLDER = Path(
    r"C:\Users\timob\OneDrive - UvA\Project 1\GitHub Map\Project-natuurkunde-sterrenkunde-1-Groep-22\Data_Analysis_Part_2\Q_lijsten_poster"
)

# =========================
# Load transformed data
# =========================
Q1_1x_transformed = np.load(SAVE_FOLDER / "Q1_1x_transformed.npy")
Q2_1x_transformed = np.load(SAVE_FOLDER / "Q2_1x_transformed.npy")

Q1_3x_transformed = np.load(SAVE_FOLDER / "Q1_3x_transformed.npy")
Q2_3x_transformed = np.load(SAVE_FOLDER / "Q2_3x_transformed.npy")

Q1_1z_transformed = np.load(SAVE_FOLDER / "Q1_1z_transformed.npy")
Q2_1z_transformed = np.load(SAVE_FOLDER / "Q2_1z_transformed.npy")

Q1_3z_transformed = np.load(SAVE_FOLDER / "Q1_3z_transformed.npy")
Q2_3z_transformed = np.load(SAVE_FOLDER / "Q2_3z_transformed.npy")

# =========================
# Load windowed data
# =========================
Q1_1x_windowed = np.load(SAVE_FOLDER / "Q1_1x_windowed.npy")
Q2_1x_windowed = np.load(SAVE_FOLDER / "Q2_1x_windowed.npy")

Q1_3x_windowed = np.load(SAVE_FOLDER / "Q1_3x_windowed.npy")
Q2_3x_windowed = np.load(SAVE_FOLDER / "Q2_3x_windowed.npy")

Q1_1z_windowed = np.load(SAVE_FOLDER / "Q1_1z_windowed.npy")
Q2_1z_windowed = np.load(SAVE_FOLDER / "Q2_1z_windowed.npy")

Q1_3z_windowed = np.load(SAVE_FOLDER / "Q1_3z_windowed.npy")
Q2_3z_windowed = np.load(SAVE_FOLDER / "Q2_3z_windowed.npy")


Q1_lists = [
    [Q1_1x, Q1_1x_transformed, Q1_1x_windowed],
    [Q1_3x, Q1_3x_transformed, Q1_3x_windowed],
    [Q1_1z, Q1_1z_transformed, Q1_1z_windowed],
    [Q1_3z, Q1_3z_transformed, Q1_3z_windowed],
]

Q2_lists = [
    [Q2_1x, Q2_1x_transformed, Q2_1x_windowed],
    [Q2_3x, Q2_3x_transformed, Q2_3x_windowed],
    [Q2_1z, Q2_1z_transformed, Q2_1z_windowed],
    [Q2_3z, Q2_3z_transformed, Q2_3z_windowed],
]

# =========================
# Titles
# =========================
column_titles = [
    "Static model",
    "Active model",
    "Windowed fit"
]

row_titles = [
    r"$x_0$",
    r"$y_0$",
    r"$a$",
    r"$b$"
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
            s=1.5,
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
    "Q1-Q2 ellipse plots",
    fontsize=34,
    fontweight="bold",
    color="white"
)

plt.tight_layout(rect=[0, 0, 1, 0.96])

plt.savefig(
    "Q1_Q2_subplot_grid_transparent.png",
    dpi=300,
    bbox_inches="tight",
    transparent=True
)

plt.show()