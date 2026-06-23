import numpy as np
import pyvista as pv

# Settings:
HoQI = "1x"

HoQIs = np.load("End_Product_Code/single_ellipse_HoQI_displacement_data.npy")

parameter_files = {
    "1x": "HoQI_1x_ellipse_parameter_timeseries.npy",
    "2x": "HoQI_2x_ellipse_parameter_timeseries.npy",
    "3x": "HoQI_3x_ellipse_parameter_timeseries.npy",
    "1z": "HoQI_1z_ellipse_parameter_timeseries.npy",
    "2z": "HoQI_2z_ellipse_parameter_timeseries.npy",
    "3z": "HoQI_3z_ellipse_parameter_timeseries.npy",
}

parameters = np.load(f"End_Product_Code/{parameter_files[HoQI]}")
# the transformation matrix for HoQI 1x
matrix_1x = np.array([
    [0, -np.sqrt(1/3), np.sqrt(1/3), 0, 0, 0],
    [0, 0, 0, 1, 0, 0]])

# the transformation matrix for HoQI 1z
matrix_1z = np.array([
    [1, 0, 0, 0, 0, 0],
    [0, -np.sqrt(1/3), np.sqrt(1/3), 0, 0, 0]])

# the transformation matrix for HoQI 2x
matrix_2x = np.array([
    [np.sqrt(1/3), 0, -np.sqrt(1/3), 0, 0, 0],
    [0, 0, 0, 0, 1, 0]])

# the transformation matrix for HoQI 2z
matrix_2z = np.array([
    [0, 1, 0, 0, 0, 0],
    [np.sqrt(1/3), 0, -np.sqrt(1/3), 0, 0, 0]])

# the transformation matrix for HoQI 3x
matrix_3x = np.array([
    [-np.sqrt(1/3), np.sqrt(1/3), 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1]])

# the transformation matrix for HoQI 3z
matrix_3z = np.array([
    [0, 0, 1, 0, 0, 0],
    [-np.sqrt(1/3), np.sqrt(1/3), 0, 0, 0, 0]])

