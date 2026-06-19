from manim import *
import numpy as np

class windowed_ellipse_fit(Scene):
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

        circle = Circle(radius=1, color=BLUE).move_to(
            axes.c2p(0, 0)
        )

        self.add(axes, x_label, y_label, circle)

        Q1 = np.load(
            r"C:\Users\janne\OneDrive\Documenten\Studie Natuur- Sterrenkunde\Jaar 1\N&S_Project\Project-natuurkunde-sterrenkunde-1-Groep-22\Data_Analysis_Part_1\1xQ1.npy"
        )

        Q2 = np.load(
            r"C:\Users\janne\OneDrive\Documenten\Studie Natuur- Sterrenkunde\Jaar 1\N&S_Project\Project-natuurkunde-sterrenkunde-1-Groep-22\Data_Analysis_Part_1\1xQ2.npy"
        )

        # ==========================================================
        # WINDOWS
        # ==========================================================

        start_index = 1819000
        end_index = 1824000

        n_windows = 5

        window_size = (end_index - start_index) // n_windows

        # VUL HIER JE 5 ELLIPSE PARAMETERS IN
        # (x0, y0, a, b, theta)

        ellipse_params = [

            (-0.22743413, -0.50297871,  2.89857111,  2.57752728,  2.15924495), # WINDOW 1

            (-0.22506378, -0.50100047,  2.88244602,  2.56059351,  2.16067717),   # WINDOW 2

            (-0.21104056, -0.5005457,   2.87346276,  2.54911861,  2.16634957),   # WINDOW 3

            (-0.22051271, -0.50469906,  2.54160085,  2.85980108,  0.59443688 + PI),   # WINDOW 4

            (-0.24281496, -0.49736554,  2.40651206,  2.6897109,   0.61042734 + PI),   # WINDOW 5
        ]

        # Hier blijven alle getransformeerde punten staan
        accumulated_circle_points = VGroup()

        colors = [
            RED,
            YELLOW,
            GREEN,
            ORANGE,
            PURPLE,
        ]

        for i in range(n_windows):

            # --------------------------------------------------
            # Data window
            # --------------------------------------------------

            start = start_index + i * window_size
            stop = start + window_size

            Qs = np.column_stack(
                (
                    Q1[start:stop],
                    Q2[start:stop]
                )
            )

            color = colors[i]

            dots = VGroup(*[
                Dot(
                    point=axes.c2p(x, y),
                    radius=0.025,
                    color=color
                )
                for x, y in Qs
            ])

            self.add(dots)

            # --------------------------------------------------
            # Ellipse parameters
            # --------------------------------------------------

            x0, y0, a, b, theta = ellipse_params[i]

            ellipse_points = []

            for t in np.linspace(0, TAU, 300):

                x = (
                    x0
                    + a*np.cos(t)*np.cos(theta)
                    - b*np.sin(t)*np.sin(theta)
                )

                y = (
                    y0
                    + a*np.cos(t)*np.sin(theta)
                    + b*np.sin(t)*np.cos(theta)
                )

                ellipse_points.append(
                    axes.c2p(x, y)
                )

            ellipse = VMobject(color=WHITE)
            ellipse.set_points_smoothly(
                ellipse_points
            )

            self.play(
                Create(ellipse),
                run_time=0.8 #run_time=1.5
            )

            # --------------------------------------------------
            # Transform ellipse -> unit circle
            # --------------------------------------------------

            unit_ellipse = circle.copy().set_color(
                WHITE
            )

            self.play(
                # Rotate(dots, angle = -theta),
                Transform(
                    ellipse,
                    unit_ellipse
                ),
                run_time=0.8 #run_time=1.5
            )

            # --------------------------------------------------
            # Transform points
            # --------------------------------------------------

            def ellipse_to_circle(x, y):
                xp = (
                    (x - x0)*np.cos(theta)
                    + (y - y0)*np.sin(theta)
                )

                yp = (
                    -(x - x0)*np.sin(theta)
                    + (y - y0)*np.cos(theta)
                )

                return xp/a, yp/b

            transformed_dots = VGroup(*[
                Dot(
                    point=(
                        circle.get_center()
                        + np.array(
                            [*ellipse_to_circle(x, y), 0]
                        )
                    ),
                    radius=0.025,
                    color=color
                )
                for x, y in Qs
            ])

            self.play(
                # Rotate(dots, angle = - theta),
                Transform(
                    dots,
                    transformed_dots
                ),
                run_time=1 #run_time=2
            )

            accumulated_circle_points.add(*dots)

            self.remove(ellipse)

            self.wait (0.3)#self.wait(0.5)

        self.wait(3)