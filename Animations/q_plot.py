from manim import *
import numpy as np 

class q_plot(Scene):
    def construct(self):

        # ─────────────────────────────
        # 1. Assenstelsel
        # ─────────────────────────────
        axes = Axes(
            x_range=[-4, 4, 0.5],
            y_range=[-4, 4, 0.5],
            x_length=6,
            y_length=6,
            axis_config={ "include_tip": False, "font_size": 15},
        )

        x_label = axes.get_x_axis_label("Q1")
        y_label = axes.get_y_axis_label("Q2")

        circle = Circle(radius=1, color=BLUE).move_to(axes.c2p(0, 0))
        self.add (axes, x_label, y_label)
        self.play(Create(circle))

        # ─────────────────────────────
        # 2. Data laden
        # ─────────────────────────────
        Q1, Q2 = np.load(r"C:\Users\janne\OneDrive\Documenten\Studie Natuur- Sterrenkunde\Jaar 1\N&S_Project\Project-natuurkunde-sterrenkunde-1-Groep-22\Data_Analysis_Part_1\1xQ1.npy"), \
                np.load(r"C:\Users\janne\OneDrive\Documenten\Studie Natuur- Sterrenkunde\Jaar 1\N&S_Project\Project-natuurkunde-sterrenkunde-1-Groep-22\Data_Analysis_Part_1\1xQ2.npy")

        # interval met nette elips 
        Q1_1 = Q1 [30000:35000]
        Q2_1 = Q2 [30000:35000]

        Qs_1 = np.column_stack((Q1_1, Q2_1))

        # ─────────────────────────────
        # 3. Batch-wise plot (50 per keer)
        # ─────────────────────────────
        batch_size = 50

        for i in range(0, len(Qs_1), batch_size):

            batch_points = Qs_1[i:i + batch_size]

            batch_dots = VGroup()

            for x, y in batch_points:
                batch_dots.add(
                    Dot(
                        point=axes.c2p(x, y),
                        radius=0.03,
                        color=RED
                    )
                )

            self.add(batch_dots)

            # snelheid van animatie
            self.wait(0.0005)

        # ─────────────────────────────
        # 4. Eindresultaat laten staan
        # ─────────────────────────────
        self.wait(2)


class q_plot_points(Scene):
    def construct(self):

        # ─────────────────────────────
        # 1. Assenstelsel
        # ─────────────────────────────
        axes = Axes(
            x_range=[-4, 4, 0.5],
            y_range=[-4, 4, 0.5],
            x_length=6,
            y_length=6,
            axis_config={ "include_tip": False, "font_size": 15},
        )

        x_label = axes.get_x_axis_label("Q1")
        y_label = axes.get_y_axis_label("Q2")

        circle = Circle(radius=1, color=BLUE).move_to(axes.c2p(0, 0))
        self.add (axes, x_label, y_label)
        self.play(Create(circle))

        # ─────────────────────────────
        # 2. Data laden
        # ─────────────────────────────
        Q1, Q2 = np.load(r"C:\Users\janne\OneDrive\Documenten\Studie Natuur- Sterrenkunde\Jaar 1\N&S_Project\Project-natuurkunde-sterrenkunde-1-Groep-22\Data_Analysis_Part_1\1xQ1.npy"), \
                np.load(r"C:\Users\janne\OneDrive\Documenten\Studie Natuur- Sterrenkunde\Jaar 1\N&S_Project\Project-natuurkunde-sterrenkunde-1-Groep-22\Data_Analysis_Part_1\1xQ2.npy")

        # interval met punten in het midden 
        Q1_1 = Q1[1819000:1824000]
        Q2_1 = Q2[1819000:1824000]

        Qs_1 = np.column_stack((Q1_1, Q2_1))

        # ─────────────────────────────
        # 3. Batch-wise plot (50 per keer)
        # ─────────────────────────────
        batch_size = 50

        for i in range(0, len(Qs_1), batch_size):

            batch_points = Qs_1[i:i + batch_size]

            batch_dots = VGroup()

            for x, y in batch_points:
                batch_dots.add(
                    Dot(
                        point=axes.c2p(x, y),
                        radius=0.03,
                        color=RED
                    )
                )

            self.add(batch_dots)

            # snelheid van animatie
            self.wait(0.0005)

        # ─────────────────────────────
        # 4. Eindresultaat laten staan
        # ─────────────────────────────
        self.wait(2)