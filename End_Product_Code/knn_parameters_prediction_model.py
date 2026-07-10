"""
Clean kNN analysis script for ellipse-parameter prediction.

This script:
1. Loads HoQI displacement data and fitted ellipse parameters.
2. Aligns both arrays using a configurable center shift.
3. Searches for the best kNN hyperparameters.
4. Compares passive/static and active/local kNN training sizes.
5. Evaluates the final passive and active models on common test blocks.
6. Saves and plots the predicted ellipse parameters.

Ellipse-parameter order:
[x0, y0, a, b, theta]
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator
from scipy.optimize import least_squares
from sklearn.metrics import mean_squared_error
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

import orthogonal_matrices as om


# ============================================================
# User settings
# ============================================================

# Choose which HoQI direction to analyse: "1x", "2x", "3x", "1z", "2z", or "3z".
SELECTED_HOQI = "3z"

# HoQI order used in raw_Q1_data.npy and raw_Q2_data.npy.
HOQI_NAMES = ("1x", "2x", "3x", "1z", "2z", "3z")

# Number of fitted parameter vectors to save per HoQI.
# With step_size = 1, this is also the number of time steps available for y.
LENGTH = 200_000
PARAMETER_TIMESERIES_LENGTH = LENGTH

# Main data settings.
START = 0
BLOCK_SIZE = 10_000

# Ellipse fitting settings for the six HoQIs, in the order:
# [1x, 2x, 3x, 1z, 2z, 3z]
PARAMETER_STEP_SIZE = 1
PARAMETER_WINDOW_SIZE_VALUES = [500, 500, 500, 300, 500, 300]
PARAMETER_WINDOW_SIZES_BY_HOQI = dict(zip(HOQI_NAMES, PARAMETER_WINDOW_SIZE_VALUES))

# The selected window size is also used as the train/test gap.
WINDOW_SIZE = PARAMETER_WINDOW_SIZES_BY_HOQI[SELECTED_HOQI]
GAP = WINDOW_SIZE

# If True, the script checks whether all parameter-timeseries files exist.
# Missing files are generated automatically before the kNN analysis starts.
GENERATE_PARAMETER_TIMESERIES_FILES = True

# Keep this False for normal use, so existing .npy files are not recalculated every run.
# Set this to True when you change PARAMETER_TIMESERIES_LENGTH, step size, or window sizes.
OVERWRITE_PARAMETER_TIMESERIES_FILES = False

# Ellipse-parameter labels. Keep this order fixed throughout the script.
PARAMETER_LABELS = ["x0", "y0", "a", "b", "theta"]

# File locations. Adjust BASE_DIR if your files are stored somewhere else.
BASE_DIR = Path(
    r"C:\Users\timob\OneDrive - UvA\Project 1\GitHub Map"
    r"\Project-natuurkunde-sterrenkunde-1-Groep-22"
)

HOQI_FILE = BASE_DIR / "Data_Analysis_Part_1" / "fitted_six_vct_list.npy"

# These raw Q files are needed only when parameter-timeseries files must be generated.
PARAMETER_OUTPUT_DIR = BASE_DIR / "End_Product_Code"
RAW_Q1_FILE = PARAMETER_OUTPUT_DIR / "raw_Q1_data.npy"
RAW_Q2_FILE = PARAMETER_OUTPUT_DIR / "raw_Q2_data.npy"


def get_parameter_file(hoqi_name: str) -> Path:
    """Return the parameter-timeseries file for one HoQI."""
    return PARAMETER_OUTPUT_DIR / f"parameter_timeseries_step_{PARAMETER_STEP_SIZE}_{hoqi_name}.npy"


# Hyperparameter search settings.
K_VALUES = [20, 50, 100, 200, 500]
WEIGHT_VALUES = ["uniform", "distance"]
P_VALUES = [1, 2]

# Validation data used during hyperparameter and center-shift selection.
OPT_TRAIN_SIZE = 20_000
OPT_VALID_SIZE = BLOCK_SIZE

# Training sizes tested for the passive/static and active/local models.
PASSIVE_TRAIN_SIZES_TO_TEST = [10_000, 20_000, 40_000, 80_000]
ACTIVE_TRAIN_SIZES_TO_TEST = [5_000, 10_000, 20_000, 40_000, 80_000]

# Output settings.
SAVE_FIGURE = True
FIGURE_FILE = Path(f"knn_poster_predictions_{SELECTED_HOQI}.png")

SAVE_PLOT_DATA = False
PLOT_DATA_FILE = Path(f"knn_plot_data_{SELECTED_HOQI}.npy")


# ============================================================
# HoQI transformation matrices
# ============================================================

HOQI_MATRIX_BY_NAME = {
    "1x": om.matrix_1x,
    "2x": om.matrix_2x,
    "3x": om.matrix_3x,
    "1z": om.matrix_1z,
    "2z": om.matrix_2z,
    "3z": om.matrix_3z,
}


# ============================================================
# Model and metric helpers
# ============================================================


def make_knn_model(k: int, weights: str, p: int):
    """Create a scaled kNN regression model."""
    return make_pipeline(
        StandardScaler(),
        KNeighborsRegressor(
            n_neighbors=k,
            weights=weights,
            p=p,
        ),
    )


def rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Calculate the root mean squared error over all output parameters."""
    return float(np.sqrt(mean_squared_error(y_true, y_pred)))


