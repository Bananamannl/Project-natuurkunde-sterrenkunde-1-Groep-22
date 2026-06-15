from ellipse_parameters import *
import numpy as np
from functions import *
from orthogonal_matrices import *
from timeseries_slider import *

HoQIs = np.load("Data_Analysis_Part_1\\HoQI_fitted_six_vct_list.npy")
# orthogonal = HoQIs @ matrix_1x
Q1, Q2 = np.load("Data_Analysis_Part_1\\1xQ1.npy"), np.load("Data_Analysis_Part_1\\1xQ2.npy")
Q1, Q2 = transform(Q1[:10000], Q2[:10000])

np.save("param_timeseries_1x_old_transform_1000.npy", parameters_timeseries(Q1, Q2, window_size=500, step_size=1))

# np.hstack((orthogonal, parameters[:, 0]))

# print(parameters.shape)

