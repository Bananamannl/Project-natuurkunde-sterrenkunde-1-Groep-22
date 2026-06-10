import numpy as np
from functions import *

def parameters(x, y, start_parameters=None):
    """
    Takes Q1 and Q2 data (np.array's) and spits out the fitting parameters
    the output is in the form of a 6-dim vector:
    (x0, y0, a, b, theta, area)
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
    vector = np.column_stack((x0, y0, a, b, theta, area))
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
        end = start + window_size

        part_Q1 = x[start:end]
        part_Q2 = y[start:end]
        
        vector, fit_parameters = parameters(part_Q1, part_Q2, start_parameters= fit_parameters)
        vectoren.append(np.ravel(vector))
    return np.array(vectoren)

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