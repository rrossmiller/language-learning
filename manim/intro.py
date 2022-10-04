from manim import *


class CreateCircle(Scene):
    def construct(self):
        circle = Circle()
        circle.set_fill(PINK, opacity=0.3)

        self.play(Create(circle))


class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()
        circle.set_fill(PINK, opacity=1)

        square = Square()
        square.set_fill(BLUE, opacity=1)
        square.next_to(circle, RIGHT, buff=0.5)

        triangle = Triangle()
        triangle.set_fill(GREEN, opacity=1)
        triangle.next_to(circle, LEFT, buff=0.5)

        self.play(Create(square))
        self.play(square.animate.rotate(PI / 4))
        self.play(ReplacementTransform(square, circle))
        self.play(circle.animate.flip())
        self.play(ReplacementTransform(circle, triangle))
        # self.play(Create(circle))
        # self.play(Transform(square, circle))
        # self.play(FadeOut(square))


class DifferentRotations(Scene):
    def construct(self):
        left_square = Square(color=BLUE, fill_opacity=0.7).shift(2 * LEFT)
        center_square = Square(color=PINK, fill_opacity=0.7)
        center_circle = Circle(color=YELLOW, fill_opacity=0.7)
        right_square = Square(color=GREEN, fill_opacity=0.7).shift(2 * RIGHT)
        self.play(
            ReplacementTransform(center_circle, center_square),
            left_square.animate.rotate(PI),
            Rotate(right_square, angle=PI),
            run_time=2,
        )
        self.wait()
