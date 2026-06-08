import numpy as np
import matplotlib.pyplot as plt
from ellipse_parameters import *
displacements = np.load("Data_Analyse_Dataset_1/fitted_six_vct_list.npy")
HoQIs = np.load("Data_Analyse_Dataset_1/HoQI_fitted_six_vct_list.npy")
Q1_1x, Q2_1x = np.load("Data_Analyse_Dataset_1/1xQ1.npy"), np.load("Data_Analyse_Dataset_1/1xQ2.npy")
Q1_2x, Q2_2x = np.load("Data_Analyse_Dataset_1/2xQ1.npy"), np.load("Data_Analyse_Dataset_1/2xQ2.npy")
Q1_3x, Q2_3x = np.load("Data_Analyse_Dataset_1/3xQ1.npy"), np.load("Data_Analyse_Dataset_1/3xQ2.npy")
Q1_1z, Q2_1z = np.load("Data_Analyse_Dataset_1/1zQ1.npy"), np.load("Data_Analyse_Dataset_1/1zQ2.npy")
Q1_2z, Q2_2z = np.load("Data_Analyse_Dataset_1/2zQ1.npy"), np.load("Data_Analyse_Dataset_1/2zQ2.npy")
Q1_3z, Q2_3z = np.load("Data_Analyse_Dataset_1/3zQ1.npy"), np.load("Data_Analyse_Dataset_1/3zQ2.npy")

vectors = parameters_timeseries(Q1_3z, Q2_3z, window_size=500, step_size=100)
displacements = period_data(displacements, window_size=500, step_size=100)
HoQIs = period_data(HoQIs, window_size=500, step_size=100)


all_data = np.column_stack((vectors, HoQIs))
corr_matrix = np.corrcoef(all_data, rowvar=False)

cross_corr = corr_matrix[:6, 6:]

x_labels = ["x0", "y0", "theta", "a", "b", "area"]
d_labels = ["x", "y", "z", "Rx", "Ry", "Rz"]
h_labels = ["1x", "2x", "3x", "1z", "2z", "3z"]

plt.figure(figsize=(6, 5))
plt.imshow(corr_matrix, vmin=-1, vmax=1)
plt.colorbar(label="correlation")

plt.xticks(range(6), h_labels, rotation=45)
plt.yticks(range(6), x_labels)

plt.xlabel("Displacements")
plt.ylabel("Ellipse parameters")
plt.title("Correlation: ellipse parameters vs displacements")

plt.tight_layout()
plt.show()