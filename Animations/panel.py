from manim import *

def make_left_panel():
    panel_title = Text("HoQI Measurements", font_size=34, weight=BOLD)
    panel_subtitle = Text("(for 1 HoQI)", font_size=24, weight=BOLD)

    panel_title.to_corner(UL).shift(RIGHT * 0.4 + DOWN * 0.3)
    panel_subtitle.next_to(panel_title, DOWN, buff=0.15)

    rows = VGroup()
    v_groups = VGroup()

    pd_names = ["PD1", "PD2", "PD3"]
    start_opacities = [0.35, 0.65, 1.0]

    for i in range(3):
        pd_text = Text(pd_names[i], font_size=34, weight=BOLD)

        box = Square(side_length=0.55)
        box.set_stroke(BLACK, width=5)
        box.set_fill(WHITE, opacity=0.8)

        red_circle = Circle(radius=0.15)
        red_circle.set_stroke(RED, width=6)
        red_circle.set_fill(opacity=0)

        circle_group = VGroup(red_circle)
        circle_group.set_opacity(start_opacities[i])

        row = VGroup(pd_text, box, circle_group)
        row.arrange(RIGHT, buff=0.35)

        circle_group.move_to(box.get_center())

        rows.add(row)
        v_groups.add(circle_group)

    rows.arrange(DOWN, buff=0.3)
    rows.next_to(panel_subtitle, DOWN, buff=0.45)
    rows.align_to(panel_title, LEFT).shift(RIGHT * 1.1)

    left_panel = VGroup(panel_title, panel_subtitle, rows)

    return left_panel, v_groups