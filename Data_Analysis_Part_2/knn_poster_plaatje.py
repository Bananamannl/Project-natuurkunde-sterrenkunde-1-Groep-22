import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path
from matplotlib.ticker import MaxNLocator

from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error

from orthogonal_matrices import *


# ============================================================
# Settings
# ============================================================



window_size = 500
start = 0
length = 200000

gap = window_size
block_size = 10000

labels = ["x0", "y0", "a", "b", "theta"]

# Hyperparameter search
k_values = [20, 50, 100, 200, 500]
weight_values = ["uniform", "distance"]
p_values = [1, 2]

# Data used to choose kNN hyperparameters
opt_train_size = 20000
opt_valid_size = block_size

# Training-size comparison
passive_train_sizes_to_test = [10000, 20000, 40000, 80000]
active_train_sizes_to_test = [5000, 10000, 20000, 40000, 80000]

# Output
save_figure = True
figure_name = "knn_poster_predictions.png"


# ============================================================
# Helper functions
# ============================================================

def make_knn_model(k, weights, p):
    return make_pipeline(
        StandardScaler(),
        KNeighborsRegressor(
            n_neighbors=k,
            weights=weights,
            p=p
        )
    )


def rmse(y_true, y_pred):
    return np.sqrt(mean_squared_error(y_true, y_pred))

def test_center_shifts():
    shifts_to_test = range(0, window_size + 1, 50)

    results = []

    print("\n================ CENTER SHIFT TEST ================")

    for shift in shifts_to_test:
        X_shift, y_shift = load_and_align_data(shift)

        valid_start = opt_train_size + gap
        valid_end = valid_start + opt_valid_size

        X_train = X_shift[:opt_train_size]
        y_train = y_shift[:opt_train_size]

        X_valid = X_shift[valid_start:valid_end]
        y_valid = y_shift[valid_start:valid_end]

        model = make_knn_model(
            k=200,
            weights="distance",
            p=1
        )

        model.fit(X_train, y_train)
        y_pred = model.predict(X_valid)

        shift_rmse = rmse(y_valid, y_pred)

        results.append((shift_rmse, shift))

        print(f"center_shift = {shift:4d} | validation RMSE = {shift_rmse:.6f}")

    results = sorted(results, key=lambda row: row[0])

    best_rmse, best_shift = results[0]

    print("\nBest center shift:")
    print(f"center_shift = {best_shift}")
    print(f"validation RMSE = {best_rmse:.6f}")
    print("===================================================")

    return best_shift

def load_and_align_data(center_shift):
    HoQIs = np.load(r"C:\Users\timob\OneDrive - UvA\Project 1\GitHub Map\Project-natuurkunde-sterrenkunde-1-Groep-22\Data_Analysis_Part_1\fitted_six_vct_list.npy")
    parameters = np.load(r"param_timeseries_3z_step_size_10_window_size_500.npy")
    parameters = np.repeat(parameters, 10, axis=0)

    parameters = parameters[:length]

    y = parameters[:, :5]

    X = HoQIs[
        start + center_shift : start + center_shift + len(y)
    ] @ matrix_3z.T

    N = min(len(X), len(y))
    X = X[:N]
    y = y[:N]

    return X, y


def optimize_knn_parameters(X, y):
    valid_start = opt_train_size + gap
    valid_end = valid_start + opt_valid_size

    if valid_end > len(X):
        raise ValueError("Not enough data for hyperparameter optimization.")

    X_train = X[:opt_train_size]
    y_train = y[:opt_train_size]

    X_valid = X[valid_start:valid_end]
    y_valid = y[valid_start:valid_end]

    results = []

    for k in k_values:
        for weights in weight_values:
            for p in p_values:
                model = make_knn_model(k, weights, p)
                model.fit(X_train, y_train)

                y_pred = model.predict(X_valid)

                mse = mean_squared_error(y_valid, y_pred)
                value_rmse = np.sqrt(mse)

                results.append((mse, value_rmse, k, weights, p))

    results = sorted(results, key=lambda row: row[0])

    print("\n================ BEST kNN PARAMETERS ================")
    for mse, value_rmse, k, weights, p in results[:5]:
        print(
            f"k={k:3d}, weights={weights:8s}, p={p}, "
            f"MSE={mse:.8e}, RMSE={value_rmse:.8e}"
        )

    best_mse, best_rmse, best_k, best_weights, best_p = results[0]

    print("\nChosen:")
    print(f"best_k       = {best_k}")
    print(f"best_weights = {best_weights}")
    print(f"best_p       = {best_p}")
    print("=====================================================")

    return best_k, best_weights, best_p