def rmse_per_parameter(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    """Calculate the RMSE separately for [x0, y0, a, b, theta]."""
    return np.sqrt(np.mean((y_true - y_pred) ** 2, axis=0))




# ============================================================
# Ellipse fitting and parameter-file generation
# ============================================================


def ellipse_residuals(params: np.ndarray, x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """
    Residual for a rotated ellipse.

    Parameter order:
    [x0, y0, a, b, theta]
    """
    x0, y0, a, b, theta = params

    xp = (x - x0) * np.cos(theta) + (y - y0) * np.sin(theta)
    yp = -(x - x0) * np.sin(theta) + (y - y0) * np.cos(theta)

    return xp**2 / a**2 + yp**2 / b**2 - 1


def fit_ellipse_parameters(
    q1_window: np.ndarray,
    q2_window: np.ndarray,
    start_parameters: np.ndarray,
) -> tuple[np.ndarray | None, np.ndarray]:
    """
    Fit one ellipse window.

    Returns
    -------
    fitted_parameters:
        The fitted [x0, y0, a, b, theta] vector, or None if the fit failed.
    next_start_parameters:
        The parameter vector used as the starting point for the next window.
    """
    try:
        fit = least_squares(
            ellipse_residuals,
            x0=start_parameters,
            args=(q1_window, q2_window),
        )

        if not fit.success:
            return None, start_parameters

        fitted_parameters = fit.x.copy()

        # Keep the ellipse axes positive and theta in a fixed interval.
        fitted_parameters[2] = abs(fitted_parameters[2])
        fitted_parameters[3] = abs(fitted_parameters[3])
        fitted_parameters[4] = fitted_parameters[4] % np.pi

        return fitted_parameters, fitted_parameters

    except ValueError:
        return None, start_parameters


def calculate_parameter_timeseries(
    q1: np.ndarray,
    q2: np.ndarray,
    window_size: int,
    step_size: int = PARAMETER_STEP_SIZE,
) -> np.ndarray:
    """
    Calculate a sliding-window ellipse-parameter timeseries.

    With step_size = 1, the output contains one parameter vector for each
    possible window start:
        len(output) = len(q1) - window_size + 1

    Each row has the order:
        [x0, y0, a, b, theta]
    """
    if len(q1) != len(q2):
        raise ValueError("q1 and q2 must have the same length.")

    if len(q1) < window_size:
        raise ValueError("Not enough Q1/Q2 points for the chosen window size.")

    parameter_vectors = []
    current_start_parameters = np.array([0, 0, 1, 1, 0], dtype=float)

    for start_index in range(0, len(q1) - window_size + 1, step_size):
        current_window_size = window_size

        while True:
            end_index = start_index + current_window_size

            if end_index > len(q1):
                print(f"No larger window available at start_index={start_index}.")
                break

            q1_window = q1[start_index:end_index]
            q2_window = q2[start_index:end_index]

            fitted_vector, next_start_parameters = fit_ellipse_parameters(
                q1_window=q1_window,
                q2_window=q2_window,
                start_parameters=current_start_parameters,
            )

            if fitted_vector is None:
                current_window_size += 50
                continue

            fitted_vector = np.ravel(fitted_vector)

            # After the first fit, reject sudden jumps in x0, y0, a, and b.
            # If the jump is too large, try again with a slightly larger window.
            if parameter_vectors:
                allowed_jump = np.array([0.2, 0.2, 0.5, 0.5])

                lower_bounds = current_start_parameters[:4] - allowed_jump
                upper_bounds = current_start_parameters[:4] + allowed_jump

                lower_bounds[2] = max(lower_bounds[2], 0.001)
                lower_bounds[3] = max(lower_bounds[3], 0.001)

                too_low = fitted_vector[:4] < lower_bounds
                too_high = fitted_vector[:4] > upper_bounds

                if np.any(too_low) or np.any(too_high):
                    current_window_size += 50
                    print(
                        f"Fit jump too large at start_index={start_index}; "
                        f"trying window_size={current_window_size}."
                    )
                    continue

            current_start_parameters = next_start_parameters
            parameter_vectors.append(fitted_vector)
            break

    return np.array(parameter_vectors)


def save_all_parameter_timeseries_files() -> None:
    """
    Save parameter-timeseries files for all six HoQIs.

    Output filenames:
        parameter_timeseries_step_1_1x.npy
        parameter_timeseries_step_1_2x.npy
        parameter_timeseries_step_1_3x.npy
        parameter_timeseries_step_1_1z.npy
        parameter_timeseries_step_1_2z.npy
        parameter_timeseries_step_1_3z.npy
    """
    PARAMETER_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if not RAW_Q1_FILE.exists() or not RAW_Q2_FILE.exists():
        raise FileNotFoundError(
            "Cannot generate parameter timeseries because raw_Q1_data.npy and/or "
            "raw_Q2_data.npy were not found. First create these files, or set "
            "GENERATE_PARAMETER_TIMESERIES_FILES = False if the parameter files already exist."
        )

    q1_list = np.load(RAW_Q1_FILE)
    q2_list = np.load(RAW_Q2_FILE)

    if q1_list.shape[0] < len(HOQI_NAMES) or q2_list.shape[0] < len(HOQI_NAMES):
        raise ValueError("raw_Q1_data.npy and raw_Q2_data.npy must contain six HoQI rows.")

    for row_index, hoqi_name in enumerate(HOQI_NAMES):
        output_file = get_parameter_file(hoqi_name)

        if output_file.exists() and not OVERWRITE_PARAMETER_TIMESERIES_FILES:
            print(f"Parameter file already exists, skipping: {output_file.name}")
            continue

        window_size = PARAMETER_WINDOW_SIZES_BY_HOQI[hoqi_name]

        # To save exactly PARAMETER_TIMESERIES_LENGTH parameter vectors with step_size = 1,
        # we need this many raw Q1/Q2 points:
        required_raw_points = PARAMETER_TIMESERIES_LENGTH + window_size - 1

        if q1_list.shape[1] < required_raw_points or q2_list.shape[1] < required_raw_points:
            raise ValueError(
                f"Not enough raw Q1/Q2 points for {hoqi_name}. "
                f"Need {required_raw_points}, but got "
                f"Q1={q1_list.shape[1]} and Q2={q2_list.shape[1]}."
            )

        print(
            f"\nSaving parameter timeseries for {hoqi_name}: "
            f"step_size={PARAMETER_STEP_SIZE}, window_size={window_size}, "
            f"length={PARAMETER_TIMESERIES_LENGTH}"
        )

        q1 = q1_list[row_index, :required_raw_points]
        q2 = q2_list[row_index, :required_raw_points]

        parameter_timeseries = calculate_parameter_timeseries(
            q1=q1,
            q2=q2,
            window_size=window_size,
            step_size=PARAMETER_STEP_SIZE,
        )

        parameter_timeseries = parameter_timeseries[:PARAMETER_TIMESERIES_LENGTH]

        np.save(output_file, parameter_timeseries)
        print(f"Saved: {output_file}")


def ensure_parameter_timeseries_files() -> None:
    """Generate missing parameter-timeseries files before the kNN analysis starts."""
    if not GENERATE_PARAMETER_TIMESERIES_FILES:
        return

    missing_files = [
        get_parameter_file(hoqi_name)
        for hoqi_name in HOQI_NAMES
        if not get_parameter_file(hoqi_name).exists()
    ]

    if not missing_files and not OVERWRITE_PARAMETER_TIMESERIES_FILES:
        print("\nAll parameter-timeseries files already exist.")
        return

    save_all_parameter_timeseries_files()


# ============================================================
# Data loading and alignment
# ============================================================


def get_hoqi_matrix(hoqi_name: str) -> np.ndarray:
    """Return the 2D transformation matrix for the selected HoQI."""
    if hoqi_name not in HOQI_MATRIX_BY_NAME:
        valid_names = ", ".join(HOQI_MATRIX_BY_NAME)
        raise ValueError(f"Unknown HoQI '{hoqi_name}'. Choose one of: {valid_names}.")

    return HOQI_MATRIX_BY_NAME[hoqi_name]


def load_and_align_data(center_shift: int) -> tuple[np.ndarray, np.ndarray]:
    """
    Load HoQI data and the automatically generated ellipse parameters.

    The parameter-timeseries files are saved with step_size = 1, so the
    parameter array already has datapoint-level spacing and does not need
    to be repeated.
    """
    hoqis = np.load(HOQI_FILE)

    parameter_file = get_parameter_file(SELECTED_HOQI)
    if not parameter_file.exists():
        raise FileNotFoundError(
            f"Parameter file not found: {parameter_file}. "
            "Run the script with GENERATE_PARAMETER_TIMESERIES_FILES = True."
        )

    parameters = np.load(parameter_file)
    parameters = parameters[:LENGTH]

    # Use only the five ellipse parameters: [x0, y0, a, b, theta].
    y = parameters[:, :5]

    # Transform the six HoQI signals to the selected 2D HoQI plane.
    matrix = get_hoqi_matrix(SELECTED_HOQI)
    x_start = START + center_shift
    x_end = x_start + len(y)
    X = hoqis[x_start:x_end] @ matrix.T

    # Keep only the shared length in case one array is slightly shorter.
    n_samples = min(len(X), len(y))
    X = X[:n_samples]
    y = y[:n_samples]

    if len(X) == 0:
        raise ValueError("No aligned samples found. Check START, LENGTH, and center_shift.")

    return X, y

# ============================================================
# Selection steps
# ============================================================


def get_validation_split(X: np.ndarray, y: np.ndarray):
    """Create a fixed train/validation split with a gap in between."""
    valid_start = OPT_TRAIN_SIZE + GAP
    valid_end = valid_start + OPT_VALID_SIZE

    if valid_end > len(X):
        raise ValueError("Not enough data for the validation split.")

    X_train = X[:OPT_TRAIN_SIZE]
    y_train = y[:OPT_TRAIN_SIZE]
    X_valid = X[valid_start:valid_end]
    y_valid = y[valid_start:valid_end]

    return X_train, y_train, X_valid, y_valid


def find_best_center_shift() -> int:
    """Test several center shifts and return the shift with the lowest validation RMSE."""
    shifts_to_test = range(0, WINDOW_SIZE + 1, 50)
    results = []

    print("\n================ CENTER SHIFT TEST ================")

    for shift in shifts_to_test:
        X_shift, y_shift = load_and_align_data(center_shift=shift)
        X_train, y_train, X_valid, y_valid = get_validation_split(X_shift, y_shift)

        # Fixed model used only to compare center shifts fairly.
        model = make_knn_model(k=200, weights="distance", p=1)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_valid)
        validation_rmse = rmse(y_valid, y_pred)

        results.append((validation_rmse, shift))
        print(f"center_shift = {shift:4d} | validation RMSE = {validation_rmse:.6f}")

    best_rmse, best_shift = min(results, key=lambda row: row[0])

    print("\nBest center shift:")
    print(f"center_shift = {best_shift}")
    print(f"validation RMSE = {best_rmse:.6f}")
    print("===================================================")

    return best_shift


def optimize_knn_parameters(X: np.ndarray, y: np.ndarray) -> tuple[int, str, int]:
    """Search over k, weights, and p, then return the best kNN settings."""
    X_train, y_train, X_valid, y_valid = get_validation_split(X, y)
    results = []

    for k in K_VALUES:
        for weights in WEIGHT_VALUES:
            for p in P_VALUES:
                model = make_knn_model(k=k, weights=weights, p=p)
                model.fit(X_train, y_train)

                y_pred = model.predict(X_valid)
                mse = mean_squared_error(y_valid, y_pred)
                validation_rmse = np.sqrt(mse)

                results.append((mse, validation_rmse, k, weights, p))

    results = sorted(results, key=lambda row: row[0])

    print("\n================ BEST kNN PARAMETERS ================")
    for mse, validation_rmse, k, weights, p in results[:5]:
        print(
            f"k={k:3d}, weights={weights:8s}, p={p}, "
            f"MSE={mse:.8e}, RMSE={validation_rmse:.8e}"
        )

    _, _, best_k, best_weights, best_p = results[0]

    print("\nChosen:")
    print(f"best_k       = {best_k}")
    print(f"best_weights = {best_weights}")
    print(f"best_p       = {best_p}")
    print("=====================================================")

    return best_k, best_weights, best_p


def get_common_test_start(X: np.ndarray) -> int:
    """Return the first test index that is valid for all model comparisons."""
    valid_start = OPT_TRAIN_SIZE + GAP
    valid_end = valid_start + OPT_VALID_SIZE

    common_test_start = max(
        valid_end + GAP,
        max(PASSIVE_TRAIN_SIZES_TO_TEST) + GAP,
        max(ACTIVE_TRAIN_SIZES_TO_TEST) + GAP,
    )

    if common_test_start + BLOCK_SIZE > len(X):
        raise ValueError("Not enough data left for common test blocks.")

    return common_test_start


def iter_test_blocks(first_test_start: int, n_samples: int):
    """Yield test-block start and end indices."""
    for test_start in range(first_test_start, n_samples - BLOCK_SIZE + 1, BLOCK_SIZE):
        yield test_start, test_start + BLOCK_SIZE


def choose_passive_train_size(
    X: np.ndarray,
    y: np.ndarray,
    best_k: int,
    best_weights: str,
    best_p: int,
    first_test_start: int,
) -> int:
    """Choose the passive training size with the lowest mean test-block RMSE."""
    results = []

    for train_size in PASSIVE_TRAIN_SIZES_TO_TEST:
        model = make_knn_model(best_k, best_weights, best_p)
        model.fit(X[:train_size], y[:train_size])

        block_rmses = []
        for test_start, test_end in iter_test_blocks(first_test_start, len(X)):
            y_pred = model.predict(X[test_start:test_end])
            block_rmses.append(rmse(y[test_start:test_end], y_pred))

        if not block_rmses:
            raise ValueError("No test blocks available for passive training-size selection.")

        results.append(
            {
                "train_size": train_size,
                "rmse_mean": np.mean(block_rmses),
                "rmse_std": np.std(block_rmses),
            }
        )

    print("\n================ PASSIVE TRAIN SIZE TEST ================")
    print("train_size | passive RMSE")
    for row in results:
        print(f"{row['train_size']:10d} | {row['rmse_mean']:.5f} ± {row['rmse_std']:.5f}")
    print("=========================================================")

    best_row = min(results, key=lambda row: row["rmse_mean"])
    return int(best_row["train_size"])


def choose_active_train_size(
    X: np.ndarray,
    y: np.ndarray,
    best_k: int,
    best_weights: str,
    best_p: int,
    first_test_start: int,
) -> int:
    """Choose the active/local training size with the lowest mean test-block RMSE."""
    results = []

    for local_train_size in ACTIVE_TRAIN_SIZES_TO_TEST:
        active_rmses = []
        baseline_rmses = []

        for test_start, test_end in iter_test_blocks(first_test_start, len(X)):
            local_train_start = test_start - GAP - local_train_size
            local_train_end = test_start - GAP

            X_local_train = X[local_train_start:local_train_end]
            y_local_train = y[local_train_start:local_train_end]
            X_test = X[test_start:test_end]
            y_test = y[test_start:test_end]

            active_model = make_knn_model(best_k, best_weights, best_p)
            active_model.fit(X_local_train, y_local_train)

            y_pred = active_model.predict(X_test)
            active_rmses.append(rmse(y_test, y_pred))

            # Baseline: predict the mean of the recent local training block.
            baseline_pred = np.tile(np.mean(y_local_train, axis=0), (len(y_test), 1))
            baseline_rmses.append(rmse(y_test, baseline_pred))

        if not active_rmses:
            raise ValueError("No test blocks available for active training-size selection.")

        active_mean = np.mean(active_rmses)
        baseline_mean = np.mean(baseline_rmses)
        active_improvement = 100 * (1 - active_mean / baseline_mean)

        results.append(
            {
                "local_train_size": local_train_size,
                "active_rmse_mean": active_mean,
                "active_rmse_std": np.std(active_rmses),
                "baseline_rmse_mean": baseline_mean,
                "baseline_rmse_std": np.std(baseline_rmses),
                "active_improvement": active_improvement,
            }
        )

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
    return int(best_row["local_train_size"])


# ============================================================
# Final evaluation
# ============================================================


def evaluate_final_models(
    X: np.ndarray,
    y: np.ndarray,
    best_k: int,
    best_weights: str,
    best_p: int,
    passive_train_size: int,
    active_train_size: int,
    first_test_start: int,
) -> dict[str, np.ndarray]:
    """Evaluate passive, active, and baseline models on identical test blocks."""
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

    for test_start, test_end in iter_test_blocks(first_test_start, len(X)):
        X_test = X[test_start:test_end]
        y_test = y[test_start:test_end]

        # Passive/static model: one model trained on the first part of the data.
        y_pred_passive = passive_model.predict(X_test)
        y_pred_passive_all[test_start:test_end] = y_pred_passive

        # Active/local model: retrain on the data directly before each test block.
        local_train_start = test_start - GAP - active_train_size
        local_train_end = test_start - GAP
        X_local_train = X[local_train_start:local_train_end]
        y_local_train = y[local_train_start:local_train_end]

        active_model = make_knn_model(best_k, best_weights, best_p)
        active_model.fit(X_local_train, y_local_train)

        y_pred_active = active_model.predict(X_test)
        y_pred_active_all[test_start:test_end] = y_pred_active

        # Baseline: predict the mean of the local training block.
        baseline_pred = np.tile(np.mean(y_local_train, axis=0), (len(y_test), 1))

        block_starts.append(test_start)
        passive_rmses.append(rmse(y_test, y_pred_passive))
        active_rmses.append(rmse(y_test, y_pred_active))
        baseline_rmses.append(rmse(y_test, baseline_pred))
        passive_rmse_per_param.append(rmse_per_parameter(y_test, y_pred_passive))
        active_rmse_per_param.append(rmse_per_parameter(y_test, y_pred_active))

    if not block_starts:
        raise ValueError("No test blocks were evaluated. Check LENGTH, BLOCK_SIZE, and train sizes.")

    return {
        "block_starts": np.array(block_starts),
        "passive_rmses": np.array(passive_rmses),
        "active_rmses": np.array(active_rmses),
        "baseline_rmses": np.array(baseline_rmses),
        "passive_rmse_per_param": np.array(passive_rmse_per_param),
        "active_rmse_per_param": np.array(active_rmse_per_param),
        "y_pred_passive_all": y_pred_passive_all,
        "y_pred_active_all": y_pred_active_all,
    }


def print_final_summary(
    results: dict[str, np.ndarray],
    best_k: int,
    best_weights: str,
    best_p: int,
    passive_train_size: int,
    active_train_size: int,
) -> None:
    """Print the final RMSE summary for the poster/report."""
    passive_rmses = results["passive_rmses"]
    active_rmses = results["active_rmses"]
    baseline_rmses = results["baseline_rmses"]

    passive_mean = np.mean(passive_rmses)
    passive_std = np.std(passive_rmses)
    active_mean = np.mean(active_rmses)
    active_std = np.std(active_rmses)
    baseline_mean = np.mean(baseline_rmses)
    baseline_std = np.std(baseline_rmses)

    passive_improvement = 100 * (1 - passive_mean / baseline_mean)
    active_improvement = 100 * (1 - active_mean / baseline_mean)
    active_vs_passive = 100 * (1 - active_mean / passive_mean)
    active_better_blocks = 100 * np.mean(active_rmses < passive_rmses)

    print("\n================ SUMMARY ================")
    print(
        f"HoQI: {SELECTED_HOQI} | "
        f"kNN: k={best_k}, weights={best_weights}, p={best_p} | "
        f"blocks={len(passive_rmses)}, block_size={BLOCK_SIZE}"
    )
    print(
        f"Training: passive={passive_train_size}, "
        f"active/local={active_train_size}, gap={GAP}"
    )

    print("\nRMSE over test blocks:")
    print(f"Baseline : {baseline_mean:.5f} ± {baseline_std:.5f}")
    print(f"Passive  : {passive_mean:.5f} ± {passive_std:.5f}  ({passive_improvement:.1f}% lower than baseline)")
    print(f"Active   : {active_mean:.5f} ± {active_std:.5f}  ({active_improvement:.1f}% lower than baseline)")

    print("\nActive vs passive:")
    print(f"RMSE difference: {active_vs_passive:.1f}%")
    print(f"Active better in {active_better_blocks:.1f}% of test blocks")

    print("\nPer parameter RMSE, passive -> active:")
    for i, label in enumerate(PARAMETER_LABELS):
        passive_param = np.mean(results["passive_rmse_per_param"][:, i])
        active_param = np.mean(results["active_rmse_per_param"][:, i])
        improvement = 100 * (1 - active_param / passive_param)

        print(
            f"{label:5s}: "
            f"{passive_param:.5f} -> {active_param:.5f} "
            f"({improvement:+.1f}%)"
        )

    print("=========================================\n")


# ============================================================
# Plotting
# ============================================================


def save_plot_data(
    x_axis: np.ndarray,
    y: np.ndarray,
    results: dict[str, np.ndarray],
    center_shift: int,
    passive_train_size: int,
) -> None:
    """Save the arrays needed to recreate the final prediction plot."""
    plot_data = {
        "x": x_axis,
        "y_true": y,
        "y_pred_passive": results["y_pred_passive_all"],
        "y_pred_active": results["y_pred_active_all"],
        "labels": np.array(PARAMETER_LABELS),
        "center_shift": center_shift,
        "passive_train_size": passive_train_size,
        "selected_hoqi": SELECTED_HOQI,
    }

    np.save(PLOT_DATA_FILE, plot_data)
    print(f"\nSaved plot data as: {PLOT_DATA_FILE}")


def plot_poster_figure(
    X: np.ndarray,
    y: np.ndarray,
    center_shift: int,
    results: dict[str, np.ndarray],
    passive_train_size: int,
) -> None:
    """Plot the fitted ellipse parameters and both kNN predictions."""
    y_pred_passive_all = results["y_pred_passive_all"]
    y_pred_active_all = results["y_pred_active_all"]

    x_axis = np.arange(len(X)) + center_shift

    if SAVE_PLOT_DATA:
        save_plot_data(x_axis, y, results, center_shift, passive_train_size)

    fig, axes = plt.subplots(
        len(PARAMETER_LABELS),
        1,
        figsize=(14, 11),
        sharex=True,
    )

    for i, label in enumerate(PARAMETER_LABELS):
        ax = axes[i]

        ax.plot(x_axis, y[:, i], linewidth=1.0, label="Windowed ellipse fit")
        ax.plot(x_axis, y_pred_passive_all[:, i], linewidth=1.1, label="Passive/static kNN")
        ax.plot(x_axis, y_pred_active_all[:, i], linewidth=1.0, alpha=0.75, label="Active/local kNN")

        # Highlight the data used to train the passive/static model.
        ax.axvspan(
            center_shift,
            center_shift + passive_train_size,
            alpha=0.12,
            label="Passive training data" if i == 0 else None,
        )

        ax.set_ylabel(label)
        ax.yaxis.set_major_locator(MaxNLocator(nbins=3))
        ax.grid(alpha=0.25)

        if i == 0:
            ax.set_title(
                f"Ellipse parameter predictions for {SELECTED_HOQI}: passive and active kNN",
                fontsize=14,
                fontweight="bold",
            )

    axes[-1].set_xlabel("Datapoint / time")

    lines, legend_labels = axes[0].get_legend_handles_labels()
    fig.legend(lines, legend_labels, loc="upper right", bbox_to_anchor=(0.98, 0.98))

    plt.tight_layout(rect=[0, 0, 0.88, 0.96])

    if SAVE_FIGURE:
        plt.savefig(FIGURE_FILE, dpi=300, bbox_inches="tight")
        print(f"\nSaved figure as: {FIGURE_FILE}")

    plt.show()


# ============================================================
# Main script
# ============================================================


def main() -> None:
    """Run the complete kNN analysis pipeline."""
    ensure_parameter_timeseries_files()

    center_shift = find_best_center_shift()
    X, y = load_and_align_data(center_shift=center_shift)

    print("\n================ DATA ================")
    print(f"selected HoQI       : {SELECTED_HOQI}")
    print(f"chosen center shift : {center_shift}")
    print(f"X shape             : {X.shape}")
    print(f"y shape             : {y.shape}")
    print("======================================")

    best_k, best_weights, best_p = optimize_knn_parameters(X, y)
    first_test_start = get_common_test_start(X)

    best_passive_train_size = choose_passive_train_size(
        X=X,
        y=y,
        best_k=best_k,
        best_weights=best_weights,
        best_p=best_p,
        first_test_start=first_test_start,
    )

    best_active_train_size = choose_active_train_size(
        X=X,
        y=y,
        best_k=best_k,
        best_weights=best_weights,
        best_p=best_p,
        first_test_start=first_test_start,
    )

    final_results = evaluate_final_models(
        X=X,
        y=y,
        best_k=best_k,
        best_weights=best_weights,
        best_p=best_p,
        passive_train_size=best_passive_train_size,
        active_train_size=best_active_train_size,
        first_test_start=first_test_start,
    )

    print_final_summary(
        results=final_results,
        best_k=best_k,
        best_weights=best_weights,
        best_p=best_p,
        passive_train_size=best_passive_train_size,
        active_train_size=best_active_train_size,
    )

    plot_poster_figure(
        X=X,
        y=y,
        center_shift=center_shift,
        results=final_results,
        passive_train_size=best_passive_train_size,
    )


if __name__ == "__main__":
    main()
