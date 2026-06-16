from ellipse_parameters import *
import numpy as np


def parameters_with_signal(x, y, start_parameters=None):
    """
    Takes Q1 and Q2 data (np.array's) and spits out the fitting parameters
    the output is in the form of a 5-dim vector:
    (x0, y0, a, b, theta)
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
    if a > 10:
        vector = None
    elif b > 10:
        vector = None
    elif x0 > 10:
        vector = None
    elif y0 > 10:
        vector = None
    else:
        vector = np.column_stack((x0, y0, a, b, theta))
    start_parameters = [x0, y0, a, b, theta]
    return vector, start_parameters

def parameters_timeseries(x, y, window_size=None, step_size=None):
    """
    output: lijst met 6-dim vectoren
    """
    if window_size is None:
        window_size = 1000
    if step_size is None:
        step_size = 100

    vectoren = []
    fit_parameters = [0, 0, 1, 1, 0]

    for start in range(0, len(x) - window_size + 1, step_size):
        print(start)

        current_window_size = window_size

        while True:
            end = start + current_window_size

            part_Q1 = x[start:end]
            part_Q2 = y[start:end]

            vector, new_fit_parameters = parameters_with_signal(
                part_Q1,
                part_Q2,
                start_parameters=fit_parameters
            )

            if vector is None:
                current_window_size += 50
                print(
                    f"Fit fout bij start={start}, probeer opnieuw met "
                    f"window_size={current_window_size}"
                )
                continue

            # Alleen als vector goed is, sla je hem op
            fit_parameters = new_fit_parameters
            vectoren.append(np.ravel(vector))

            # Nu pas klaar met deze start
            break
    return np.array(vectoren)

Q1, Q2 = np.load(r"C:\Users\timob\OneDrive - UvA\Project 1\GitHub Map\Project-natuurkunde-sterrenkunde-1-Groep-22\Data_Analysis_Part_1\1xQ1.npy"), np.load(r"C:\Users\timob\OneDrive - UvA\Project 1\GitHub Map\Project-natuurkunde-sterrenkunde-1-Groep-22\Data_Analysis_Part_1\1xQ2.npy")

params = parameters(Q1, Q2)