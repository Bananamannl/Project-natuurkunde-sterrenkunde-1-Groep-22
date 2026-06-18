import numpy as np
from functions import *

def residuals(params, x, y):
    x0, y0, a, b, theta = params
    xp = (x - x0) * np.cos(theta) + (y - y0) * np.sin(theta)
    yp = - (x - x0) * np.sin(theta) + (y - y0) * np.cos(theta)
    return xp ** 2 / a ** 2 + yp ** 2 / b ** 2 - 1

def parameters_with_signal(x, y, start_parameters):
    """
    Input: Q1, Q2, starting parameters [x0, y0, a, b, theta]
    Output: [x0, y0, a, b, theta], [x0, y0, a, b, theta]
    This fits a given set Q1, Q2 with starting parameters
    """
    try:
        fit = least_squares(
            residuals,
            start_parameters,
            args=(x, y)
        )

        if not fit.success:
            return None, start_parameters

        vector = fit.x.copy()
        vector[2] = abs(vector[2])
        vector[3] = abs(vector[3])

        # theta beperken tot [0, pi)
        vector[4] = vector[4] % np.pi

        return vector, vector

    except ValueError:
        return None, start_parameters

def parameters_timeseries_interactive(x, y, window_size=None, step_size=None):
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
        print(start)

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
                delta = np.array([0.1, 0.1, 0.25, 0.25])  # zonder theta

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
            vectoren.append(vector)
            break
            
    vectoren = np.array(vectoren)

    # Repeat the parameters so almost every point has corresponding parameters (except for the last ones)
    parameters = np.repeat(vectoren, step_size, axis=0)
    return parameters
