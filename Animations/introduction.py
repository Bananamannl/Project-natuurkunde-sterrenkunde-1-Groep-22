from manim import *
import numpy as np


class introduction(Scene):
    def make_leg(self, hip, knee, ankle, color=WHITE):
        thigh = Line(hip, knee, stroke_width=8, color=color)
        shin = Line(knee, ankle, stroke_width=8, color=color)

        return VGroup(thigh, shin)

    def make_impact(self, contact_point):
        return VGroup(
            Line(contact_point + LEFT * 0.15, contact_point + LEFT * 0.55 + UP * 0.25),
            Line(contact_point + RIGHT * 0.15, contact_point + RIGHT * 0.55 + UP * 0.25),
            Line(contact_point + UP * 0.05, contact_point + UP * 0.45),
        ).set_stroke(YELLOW, width=5)

    def make_ground_vibration(self, contact_point):
        vibration = VGroup()

        for radius, opacity in [(1.0, 0.35), (1.45, 0.20), (1.9, 0.1)]:
            arc = Arc(
                radius=radius * 0.12,
                start_angle=PI,
                angle=PI,
                arc_center=contact_point,
                color=BLUE_B,
                stroke_width=6
            )
            arc.set_opacity(opacity)
            vibration.add(arc)

        return vibration

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

        ground = Line(
            LEFT * 4 + UP * ground_y,
            RIGHT * 4 + UP * ground_y,
            stroke_width=4
        )

        # --- Poppetje (Hoofd 0.40, armen exact 1.15) ---
        neck = np.array([0, 0.85, 0])
        hip = np.array([0, -0.6, 0])
        shoulder = np.array([0, 0.40, 0])

        head = Circle(radius=0.40, color=WHITE, stroke_width=5)
        head.move_to(np.array([0, 1.35, 0]))

        body = Line(neck, hip, stroke_width=8)

        # Armen ingesteld op exact 1.15 (0.95 breedte + 0.65 drop = ~1.15 totale lengte)
        arms = VGroup(
            Line(shoulder, shoulder + LEFT * 0.95 + DOWN * 0.65, stroke_width=7),
            Line(shoulder, shoulder + RIGHT * 0.95 + DOWN * 0.65, stroke_width=7),
        )

        upper_body = VGroup(head, body, arms)

        # Het standbeen (links voor de kijker) startposities
        support_leg_down = self.make_leg(
            hip,
            np.array([-0.35, -1.45, 0]),
            np.array([-0.75, ground_y, 0]),
            color=WHITE
        )

        # Standbeen rekt licht mee omhoog, voet blijft muurvast op de grond staan
        support_leg_up = self.make_leg(
            hip + UP * 0.04,
            np.array([-0.33, -1.41, 0]),
            np.array([-0.75, ground_y, 0]),
            color=WHITE
        )

        stomp_leg_down = self.make_leg(
            hip,
            np.array([0.45, -1.45, 0]),
            np.array([0.95, ground_y, 0]),
            color=WHITE
        )

        stomp_leg_up = self.make_leg(
            hip + UP * 0.04,
            np.array([0.65, -1.01, 0]),
            np.array([1.15, -1.65, 0]),
            color=WHITE
        )

        current_upper_body = upper_body.copy()
        current_support_leg = support_leg_down.copy()
        current_stomp_leg = stomp_leg_down.copy()

        figure = VGroup(current_upper_body, current_support_leg, current_stomp_leg)

        self.add(ground)
        self.play(FadeIn(figure))
        self.wait(0.5)

        contact_point = np.array([0.95, ground_y, 0])

        for _ in range(2):
            # OMHOOG BEWEGEN: Standvoet blijft perfect op de grond staan
            self.play(
                Transform(current_stomp_leg, stomp_leg_up),
                Transform(current_support_leg, support_leg_up),
                current_upper_body.animate.shift(UP * 0.04),
                run_time=0.45,
                rate_func=smooth
            )

            impact = self.make_impact(contact_point)
            vibration = self.make_ground_vibration(contact_point)

            # NEERSTORTEN
            self.play(
                Transform(current_stomp_leg, stomp_leg_down),
                Transform(current_support_leg, support_leg_down),
                current_upper_body.animate.shift(DOWN * 0.04),
                run_time=0.16,
                rate_func=rush_into
            )

            self.play(
                Create(impact),
                Create(vibration),
                run_time=0.05
            )

            self.play(
                FadeOut(impact),
                vibration.animate.scale(12, about_point=contact_point).set_opacity(0),
                run_time=2.0,
                rate_func=linear
            )

            self.wait(0.15)

        self.wait(0.4)

        everything = VGroup(ground, figure)

        self.play(
            everything.animate.shift(UP * 15),
            run_time=1.0,
            rate_func=smooth
        )

        tube_shell, straight_laser, tube_width = self.make_tube()

        tube_group = VGroup(tube_shell, straight_laser)
        tube_group.move_to(ORIGIN + DOWN * 6)

        self.play(
            tube_group.animate.shift(UP * 6),
            run_time=1.2,
            rate_func=smooth
        )

        self.wait(0.3)

        # --- PIJLEN EN POSITIES ---
        
        # Groep 1: Witte pijl (Gecentreerd op X=0, stopt vlak onder de armrand op Y=-0.42)
        arrow = Arrow(
            start=ORIGIN + DOWN * 2.06, 
            end=ORIGIN + DOWN * 0.42,   
            buff=0.05, 
            stroke_width=4, 
            max_tip_length_to_length_ratio=0.25, 
            color=WHITE
        )
        label_text = Tex(r"\text{Gravitational wave detector (arm)}", font_size=30, color=WHITE)
        label_text.next_to(arrow.get_start(), DOWN, buff=0.3) 
        
        white_label_group = VGroup(arrow, label_text)
        
        # Groep 2: Rode pijl (Eindpunt afgesteld op perfecte afstand boven laserlijn)
        laser_arrow = Arrow(
            start=ORIGIN + UP * 1.25 + RIGHT * 1.66,
            end=ORIGIN + UP * 0.10 + RIGHT * 0.26,   
            buff=0.05,
            stroke_width=4, 
            max_tip_length_to_length_ratio=0.25, 
            color=RED
        )
        laser_label = Tex(r"\text{Seismic noise injected into the measurements}", font_size=30, color=RED)
        laser_label.next_to(laser_arrow.get_start(), UP, buff=0.3) 
        
        red_label_group = VGroup(laser_arrow, laser_label)
        
        # Gelaagde timing
        self.play(FadeIn(white_label_group, shift=UP * 0.2), run_time=0.6)
        self.wait(0.7)
        self.play(FadeIn(red_label_group, shift=UP * 0.2), run_time=0.6)
        
        self.wait(1.8)  
        
        self.play(
            FadeOut(white_label_group),
            FadeOut(red_label_group),
            run_time=0.5
        )
        self.wait(0.6)

        # Trackers
        amp = ValueTracker(0.22)
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

        shockwave = self.make_shockwave()
        self.add(shockwave)

        # 1. GOLVEN REIZEN OMLAAG
        self.play(
            shockwave.animate.scale(2.5).move_to(ORIGIN + UP * 2.5),
            run_time=0.8,
            rate_func=linear
        )

        # 2. SPRONG
        self.remove(straight_laser)
        self.add(wavy_laser)

        # 3. AFZWAKKEN
        self.play(
            shockwave.animate.scale(4.5).move_to(ORIGIN + DOWN * 1.5).set_opacity(0),
            amp.animate.set_value(0),
            phase.animate.set_value(16 * PI),
            run_time=3.5,
            rate_func=linear
        )

        self.wait(1)