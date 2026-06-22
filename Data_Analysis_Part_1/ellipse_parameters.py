import numpy as np
from ellipse_fitting_and_reshaping_3_4 import *
import matplotlib.pyplot as plt

def parameters(x, y, start_parameters=None):
    """
    Takes Q1 and Q2 data (np.array's) and spits out the fitting parameters
    the output is in the form of a 6-dim vector:
    (x0, y0, theta, a, b, area)
    """
    if start_parameters is None:
        start_parameters = [0, 0, 1, 1, 0]
    results = least_squares(
        residuals,
        x0 = start_parameters,
        args = (x, y)
    )
    x0, y0, a, b, theta = results.x
    if b > a:
        a, b = b, a
        theta += np.pi / 2
    area = np.pi * a * b
    vector = np.column_stack((x0, y0, theta, a, b, area))
    start_parameters = [x0, y0, a, b, theta]
    return vector, start_parameters

def parameters_timeseries(x, y, window_size=None, step_size=None):
    """
    Input: Q1, Q2, window_size= , step_size=
    output: (N, 5) np array with N vectors where: vector = [x0, y0, a, b, theta]
    """

    if window_size is None:
        window_size = 250
    if step_size is None:
        step_size = 100
    # Start with an empty list and basic starting fit parameters
    vectoren = []
    fit_parameters = np.array([0, 0, 1, 1, 0])

    # For every window:
    for start in range(0, len(x) - window_size + 1, step_size):

        current_window_size = window_size


        while True:
            end = start + current_window_size
            if end > len(x):
                print(f"Geen grotere window meer mogelijk bij start={start}")
                break
            part_Q1 = x[start:end]
            part_Q2 = y[start:end]
            vector, new_fit_parameters = parameters_with_signal(
                part_Q1,
                part_Q2,
                start_parameters=fit_parameters
            )

            if vector is None:
                current_window_size += 50
                continue

            vector = np.ravel(vector)

            # Eerste fit altijd accepteren
            if len(vectoren) > 0:
                delta = np.array([0.2, 0.2, 0.5, 0.5])  # zonder theta

                lower_bounds = fit_parameters[:4] - delta
                upper_bounds = fit_parameters[:4] + delta

                lower_bounds[2] = max(lower_bounds[2], 0.001)
                lower_bounds[3] = max(lower_bounds[3], 0.001)

                if np.any(vector[:4] < lower_bounds) or np.any(vector[:4] > upper_bounds):
                    current_window_size += 50
                    print(
                        f"Fit buiten toegestane sprong bij start={start}, probeer opnieuw met "
                        f"window_size={current_window_size}"
                    )
                    continue

            fit_parameters = new_fit_parameters
            vectoren.append(np.ravel(vector))
            break
            
    vectoren = np.array(vectoren)

    # Repeat the parameters so almost every point has corresponding parameters (except for the last ones)
    return vectoren

def period_data(data, window_size=None, step_size=None, lag=None):
    if window_size is None:
        window_size = 1000
    if step_size is None:
        step_size = 100    
    if lag is None:
        lag = 0
    starts = np.arange(0, len(data) - window_size + 1, step_size)
    indices = starts + lag
    indices = indices[indices < len(data)]
    period_data = data[indices]

    return period_data

# # # Snelle test
# vectors = parameters_timeseries(Q1, Q2, window_size=1000, step_size=500)
# #vectors = np.load("Data_Analysis_Part_1/fitted_six_vct_list.npy")
# print("Shape:", vectors.shape)
# print("Eerste 5 vectors:")
# print(vectors[:5])

# print("NaN?", np.isnan(vectors).any())
# print("Inf?", np.isinf(vectors).any())

# plt.plot(vectors)
# plt.legend(["x0", "y0", "theta", "a", "b", "area"])
# plt.xlabel("window index")
# plt.ylabel("waarde")
# plt.title("Snelle test ellipsparameters")
# plt.show()