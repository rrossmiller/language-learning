from manim import *

class MathTeXDemo(Scene):
    def construct(self):
        rtarrow = MathTex(r"\xrightarrow{x^6y^8}", font_size=96)
        rtarrow.arrange(DOWN)
        self.add(rtarrow)
        self.wait()