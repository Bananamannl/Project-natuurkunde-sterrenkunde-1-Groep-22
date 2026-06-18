import numpy as np
import pyvista as pv


def slider_plot_Q1_Q2(Q1, Q2, window_size=10000, point_size=3):
    """
    2D PyVista plot of Q1 vs Q2 with:
    - live updating slider
    - visible moving window of points
    - unit circle shown at the same time
    """

    Q1 = np.asarray(Q1)
    Q2 = np.asarray(Q2)

    N = min(len(Q1), len(Q2))
    Q1 = Q1[:N]
    Q2 = Q2[:N]

    if window_size > N:
        window_size = N

    # Data in 3D format, but z = 0 so it is a 2D plot
    data = np.column_stack((Q1, Q2, np.zeros(N)))

    # Initial visible window
    cloud = pv.PolyData(data[:window_size])
    cloud["time"] = np.linspace(0, 1, window_size)

    plotter = pv.Plotter()
    plotter.set_background("white")

    # Points
    plotter.add_mesh(
        cloud,
        scalars="time",
        cmap="viridis",
        render_points_as_spheres=True,
        point_size=point_size,
        opacity=0.9,
        scalar_bar_args={"title": "Time in window"}
    )

    # Unit circle
    theta = np.linspace(0, 2 * np.pi, 500)
    circle_points = np.column_stack((
        np.cos(theta),
        np.sin(theta),
        np.zeros_like(theta)
    ))

    circle = pv.PolyData(circle_points)
    circle.lines = np.hstack((
        [len(circle_points)],
        np.arange(len(circle_points))
    ))

    plotter.add_mesh(
        circle,
        color="red",
        line_width=3,
        label="Unit circle"
    )

    # Origin
    origin = pv.PolyData(np.array([[0, 0, 0]]))
    plotter.add_mesh(
        origin,
        color="black",
        point_size=10,
        render_points_as_spheres=True
    )

    # Fixed bounds based on full data + unit circle
    x_min = min(np.min(Q1), -1)
    x_max = max(np.max(Q1), 1)
    y_min = min(np.min(Q2), -1)
    y_max = max(np.max(Q2), 1)

    margin_x = 0.05 * (x_max - x_min)
    margin_y = 0.05 * (y_max - y_min)

    bounds = [
        x_min - margin_x, x_max + margin_x,
        y_min - margin_y, y_max + margin_y,
        -0.1, 0.1
    ]

    plotter.show_bounds(
        bounds=bounds,
        grid="front",
        location="outer",
        all_edges=True,
        xlabel="Q1",
        ylabel="Q2",
        zlabel="",
        font_size=12
    )

    plotter.add_axes(
        xlabel="Q1",
        ylabel="Q2",
        zlabel="",
        line_width=2,
        labels_off=False
    )

    plotter.add_text(
        "Q1 vs Q2 with moving window",
        position="upper_left",
        font_size=12,
        color="black"
    )

    def update_window(value):
        start = int(value)
        end = start + window_size

        visible_data = data[start:end]

        cloud.points = visible_data
        cloud["time"] = np.linspace(0, 1, len(visible_data))

        plotter.render()

    plotter.add_slider_widget(
        callback=update_window,
        rng=[0, N - window_size],
        value=0,
        title="Start index",
        interaction_event="always",
        style="modern",
        fmt="%.0f"
    )

    # Make it look 2D
    plotter.view_xy()
    plotter.reset_camera()

    plotter.show()

Q1, Q2 = np.load(r"C:\Users\timob\OneDrive - UvA\Project 1\GitHub Map\Project-natuurkunde-sterrenkunde-1-Groep-22\Data_Analysis_Part_1\1xQ1.npy"), np.load(r"C:\Users\timob\OneDrive - UvA\Project 1\GitHub Map\Project-natuurkunde-sterrenkunde-1-Groep-22\Data_Analysis_Part_1\1xQ2.npy")


slider_plot_Q1_Q2(Q1, Q2)