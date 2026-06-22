"""
This piece of code will be designed to take in two lists of Q1 and Q2, which will then be cut up into a bunch of windows, which will each have an ellipse fitted to them, with the average parameters of all ellipses that are fitted to a point being used to subseqently transform the position of this point as in the ellipse transformation function writen by Timo. This will hopefully recude the noise inherent in the data. First we will write a testing peice of code where the window size will be the same as the step size, as to make sure that the whole process works. We will also then be checking the influence on the noise levels at all steps in the process.
"""

import numpy as np
import matplotlib.pyplot as plt
from ellipse_parameters import *


# Defining the window ellipse fitting function with step size the same as windo size
def standard_step_window_ellipse_fitting(Q1, Q2, window_size):
    # This outputs a 6 x floor(len(Q1) / window_size) matrix with the parameters of the differen ellipses. The bottom row is area, which we don't need, so we remove it
    params_matrix = parameters_timeseries(Q1,Q2, window_size=window_size, step_size=window_size)[ : , 0:5]


    return_Q1 = []
    return_Q2 = []
    for start in range(0, len(Q1) - window_size + 1, window_size):
        end = start + window_size

        part_Q1 = Q1[start:end]
        part_Q2 = Q2[start:end]
        
        x0, y0, a, b, theta = params_matrix[int(start / window_size), : ]
        vectors = np.column_stack((part_Q1, part_Q2))
        centre = np.array([x0, y0])
        squeeze = np.array([a, b])
        R = np.array([[np.cos(theta), - np.sin(theta)], 
                    [np.sin(theta), np.cos(theta)]])
        centred = vectors - centre
        rotated = centred @ R
        unit_vectors = rotated / squeeze
        transformed_part_Q1, transformed_part_Q2 = unit_vectors[:, 0], unit_vectors[:, 1]
        return_Q1.append(list(transformed_part_Q1))
        return_Q2.append(list(transformed_part_Q2))

    return np.array(return_Q1).flatten(), np.array(return_Q2).flatten()

# Defining function with overlap
def parameters(x, y, start_parameters=None):
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
        raise ValueError("a > 10, kies een groter window_size")
    vector = np.column_stack((x0, y0, a, b, theta))
    start_parameters = [x0, y0, a, b, theta]
    return vector, start_parameters

def variable_step_window_ellipse_fitting(Q1, Q2, window_size, step_size):
    # This outputs a 6 x floor(len(Q1) / window_size) matrix with the parameters of the differen ellipses. The bottom row is area, which we don't need, so we remove it
    params_matrix = parameters_timeseries(Q1,Q2, window_size=window_size, step_size=step_size)[ : , 0:5]

    return_Q1 = []
    return_Q2 = []
    for start in range(window_size-step_size, len(Q1) - window_size + 1, step_size):
        end = start + step_size

        part_Q1 = Q1[start:end]
        part_Q2 = Q2[start:end]
        
        list_x0, list_y0, list_a, list_b, list_theta = np.transpose(params_matrix[int((start / step_size) - (window_size / step_size) + 1) : int((start / step_size) + (window_size / step_size)), : ])
        vectors = np.column_stack((part_Q1, part_Q2))

        x0 = np.average(list_x0)
        y0 = np.average(list_y0)
        a = np.average(list_a)
        b = np.average(list_b)
        theta = np.average(list_theta)

        centre = np.array([x0, y0])
        squeeze = np.array([a, b])
        R = np.array([[np.cos(theta), - np.sin(theta)], 
                    [np.sin(theta), np.cos(theta)]])
        centred = vectors - centre
        rotated = centred @ R
        unit_vectors = rotated / squeeze
        transformed_part_Q1, transformed_part_Q2 = unit_vectors[:, 0], unit_vectors[:, 1]
        return_Q1.append(list(transformed_part_Q1))
        return_Q2.append(list(transformed_part_Q2))

    return np.array(return_Q1).flatten(), np.array(return_Q2).flatten()

# Using the function to plot the new circles

