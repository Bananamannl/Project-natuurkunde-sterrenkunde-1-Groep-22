import numpy as np
from functions import *
import pyvista as pv
from windowed_ellipse_fitting import *

matrix_1x = np.array([
    [0, -np.sqrt(1/3), np.sqrt(1/3), 0, 0, 0],
    [0, 0, 0, 1/3, 1/3, 1/3]
])
#output: (y, z)

matrix_1z = np.array([
    [-2/3, 1/3, 1/3, 0, 0, 0],
    [0, -np.sqrt(1/3), np.sqrt(1/3), 0, 0, 0]
])
#output: (x, y)

matrix_3z = np.array([
    [-1/np.sqrt(3), 1/np.sqrt(3), 0, 0, 0, 0],
    [1/3, 1/3, -2/3, 0, 0, 0]])

def orthagonal_displacement_and_norms(HoQIs, matrix, x, y):
    """
    a function that takes in: the HoQI displacements list, a particular othogonal transformation matrix, the Q1, Q2 for the HoQI you are looking at.
    The function's output is a (3.000.000, 3) np array that has the ortogonal positions in row 1 and 2 and the norm of every data point in row 3
    """
    vectors = HoQIs @ matrix.T
    norms = (np.sqrt(x**2 + y **2) -1 ) * 100
    return np.hstack((vectors, norms[:, None]))


HoQIs, Q1, Q2 = np.load("Data_Analysis_Part_1\HoQI_fitted_six_vct_list.npy"), np.load("Data_Analysis_Part_1\\3zQ1.npy"), np.load("Data_Analysis_Part_1\\3zQ2.npy")
Q1, Q2 = standard_step_window_ellipse_fitting(Q1, Q2, window_size=250)

#code voor de plot
points = orthagonal_displacement_and_norms(HoQIs, matrix_3z, Q1, Q2)

np.save("test_3d_vector_norms_3z.npy", points)
# less_points = points[10000:12000]

# cloud = pv.PolyData(less_points)

# plotter = pv.Plotter()

# plotter.add_mesh(
#     cloud,
#     render_points_as_spheres=False,
#     point_size=5
# )

# # Bepaal schaal voor assenlijnen
# max_range = np.max(np.abs(less_points))

# x_axis = pv.Line((-max_range, 0, 0), (max_range, 0, 0))
# y_axis = pv.Line((0, -max_range, 0), (0, max_range, 0))
# z_axis = pv.Line((0, 0, -max_range), (0, 0, max_range))

# plotter.add_mesh(x_axis, line_width=3)
# plotter.add_mesh(y_axis, line_width=3)
# plotter.add_mesh(z_axis, line_width=3)

# # Nulpunt
# origin = pv.Sphere(radius=max_range * 0.01, center=(0, 0, 0))
# plotter.add_mesh(origin, color="red")

# plotter.add_axes(
#     xlabel="y",
#     ylabel="z",
#     zlabel="norm"
# )


# plane = pv.Plane(
#     center=(0, 0, 0),
#     direction=(0, 0, 1),
#     i_size=2 * max_range,
#     j_size=2 * max_range
# )

# plotter.add_mesh(
#     plane,
#     opacity=0.25,
#     color="gray"
# )
# plotter.show()