from manim import *

class credits_scroll(Scene):
    def construct(self):

        # ─────────────────────────────
        # 1. Credits tekst (6 regels)
        # ─────────────────────────────
        credits = VGroup(
        VGroup(
            Text("We offer our thanks to:"),
            Text("Johannes Lehmann — OmniSens"),
            Text("Conor Mow-Lowry — OmniSens"),
            Text("Clara Nellist — UvA"),
            Text("Joshua Dijksman — UvA"),
            Text("for making this project possible!"),
        ) .arrange(DOWN, buff = 0.3), 

        VGroup(
            Text("This animation was produced by:"), 
            Text("Timo Boomsma"),
            Text("Kesse Donders"), 
            Text("Janne Lemmens"), 
            Text("Merijn Post")
        ).arrange(DOWN, buff = 0.3)
        ).arrange(DOWN, buff = 1.2)

        # Startpositie: onder het scherm
        credits.move_to(DOWN * 10)

        # ─────────────────────────────
        # 2. Animatie: scroll omhoog
        # ─────────────────────────────
        self.play(
            credits.animate.shift(UP * 19),
            run_time=6,
            rate_func=linear
        )

        self.wait(1)

