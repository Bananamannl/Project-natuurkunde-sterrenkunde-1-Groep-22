from manim import *

class dof(Scene):
    def construct(self):

        arctan_text = MathTex(
            r"\arctan\left(\frac{Q_1}{Q_2}\right)"
            r"="
            r"\phi_{\mathrm{rel}}"
        )
        arctan_text.move_to(UP * 1.5)
        self.add(arctan_text)

        displacements = MathTex(
            r"d = \frac{\lambda\phi_{rel}}{4\pi}"
        )
        self.wait(1)
        self.play(Write(displacements))
        self.wait(3)

        # =========================
        # Vector opgesplitst
        # =========================
        d_label = MathTex(r"\vec{d}=").scale(0.8)

        d_vector = MathTex(
            r"\begin{pmatrix}"
            r"d_{1_x}\\"
            r"d_{2_x}\\"
            r"d_{3_x}\\"
            r"d_{1_z}\\"
            r"d_{2_z}\\"
            r"d_{3_z}"
            r"\end{pmatrix}"
        ).scale(0.8)

        HoQI_vector = VGroup(d_label, d_vector).arrange(RIGHT, buff=0.15)
        HoQI_vector.move_to(ORIGIN)

        M = MathTex(
            r"\begin{pmatrix}"
            r"-\frac{2}{3} & \frac{1}{3} & \frac{1}{3} & 0 & 0 & 0 \\"
            r"0 & -\frac{1}{\sqrt{3}} & \frac{1}{\sqrt{3}} & 0 & 0 & 0 \\"
            r"0 & 0 & 0 & \frac{1}{3} & \frac{1}{3} & \frac{1}{3} \\"
            r"0 & 0 & 0 & \frac{2}{3R} & -\frac{1}{3R} & -\frac{1}{3R} \\"
            r"0 & 0 & 0 & 0 & \frac{1}{\sqrt{3}R} & -\frac{1}{\sqrt{3}R} \\"
            r"\frac{1}{3R} & \frac{1}{3R} & \frac{1}{3R} & 0 & 0 & 0"
            r"\end{pmatrix}"
        ).scale(0.42)

        times = MathTex(r"\cdot").scale(0.9)

        x_label = MathTex(r"\vec{x}=").scale(0.8)

        product_vector = MathTex(
            r"\vec{x}="
            r"\begin{pmatrix}"
            r"-\frac{2}{3}d_{1_x}+\frac{1}{3}d_{2_x}+\frac{1}{3}d_{3_x}\\[0.35em]"
            r"-\frac{1}{\sqrt{3}}d_{2_x}+\frac{1}{\sqrt{3}}d_{3_x}\\[0.35em]"
            r"\frac{1}{3}d_{1_z}+\frac{1}{3}d_{2_z}+\frac{1}{3}d_{3_z}\\[0.35em]"
            r"\frac{2}{3R}d_{1_z}-\frac{1}{3R}d_{2_z}-\frac{1}{3R}d_{3_z}\\[0.35em]"
            r"\frac{1}{\sqrt{3}R}d_{2_z}-\frac{1}{\sqrt{3}R}d_{3_z}\\[0.35em]"
            r"\frac{1}{3R}d_{1_x}+\frac{1}{3R}d_{2_x}+\frac{1}{3R}d_{3_x}"
            r"\end{pmatrix}"
        ).scale(0.55)

        # =========================
        # Animatie
        # =========================
        self.play(
            FadeOut(arctan_text),
            FadeOut(displacements)
        )

        # Eerst alleen d-vector laten zien
        self.play(FadeIn(HoQI_vector, shift=UP * 0.2))
        self.wait(1)

        # Eindpositie: matrix + vector samen netjes gecentreerd
        target_pair = VGroup(
            M.copy(),
            HoQI_vector.copy()
        ).arrange(RIGHT, buff=0.55)

        target_pair.move_to(ORIGIN)

        # M is nog niet zichtbaar, dus deze mag direct naar zijn start/eindplek
        M.move_to(target_pair[0].get_center())

        self.play(
            HoQI_vector.animate.move_to(target_pair[1].get_center()),
            FadeIn(M, shift=RIGHT * 0.25),
            run_time=1.2
        )
        self.wait(1)

        # Maak er een nette matrix-vector vermenigvuldiging van:
        # label "d =" verdwijnt, matrix en vector schuiven netjes naast elkaar
        target_layout = VGroup(
            x_label.copy(),
            M.copy(),
            times.copy(),
            d_vector.copy()
        ).arrange(RIGHT, buff=0.25)

        target_layout.move_to(UP * 1.2)

        x_label.move_to(target_layout[0].get_center())

        self.play(
            FadeOut(d_label),
            FadeIn(x_label),
            M.animate.move_to(target_layout[1].get_center()),
            FadeIn(times.move_to(target_layout[2].get_center())),
            d_vector.animate.move_to(target_layout[3].get_center()),
            run_time=1.2
        )

        # Kleine highlight op vermenigvuldiging
        self.play(
            Circumscribe(VGroup(M, d_vector), color=YELLOW, buff=0.15),
            run_time=1
        )

        # Product uitschrijven
        product_vector.move_to(DOWN * 1.7)

        self.play(Write(product_vector), run_time=2)
        self.wait(1)

        # Eindvector met fysische vrijheidsgraden
        DOF_vector = MathTex(
            r"\begin{pmatrix}"
            r"x\\"
            r"y\\"
            r"z\\"
            r"R_x\\"
            r"R_y\\"
            r"R_z"
            r"\end{pmatrix}"
        ).scale(0.9)

        # Zet hem exact op de plek van de uitgeschreven productvector
        DOF_vector.move_to(product_vector)

        self.play(
            ReplacementTransform(product_vector, DOF_vector),
            run_time=1.2
        )
        self.wait(0.5)
