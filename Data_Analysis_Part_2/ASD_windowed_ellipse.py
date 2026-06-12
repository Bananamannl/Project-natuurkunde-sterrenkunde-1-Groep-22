import numpy as np
import matplotlib.pyplot as plt
from windowed_ellipse_fitting import *
from functions import *

segment_time_set = 1000
fs_set = 1000

Q1_list = np.load('Data_Analysis_Part_1/2zQ1.npy')[:3000000]
Q2_list = np.load('Data_Analysis_Part_1/2zQ2.npy')[:3000000]

transformed_Q1, transformed_Q2 = transform(Q1_list, Q2_list)

windowed_transformed_Q1, windowed_transformed_Q2 = standard_step_window_ellipse_fitting(Q1_list, Q2_list, window_size=250)

length_3x_lijst = Q1_Q2_Length(Q1_list, Q2_list)
transformed_length_3x_lijst = Q1_Q2_Length(transformed_Q1, transformed_Q2)
windowed_transformed_length_3x_lijst = Q1_Q2_Length(windowed_transformed_Q1, windowed_transformed_Q2)

base_asd = get_asd(length_3x_lijst, fs=fs_set, segment_time=segment_time_set)
transformed_asd = get_asd(transformed_length_3x_lijst, fs=fs_set, segment_time=segment_time_set)
windowed_transformed_asd = get_asd(windowed_transformed_length_3x_lijst, fs=fs_set, segment_time=segment_time_set)

figure, axes =plt.subplots(3, 1)
axes[0].loglog(base_asd.frequencies.value, base_asd, 'b')
axes[0].set_xlabel("Frequency (Hz)")
axes[0].set_ylabel("ASD (um Hz^(-1/2))")
axes[0].set_xlim(1e-3, 1e3)
axes[0].grid(True, which="both")
axes[0].set_title('ASD diagram for the raw data (3z)')

axes[1].loglog(transformed_asd.frequencies.value, transformed_asd, 'r')
axes[1].set_xlabel("Frequency (Hz)")
axes[1].set_ylabel("ASD (um Hz^(-1/2))")
axes[1].set_xlim(1e-3, 1e3)
axes[1].grid(True, which="both")
axes[1].set_title('ASD diagram for the transformed data (3z)')

axes[2].loglog(windowed_transformed_asd.frequencies.value, windowed_transformed_asd, 'g')
axes[2].set_xlabel("Frequency (Hz)")
axes[2].set_ylabel("ASD (um Hz^(-1/2))")
axes[2].set_xlim(1e-3, 1e3)
axes[2].grid(True, which="both")
axes[2].set_title('ASD diagram for the windowed transformed data (3z)')

plt.subplots_adjust(hspace=0.312)
plt.show()