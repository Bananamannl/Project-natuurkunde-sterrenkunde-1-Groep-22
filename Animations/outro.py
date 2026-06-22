from manim import *
import numpy as np


class outro(Scene):
    def construct(self):
        self.camera.background_color = "#02040a"

        # =========================
        # Settings
        # =========================
        BH_RADIUS = 0.28
        INSPIRAL_TIME = 8.0

        t = ValueTracker(0)

        # =========================
        # Helper functies
        # =========================
        def s_from_t(t_val):
            return np.clip(t_val / INSPIRAL_TIME, 0, 1)

        def black_hole_position_from_s(s_val, side=1):
            """
            s = 0: ver uit elkaar
            s = 1: exact over elkaar heen in het midden
            """
            separation = interpolate(5.0, 0.0, s_val)

            # Sterk versnellende rotatie richting het einde
            angle = 2 * PI * (0.7 + 9.0 * s_val**1.65)

            x = side * separation / 2 * np.cos(angle)
            y = side * separation / 2 * np.sin(angle)

            return np.array([x, y, 0])

        def black_hole_position(side=1):
            return black_hole_position_from_s(s_from_t(t.get_value()), side)

        def make_black_hole(radius=BH_RADIUS, glow_color=BLUE):
            glow2 = Circle(radius=radius * 2.7)
            glow2.set_stroke(glow_color, width=18, opacity=0.10)

            glow1 = Circle(radius=radius * 1.8)
            glow1.set_stroke(glow_color, width=10, opacity=0.22)

            disk = Circle(radius=radius)
            disk.set_fill(BLACK, opacity=1)
            disk.set_stroke(WHITE, width=1.4, opacity=0.75)

            return VGroup(glow2, glow1, disk)

        # =========================
        # Achtergrond met sterren
        # =========================
        stars = VGroup()
        rng = np.random.default_rng(4)

        for _ in range(160):
            x = rng.uniform(-7, 7)
            y = rng.uniform(-4, 4)
            r = rng.uniform(0.008, 0.025)
            opacity = rng.uniform(0.25, 0.85)

            star = Dot([x, y, 0], radius=r, color=WHITE)
            star.set_opacity(opacity)
            stars.add(star)

        self.add(stars)

        # =========================
        # Zwarte gaten
        # =========================
        bh1 = make_black_hole(BH_RADIUS, BLUE)
        bh2 = make_black_hole(BH_RADIUS, TEAL)

        bh1.add_updater(lambda m: m.move_to(black_hole_position(1)))
        bh2.add_updater(lambda m: m.move_to(black_hole_position(-1)))

        # =========================
        # Propagerende cirkelgolven uit de zwarte gaten
        # =========================
        emission_times = np.arange(0.0, INSPIRAL_TIME, 0.28)

        def propagating_waves(side=1, color=BLUE_A):
            group = VGroup()

            current_t = t.get_value()

            wave_speed = 1.25
            max_age = 2.1

            for emit_t in emission_times:
                age = current_t - emit_t

                if age < 0 or age > max_age:
                    continue

                # Belangrijk:
                # Het centrum is de positie van het zwarte gat
                # OP HET MOMENT DAT DE GOLF WERD UITGEZONDEN.
                s_emit = s_from_t(emit_t)
                center = black_hole_position_from_s(s_emit, side)

                radius = BH_RADIUS * 1.3 + wave_speed * age
                opacity = 0.38 * (1 - age / max_age)

                ring = Circle(radius=radius)
                ring.move_to(center)
                ring.set_stroke(color, width=2.2, opacity=opacity)

                group.add(ring)

            return group

        waves1 = always_redraw(lambda: propagating_waves(1, BLUE_A))
        waves2 = always_redraw(lambda: propagating_waves(-1, TEAL_A))

        self.add(waves1, waves2)
        self.add(bh1, bh2)

        # =========================
        # Inspiral tot exact samenvallen
        # =========================
        self.play(
            t.animate.set_value(INSPIRAL_TIME),
            run_time=INSPIRAL_TIME,
            rate_func=rate_functions.ease_in_quad
        )

        # =========================
        # Zodra ze exact samenvallen: zwarte gaten verdwijnen
        # =========================
        bh1.clear_updaters()
        bh2.clear_updaters()

        self.remove(bh1, bh2, waves1, waves2)

        # =========================
        # Zwarte cirkelgolf vanuit het midden
        # =========================
        black_fill = Circle(radius=0.04)
        black_fill.move_to(ORIGIN)
        black_fill.set_fill(BLACK, opacity=1)
        black_fill.set_stroke(GREY_B, width=2.5, opacity=0.45)

        self.add(black_fill)

        self.play(
            black_fill.animate.scale(230),
            run_time=2.4,
            rate_func=rate_functions.ease_out_cubic
        )

        # Eindbeeld: volledig zwart, geen zwarte gaten meer zichtbaar
        black_screen = Rectangle(
            width=config.frame_width + 1,
            height=config.frame_height + 1
        )
        black_screen.set_fill(BLACK, opacity=1)
        black_screen.set_stroke(opacity=0)

        self.add(black_screen)
        self.wait(0.5)