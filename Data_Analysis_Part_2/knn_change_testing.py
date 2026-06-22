import numpy as np
import matplotlib.pyplot as plt

from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error

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

window_size = 500
step_size = 1

start = 0
length = 200000

best_k = 200
best_weights = "distance"
best_p = 1

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

print("counter:", counter)


# =========================
# Make X and y
# =========================

X = HoQIs[start:start + length] @ matrix_1x.T
y = parameters[:, :5]

# Make sure X and y have equal length
N = min(len(X), len(y))
X = X[:N]
y = y[:N]

print("X shape:", X.shape)
print("y shape:", y.shape)


# =========================
# Helper function
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

for test_start in range(train_size + gap, N - block_size, block_size):
    test_end = test_start + block_size

    X_test_block = X[test_start:test_end]
    y_test_block = y[test_start:test_end]

    # -------------------------
    # Fixed early model
    # -------------------------
    y_pred_fixed = fixed_model.predict(X_test_block)
    fixed_rmse = np.sqrt(mean_squared_error(y_test_block, y_pred_fixed))

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
# Poster summary metrics
# =========================

fixed_mean = np.mean(fixed_rmses)
local_mean = np.mean(local_rmses)
baseline_mean = np.mean(baseline_rmses)

fixed_std = np.std(fixed_rmses)
local_std = np.std(local_rmses)
baseline_std = np.std(baseline_rmses)

fixed_improvement = 100 * (1 - fixed_mean / baseline_mean)
local_improvement = 100 * (1 - local_mean / baseline_mean)

active_vs_passive = 100 * (1 - local_mean / fixed_mean)
local_better_blocks = 100 * np.mean(local_rmses < fixed_rmses)

print("\n================ POSTER RESULTS ================")

print(f"Baseline RMSE:        {baseline_mean:.5f} ± {baseline_std:.5f}")
print(f"Passive/static RMSE:  {fixed_mean:.5f} ± {fixed_std:.5f}")
print(f"Active/local RMSE:    {local_mean:.5f} ± {local_std:.5f}")

print("\nImprovement compared to baseline:")
print(f"Passive/static model: {fixed_improvement:.1f}% lower RMSE")
print(f"Active/local model:   {local_improvement:.1f}% lower RMSE")

print("\nActive vs passive:")
print(f"Active model has {active_vs_passive:.1f}% lower RMSE than passive model")
print(f"Active model is better in {local_better_blocks:.1f}% of test blocks")

print("\nRMSE per ellipse parameter:")
print("parameter | passive RMSE | active RMSE | active improvement")
for i, label in enumerate(labels):
    fixed_param = np.mean(fixed_rmse_per_param[:, i])
    local_param = np.mean(local_rmse_per_param[:, i])
    improvement = 100 * (1 - local_param / fixed_param)

    print(
        f"{label:8s} | "
        f"{fixed_param:.5f}      | "
        f"{local_param:.5f}    | "
        f"{improvement:6.1f}%"
    )

print("================================================")

exit()

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
# Plot 1: RMSE over time
# =========================

plt.figure(figsize=(8, 4))
plt.plot(block_starts, fixed_rmses, marker="o", label="Fixed early training")
plt.plot(block_starts, local_rmses, marker="o", label="Local recent training")
plt.plot(block_starts, baseline_rmses, marker="o", label="Baseline")
plt.xlabel("Start index of test block")
plt.ylabel("RMSE")
plt.title("KNN prediction error over time")
plt.legend()
plt.tight_layout()
plt.show()


# =========================
# Plot 2: Ratio fixed/local
# =========================

plt.figure(figsize=(8, 4))
plt.plot(block_starts, fixed_rmses / local_rmses, marker="o")
plt.axhline(1, linestyle="--")
plt.xlabel("Start index of test block")
plt.ylabel("Fixed RMSE / Local RMSE")
plt.title("Does local retraining improve prediction?")
plt.tight_layout()
plt.show()


# =========================
# Plot 3: RMSE per parameter
# =========================

x_pos = np.arange(len(labels))

plt.figure(figsize=(7, 4))
plt.bar(x_pos - 0.2, np.mean(fixed_rmse_per_param, axis=0), width=0.4, label="Fixed early")
plt.bar(x_pos + 0.2, np.mean(local_rmse_per_param, axis=0), width=0.4, label="Local recent")
plt.xticks(x_pos, labels)
plt.ylabel("RMSE")
plt.title("Average RMSE per parameter")
plt.legend()
plt.tight_layout()
plt.show()


# =========================
# Plot 4: Example prediction on last block
# =========================

example_start = block_starts[-1]
example_end = example_start + block_size

X_example = X[example_start:example_end]
y_example = y[example_start:example_end]

y_fixed_example = fixed_model.predict(X_example)

local_train_start = example_start - gap - block_size
local_train_end = example_start - gap

example_local_model = make_knn_model()
example_local_model.fit(X[local_train_start:local_train_end], y[local_train_start:local_train_end])
y_local_example = example_local_model.predict(X_example)

for i, label in enumerate(labels):
    plt.figure(figsize=(9, 3))
    plt.plot(y_example[:, i], label="Real")
    plt.plot(y_fixed_example[:, i], label="Fixed early prediction")
    plt.plot(y_local_example[:, i], label="Local recent prediction")
    plt.xlabel("Index within final test block")
    plt.ylabel(label)
    plt.title(f"Prediction example: {label}")
    plt.legend()
    plt.tight_layout()
    plt.show()