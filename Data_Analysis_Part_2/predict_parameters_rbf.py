import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import RBFInterpolator
import time

from ellipse_parameters import *

"This code takes two lists (Q1 and Q2) of a certain HoQI, both with three million elements."
"The data is then split up into 300 chunks, which makes the chunk size equal to 10.000."
"For each of these chunks, there are 9.901 windows (window size = 100), of which everyime the five ellipse parameters are being calculated."
"After this real-time ellipse fitting, the code fits an rbf (an interpolating function) through the 9901 relevant data points."
"This rbf is used to predict the ellipse parameters of the next chunk of data, after which the (Q1, Q2) points get transformed real-time."
"So, except for chunk 0, the (Q1, Q2) points of each chunk are transformed using the rbf of the previous chunk."

# importing the HoQI data, and the Q1 and Q2 lists
HoQIs, Q1, Q2 = np.load("Data_Analysis_Part_1\HoQI_fitted_six_vct_list.npy"), np.load("Data_Analysis_Part_1\\2xQ1.npy"), np.load("Data_Analysis_Part_1\\2xQ2.npy")
block_size = 300000 # the amount of data points being used for the plot
HoQIs_block, Q1_block, Q2_block = HoQIs[0:block_size], Q1[0:block_size], Q2[0:block_size]

window_size = 500 # use for 1x and 2x
# window_size = 210 # use for 3x
# window_size = 250 # use for 1z, 2z and 3z

# the transformation matrix for HoQI 1x
matrix_1x = np.array([
    [0, -np.sqrt(1/3), np.sqrt(1/3), 0, 0, 0],
    [0, 0, 0, 1/3, 1/3, 1/3]])

# the transformation matrix for HoQI 1z
matrix_1z = np.array([
    [-2/3, 1/3, 1/3, 0, 0, 0],
    [0, -np.sqrt(1/3), np.sqrt(1/3), 0, 0, 0]])

# the transformation matrix for HoQI 2x
matrix_2x = np.array([
    [1/np.sqrt(3), 0, -1/np.sqrt(3), 0, 0, 0],
    [0, 0, 0, 1/3, 1/3, 1/3]])

# the transformation matrix for HoQI 2z
matrix_2z = np.array([
    [1/np.sqrt(3), 0, -1/np.sqrt(3), 0, 0, 0],
    [-1/3, 2/3, -1/3, 0, 0, 0]])

# the transformation matrix for HoQI 3x
matrix_3x = np.array([
    [-1/np.sqrt(3), 1/np.sqrt(3), 0, 0, 0, 0],
    [0, 0, 0, 1/3, 1/3, 1/3]])

# the transformation matrix for HoQI 3z
matrix_3z = np.array([
    [-1/np.sqrt(3), 1/np.sqrt(3), 0, 0, 0, 0],
    [1/3, 1/3, -2/3, 0, 0, 0]])

# this function returns both orthogonal positions with the relevant parameter value (so it basically returns the coordinates of all points in the 3D plot)
def orthogonal_position_and_parameter(HoQIs, matrix, param):
    vectors = HoQIs @ matrix.T
    return np.hstack((vectors, param[:, None]))

chunk_size = 10000
n_chunks = block_size / chunk_size 
lag = 0

Q1_chunk_0 = []
Q2_chunk_0 = []

# introducing our transformed Q lists
Q1_transformed_list = []
Q2_transformed_list = []

# we are going to make a separate rbf function for each chunk, for each individual ellipse parameter
# rbf_x0_list, rbf_y0_list, rbf_a_list, rbf_b_list, rbf_theta_list = [], [], [], [], []

