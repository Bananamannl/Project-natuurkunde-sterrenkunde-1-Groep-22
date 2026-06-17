from manim import *
import numpy as np

class CylinderScene(ThreeDScene):
    def cylinder_between(self, start, end, radius=0.12, color=GREY):
        """
        Maakt een cilinder tussen twee punten.
        """
        direction = end - start
        length = np.linalg.norm(direction)

        cyl = Cylinder(
            radius=radius,
            height=length,
            direction=direction / length,
            resolution=24
        )
        cyl.move_to((start + end) / 2)
        cyl.set_fill(color, opacity=1)
        cyl.set_stroke(color, width=1)

        return cyl

    def construct(self):
        self.set_camera_orientation(
            phi=70 * DEGREES,
            theta=45 * DEGREES
        )

        # =========================
        # Grote platte basiscilinder
        # =========================
        base_radius = 3
        base_height = 0.5

        base = Cylinder(
            radius=base_radius,
            height=base_height,
            direction=UP,
            resolution=32
        )
        base.set_fill(BLUE_D, opacity=0.8)
        base.set_stroke(WHITE, width=1)

        # =========================
        # Klein cilindertje bovenaan
        # =========================
        top_radius = 0.25
        top_height = 0.35

        top_cylinder = Cylinder(
            radius=top_radius,
            height=top_height,
            direction=UP,
            resolution=24
        )
        top_cylinder.set_fill(GREY_BROWN, opacity=1)
        top_cylinder.set_stroke(WHITE, width=1)

        # Plaats van het kleine cilindertje
        top_center = np.array([0, 2.4, 0])
        top_cylinder.move_to(top_center)

        # Onderkant van het kleine cilindertje:
        top_bottom = top_center + np.array([0, -top_height / 2, 0])

        # =========================
        # 3 schuine armen
        # Punten op de bovenkant van de basis
        # =========================
        y_base_top = base_height / 2

        arm_start_1 = np.array([-1.7, y_base_top, -0.8])
        arm_start_2 = np.array([0.0,  y_base_top,  1.8])
        arm_start_3 = np.array([1.7,  y_base_top, -0.8])

        arm1 = self.cylinder_between(arm_start_1, top_bottom, radius=0.12, color=GREY)
        arm2 = self.cylinder_between(arm_start_2, top_bottom, radius=0.12, color=GREY)
        arm3 = self.cylinder_between(arm_start_3, top_bottom, radius=0.12, color=GREY)

        arms = VGroup(arm1, arm2, arm3)

        # =========================
        # Animatie
        # =========================
        self.play(Create(base))
        self.play(Create(arms), Create(top_cylinder))
        self.wait(2)