def get_common_test_start(X):
    valid_start = opt_train_size + gap
    valid_end = valid_start + opt_valid_size

    max_passive_train = max(passive_train_sizes_to_test)
    max_active_train = max(active_train_sizes_to_test)

    common_test_start = max(
        valid_end + gap,
        max_passive_train + gap,
        max_active_train + gap
    )

    if common_test_start + block_size > len(X):
        raise ValueError("Not enough data left for common test blocks.")

    return common_test_start


def test_passive_train_sizes(X, y, best_k, best_weights, best_p, common_test_start):
    results = []

    for train_size in passive_train_sizes_to_test:
        model = make_knn_model(best_k, best_weights, best_p)
        model.fit(X[:train_size], y[:train_size])

        rmses = []

        for test_start in range(common_test_start, len(X) - block_size + 1, block_size):
            test_end = test_start + block_size

            y_pred = model.predict(X[test_start:test_end])
            value_rmse = rmse(y[test_start:test_end], y_pred)

            rmses.append(value_rmse)

        results.append({
            "train_size": train_size,
            "rmse_mean": np.mean(rmses),
            "rmse_std": np.std(rmses)
        })

    print("\n================ PASSIVE TRAIN SIZE TEST ================")
    print("train_size | passive RMSE")
    for row in results:
        print(
            f"{row['train_size']:10d} | "
            f"{row['rmse_mean']:.5f} ± {row['rmse_std']:.5f}"
        )
    print("=========================================================")

    best_row = min(results, key=lambda row: row["rmse_mean"])
    return best_row["train_size"]


def test_active_train_sizes(X, y, best_k, best_weights, best_p, common_test_start):
    results = []

    for local_train_size in active_train_sizes_to_test:
        active_rmses = []
        baseline_rmses = []

        for test_start in range(common_test_start, len(X) - block_size + 1, block_size):
            test_end = test_start + block_size

            local_train_start = test_start - gap - local_train_size
            local_train_end = test_start - gap

            X_local_train = X[local_train_start:local_train_end]
            y_local_train = y[local_train_start:local_train_end]

            local_model = make_knn_model(best_k, best_weights, best_p)
            local_model.fit(X_local_train, y_local_train)

            y_pred = local_model.predict(X[test_start:test_end])
            active_rmse = rmse(y[test_start:test_end], y_pred)

            baseline_pred = np.tile(
                np.mean(y_local_train, axis=0),
                (block_size, 1)
            )
            baseline_rmse = rmse(y[test_start:test_end], baseline_pred)

            active_rmses.append(active_rmse)
            baseline_rmses.append(baseline_rmse)

        active_mean = np.mean(active_rmses)
        baseline_mean = np.mean(baseline_rmses)

        active_improvement = 100 * (1 - active_mean / baseline_mean)

        results.append({
            "local_train_size": local_train_size,
            "active_rmse_mean": active_mean,
            "active_rmse_std": np.std(active_rmses),
            "baseline_rmse_mean": baseline_mean,
            "baseline_rmse_std": np.std(baseline_rmses),
            "active_improvement": active_improvement
        })

    print("\n================ ACTIVE TRAIN SIZE TEST ================")
    print("local_train_size | baseline RMSE | active RMSE | improvement")
    for row in results:
        print(
            f"{row['local_train_size']:16d} | "
            f"{row['baseline_rmse_mean']:.5f} ± {row['baseline_rmse_std']:.5f} | "
            f"{row['active_rmse_mean']:.5f} ± {row['active_rmse_std']:.5f} | "
            f"{row['active_improvement']:6.1f}%"
        )
    print("========================================================")

    best_row = min(results, key=lambda row: row["active_rmse_mean"])
    return best_row["local_train_size"]


