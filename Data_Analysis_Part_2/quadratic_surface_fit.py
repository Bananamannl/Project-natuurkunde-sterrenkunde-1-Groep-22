import numpy as np
from functions import *
from ellipse_parameters import *
import matplotlib.pyplot as plt
import pyvista as pv

HoQIs, Q1, Q2 = np.load("Data_Analysis_Part_1\HoQI_fitted_six_vct_list.npy"), np.load("Data_Analysis_Part_1\\1zQ1.npy"), np.load("Data_Analysis_Part_1\\1zQ2.npy")
# Q1, Q2 = transform(Q1[0:10000], Q2[0:10000])
Q1, Q2 = (Q1[0:10000], Q2[0:10000])
parameters = parameters_timeseries(Q1, Q2, window_size=100, step_size=1)

a = parameters[:, 0]

matrix_1z = np.array([
    [-2/3, 1/3, 1/3, 0, 0, 0],
    [0, -np.sqrt(1/3), np.sqrt(1/3), 0, 0, 0]
])

def orthagonal_displacement_and_parameter(HoQIs, matrix, a):
    """
    a function that takes in: the HoQI displacements list, a particular othogonal transformation matrix, the Q1, Q2 for the HoQI you are looking at.
    The function's output is a (3.000.000, 3) np array that has the ortogonal positions in row 1 and 2 and the norm of every data point in row 3
    """
    vectors = HoQIs[:9901] @ matrix.T
    a = (a - np.mean(a)) * 1000
    return np.hstack((vectors, a[:, None]))

points = orthagonal_displacement_and_parameter(HoQIs, matrix_1z, a)



x = points[:, 0]
y = points[:, 1]
z = points[:, 2]

A = np.column_stack((
    np.ones_like(x),
    x,
    y,
    x*y,
    x ** 2 * y,
    y ** 2 * x,
    x**2 * y**2,
    x**2,
    y**2,
    x**3,
    y**3,
    x**3 * y,
    x**3 * y**2,
    x**3 * y **3,
    y**3 * x**2,
    y**3 * x
))

coeffs = np.linalg.lstsq(A, z, rcond=None)[0]

print(np.array2string(coeffs, separator=", "))