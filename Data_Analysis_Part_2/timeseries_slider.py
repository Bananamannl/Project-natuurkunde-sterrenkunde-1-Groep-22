import numpy as np
import pyvista as pv

#Settings
data_path = "Data_Analysis_Part_2\\test_3d_vector_norms_3z.npy"
window_size = 50000
point_size = 3

#Load the data
data = np.load(data_path)

def slider_plot(data, window_size=50000, point_size=3):
    """
    A function for creating a 
    """

    #Set the first window
    plotter = pv.Plotter()
    plotter.set_background("white")

    cloud = pv.PolyData(data[0:window_size])

    #Set the color transotion
    time_colors = np.linspace(0, 1, window_size)
    cloud["time"] = time_colors

    #Plot the first window
    plotter.add_mesh(
        cloud,
        scalars="time",
        cmap="viridis",
        render_points_as_spheres=True,
        point_size=point_size,
        opacity=0.9,
        scalar_bar_args={"title": "Time in window"}
    )

    #Determine axes bounds
    x_min, y_min, z_min = np.min(data, axis=0)
    x_max, y_max, z_max = np.max(data, axis=0)

    #Plot axes
    plotter.show_bounds(
        bounds=(x_min, x_max, y_min, y_max, z_min, z_max),
        grid="front",
        location="outer",
        all_edges=True,
        xlabel="Q1",
        ylabel="Q2",
        zlabel="Norm",
        font_size=12
    )

    #Plot a small coordinate system in te botom left
    plotter.add_axes(
        xlabel="Q1",
        ylabel="Q2",
        zlabel="Norm",
        line_width=2,
        labels_off=False
    )

    #Titel
    plotter.add_text(
        "3D point cloud over time",
        position="upper_left",
        font_size=12,
        color="black"
    )
    plotter.view_isometric() #Set the standard viewing angle

    #Slider functie
    def update_window(value):
        start = int(value)
        end = start + window_size
        cloud.points = data[start:end]

        plotter.render()

    plotter.add_slider_widget(
        callback=update_window,
        rng=[0, len(data) - window_size],
        value=0,
        title="Start index",
        interaction_event="always",
        style="modern",
        fmt="%.0f"
    )

    plotter.show()