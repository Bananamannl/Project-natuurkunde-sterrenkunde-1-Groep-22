from manim import *
from mass import *
import numpy as np


class Hoqis1(ThreeDScene):
    def construct(self):
        # Bovenaanzicht
        self.set_camera_orientation(
            phi=0 * DEGREES,
            theta=0 * DEGREES
        )

        # =========================
        # Assenstelsel
        # =========================
        axes = ThreeDAxes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            z_range=[-1, 2, 1],
            x_length=8,
            y_length=8,
            z_length=3,
        )

        axes.set_opacity(0.45)

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

        # z-positie van de HoQI's boven de kubussen
        z_hoqi_top = z_mass + cube_size / 2 + gap

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

        # =========================
        # Animatie
        # =========================
        self.play(Create(axes))
        self.play(Create(base))
        self.play(FadeIn(m))
        self.play(FadeIn(hoqis))
        self.play(FadeIn(center_dot))
        self.wait(2)
        self.move_camera(
            phi=65 * DEGREES,
            theta=45 * DEGREES,
            run_time=1
        )
        self.wait(2)
