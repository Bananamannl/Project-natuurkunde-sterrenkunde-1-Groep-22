import numpy as np
import matplotlib.pyplot as plt

from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error

from matplotlib.ticker import MaxNLocator

from find_windows_interactive import *
from orthogonal_matrices import *


# =========================
# Load data
# =========================

HoQIs = np.load("Data_Analysis_Part_1\\HoQI_fitted_six_vct_list.npy")
Q1 = np.load("Data_Analysis_Part_1\\1xQ1.npy")
Q2 = np.load("Data_Analysis_Part_1\\1xQ2.npy")


# =========================
# Settings
# =========================

window_size = 250
step_size = 1

start = 0
length = 50000

best_k = 200
best_weights = "distance"
best_p = 1

train_size = 10000
block_size = 5000
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

print("counter:", counter)


# =========================
# Make X and y
# =========================

X = HoQIs[start:start + length] @ matrix_1x.T
y = parameters[:, :5]

N = min(len(X), len(y))
X = X[:N]
y = y[:N]

print("X shape:", X.shape)
print("y shape:", y.shape)


# =========================
# Helper function
# Exact same KNN model
# =========================

def make_knn_model():
    return make_pipeline(
        StandardScaler(),
        KNeighborsRegressor(
            n_neighbors=best_k,
            weights=best_weights,
            p=best_p
        )
    )


# =========================
# Fixed early model
# =========================

fixed_model = make_knn_model()
fixed_model.fit(X[:train_size], y[:train_size])


# =========================
# Test over later blocks
# =========================

block_starts = []
fixed_rmses = []
local_rmses = []
baseline_rmses = []

fixed_rmse_per_param = []
local_rmse_per_param = []

# Arrays waarin we alle testvoorspellingen opslaan
# Buiten de testblokken blijven ze NaN
y_pred_fixed_all = np.full_like(y, np.nan, dtype=float)
y_pred_local_all = np.full_like(y, np.nan, dtype=float)

for test_start in range(train_size + gap, N - block_size, block_size):
    test_end = test_start + block_size

    X_test_block = X[test_start:test_end]
    y_test_block = y[test_start:test_end]

    # -------------------------
    # Fixed early model
    # -------------------------
    y_pred_fixed = fixed_model.predict(X_test_block)
    fixed_rmse = np.sqrt(mean_squared_error(y_test_block, y_pred_fixed))

    y_pred_fixed_all[test_start:test_end] = y_pred_fixed

    # -------------------------
    # Local recent model
    # Train on block directly before test block
    # -------------------------
    local_train_start = test_start - gap - block_size
    local_train_end = test_start - gap

    X_local_train = X[local_train_start:local_train_end]
    y_local_train = y[local_train_start:local_train_end]

    local_model = make_knn_model()
    local_model.fit(X_local_train, y_local_train)

    y_pred_local = local_model.predict(X_test_block)
    local_rmse = np.sqrt(mean_squared_error(y_test_block, y_pred_local))

    y_pred_local_all[test_start:test_end] = y_pred_local

    # -------------------------
    # Baseline: mean of local training block
    # -------------------------
    baseline_pred = np.tile(
        np.mean(y_local_train, axis=0),
        (len(y_test_block), 1)
    )

    baseline_rmse = np.sqrt(mean_squared_error(y_test_block, baseline_pred))

    # -------------------------
    # Save results
    # -------------------------
    block_starts.append(test_start)
    fixed_rmses.append(fixed_rmse)
    local_rmses.append(local_rmse)
    baseline_rmses.append(baseline_rmse)

    fixed_rmse_per_param.append(
        np.sqrt(np.mean((y_test_block - y_pred_fixed) ** 2, axis=0))
    )

    local_rmse_per_param.append(
        np.sqrt(np.mean((y_test_block - y_pred_local) ** 2, axis=0))
    )


block_starts = np.array(block_starts)
fixed_rmses = np.array(fixed_rmses)
local_rmses = np.array(local_rmses)
baseline_rmses = np.array(baseline_rmses)

fixed_rmse_per_param = np.array(fixed_rmse_per_param)
local_rmse_per_param = np.array(local_rmse_per_param)


# =========================
# Print summary
# =========================

print("\nAverage RMSE:")
print("Fixed early model:", np.mean(fixed_rmses))
print("Local recent model:", np.mean(local_rmses))
print("Baseline:", np.mean(baseline_rmses))

print("\nImprovement compared to baseline:")
print("Fixed early model:", np.mean(baseline_rmses) / np.mean(fixed_rmses))
print("Local recent model:", np.mean(baseline_rmses) / np.mean(local_rmses))

print("\nRMSE per parameter, fixed early model:")
for label, value in zip(labels, np.mean(fixed_rmse_per_param, axis=0)):
    print(label, value)

print("\nRMSE per parameter, local recent model:")
for label, value in zip(labels, np.mean(local_rmse_per_param, axis=0)):
    print(label, value)


# =========================
# Main plot:
# One figure, all parameters underneath each other
# No error plot
# =========================

fig, axes = plt.subplots(
    len(labels), 1,
    figsize=(14, 11),
    sharex=True
)

x = np.arange(N)

for i, label in enumerate(labels):
    ax = axes[i]

    # Echte parameter
    ax.plot(
        x,
        y[:, i],
        linewidth=1.0,
        label="Window ellipse fitted"
    )

    # Fixed early KNN voorspelling
    ax.plot(
        x,
        y_pred_fixed_all[:, i],
        linewidth=1.1,
        label="Static kNN prediction model"
    )

    # Local recent KNN voorspelling
    ax.plot(
        x,
        y_pred_local_all[:, i],
        linewidth=1.0,
        alpha=0.75,
        label="Active kNN prediction model"
    )

    # Trainingsgebied aangeven
    ax.axvspan(
        0,
        train_size,
        alpha=0.12,
        label="Training data" if i == 0 else None
    )

    ax.set_ylabel(label)
    ax.yaxis.set_major_locator(MaxNLocator(nbins=3))

    ax.grid(alpha=0.25)

    if i == 0:
        ax.set_title(
            "Ellipse parameter predictions for static and active kNN models",
            fontsize=14,
            fontweight="bold"
        )

axes[-1].set_xlabel("datapunt / tijd")


# =========================
# One clean legend
# =========================

lines, legend_labels = axes[0].get_legend_handles_labels()

fig.legend(
    lines,
    legend_labels,
    loc="upper right",
    bbox_to_anchor=(0.98, 0.98)
)

plt.tight_layout(rect=[0, 0, 0.88, 0.96])
plt.show()