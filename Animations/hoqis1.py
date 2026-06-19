from manim import *
from mass import *
import numpy as np


class Hoqis1(ThreeDScene):
    def construct(self):
        # Bovenaanzicht
        self.set_camera_orientation(
            phi=0 * DEGREES,
            theta=-90 * DEGREES
        )

        # =========================
        # Base
        # =========================
        base_radius = 3
        base_height = 0.5

        base = Cylinder(
            radius=base_radius,
            height=base_height,
            direction=OUT,
            resolution=64
        )

        base.set_fill(GRAY, opacity=0.7)
        base.set_stroke(WHITE, width=2)

        # =========================
        # Massa
        # =========================
        rod_length = 0.8
        cube_size = 0.4

        m = mass(rod_length)

        z_base_top = base_height / 2
        z_mass = z_base_top + 0.8

        mass_center = np.array([0, 0, z_mass])
        m.shift(mass_center)

        # =========================
        # HoQI's naast én boven de kubussen
        # =========================
        hoqis_side = VGroup()
        hoqis_top = VGroup()

        hoqi_width = 0.28
        hoqi_height = 0.10
        gap = 0.2

        z_hoqi_side = z_mass + 0.05


        for angle in [90 * DEGREES, 210 * DEGREES, 330 * DEGREES]:
            # Richting van de arm
            direction = np.array([
                np.cos(angle),
                np.sin(angle),
                0
            ])

            # Richting naast de kubus
            side_direction = np.array([
                direction[1],
                -direction[0],
                0
            ])

            # Centrum van de kubus
            cube_center = mass_center + direction * rod_length

            # =========================
            # 1. HoQI naast de kubus
            # =========================
            hoqi_side = Rectangle(
                width=hoqi_width,
                height=hoqi_height,
                color=RED,
                fill_color=RED,
                fill_opacity=1
            )

            hoqi_side.rotate(angle - 90 * DEGREES, axis=OUT)

            side_offset = cube_size / 2 + gap + hoqi_height / 2

            hoqi_side_center = cube_center + side_direction * side_offset
            hoqi_side_center[2] = z_hoqi_side

            hoqi_side.move_to(hoqi_side_center)

            # =========================
            # 2. HoQI boven de kubus in z-richting
            # =========================
            hoqi_top = Prism(
                dimensions=[
                    hoqi_height,  # x-dikte
                    hoqi_height,  # y-dikte
                    hoqi_width    # z-lengte, dus lange zijde omhoog
                ]
            )

            hoqi_top.set_fill(RED, opacity=1)
            hoqi_top.set_stroke(RED, width=1)

            hoqi_top_center = np.array([
                cube_center[0],
                cube_center[1],
                z_mass + cube_size / 2 + gap + hoqi_width / 2
            ])

            hoqi_top.move_to(hoqi_top_center)

            hoqis_side.add(hoqi_side)
            hoqis_top.add(hoqi_top)

        hoqis = VGroup(hoqis_side, hoqis_top)

        center_dot = Dot3D(
            point=mass_center,
            radius=0.04,
            color=BLUE
        )
        setup = VGroup(base, m, hoqis, center_dot)

        position_setup = UP * 3.5

        # =========================
        # Linker 2D HoQI-measurement panel
        # =========================
        panel_title = Text("HoQI Measurements", font_size=34, weight=BOLD)
        panel_subtitle = Text("(for 1 HoQI)", font_size=24, weight=BOLD)

        panel_title.to_corner(UL).shift(RIGHT * 0.4 + DOWN * 0.3)
        panel_subtitle.next_to(panel_title, DOWN, buff=0.15)

        rows = VGroup()
        v_groups = VGroup()
        boxes_group = VGroup()

        pd_names = ["PD1", "PD2", "PD3"]
        start_opacities = [0.35, 0.65, 1.0]

        for i in range(3):
            pd_text = Text(pd_names[i], font_size=34, weight=BOLD)

            box = Square(side_length=0.55)
            box.set_stroke(BLACK, width=5)
            box.set_fill(WHITE, opacity=0.8)

            boxes_group.add(box)

            red_circle = Circle(radius=0.15)
            red_circle.set_stroke(RED, width=6)
            red_circle.set_fill(opacity=0)

            circle_group = VGroup(red_circle)

            circle_group.set_opacity(start_opacities[i])

            row = VGroup(pd_text, box, circle_group)
            row.arrange(RIGHT, buff=0.35)

            # na arrange opnieuw exact in het midden van het vierkant zetten
            circle_group.move_to(box.get_center())

            rows.add(row)
            v_groups.add(circle_group)

        rows.arrange(DOWN, buff=0.3)
        rows.next_to(panel_subtitle, DOWN, buff=0.45)
        rows.align_to(panel_title, LEFT).shift(RIGHT * 1.1)

        left_panel = VGroup(panel_title, panel_subtitle, rows)

        self.add_fixed_in_frame_mobjects(left_panel)
        left_panel.set_opacity(0)

        highlight_box = SurroundingRectangle(
            boxes_group,
            color=YELLOW,
            stroke_width=5,
            buff=0.15
        )

        highlight_box.set_fill(opacity=0)          # geen gevulde rechthoek
        highlight_box.set_stroke(YELLOW, width=5, opacity=0)  # begin onzichtbare rand

        self.add_fixed_in_frame_mobjects(highlight_box)

        HoQI_title = Text("HoQI", font_size=34, weight=BOLD)
        HoQI_subtitle = Text("(Homodyne Quadrature Interferometer)", font_size=24, weight=BOLD)

        title_and_subtitle = VGroup(HoQI_title, HoQI_subtitle)

        title_and_subtitle.arrange(DOWN, buff=0.15)
        title_and_subtitle.to_edge(UP, buff=0.4)
        title_and_subtitle.set_opacity(0)
        self.add_fixed_in_frame_mobjects(title_and_subtitle)
        # =========================
        # Animatie
        # =========================
        self.add(base, m)
        self.wait(1)
        self.play(
            FadeIn(hoqis), 
            run_time=2,
        )
        all = VGroup(base, m, hoqis)
        self.play(
            all.animate.shift(DOWN * 0.5),
            title_and_subtitle.animate.set_opacity(1)
        )
        self.wait(2)
        self.play(
            all.animate.shift(UP * 0.5),
            title_and_subtitle.animate.set_opacity(0) 
        )

        self.move_camera(
            phi=65 * DEGREES,
            theta=45 * DEGREES,
            run_time=1
        )
        self.wait(1)

        self.move_camera(
            phi=0 * DEGREES,
            theta=0 * DEGREES,
            run_time=1
        )

        self.play(
            setup.animate.shift(position_setup),
            left_panel.animate.set_opacity(1),
            run_time=1
        )

        # Verplaats centrum mee
        current_mass_center = mass_center + position_setup


        self.play(
            Rotate(
                m,
                angle=12 * DEGREES,
                axis=OUT,
                about_point=current_mass_center
            ),
            hoqis.animate.set_opacity(0.35),
            v_groups[0].animate.set_opacity(1.0),
            v_groups[1].animate.set_opacity(0.25),
            v_groups[2].animate.set_opacity(0.8),
            run_time=1
        )

        self.play(
            Rotate(
                m,
                angle=-24 * DEGREES,
                axis=OUT,
                about_point=current_mass_center
            ),
            hoqis.animate.set_opacity(1.0),
            v_groups[0].animate.set_opacity(0.4),
            v_groups[1].animate.set_opacity(0.75),
            v_groups[2].animate.set_opacity(0.3),
            highlight_box.animate.set_stroke(opacity=1),
            run_time=1
        )

        self.play(
            Rotate(
                m,
                angle=24 * DEGREES,
                axis=OUT,
                about_point=current_mass_center
            ),
            hoqis.animate.set_opacity(0.35),
            v_groups[0].animate.set_opacity(1.0),
            v_groups[1].animate.set_opacity(0.25),
            v_groups[2].animate.set_opacity(0.8),
            run_time=1
        )

        self.play(highlight_box.animate.set_stroke(opacity=0), run_time=0.2)

        self.play(
            Rotate(
                m,
                angle=-24 * DEGREES,
                axis=OUT,
                about_point=current_mass_center
            ),
            hoqis.animate.set_opacity(1.0),
            v_groups[0].animate.set_opacity(0.4),
            v_groups[1].animate.set_opacity(0.75),
            v_groups[2].animate.set_opacity(0.3),
            run_time=1
        )

        self.play(
            Rotate(
                m,
                angle=12 * DEGREES,
                axis=OUT,
                about_point=current_mass_center
            ),
            hoqis.animate.set_opacity(0.7),
            v_groups[0].animate.set_opacity(0.8),
            v_groups[1].animate.set_opacity(0.3),
            v_groups[2].animate.set_opacity(1.0),
            run_time=1
        )
        self.wait(2)
        self.play(
            FadeOut(all),
            left_panel.animate.move_to(LEFT * 4)
        )
        self.wait(1)
