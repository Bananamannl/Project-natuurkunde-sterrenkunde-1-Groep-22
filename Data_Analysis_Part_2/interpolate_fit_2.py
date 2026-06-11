from scipy.interpolate import RBFInterpolator
from functions import *
from ellipse_parameters import *
import numpy as np
import pyvista as pv

HoQIs, Q1, Q2 = np.load("Data_Analysis_Part_1\HoQI_fitted_six_vct_list.npy"), np.load("Data_Analysis_Part_1\\1zQ1.npy"), np.load("Data_Analysis_Part_1\\1zQ2.npy")
Q1, Q2 = transform(Q1[0:10000], Q2[0:10000])
# Q1, Q2 = (Q1[0:10000], Q2[0:10000])
parameters = parameters_timeseries(Q1, Q2, window_size=100, step_size=1)

a = parameters[:, 2]

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

# Data
x_data = points[:, 0]
y_data = points[:, 1]
z_data = points[:, 2]

xy_data = np.column_stack((x_data, y_data))

# RBF fit
rbf = RBFInterpolator(
    xy_data,
    z_data,
    kernel="thin_plate_spline",
    smoothing=0.01
)

# Grid maken
x_grid = np.linspace(x_data.min(), x_data.max(), 100)
y_grid = np.linspace(y_data.min(), y_data.max(), 100)

X, Y = np.meshgrid(x_grid, y_grid)
xy_grid = np.column_stack((X.ravel(), Y.ravel()))

Z = rbf(xy_grid).reshape(X.shape)

# Surface maken
surface = pv.StructuredGrid(X, Y, Z)

# Originele datapunten
cloud = pv.PolyData(points)

plotter = pv.Plotter()

plotter.add_mesh(
    surface,
    opacity=0.45,
    color="orange",
    show_edges=False
)

plotter.add_mesh(
    cloud,
    render_points_as_spheres=False,
    point_size=5,
    color="lightblue"
)

plotter.add_axes(
    xlabel="x",
    ylabel="y",
    zlabel="a"
)

plotter.show()