def evaluate_final_models(
    X,
    y,
    best_k,
    best_weights,
    best_p,
    passive_train_size,
    active_train_size,
    first_test_start
):
    passive_model = make_knn_model(best_k, best_weights, best_p)
    passive_model.fit(X[:passive_train_size], y[:passive_train_size])

    block_starts = []

    passive_rmses = []
    active_rmses = []
    baseline_rmses = []

    passive_rmse_per_param = []
    active_rmse_per_param = []

    y_pred_passive_all = np.full_like(y, np.nan, dtype=float)
    y_pred_active_all = np.full_like(y, np.nan, dtype=float)

    for test_start in range(first_test_start, len(X) - block_size + 1, block_size):
        test_end = test_start + block_size

        X_test = X[test_start:test_end]
        y_test = y[test_start:test_end]

        # Passive/static model
        y_pred_passive = passive_model.predict(X_test)
        passive_value_rmse = rmse(y_test, y_pred_passive)

        y_pred_passive_all[test_start:test_end] = y_pred_passive

        # Active/local model
        local_train_start = test_start - gap - active_train_size
        local_train_end = test_start - gap

        X_local_train = X[local_train_start:local_train_end]
        y_local_train = y[local_train_start:local_train_end]

        active_model = make_knn_model(best_k, best_weights, best_p)
        active_model.fit(X_local_train, y_local_train)

        y_pred_active = active_model.predict(X_test)
        active_value_rmse = rmse(y_test, y_pred_active)

        y_pred_active_all[test_start:test_end] = y_pred_active

        # Baseline: mean of recent local training block
        baseline_pred = np.tile(
            np.mean(y_local_train, axis=0),
            (len(y_test), 1)
        )
        baseline_value_rmse = rmse(y_test, baseline_pred)

        block_starts.append(test_start)

        passive_rmses.append(passive_value_rmse)
        active_rmses.append(active_value_rmse)
        baseline_rmses.append(baseline_value_rmse)

        passive_rmse_per_param.append(
            np.sqrt(np.mean((y_test - y_pred_passive) ** 2, axis=0))
        )
        active_rmse_per_param.append(
            np.sqrt(np.mean((y_test - y_pred_active) ** 2, axis=0))
        )

    return {
        "block_starts": np.array(block_starts),
        "passive_rmses": np.array(passive_rmses),
        "active_rmses": np.array(active_rmses),
        "baseline_rmses": np.array(baseline_rmses),
        "passive_rmse_per_param": np.array(passive_rmse_per_param),
        "active_rmse_per_param": np.array(active_rmse_per_param),
        "y_pred_passive_all": y_pred_passive_all,
        "y_pred_active_all": y_pred_active_all
    }


def print_final_summary(results, best_k, best_weights, best_p, passive_train_size, active_train_size):
    passive_rmses = results["passive_rmses"]
    active_rmses = results["active_rmses"]
    baseline_rmses = results["baseline_rmses"]

    passive_rmse_per_param = results["passive_rmse_per_param"]
    active_rmse_per_param = results["active_rmse_per_param"]

    passive_mean, passive_std = np.mean(passive_rmses), np.std(passive_rmses)
    active_mean, active_std = np.mean(active_rmses), np.std(active_rmses)
    baseline_mean, baseline_std = np.mean(baseline_rmses), np.std(baseline_rmses)

    passive_improvement = 100 * (1 - passive_mean / baseline_mean)
    active_improvement = 100 * (1 - active_mean / baseline_mean)

    active_vs_passive = 100 * (1 - active_mean / passive_mean)
    active_better_blocks = 100 * np.mean(active_rmses < passive_rmses)

    print("\n================ SUMMARY ================")

    print(
        f"kNN: k={best_k}, weights={best_weights}, p={best_p} | "
        f"blocks={len(passive_rmses)}, block_size={block_size}"
    )

    print(
        f"Training: passive={passive_train_size}, "
        f"active/local={active_train_size}, gap={gap}"
    )

    print("\nRMSE over test blocks:")
    print(f"Baseline : {baseline_mean:.5f} ± {baseline_std:.5f}")
    print(f"Passive  : {passive_mean:.5f} ± {passive_std:.5f}  ({passive_improvement:.1f}% lower than baseline)")
    print(f"Active   : {active_mean:.5f} ± {active_std:.5f}  ({active_improvement:.1f}% lower than baseline)")

    print("\nActive vs passive:")
    print(f"RMSE difference: {active_vs_passive:.1f}%")
    print(f"Active better in {active_better_blocks:.1f}% of test blocks")

    print("\nPer parameter RMSE, passive -> active:")
    for i, label in enumerate(labels):
        passive_param = np.mean(passive_rmse_per_param[:, i])
        active_param = np.mean(active_rmse_per_param[:, i])
        improvement = 100 * (1 - active_param / passive_param)

        print(
            f"{label:5s}: "
            f"{passive_param:.5f} -> {active_param:.5f} "
            f"({improvement:+.1f}%)"
        )

    print("=========================================\n")


