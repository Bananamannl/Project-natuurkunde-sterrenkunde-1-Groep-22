from manim import *
from panel import make_left_panel

class NextScene(Scene):
    def construct(self):
        left_panel, v_groups = make_left_panel()

        self.add(left_panel)  # meteen zichtbaar

        
        self.wait(2)