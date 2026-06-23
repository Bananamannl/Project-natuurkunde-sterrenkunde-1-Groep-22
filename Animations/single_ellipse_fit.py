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

        ellipse = VMobject(color=WHITE)
        ellipse.set_points_smoothly(ellipse_points)

        params_text = VGroup(
            Tex(r"\text{Ellipse parameters:}").scale(1),
            MathTex(r"x_0 = -0.220").scale(0.6),
            MathTex(r"y_0 = -0.501").scale(0.6),
            MathTex(r"a = 2.902").scale(0.6),
            MathTex(r"b = 2.578").scale(0.6),
            MathTex(r"\theta = 2.160").scale(0.6),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)

        function_text = VGroup(
            MathTex(r"\text{Elliptical model:}").scale(1),
            MathTex(
                r"\begin{pmatrix} x \\ y \end{pmatrix}"
                r"="
                r"\begin{pmatrix} x_0 \\ y_0 \end{pmatrix}"
                r"+"
                r"\begin{pmatrix}"
                r"\cos(\theta) & -\sin(\theta)\\"
                r"\sin(\theta) & \cos(\theta)"
                r"\end{pmatrix}"
                r"\begin{pmatrix}"
                r"a\cos(\phi)\\"
                r"b\sin(\phi)"
                r"\end{pmatrix}"
            ).scale(0.55)
                ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)

        text = VGroup(params_text, function_text).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.75
        )

        scene_group = VGroup(axes, circle, x_label, y_label, dots, ellipse)

        self.add(axes, circle, x_label, y_label, dots)
        self.wait(1)
        self.play(Create(ellipse))
        self.wait(1)

        text.to_corner(UL).shift(DOWN * 0.9 + RIGHT * 0.6)

        self.play(
            scene_group.animate.shift(RIGHT * 2.6),
            FadeIn(text)
        )
        self.wait(1)

        def ellipse_to_circle(x, y):
            xp = (x - x0) * np.cos(theta) + (y - y0) * np.sin(theta)
            yp = -(x - x0) * np.sin(theta) + (y - y0) * np.cos(theta)
            return xp / a, yp / b

        unit_ellipse = circle.copy().set_color(WHITE)

        transformed_dots = VGroup(*[
            Dot(
                point=circle.get_center() + np.array([*ellipse_to_circle(x, y), 0]),
                radius=0.03,
                color=RED
            )
            for x, y in Qs
        ])

        self.play(Transform(ellipse, unit_ellipse), run_time=2)
        self.wait(0.5)

        self.play(Transform(dots, transformed_dots), run_time=3)
        self.play(FadeOut(unit_ellipse, circle, ellipse))
        self.wait(2)
        self.play(scene_group.animate.shift(LEFT * 7.5), text.animate.shift(LEFT * 7.5))
        self.play(FadeOut(text))

        Q_formulas = VGroup(
            MathTex(
                r"Q_1",
                r"\propto",
                r"\sin\left(\phi-\frac{\pi}{4}\right)"
            ),
            MathTex(
                r"Q_2",
                r"\propto",
                r"\cos\left(\phi-\frac{\pi}{4}\right)"
            )
        )

        tan_text = MathTex(
            r"\frac{Q_1}{Q_2}"
            r"="
            r"\frac{\sin\left(\phi-\frac{\pi}{4}\right)}"
            r"{\cos\left(\phi-\frac{\pi}{4}\right)}"
            r"="
            r"\tan\left(\phi-\frac{\pi}{4}\right)"
        )

        arctan_text = MathTex(
            r"\arctan\left(\frac{Q_1}{Q_2}\right)"
            r"="
            r"\phi_{\mathrm{opt}}"
        )

        all_formulas = VGroup(
            Q_formulas,
            tan_text,
            arctan_text
        )

        Q_formulas.arrange(DOWN, aligned_edge=LEFT, buff=0.35)

        all_formulas.arrange(DOWN, aligned_edge=LEFT, buff=0.65)
        all_formulas.scale(0.8)
        all_formulas.to_edge(RIGHT, buff=0.5)
        all_formulas.shift(UP * 0.3)

        all_gone = VGroup(tan_text, Q_formulas, scene_group)
        self.play(Write(Q_formulas)) 
        self.play(Write(tan_text))
        self.wait(1)
        self.play(Write(arctan_text))
        self.wait(2)
        self.play(FadeOut(all_gone))
        self.play(arctan_text.animate.move_to([0, 1.5, 0]))
        self.wait(2)