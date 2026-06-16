from ellipse_parameters import *
import numpy as np

Q1, Q2 = np.load("Data_Analysis_Part_1\\2xQ1.npy"), np.load("Data_Analysis_Part_1\\2xQ2.npy")
Q1, Q2 = Q1[:500000], Q2[:500000]

parameters = parameters_timeseries(Q1, Q2, window_size=500, step_size=10)
parameters = np.repeat(parameters, 10, axis=0)
np.save("param_timeseries_1x_step_size_10_window_size_500.npy", parameters)

Q1, Q2 = np.load("Data_Analysis_Part_1\\2zQ1.npy"), np.load("Data_Analysis_Part_1\\2zQ2.npy")
Q1, Q2 = Q1[:500000], Q2[:500000]

parameters = parameters_timeseries(Q1, Q2, window_size=250, step_size=1)
np.save("param_timeseries_3z_old_transform_step_size_1_window_size_250.npy", parameters)

# Q1, Q2 = np.load("Data_Analysis_Part_1\\2xQ1.npy"), np.load("Data_Analysis_Part_1\\2xQ2.npy")
# Q1, Q2 = transform(Q1, Q2)

# parameters = parameters_timeseries(Q1, Q2, window_size=500, step_size=1)
# np.save("param_timeseries_2x_old_transform_step_size_1_window_size_500.npy", parameters)

# Q1, Q2 = np.load("Data_Analysis_Part_1\\3xQ1.npy"), np.load("Data_Analysis_Part_1\\3xQ2.npy")
# Q1, Q2 = transform(Q1, Q2)

# parameters = parameters_timeseries(Q1, Q2, window_size=210, step_size=1)
# np.save("param_timeseries_3x_old_transform_step_size_1_window_size_210.npy", parameters)

# Q1, Q2 = np.load("Data_Analysis_Part_1\\1xQ1.npy"), np.load("Data_Analysis_Part_1\\1xQ2.npy")
# Q1, Q2 = transform(Q1, Q2)

# parameters = parameters_timeseries(Q1, Q2, window_size=500, step_size=1)
# np.save("param_timeseries_1x_old_transform_step_size_1_window_size_500.npy", parameters)