def slider_plot_parameters(HoQI, HoQIs, parameters, window_size=50000, point_size=3):
    """
    3D plot where:
    x-axis = orthogonal movement component 1
    y-axis = orthogonal movement component 2
    z-axis = ellipse parameter of choice

    Press 'n' to switch to the next parameter.
    """

    # Choose the matrix for the right HoQI
    matrices = {
        "1x": matrix_1x,
        "2x": matrix_2x,
        "3x": matrix_3x,
        "1z": matrix_1z,
        "2z": matrix_2z,
        "3z": matrix_3z,
    }

    step_sizes = {
        "1x": 50,
        "2x": 50,
        "3x": 50,
        "1z": 50,
        "2z": 100,
        "3z": 50,
    }

    matrix = matrices[HoQI]

    print(HoQIs.shape)
    print(matrix.shape)
    # Calculating orthogonal movement 
    orthogonal_movement = HoQIs.T @ matrix.T


    # Repeating parameters
    parameters = np.repeat(parameters, step_sizes[HoQI], axis=0)
    # Shortening the longer data
    N = min(len(orthogonal_movement), len(parameters))
    orthogonal_movement = orthogonal_movement[:N]
    parameters = parameters[:N]

    # Defining the parameter names and scalars for each parameter
    # If stuff blows up (Theta might...) you can change these values 
    parameter_names = ["x0", "y0", "a", "b", "theta"]

    parameter_scales = {
        "x0": 1000,
        "y0": 1000,
        "a": 1000,
        "b": 1000,
        "theta": 1000,
    }

    # Saving current slider and parameter index
    current_parameter_index = [0]
    current_start_index = [0]

    # Select the data depending on the parameter you want to see
    def make_data(parameter_index):
        parameter_name = parameter_names[parameter_index]

        raw_z = parameters[:, parameter_index]

        # Relatieve change
        z = raw_z - np.mean(raw_z)

        # Scaling the parameters
        z = z * parameter_scales[parameter_name]

        return np.column_stack((
            orthogonal_movement[:, 0],
            orthogonal_movement[:, 1],
            z
        ))

    # Find out the bounds for the fit depending on the parameter
    def get_bounds_for_parameter(parameter_index):
        """
        Bounds based on the full dataset for the current parameter,
        not only on the currently visible window.
        """
        all_data = make_data(parameter_index)

        x_min, y_min, z_min = np.min(all_data, axis=0)
        x_max, y_max, z_max = np.max(all_data, axis=0)

        return x_min, x_max, y_min, y_max, z_min, z_max

    # Update the bounds  
    def update_bounds(parameter_index):
        """
        Redraw bounds for the full range of the current parameter.
        """
        bounds = get_bounds_for_parameter(parameter_index)

        plotter.remove_bounds_axes()

        plotter.show_bounds(
            bounds=bounds,
            grid="front",
            location="outer",
            all_edges=True,
            xlabel="Orthogonal component 1",
            ylabel="Orthogonal component 2",
            zlabel="Scaled parameter change",
            font_size=12
        )

    # First data
    data = make_data(current_parameter_index[0])

    # Make a plotter
    plotter = pv.Plotter()
    plotter.set_background("white")

    # Make the first cloud
    cloud = pv.PolyData(data[0:window_size])

    # Color gradient in each window
    time_colors = np.linspace(0, 1, len(cloud.points))
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

    # Initial bounds based on the full data range of the first parameter
    initial_bounds = get_bounds_for_parameter(current_parameter_index[0])

    # Show the bounds 
    plotter.show_bounds(
        bounds=initial_bounds,
        grid="front",
        location="outer",
        all_edges=True,
        xlabel="Orthogonal component 1",
        ylabel="Orthogonal component 2",
        zlabel="Scaled parameter change",
        font_size=12
    )

    # Plot the axes
    plotter.add_axes(
        xlabel="Orthogonal 1",
        ylabel="Orthogonal 2",
        zlabel="Parameter",
        line_width=2,
        labels_off=False
    )

    # Titel
    parameter = parameter_names[current_parameter_index[0]]

    title_actor = plotter.add_text(
        f"{parameter} against orthogonal movement of HoQI {HoQI}",
        position="upper_left",
        font_size=12,
        color="black"
    )

    # Add visible origin as a point
    origin = pv.PolyData(np.array([[0, 0, 0]]))

    plotter.add_mesh(
        origin,
        color="black",
        point_size=10,
        render_points_as_spheres=True
    )

    plotter.view_isometric()
    plotter.reset_camera()

    def update_cloud(update_bounds_flag=False):
        """
        Updates points.
        Bounds are only updated when update_bounds_flag=True.
        Bounds are then based on the current parameter.
        """
        parameter_index = current_parameter_index[0]
        start = current_start_index[0]
        end = start + window_size

        new_data = make_data(parameter_index)
        visible_data = new_data[start:end]

        cloud.points = visible_data

        if update_bounds_flag:
            update_bounds(parameter_index)

        plotter.render()

    def update_window(value):
        """
        Gets called by the slider.
        Only updates the visible points, not the bounds.
        """
        current_start_index[0] = int(value)
        update_cloud(update_bounds_flag=False)

    def next_parameter():
        """
        Gets called when pressing 'n'.
        Updates points, title, and bounds for the full range of the new parameter.
        """
        current_parameter_index[0] += 1
        current_parameter_index[0] %= len(parameter_names)

        parameter = parameter_names[current_parameter_index[0]]

        # Update cloud and full-parameter bounds
        update_cloud(update_bounds_flag=True)

        # Replace title
        nonlocal title_actor
        plotter.remove_actor(title_actor)

        title_actor = plotter.add_text(
            f"{parameter} against orthogonal movement of HoQI {HoQI}",
            position="upper_left",
            font_size=12,
            color="black"
        )

        plotter.render()

    # Slider
    plotter.add_slider_widget(
        callback=update_window,
        rng=[0, len(data) - window_size],
        value=0,
        title="Start index",
        interaction_event="always",
        style="modern",
        fmt="%.0f"
    )

    # Link the 'n' key to the next parameter
    plotter.add_key_event("n", next_parameter)

    plotter.show()

slider_plot_parameters(HoQI, HoQIs=HoQIs, parameters=parameters)