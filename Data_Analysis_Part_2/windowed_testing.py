"""
This piece of code will be designed to take in two lists of Q1 and Q2, which will then be cut up into a bunch of windows, which will each have an ellipse fitted to them, with the average parameters of all ellipses that are fitted to a point being used to subseqently transform the position of this point as in the ellipse transformation function writen by Timo. This will hopefully recude the noise inherent in the data. First we will write a testing peice of code where the window size will be the same as the step size, as to make sure that the whole process works. We will also then be checking the influence on the noise levels at all steps in the process.
"""

import numpy as np
import matplotlib.pyplot as plt
from ellipse_parameters import *
from matplotlib.ticker import LinearLocator, FormatStrFormatter


def plot_ellipse_parameters(params, title="Ellipse parameters"):
    names = ["x0", "y0", "a", "b", "theta"]

    fig, axes = plt.subplots(5, 1, figsize=(12, 10), sharex=True)
    axes = axes.ravel()

    fig.suptitle(title, fontsize=16, fontweight="bold")

    for i in range(5):
        axes[i].plot(params[:, i], linewidth=1)

        axes[i].set_ylabel(names[i], fontsize=11)
        axes[i].set_title(f"Parameter {names[i]}", loc="left", fontsize=11)
        axes[i].grid(True, alpha=0.3)

        # precies 3 y-as aanduidingen
        axes[i].yaxis.set_major_locator(LinearLocator(3))
        axes[i].yaxis.set_major_formatter(FormatStrFormatter("%.2f"))

    axes[-1].set_xlabel("Window index", fontsize=12)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()

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
def variable_step_window_ellipse_fitting(Q1, Q2, window_size, step_size):
    # This outputs a 6 x floor(len(Q1) / window_size) matrix with the parameters of the differen ellipses. The bottom row is area, which we don't need, so we remove it
    params_matrix = parameters_timeseries(Q1,Q2, window_size=window_size, step_size=step_size)[ : , 0:5]

    plot_ellipse_parameters(params_matrix)
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


Q1, Q2 = np.load(r"C:\Users\timob\OneDrive - UvA\Project 1\GitHub Map\Project-natuurkunde-sterrenkunde-1-Groep-22\Data_Analysis_Part_1\2zQ1.npy"), np.load(r"C:\Users\timob\OneDrive - UvA\Project 1\GitHub Map\Project-natuurkunde-sterrenkunde-1-Groep-22\Data_Analysis_Part_1\2zQ2.npy")

variable_step_window_ellipse_fitting(Q1, Q2, window_size=300, step_size=50)

