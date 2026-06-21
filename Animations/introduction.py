from manim import *
import numpy as np


class introduction(Scene):
    def make_leg(self, hip, knee, ankle, color=WHITE):
        thigh = Line(hip, knee, stroke_width=8, color=color)
        shin = Line(knee, ankle, stroke_width=8, color=color)

        return VGroup(thigh, shin)
    def arrow_and_text(self):
        text = Text("Gravitational wave detector (arm)", font_size=24, weight=BOLD)
        arrow = 
    def make_impact(self, contact_point):
        return VGroup(
            Line(contact_point + LEFT * 0.15, contact_point + LEFT * 0.55 + UP * 0.25),
            Line(contact_point + RIGHT * 0.15, contact_point + RIGHT * 0.55 + UP * 0.25),
            Line(contact_point + UP * 0.05, contact_point + UP * 0.45),
        ).set_stroke(YELLOW, width=5)
    def make_tube(self):
        tube_width = config.frame_width + 4
        tube_height = 0.75

        tube_body = Rectangle(
            width=tube_width,
            height=tube_height,
            color=WHITE,
            stroke_width=4
        )
        tube_body.set_fill(GRAY, opacity=1)

        inner_shadow = Rectangle(
            width=tube_width,
            height=tube_height * 0.35,
            color=DARK_GRAY,
            stroke_width=0
        )
        inner_shadow.set_fill(DARK_GRAY, opacity=0.6)

        highlight = Line(
            LEFT * tube_width / 2 + UP * 0.22,
            RIGHT * tube_width / 2 + UP * 0.22,
            stroke_width=3,
            color=LIGHT_GRAY
        )
        highlight.set_opacity(0.7)

        laser_glow = Line(
            LEFT * tube_width / 2,
            RIGHT * tube_width / 2,
            stroke_width=14,
            color=RED
        )
        laser_glow.set_opacity(0.25)

        laser_core = Line(
            LEFT * tube_width / 2,
            RIGHT * tube_width / 2,
            stroke_width=5,
            color=RED
        )

        tube_shell = VGroup(tube_body, inner_shadow, highlight)
        straight_laser = VGroup(laser_glow, laser_core)

        return tube_shell, straight_laser, tube_width
    def make_shockwave(self):
        shockwave = VGroup()

        for radius, opacity in [(1.0, 0.35), (1.45, 0.20), (1.9, 0.1)]:
            arc = Arc(
                radius=radius,
                start_angle=PI,
                angle=PI,
                color=BLUE_B,
                stroke_width=6
            )
            arc.set_opacity(opacity)
            shockwave.add(arc)

        shockwave.scale(1.3)
        shockwave.move_to(UP * 5)

        return shockwave

    def construct(self):
        ground_y = -2.4

        # =========================
        # Grond
        # =========================
        ground = Line(
            LEFT * 4 + UP * ground_y,
            RIGHT * 4 + UP * ground_y,
            stroke_width=4
        )

        # =========================
        # Punten stick figure
        # =========================
        neck = np.array([0, 0.75, 0])
        hip = np.array([0, -0.6, 0])
        shoulder = np.array([0, 0.35, 0])

        # =========================
        # Lichaam
        # =========================
        head = Circle(radius=0.32, color=WHITE, stroke_width=5)
        head.move_to(np.array([0, 1.2, 0]))

        body = Line(neck, hip, stroke_width=8)

        arms = VGroup(
            Line(shoulder, shoulder + LEFT * 0.75 + DOWN * 0.35, stroke_width=7),
            Line(shoulder, shoulder + RIGHT * 0.75 + DOWN * 0.35, stroke_width=7),
        )

        upper_body = VGroup(head, body, arms)

        # =========================
        # Vast linkerbeen
        # =========================
        support_leg = self.make_leg(
            hip,
            np.array([-0.35, -1.45, 0]),
            np.array([-0.75, ground_y, 0]),
            color=WHITE
        )

        # Deze groep moet samen bewegen, zodat buik en linkerbeen verbonden blijven
        fixed_body = VGroup(upper_body, support_leg)

        # =========================
        # Stampbeen poses
        # =========================
        stomp_leg_down = self.make_leg(
            hip,
            np.array([0.45, -1.45, 0]),
            np.array([0.95, ground_y, 0]),
            color=WHITE
        )

        stomp_leg_up = self.make_leg(
            hip,
            np.array([0.65, -1.05, 0]),
            np.array([1.15, -1.65, 0]),
            color=WHITE
        )

        stomp_leg = stomp_leg_down.copy()

        figure = VGroup(fixed_body, stomp_leg)

        self.add(ground)
        self.play(FadeIn(figure))
        self.wait(0.5)

        contact_point = np.array([0.95, ground_y, 0])

        # =========================
        # Stamp animatie
        # =========================
        for _ in range(2):
            self.play(
                Transform(stomp_leg, stomp_leg_up),
                fixed_body.animate.shift(UP * 0.04),
                run_time=0.45,
                rate_func=smooth
            )

            impact = self.make_impact(contact_point)

            self.play(
                Transform(stomp_leg, stomp_leg_down),
                fixed_body.animate.shift(DOWN * 0.04),
                run_time=0.16,
                rate_func=rush_into
            )

            self.play(
                Create(impact),
                figure.animate.shift(DOWN * 0.05),
                run_time=0.08
            )

            self.play(
                FadeOut(impact),
                figure.animate.shift(UP * 0.05),
                run_time=0.15
            )

            self.wait(0.15)

        self.wait(0.4)

        # =========================
        # Alles uit beeld omhoog
        # =========================
        everything = VGroup(ground, figure)

        self.play(
            everything.animate.shift(UP * 15),
            run_time=1.0,
            rate_func=smooth
        )

        # =========================
        # Grijze buis komt in beeld
        # =========================
        tube_shell, straight_laser, tube_width = self.make_tube()

        tube_group = VGroup(tube_shell, straight_laser)
        tube_group.move_to(ORIGIN + DOWN * 6)

        self.play(
            tube_group.animate.shift(UP * 6),
            run_time=1.2,
            rate_func=smooth
        )

        self.wait(0.3)

        # =========================
        # Shockwave komt van boven
        # =========================
        shockwave = self.make_shockwave()

        self.play(
            shockwave.animate.scale(15).move_to(ORIGIN + UP * 0.15),
            run_time=1.8,
            rate_func=rush_into
        )

        # =========================
        # Laser gaat golven
        # =========================
        amp = ValueTracker(0)
        phase = ValueTracker(0)

        def make_wavy_laser():
            amplitude = amp.get_value()
            phase_value = phase.get_value()
            k = 4.5

            glow = ParametricFunction(
                lambda x: np.array([
                    x,
                    amplitude * np.sin(k * x - phase_value),
                    0
                ]),
                t_range=[-tube_width / 2, tube_width / 2, 0.04],
                color=RED
            )
            glow.set_stroke(width=15, opacity=0.25)

            core = ParametricFunction(
                lambda x: np.array([
                    x,
                    amplitude * np.sin(k * x - phase_value),
                    0
                ]),
                t_range=[-tube_width / 2, tube_width / 2, 0.04],
                color=RED
            )
            core.set_stroke(width=5, opacity=1)

            return VGroup(glow, core)

        wavy_laser = always_redraw(make_wavy_laser)

        self.remove(straight_laser)
        self.add(wavy_laser)

        # Shockwave verdwijnt, laser krijgt ineens amplitude
        self.play(
            FadeOut(shockwave),
            amp.animate.set_value(0.22),
            phase.animate.set_value(2 * PI),
            run_time=0.35,
            rate_func=rush_from
        )

        # Laser golft en dempt langzaam terug naar stil
        self.play(
            amp.animate.set_value(0),
            phase.animate.set_value(14 * PI),
            run_time=3.5,
            rate_func=linear
        )

        self.wait(1)