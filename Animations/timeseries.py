from manim import *
import numpy as np

class time_series(Scene):
    def construct(self):
        ## Instellingen
        graph_width = 3
        graph_height = 2

        pos_list = [[-5, 2, 0], [-0.5, 2, 0], [4, 2, 0], [-5, -2, 0], [-0.5, -2, 0], [4, -2, 0]]

        plot_names = ["X", "Y", "Z", "RX", "RY", "RZ"]

        graphs = VGroup()

        axes_list = VGroup()
        x_labels = VGroup()
        y_labels = VGroup()
        names = VGroup()

        ## Data import
        pos_data = np.load("C:/Users/Admin/Documents/Programmer_Projecten/Project-natuurkunde-sterrenkunde-1-Groep-22/Data_Analysis_Part_1/fitted_six_vct_list.npy")

        for i in range(0, 6):
            axes = Axes(
                x_range= [0, len(pos_data[0:int(3e6), i]), 600000],
                y_range= [min(pos_data[0:int(3e6), i]), max(pos_data[0:int(3e6), i]), 100],
                x_length= graph_width,
                y_length= graph_height,
                tips= False,
                axis_config={
                    "color": WHITE,
                    "stroke_width": 5,
                }
            )

            axes.move_to(pos_list[i])
            x_lab = axes.get_x_axis_label(Tex("Time (ms)").scale(0.4), edge=RIGHT, direction=RIGHT, buff=0.2)
            if i < 3:
                y_lab = axes.get_y_axis_label(Tex("Displacement (um)").scale(0.4).rotate(PI/2), edge=LEFT, direction=LEFT, buff=0.2)
            else: 
                y_lab = axes.get_y_axis_label(Tex("Displacement (urad)").scale(0.4).rotate(PI/2), edge=LEFT, direction=LEFT, buff=0.2)

            name = Text(plot_names[i]).next_to(axes, UP, buff = 0)

            axes_list.add(axes)
            x_labels.add(x_lab)
            y_labels.add(y_lab)
            names.add(name)

            batch_points = [pos_data[l, i] for l in range(0, len(pos_data[0:int(3e6), i]), 1000)]

            time = [l for l in range(0, len(pos_data[0:int(3e6), i]), 1000)] 

            graph = axes.plot_line_graph(time, batch_points, add_vertex_dots=False, line_color = BLUE, stroke_width = 0.8)
            graphs.add(graph)

        self.wait(0.5)
        self.play(Create(axes_list, run_time=0.8), Write(x_labels, run_time=0.8), Write(y_labels, run_time=0.8), Write(names))
        self.wait(0.3)

        self.play(Write(graphs, run_time=5))
        self.wait(2)