for i in range(int(n_chunks)): # for loop for each chunk individually
    t0 = time.time()

    # the start and end of each chunk (the start is included; the end is not)
    start, end = i * chunk_size + lag, (i + 1) * chunk_size + lag

    # lag = 0, dus voor de window 0 t/m 99 gebruiken we tijdstip 0, dus eindigt een chunk bij tijdstip (chunk_size - window_size + 1) ipv (chunk_size) --> gooi de laatste (window_size - 1) termen weg
    HoQIs_chunk = HoQIs_block[start:end-(window_size - 1)]

    # berekent voor elke HoQI-vector de positie in het orthogonale vlak (in de huidige chunk)
    orthogonal_position = HoQIs_chunk @ matrix_2x.T

    # the transformation of the previous Q1 and Q2:
    if i > 0: # i > 0, omdat er voor de eerste ('nulde') chunk nog geen vorige chunk is, dus nog geen rbf op basis waarvan de parameters voorspeld kunnen worden
        x0_predicted = rbf_x0(orthogonal_position)
        y0_predicted = rbf_y0(orthogonal_position)
        a_predicted = rbf_a(orthogonal_position)
        b_predicted = rbf_b(orthogonal_position)
        theta_predicted = rbf_theta(orthogonal_position)

        # x0_predicted = rbf_x0_list[i-1](orthogonal_position)
        # y0_predicted = rbf_y0_list[i-1](orthogonal_position)
        # a_predicted = rbf_a_list[i-1](orthogonal_position)
        # b_predicted = rbf_b_list[i-1](orthogonal_position)
        # theta_predicted = rbf_theta_list[i-1](orthogonal_position)

        # transforming time
        Q1_centered = Q1_block[start:end-(window_size - 1)] - x0_predicted
        Q2_centered = Q2_block[start:end-(window_size - 1)] - y0_predicted

        Q1_t = (np.cos(theta_predicted) * Q1_centered + np.sin(theta_predicted) * Q2_centered) / a_predicted
        Q2_t = (-np.sin(theta_predicted) * Q1_centered + np.cos(theta_predicted) * Q2_centered) / b_predicted

        Q1_transformed_list.append(Q1_t)
        Q2_transformed_list.append(Q2_t)

        # print the range in which the predicted parameters values fall
        # print(f"a_predicted range: {a_predicted.min():.3f} - {a_predicted.max():.3f}")
        # print(f"b_predicted range: {b_predicted.min():.3f} - {b_predicted.max():.3f}")
        # print(f"x0_predicted range: {x0_predicted.min():.3f} - {x0_predicted.max():.3f}")
        # print(f"y0_predicted range: {y0_predicted.min():.3f} - {y0_predicted.max():.3f}")
        # print(f"theta_predicted range: {theta_predicted.min():.3f} - {theta_predicted.max():.3f}")
    else: # for chunk 0 (this causes the ellipse in the plot)
        Q1_nt = Q1_block[start:end-(window_size - 1)]
        Q2_nt = Q2_block[start:end-(window_size - 1)]

        Q1_chunk_0.append(Q1_nt)
        Q2_chunk_0.append(Q2_nt)
 
    t1 = time.time()

    # for each window of the relevant chunk, the five ellipse parameters are calculated, which results in a (chunk_size - window_size + 1)x5 matrix
    params = parameters_timeseries(Q1_block[start:end], Q2_block[start:end], window_size=window_size, step_size=1)

    t2 = time.time()

    # elke ellipsparameter correspondeert met een bepaalde kolom uit 'params'
    x0, y0, a, b, theta = params[:,0], params[:,1], params[:,2], params[:,3], params[:,4]

    # print the range of the values of the ellipse parameters of the current chunk
    # print(f"a_true_value range: {a.min():.3f} - {a.max():.3f}")
    # define a 'bad point', and print the corresponding amount
    # print(f"amount of bad points (a): {(a > 5).sum()} van {len(a)}")

    # thin plate spline kernel for an optimal fit 
    # neighbors: rbf only uses the closest 100 points in the orthogonal plane to predict the corresponding value of the assosoiated ellipse parameter; this in order to reduce running time
    # an rbf (interpolating function) is trained for each individual ellipse parameter
    rbf_x0 = RBFInterpolator(orthogonal_position, x0, kernel="thin_plate_spline", smoothing=0.1, neighbors=100)
    rbf_y0 = RBFInterpolator(orthogonal_position, y0, kernel="thin_plate_spline", smoothing=0.1, neighbors=100)
    rbf_a = RBFInterpolator(orthogonal_position, a, kernel="thin_plate_spline", smoothing=0.1, neighbors=100)
    rbf_b = RBFInterpolator(orthogonal_position, b, kernel="thin_plate_spline", smoothing=0.1, neighbors=100)
    rbf_theta = RBFInterpolator(orthogonal_position, theta, kernel="thin_plate_spline", smoothing=0.1, neighbors=100)

    # the rbf is added to the associated list of rbf's, so that each chunk can be transformed with its own (or better said: the previous) chunk
    # rbf_x0_list.append(rbf_x0)
    # rbf_y0_list.append(rbf_y0)
    # rbf_a_list.append(rbf_a)
    # rbf_b_list.append(rbf_b)
    # rbf_theta_list.append(rbf_theta)

    t3 = time.time()

    print(f"Chunk {i}: other={t1-t0:.2f}s; parameters_timeseries={t2-t1:.2f}s; RBF={t3-t2:.2f}s.")

    # if i == 3:
    #     break

# arrays --> lists
Q1_nt_plot = np.concatenate(Q1_chunk_0)
Q2_nt_plot = np.concatenate(Q2_chunk_0)

Q1_t_plot = np.concatenate(Q1_transformed_list)
Q2_t_plot = np.concatenate(Q2_transformed_list)

# the plot
plt.figure(figsize=(6, 6))
plt.scatter(Q1_nt_plot, Q2_nt_plot, s=0.1, color='red', label='non-transformed')
plt.scatter(Q1_t_plot, Q2_t_plot, s=0.1, color='green', label='transformed')
plt.xlim(-2.5, 2.5)
plt.ylim(-2.5, 2.5)
plt.xlabel('Q1')
plt.ylabel('Q2')
plt.axis('equal')
plt.legend(fontsize=8, loc= 'upper right')
plt.title('(Q1, Q2) plot using rbf predicting')
plt.savefig("Q1_Q2_RDF_Predicted_1.png")
plt.show()