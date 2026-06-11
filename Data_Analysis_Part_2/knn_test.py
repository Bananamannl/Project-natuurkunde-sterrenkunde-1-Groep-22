import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from ellipse_parameters import *

####Let op, we beginnen met 1z!!!
matrix_1z = np.array([
    [-2/3, 1/3, 1/3, 0, 0, 0],
    [0, -np.sqrt(1/3), np.sqrt(1/3), 0, 0, 0]
])
HoQIs = np.load("Data_Analysis_Part_1\HoQI_fitted_six_vct_list.npy")
Q1, Q2 = np.load("Data_Analysis_Part_1\\1zQ1.npy"), np.load("Data_Analysis_Part_1\\1zQ2.npy")

orth_movement = HoQIs[:40000] @ matrix_1z.T

parameters = parameters_timeseries(Q1[:40099], Q2[:40099], window_size=100, step_size=1)

# X = input: displacements / HoQI vectors
X = orth_movement          # shape (N, 2)

# y = output: ellipse parameters
y = parameters[:, :5]     # shape (N, 5)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=False
)

model = make_pipeline(
    StandardScaler(),
    KNeighborsRegressor(n_neighbors=10, weights="distance")
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)


labels = ["x0", "y0", "a", "b", "theta"]

import matplotlib.pyplot as plt

labels = ["x0", "y0", "a", "b", "theta"]

param_index = 0  # verander naar 0 t/m 4

plt.figure(figsize=(5, 5))
plt.scatter(y_test[:, param_index], y_pred[:, param_index], s=5)

min_val = min(y_test[:, param_index].min(), y_pred[:, param_index].min())
max_val = max(y_test[:, param_index].max(), y_pred[:, param_index].max())

plt.plot([min_val, max_val], [min_val, max_val], linestyle="--")

plt.xlabel("Real")
plt.ylabel("Predicted")
plt.title(f"Real vs predicted: {labels[param_index]}")
plt.axis("equal")
plt.tight_layout()
plt.show()