def plot_poster_figure(X, y, center_shift, results, passive_train_size):
    y_pred_passive_all = results["y_pred_passive_all"]
    y_pred_active_all = results["y_pred_active_all"]

    fig, axes = plt.subplots(
        len(labels),
        1,
        figsize=(14, 11),
        sharex=True
    )

    x = np.arange(len(X)) + center_shift

    image_format_data = {
        "x": x,
        "y_true": y,
        "y_pred_passive": y_pred_passive_all,
        "y_pred_active": y_pred_active_all,
        "labels": np.array(labels),
        "center_shift": center_shift,
        "passive_train_size": passive_train_size,
    }

    # np.save("knn_plot_3x.npy", image_format_data)
    # print("\nSaved plot data as: knn_plot_3x.npy")

    for i, label in enumerate(labels):
        ax = axes[i]

        ax.plot(
            x,
            y[:, i],
            linewidth=1.0,
            label="Window ellipse fit"
        )

        ax.plot(
            x,
            y_pred_passive_all[:, i],
            linewidth=1.1,
            label="Passive/static kNN"
        )

        ax.plot(
            x,
            y_pred_active_all[:, i],
            linewidth=1.0,
            alpha=0.75,
            label="Active/local kNN"
        )

        ax.axvspan(
            center_shift,
            center_shift + passive_train_size,
            alpha=0.12,
            label="Passive training data" if i == 0 else None
        )

        ax.set_ylabel(label)
        ax.yaxis.set_major_locator(MaxNLocator(nbins=3))
        ax.grid(alpha=0.25)

        if i == 0:
            ax.set_title(
                "Ellipse parameter predictions for passive and active kNN models",
                fontsize=14,
                fontweight="bold"
            )

    axes[-1].set_xlabel("Datapoint / time")

    lines, legend_labels = axes[0].get_legend_handles_labels()

    fig.legend(
        lines,
        legend_labels,
        loc="upper right",
        bbox_to_anchor=(0.98, 0.98)
    )

    plt.tight_layout(rect=[0, 0, 0.88, 0.96])

    if save_figure:
        plt.savefig(
            figure_name,
            dpi=300,
            bbox_inches="tight"
        )
        print(f"\nSaved figure as: {figure_name}")

    plt.show()


# ============================================================
# Main script
# ============================================================

center_shift = test_center_shifts()

X, y = load_and_align_data(center_shift)

print("\n================ DATA ================")
print("chosen center shift:", center_shift)
print("X shape:", X.shape)
print("y shape:", y.shape)
print("======================================")

best_k, best_weights, best_p = optimize_knn_parameters(X, y)

common_test_start = get_common_test_start(X)

best_passive_train_size = test_passive_train_sizes(
    X,
    y,
    best_k,
    best_weights,
    best_p,
    common_test_start
)

best_active_train_size = test_active_train_sizes(
    X,
    y,
    best_k,
    best_weights,
    best_p,
    common_test_start
)


final_results = evaluate_final_models(
    X,
    y,
    best_k,
    best_weights,
    best_p,
    passive_train_size=best_passive_train_size,
    active_train_size=best_active_train_size,
    first_test_start=common_test_start
)

print_final_summary(
    final_results,
    best_k,
    best_weights,
    best_p,
    best_passive_train_size,
    best_active_train_size
)

plot_poster_figure(
    X,
    y,
    center_shift,
    final_results,
    best_passive_train_size
)