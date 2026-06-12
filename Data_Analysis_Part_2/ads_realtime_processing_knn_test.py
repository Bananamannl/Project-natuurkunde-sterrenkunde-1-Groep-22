import numpy as np
import matplotlib.pyplot as plt
from windowed_ellipse_fitting import *
from functions import *
from orthogonal_matrices import *
from knn_functions import *
Q1, Q2 = np.load("Data_Analysis_Part_1\\3xQ1.npy"), np.load("Data_Analysis_Part_1\\3xQ2.npy")
HoQIs = np.load("Data_Analysis_Part_1\HoQI_fitted_six_vct_list.npy")
orth_plane = HoQIs @ matrix_3x.T

Q1_transform, Q2_transform = transform(Q1, Q2)

parameters = parameters_timeseries(Q1, Q2, window_size=210, step_size=210)

tested_parameters = rolling_knn_predict_points(orth_plane, parameters, window_size=210)
Q1_knn, Q2_knn = transform_with_parameters(Q1, Q2, tested_parameters)


segment_time_set = 1000
fs_set = 1000


length_3x_lijst = Q1_Q2_Length(Q1, Q2)
transformed_length_3x_lijst = Q1_Q2_Length(Q1_transform, Q2_transform)
knn_transformed_length_3x_lijst = Q1_Q2_Length(Q1_knn, Q2_knn)

transformed_asd = get_asd(transformed_length_3x_lijst, fs=fs_set, segment_time=segment_time_set)
knn_transformed_asd = get_asd(knn_transformed_length_3x_lijst, fs=fs_set, segment_time=segment_time_set)

figure, axes =plt.subplots(2, 1)
axes[0].loglog(transformed_asd.frequencies.value, transformed_asd, 'b')
axes[0].set_xlabel("Frequency (Hz)")
axes[0].set_ylabel("ASD (um Hz^(-1/2))")
axes[0].set_xlim(1e-3, 1e3)
axes[0].grid(True, which="both")
axes[0].set_title('ASD diagram for the simple transported data (3x)')

axes[1].loglog(knn_transformed_asd.frequencies.value, knn_transformed_asd, 'r')
axes[1].set_xlabel("Frequency (Hz)")
axes[1].set_ylabel("ASD (um Hz^(-1/2))")
axes[1].set_xlim(1e-3, 1e3)
axes[1].set_ylim(1e-9, 1e2)
axes[1].grid(True, which="both")
axes[1].set_title('ASD diagram for the real time transported data (KNN) (3x)')

plt.subplots_adjust(hspace=0.312)
plt.show()