from manim import *
import numpy as np
from mass import *

class SetupScene(ThreeDScene):
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
            phi=65 * DEGREES,
            theta=45 * DEGREES
        )

        base_radius = 3
        base_height = 0.5

        base = Cylinder(
            radius=base_radius,
            height=base_height,
            direction=OUT,   # base ligt in x-y vlak
            resolution=32
        )
        base.set_fill(GRAY, opacity=0.8)
        base.set_stroke(WHITE, width=1)

        z_base_top = base_height / 2

        top_radius = 0.25
        top_height = 0.15

        top_center = np.array([0, 0, 2.6])

        top_cylinder = Cylinder(
            radius=top_radius,
            height=top_height,
            direction=OUT,
            resolution=24
        )
        top_cylinder.set_fill(GRAY, opacity=1)
        top_cylinder.set_stroke(WHITE, width=1)
        top_cylinder.move_to(top_center)

        top_bottom = top_center + np.array([0, 0, -top_height / 2])

        cable_start = top_bottom
        cable_end = np.array([0, 0, 0.7])

        cable = self.cylinder_between(
            cable_start,
            cable_end,
            radius=0.02,
            color=WHITE
        )

        arm_start_1 = np.array([-1.7, -1.0, z_base_top])
        arm_start_2 = np.array([0.0,   1.8, z_base_top])
        arm_start_3 = np.array([1.7,  -1.0, z_base_top])

        arm1 = self.cylinder_between(arm_start_1, top_bottom, radius=0.12, color=GREY)
        arm2 = self.cylinder_between(arm_start_2, top_bottom, radius=0.12, color=GREY)
        arm3 = self.cylinder_between(arm_start_3, top_bottom, radius=0.12, color=GREY)

        setup = VGroup(arm1, arm2, arm3, cable, top_cylinder)

        m = mass(0.8)
        m.shift(cable_end)

        all_objects = VGroup(base, setup, m)
        all_objects.rotate(20 * DEGREES, axis=OUT, about_point=ORIGIN)

        self.play(Create(base))
        self.play(Create(setup))
        self.play(FadeIn(m))
        self.wait(1)
        self.play(
            Rotate(
                m, 
                angle= 10 * DEGREES,
                axis=OUT,
                rate_func=there_and_back,
                run_time=1
            )
        )
        self.play(
            Rotate(
                m,
                angle=10 * DEGREES,
                axis=UP,
                rate_func=there_and_back,
                run_time=1
            )
        )
        # self.play(
        #     Rotate(
        #         all_objects,
        #         angle=360 * DEGREES,
        #         axis=OUT,          # z-as
        #         about_point=ORIGIN
        #     ),
        #     run_time=2,
        #     rate_func=linear
        # )

        self.wait(2)