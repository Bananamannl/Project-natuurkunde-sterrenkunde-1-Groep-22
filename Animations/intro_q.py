from manim import *
from panel import make_left_panel
import numpy as np


class intro_q(Scene):
    def construct(self):
        left_panel, v_groups = make_left_panel()

        # Zet panel netjes links/midden in beeld
        left_panel.move_to(LEFT * 4)

        self.add(left_panel)

        # =========================
        # Instellingen
        # =========================
        phi = ValueTracker(0)

        a = 0.7
        phi_opt = PI / 4

        graph_width = 3.2
        graph_height = 0.8
        graph_buff = 1.6

        functions = [
            lambda x: 1 + a * np.sin(2*x),
            lambda x: 1 + a * np.cos(2*x),
            lambda x: 1 - a * np.cos(2*x),
        ]

        formulas = [
            r"\text{PD1}=\frac{P_{\text{in}}}{8}(1+a\sin(\phi_{\text{opt}}))",
            r"\text{PD2}=\frac{P_{\text{in}}}{8}(1+a\cos(\phi_{\text{opt}}))",
            r"\text{PD3}=\frac{P_{\text{in}}}{8}(1-a\cos(\phi_{\text{opt}}))",
        ]

        graph_group = VGroup()
        formula_group = VGroup()

        plotted_curves = VGroup()
        moving_dots = VGroup()

        # =========================
        # Grafiekjes + formules
        # =========================
        for i in range(3):
            center = v_groups[i].get_center()

            axes = Axes(
                x_range=[0, TAU, PI / 2],
                y_range=[0, 2, 1],
                x_length=graph_width,
                y_length=graph_height,
                tips=False,
                axis_config={
                    "color": WHITE,
                    "stroke_width": 7,
                },
            )

            axes.move_to([
                center[0] + graph_buff + graph_width / 2,
                center[1],
                0
            ])

            formula = MathTex(formulas[i])
            formula.scale(0.42)
            formula.next_to(axes, RIGHT, buff=0.35)

            graph_group.add(axes)
            formula_group.add(formula)

            # Live curve die steeds verder getekend wordt
            curve = always_redraw(
                lambda i=i, axes=axes: axes.plot(
                    functions[i],
                    x_range=[0, max(phi.get_value(), 0.001), 0.02],
                    color=BLUE,
                    stroke_width=4,
                )
            )

            # Bewegend punt op de curve
            moving_dot = always_redraw(
                lambda i=i, axes=axes: Dot(
                    axes.c2p(
                        phi.get_value(),
                        functions[i](phi.get_value())
                    ),
                    radius=0.055,
                    color=YELLOW
                )
            )

            plotted_curves.add(curve)
            moving_dots.add(moving_dot)

            # Rode rondje opacity laten meebewegen
            red_dot = v_groups[i][-1]

            def make_opacity_updater(index):
                def updater(mob):
                    value = functions[index](phi.get_value())

                    # value zit ongeveer tussen 1-a en 1+a
                    opacity = inverse_interpolate(1 - a, 1 + a, value)
                    opacity = np.clip(opacity, 0.15, 1)

                    mob.set_opacity(opacity)
                return updater

            red_dot.add_updater(make_opacity_updater(i))
        self.wait(1)
        self.play(
            Create(graph_group),
            Write(formula_group),
            run_time=1.5
        )

        self.add(plotted_curves, moving_dots)

        graphs = VGroup(graph_group, formula_group, plotted_curves, moving_dots)

        self.play(
            phi.animate.set_value(TAU),
            run_time=4,
            rate_func=linear
        )

        self.wait(1)

        self.play(
            left_panel.animate.shift(LEFT * 10),
            graphs.animate.shift(LEFT * 4),
            run_time=1.5
        )

        self.remove(left_panel)
        
        # Nu gaan we Q1 en Q2 maken:
        difference_formulas = VGroup(
            MathTex(
                r"Q_1"
                r":="
                r"\text{PD1}-\text{PD2}"
                r"="
                r"\frac{\sqrt{2}aP_{\text{in}}}{8}"
                r"\sin\left(\phi-\frac{\pi}{4}\right),"
            ),
            MathTex(
                r"Q_2"
                r":="
                r"\text{PD1}-\text{PD3}"
                r"="
                r"\frac{\sqrt{2}aP_{\text{in}}}{8}"
                r"\sin\left(\phi+\frac{\pi}{4}\right),"
            )
        )

        difference_formulas.arrange(DOWN, aligned_edge=LEFT, buff=0.65)
        difference_formulas.scale(0.5)
        difference_formulas.move_to(RIGHT * 3.5 + DOWN * 0.5)

        self.play(
            Write(difference_formulas),
            run_time=2
        )

        self.wait(1)

        self.play(
            graphs.animate.shift(LEFT * 6),
            difference_formulas.animate.scale(1.5).shift(LEFT * 3.5 + UP * 2.5)
        )
        self.remove(graphs)
        self.wait(1)

        Q_formulas = VGroup(
            MathTex(
                r"Q_1",
                r"\propto",
                r"\cos\left(\phi+\frac{\pi}{4}\right)"
            ),
            MathTex(
                r"Q_2",
                r"\propto",
                r"\sin\left(\phi+\frac{\pi}{4}\right)"
            )
        )

        Q_formulas.arrange(DOWN, aligned_edge=LEFT, buff=0.65)
        Q_formulas.shift(DOWN * 1)

        self.play(
            Write(Q_formulas),
            run_time=1.5
        )
        self.wait(1)

        # =========================
        # Alleen assenstelsel
        # =========================
        axes = Axes(
            x_range=[-4, 4, 0.5],
            y_range=[-4, 4, 0.5],
            x_length=6,
            y_length=6,
            axis_config={"include_tip": False, "font_size": 15},
        )

        # Q1 en Q2 uit de formules pakken
        Q1_part = Q_formulas[0][0]
        Q2_part = Q_formulas[1][0]

        # Alles behalve Q1 en Q2
        Q_rest = VGroup(
            Q_formulas[0][1:],
            Q_formulas[1][1:]
        )

        # Doelposities als aslabels
        Q1_target = axes.get_x_axis_label(MathTex(r"Q_1"))
        Q2_target = axes.get_y_axis_label(MathTex(r"Q_2"))

        self.play(
            Transform(Q1_part, Q1_target),
            Transform(Q2_part, Q2_target),
            FadeOut(Q_rest),
            FadeOut(difference_formulas),
            run_time=1.5
        )

        self.play(
            Create(axes),
            run_time=1.5
        )

        self.wait(1)