# Q1_list = [np.load('Data_Analysis_Part_1/1xQ1.npy')[:3000000], np.load('Data_Analysis_Part_1/2xQ1.npy')[:3000000], np.load('Data_Analysis_Part_1/3xQ1.npy')[:3000000], np.load('Data_Analysis_Part_1/1zQ1.npy')[:3000000], np.load('Data_Analysis_Part_1/2zQ1.npy')[:3000000], np.load('Data_Analysis_Part_1/3zQ1.npy')[:3000000]]

# Q2_list = [np.load('Data_Analysis_Part_1/1xQ2.npy')[:3000000], np.load('Data_Analysis_Part_1/2xQ2.npy')[:3000000], np.load('Data_Analysis_Part_1/3xQ2.npy')[:3000000], np.load('Data_Analysis_Part_1/1zQ2.npy')[:3000000], np.load('Data_Analysis_Part_1/2zQ2.npy')[:3000000], np.load('Data_Analysis_Part_1/3zQ2.npy')[:3000000]]

# Q1_transformed = [0]*6
# Q2_transformed = [0]*6
# for h in range(0,6):
#     if h < 2:
#         fitted_Q1, fitted_Q2 = standard_step_window_ellipse_fitting(Q1_list[h], Q2_list[h], window_size=500)
#     elif h == 2:
#         fitted_Q1, fitted_Q2 = standard_step_window_ellipse_fitting(Q1_list[h], Q2_list[h], window_size=210)
#     else:
#         fitted_Q1, fitted_Q2 = standard_step_window_ellipse_fitting(Q1_list[h], Q2_list[h], window_size=250)
#     Q1_transformed[h] = fitted_Q1
#     Q2_transformed[h] = fitted_Q2

# Q1_variable_transformed = [0]*6
# Q2_variable_transformed = [0]*6
# for h in range(0,6):
#     if h <= 2:
#         fitted_Q1, fitted_Q2 = variable_step_window_ellipse_fitting(Q1_list[h], Q2_list[h], window_size=1000, step_size=210)
#     else:
#         fitted_Q1, fitted_Q2 = variable_step_window_ellipse_fitting(Q1_list[h], Q2_list[h], window_size=250, step_size=210)
#     Q1_variable_transformed[h] = fitted_Q1
#     Q2_variable_transformed[h] = fitted_Q2

# names_list = ['1x', '2x', '3x', '1z', '2z', '3z']

# # Make a plot of all the ellipses on top of each other
# figure, axes = plt.subplots(2, 3)
# for i in range(0,2):
#     for j in range(0,3):
#         axes[i, j].set_ylabel('Q2')
#         axes[i, j].set_xlabel('Q1')
#         axes[i, j].plot(Q1_list[i*3+j], Q2_list[i*3+j], ',')
#         axes[i, j].set_title(names_list[i*3+j])

# figure.tight_layout()
# plt.subplots_adjust(hspace=0.312, wspace=0.4)
# plt.show()

# figure, axes = plt.subplots(2, 3)
# for i in range(0,2):
#     for j in range(0,3):
#         axes[i, j].set_ylabel('Q2')
#         axes[i, j].set_xlabel('Q1')
#         axes[i, j].plot(Q1_transformed[i*3+j], Q2_transformed[i*3+j], ',g')
#         axes[i, j].set_title(names_list[i*3+j])
#         axes[i, j].set_xlim(-1.43, 1.43)

# figure.tight_layout()
# plt.subplots_adjust(hspace=0.312, wspace=0.4)
# plt.show()

# figure, axes = plt.subplots(2, 3)
# for i in range(0,2):
#     for j in range(0,3):
#         axes[i, j].set_ylabel('Q2')
#         axes[i, j].set_xlabel('Q1')
#         axes[i, j].plot(Q1_variable_transformed[i*3+j], Q2_variable_transformed[i*3+j], ',g')
#         axes[i, j].set_title(names_list[i*3+j])
#         axes[i, j].set_xlim(-1.43, 1.43)

# figure.tight_layout()
# plt.subplots_adjust(hspace=0.312, wspace=0.4)
# plt.show()