import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from ellipse_parameters import *
import matplotlib.pyplot as plt
from orthogonal_matrices import *


HoQIs = np.load("Data_Analysis_Part_1\HoQI_fitted_six_vct_list.npy")
Q1, Q2 = np.load("Data_Analysis_Part_1\\1zQ1.npy"), np.load("Data_Analysis_Part_1\\1zQ2.npy")

train_start = 0
train_lenght = 10000


training_parameters = parameters_timeseries(Q1[train_start:train_start + train_lenght + 99], 
                                            Q2[train_start:train_start + train_lenght + 99], 
                                            window_size=100, 
                                            step_size=1)

orth_movement_train = HoQIs[train_start:train_start + train_lenght] @ matrix_1z.T

# X = input: displacements / HoQI vectors
X = orth_movement_train          # shape (N, 2)

# y = output: ellipse parameters
y = training_parameters[:, :5]     # shape (N, 5)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=False
)

model = make_pipeline(
    StandardScaler(),
    KNeighborsRegressor(
        n_neighbors=200,
        weights="distance",
        p=1
    )
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)


###Voor als we willen plotten
labels = ["x0", "y0", "a", "b", "theta"]

param_index = 0  # 0=x0, 1=y0, 2=a, 3=b, 4=theta

plt.figure(figsize=(10, 4))
plt.plot(y_test[:, param_index], label="real")
plt.plot(y_pred[:, param_index], label="KNN predicted")
plt.xlabel("Test index")
plt.ylabel(labels[param_index])
plt.title(f"KNN prediction for {labels[param_index]}")
plt.legend()
plt.tight_layout()
plt.show()