from manim import *
import numpy as np


class Transformation(ThreeDScene):

    def construct(self):
        self.renderer.camera.set_theta(np.pi / 3)
        self.renderer.camera.set_phi(np.pi / 3)

        # Axes
        axes = ThreeDAxes(x_range=[-30, 30, 1], y_range=[-30, 30, 1], z_range=[-30, 30, 1], x_length=30, y_length=30,
                          z_length=30, tips=False,
                          stroke_width=1, axis_config={'include_ticks': False, 'stroke_width': 3}).set(
            color=BLUE_C).set_opacity(0.67)

        earth = Sphere(radius=1.3, resolution=(50, 50), color=BLUE, opacity=1)

        self.play(FadeIn(axes), FadeIn(earth))

        self.wait()

        sv = Dot3D(color=YELLOW, resolution=(30, 30))

        sv.next_to(earth, direction=(UP + RIGHT))

        self.play(Indicate(sv, scale_factor=2))

        group = Group(earth , axes, sv)

        self.play(Rotate(group, angle=np.pi / 5, rate_func=linear),run_time=2)

        self.play(Rotate(sv, angle= -np.pi / 5, about_point=UP))

        self.play(Indicate(sv, scale_factor=2))
