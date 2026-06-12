import numpy as np
from functions import *
import pyvista as pv


def plot_Q1_Q2_time(Q1, Q2, n_points=None, transform_data=False):
    """
    Plot Q1 en Q2 tegen de tijd in een 3D PyVista plot.

    x-as: tijd / datapuntnummer
    y-as: Q1
    z-as: Q2
    """

    Q1 = np.asarray(Q1)
    Q2 = np.asarray(Q2)

    if transform_data:
        Q1, Q2 = transform(Q1, Q2)

    if n_points is not None:
        Q1 = Q1[:n_points]
        Q2 = Q2[:n_points]

    # tijd-as: gewoon datapuntnummer
    t = np.arange(len(Q1))

    # Eventueel schalen zodat tijd niet gigantisch domineert
    t_scaled = t - np.mean(t)
    t_scaled = t_scaled / np.max(np.abs(t_scaled)) * max(np.max(np.abs(Q1)), np.max(np.abs(Q2)))

    points = np.column_stack((t_scaled, Q1, Q2))

    cloud = pv.PolyData(points)

    plotter = pv.Plotter()

    plotter.add_mesh(
        cloud,
        render_points_as_spheres=False,
        point_size=5
    )

    # Bepaal schaal voor assenlijnen
    max_range = np.max(np.abs(points))

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
        xlabel="time",
        ylabel="Q1",
        zlabel="Q2"
    )

    # Vlak bij Q2 = 0
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

Q1, Q2 = np.load("Data_Analysis_Part_1\\1xQ1.npy"), np.load("Data_Analysis_Part_1\\1xQ2.npy")
plot_Q1_Q2_time(
    Q1[:1530], Q2[:1530]
)