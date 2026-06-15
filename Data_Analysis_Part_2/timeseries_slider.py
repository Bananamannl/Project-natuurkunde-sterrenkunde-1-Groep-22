import numpy as np
import pyvista as pv

#Settings
data_path = "Data_Analysis_Part_2\\test_3d_vector_norms_3z.npy"
window_size = 50000
point_size = 3

point_color = "dodgerblue"
background_color = "white"

#Data laden
points_all = np.load(data_path)

#Plot maken met eerste window 
plotter = pv.Plotter()
plotter.set_background(background_color)

cloud = pv.PolyData(points_all[0:window_size])

#Kleur aanpassen in windows
time_colors = np.linspace(0, 1, window_size)
cloud["time"] = time_colors

plotter.add_mesh(
    cloud,
    scalars="time",
    cmap="viridis",
    render_points_as_spheres=True,
    point_size=point_size,
    opacity=0.9,
    scalar_bar_args={"title": "Time in window"}
)

#Bounds van de assen bepalen
x_min, y_min, z_min = np.min(points_all, axis=0)
x_max, y_max, z_max = np.max(points_all, axis=0)

#Assen plotten
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

#Klein assenstelsel in de hoek
plotter.add_axes(
    xlabel="Q1",
    ylabel="Q2",
    zlabel="Norm",
    line_width=2,
    labels_off=False
)

# Titel
plotter.add_text(
    "3D point cloud over time",
    position="upper_left",
    font_size=12,
    color="black"
)
plotter.view_isometric()

#Slider functie
def update_window(value):
    start = int(value)
    end = start + window_size
    cloud.points = points_all[start:end]

    plotter.render()

plotter.add_slider_widget(
    callback=update_window,
    rng=[0, len(points_all) - window_size],
    value=0,
    title="Start index",
    interaction_event="always",
    style="modern",
    fmt="%.0f"
)

plotter.show()