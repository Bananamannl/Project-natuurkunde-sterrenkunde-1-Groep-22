import numpy as np
from functions import *
from ellipse_parameters import *
import matplotlib.pyplot as plt
import pyvista as pv

HoQIs, Q1, Q2 = np.load("Data_Analysis_Part_1\HoQI_fitted_six_vct_list.npy"), np.load("Data_Analysis_Part_1\\1zQ1.npy"), np.load("Data_Analysis_Part_1\\1zQ2.npy")
# Q1, Q2 = transform(Q1[0:10000], Q2[0:10000])
Q1, Q2 = (Q1[0:10000], Q2[0:10000])
parameters = parameters_timeseries(Q1, Q2, window_size=100, step_size=1)

a = parameters[:, 4]

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

HoQI1z_a = orthagonal_displacement_and_parameter(HoQIs, matrix_1z, a)

cloud = pv.PolyData(HoQI1z_a)

plotter = pv.Plotter()

plotter.add_mesh(
    cloud,
    render_points_as_spheres=False,
    point_size=5
)

# Bepaal schaal voor assenlijnen
max_range = np.max(np.abs(HoQI1z_a))

x_axis = pv.Line((-max_range, 0, 0), (max_range, 0, 0))
y_axis = pv.Line((0, -max_range, 0), (0, max_range, 0))
z_axis = pv.Line((0, 0, -max_range), (0, 0, max_range))

plotter.add_mesh(x_axis, line_width=3)
plotter.add_mesh(y_axis, line_width=3)
plotter.add_mesh(z_axis, line_width=3)

# Nulpunt
origin = pv.Sphere(radius=max_range * 0.01, center=(0, 0, 0))
plotter.add_mesh(origin, color="red")

plotter.add_axes(
    xlabel="y",
    ylabel="z",
    zlabel="a"
)


plane = pv.Plane(
    center=(0, 0, 0),
    direction=(0, 0, 1),
    i_size=2 * max_range,
    j_size=2 * max_range
)

plotter.add_mesh(
    plane,
    opacity=0.25,
    color="gray"
)
plotter.show()