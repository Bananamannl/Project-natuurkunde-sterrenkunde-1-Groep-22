import numpy as np
import matplotlib.pyplot as plt

from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error

from ellipse_parameters import *


matrix_1z = np.array([
    [-2/3, 1/3, 1/3, 0, 0, 0],
    [0, -np.sqrt(1/3), np.sqrt(1/3), 0, 0, 0]
])

HoQIs = np.load("Data_Analysis_Part_1\\HoQI_fitted_six_vct_list.npy")
Q1 = np.load("Data_Analysis_Part_1\\1zQ1.npy")
Q2 = np.load("Data_Analysis_Part_1\\1zQ2.npy")

window_size = 100
step_size = 1

start = 0
length = 15000  # totaal stuk dat je gebruikt voor train/valid/test

parameters = parameters_timeseries(
    Q1[start:start + length + window_size - 1],
    Q2[start:start + length + window_size - 1],
    window_size=window_size,
    step_size=step_size
)

X = HoQIs[start:start + length] @ matrix_1z.T
y = parameters[:, :5]  # [x0, y0, a, b, theta]

print("X shape:", X.shape)
print("y shape:", y.shape)

gap = window_size

n = len(X)

train_end = int(0.6 * n)
valid_end = int(0.8 * n)

X_train = X[:train_end - gap]
y_train = y[:train_end - gap]

X_valid = X[train_end + gap:valid_end - gap]
y_valid = y[train_end + gap:valid_end - gap]

X_test = X[valid_end + gap:]
y_test = y[valid_end + gap:]

print(X_train.shape, y_train.shape)
print(X_valid.shape, y_valid.shape)
print(X_test.shape, y_test.shape)

results = []

for k in [1, 3, 5, 10, 20, 50, 100, 200]:
    for weights in ["uniform", "distance"]:
        for p in [1, 2]:

            model = make_pipeline(
                StandardScaler(),
                KNeighborsRegressor(
                    n_neighbors=k,
                    weights=weights,
                    p=p
                )
            )

            model.fit(X_train, y_train)
            y_valid_pred = model.predict(X_valid)

            mse = mean_squared_error(y_valid, y_valid_pred)
            rmse = np.sqrt(mse)

            results.append((mse, rmse, k, weights, p))

results = sorted(results, key=lambda x: x[0])

for mse, rmse, k, weights, p in results[:10]:
    print(f"k={k:3d}, weights={weights:8s}, p={p}, MSE={mse:.8e}, RMSE={rmse:.8e}")


#Hiermee is besloten dat de parameters: 
# k = 200
# weights = "distance"
# p = 1

best_k = 200
best_weights = "distance"
best_p = 1

# Train opnieuw op train + valid
X_train_final = X[:valid_end - gap]
y_train_final = y[:valid_end - gap]

final_model = make_pipeline(
    StandardScaler(),
    KNeighborsRegressor(
        n_neighbors=best_k,
        weights=best_weights,
        p=best_p
    )
)

final_model.fit(X_train_final, y_train_final)

# Voorspel testset
y_test_pred = final_model.predict(X_test)

# Test score
test_mse = mean_squared_error(y_test, y_test_pred)
test_rmse = np.sqrt(test_mse)

print("Test MSE:", test_mse)
print("Test RMSE:", test_rmse)

# RMSE per parameter
labels = ["x0", "y0", "a", "b", "theta"]

rmse_per_param = np.sqrt(np.mean((y_test - y_test_pred)**2, axis=0))

for label, rmse in zip(labels, rmse_per_param):
    print(label, rmse)

baseline_pred = np.tile(np.mean(y_train_final, axis=0), (len(y_test), 1))

baseline_mse = mean_squared_error(y_test, baseline_pred)
baseline_rmse = np.sqrt(baseline_mse)

print("KNN test MSE:", test_mse)
print("Baseline test MSE:", baseline_mse)
print("Improvement factor:", baseline_mse / test_mse)


labels = ["x0", "y0", "a", "b", "theta"]

for i, label in enumerate(labels):
    plt.figure(figsize=(10, 4))
    plt.plot(y_test[:, i], label="real")
    plt.plot(y_test_pred[:, i], label="KNN predicted")
    plt.xlabel("Test index")
    plt.ylabel(label)
    plt.title(f"KNN prediction on test set: {label}")
    plt.legend()
    plt.tight_layout()
    plt.show()