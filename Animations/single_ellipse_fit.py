from manim import *
import numpy as np

class single_ellipse_fit(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-4, 4, 0.5],
            y_range=[-4, 4, 0.5],
            x_length=6,
            y_length=6,
            axis_config={"include_tip": False, "font_size": 15},
        )

        x_label = axes.get_x_axis_label("Q1")
        y_label = axes.get_y_axis_label("Q2")
        circle = Circle(radius=1, color=BLUE).move_to(axes.c2p(0, 0))

        Q1, Q2 = np.load(r"C:\Users\timob\OneDrive - UvA\Project 1\GitHub Map\Project-natuurkunde-sterrenkunde-1-Groep-22\Data_Analysis_Part_1\1xQ1.npy"), np.load(r"C:\Users\timob\OneDrive - UvA\Project 1\GitHub Map\Project-natuurkunde-sterrenkunde-1-Groep-22\Data_Analysis_Part_1\1xQ2.npy")

        Qs = np.column_stack((Q1[30000:35000], Q2[30000:35000]))

        dots = VGroup(*[
            Dot(point=axes.c2p(x, y), radius=0.03, color=RED)
            for x, y in Qs
        ])

        # Ellipsparameters: [x0, y0, a, b, theta]
        # [-0.2200044  -0.50131709  2.90227141  2.57809731  2.16018091]
        x0 = -0.2200044
        y0 = -0.50131709
        a = 2.90227141
        b = 2.57809731
        theta = 2.16018091

        ellipse_points = []
        for t in np.linspace(0, TAU, 300):
            x = x0 + a * np.cos(t) * np.cos(theta) - b * np.sin(t) * np.sin(theta)
            y = y0 + a * np.cos(t) * np.sin(theta) + b * np.sin(t) * np.cos(theta)
            ellipse_points.append(axes.c2p(x, y))

        ellipse = VMobject(color=BLUE)
        ellipse.set_points_smoothly(ellipse_points)

        self.add(axes, circle, x_label, y_label, dots)
        self.wait(1)
        self.play(Create(ellipse))
        self.wait(2)