from manim import *

class LatexTest(Scene):
    def construct(self):
        eq = MathTex(
            r"\int_{-\infty}^{\infty} e^{-x^2}\,dx = \sqrt{\pi}"
        )

        self.play(Write(eq))
        self.wait()