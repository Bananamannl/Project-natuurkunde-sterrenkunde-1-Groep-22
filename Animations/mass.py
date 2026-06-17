from manim import *
import numpy as np

def mass(rod_length):
    rod_radius = 0.08
    cube_size = 0.4

    group = VGroup()

    for angle in [90*DEGREES, 210*DEGREES, 330*DEGREES]:
        direction = np.array([np.cos(angle), np.sin(angle), 0])

        rod = Cylinder(
            radius=rod_radius,
            height=rod_length,
            direction=direction,
            fill_color=BLACK,
            fill_opacity=1,
        )
        rod.move_to(direction * rod_length / 2)

        cube = Cube(
            side_length=cube_size,
            fill_color=YELLOW,
            fill_opacity=1,
            stroke_color=YELLOW_E,
        )
        cube.move_to(direction * rod_length)
        cube.rotate(angle, axis=OUT)

        group.add(rod, cube)

    return group