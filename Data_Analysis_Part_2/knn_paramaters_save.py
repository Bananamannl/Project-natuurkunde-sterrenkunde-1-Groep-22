import numpy as np
from find_windows_interactive import *

Q1 = np.load("Data_Analysis_Part_1\\3xQ1.npy")
Q2 = np.load("Data_Analysis_Part_1\\3xQ2.npy")

window_size = 500
step_size = 1

start = 0
length = 200000

train_size = 20000
block_size = 10000
gap = window_size

labels = ["x0", "y0", "a", "b", "theta"]


# =========================
# Get ellipse parameters
# =========================

parameters, counter = parameters_timeseries_interactive(
    Q1[start:start + length + window_size - 1],
    Q2[start:start + length + window_size - 1],
    window_size=window_size,
    step_size=step_size
)

np.save("parameters_for_knn_test_3x.npy", parameters)