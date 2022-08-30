from math import *

from manim import *

from manim.opengl import *

from Orbit import absorb, write_orbit

from datetime import datetime, timedelta

from solution import ask_path, ask_satellite

import numpy as np

# Configuration settings

# Need to change render to opengl


# Constants
R = 6.3781 * 10 ** 6  # Radius of Earth

scaling_factor = 1 / (12 * 10 ** 6)  # inverse of unit distance in the axis in meters

inverse_scaling = 1 / scaling_factor  # inverse of scaling factor

R = R * scaling_factor


# gets elliptical parameters - major and minor axis length with the scaling factor
def elliptial_parameter(a: float, e: float) -> dict:
    return {'width': a * 2 * scaling_factor, 'height': 2 * sqrt((1 - e ** 2) * a ** 2) * scaling_factor}


# gets the distance to focus of an ellipse from center
def get_focus(mob: Ellipse) -> float:
    a = mob.get_width() / 2
    b = mob.get_height() / 2

    return sqrt(a ** 2 - b ** 2)


# Recursive angular correction-> condenses any angle between 0 to 2pi
def angular_correction(ang) -> float:
    if 0 <= ang <= TAU:
        return ang
    elif ang > TAU:
        return angular_correction(ang - TAU)
    else:
        return angular_correction(ang + TAU)
        # SV animation snapshot


# angle between two vector
def angle(vct1: np.array, vct2: np.array) -> float:
    dot_product = np.dot(vct1, vct2)

    norm1 = np.linalg.norm(vct1)

    norm2 = np.linalg.norm(vct2)

    cos_correctiom = np.arccos(dot_product / (norm1 * norm2))
    return (180 / np.pi) * cos_correctiom


# Date and Time label generator
def date_label(tracker: ValueTracker, time: datetime) -> list:
    def utc(track: tracker, UTC: datetime = time) -> list:
        current_time = UTC + timedelta(seconds=track.get_value())
        return [current_time.year, current_time.month, current_time.day, current_time.hour, current_time.minute
            , current_time.second]

    day = Integer(utc(tracker)[2])
    day.add_updater(lambda mob: mob.set_value(utc(tracker)[2]))

    hour = Integer(utc(tracker)[3])
    hour.add_updater(lambda mob: mob.set_value(utc(tracker)[3]))

    minute = Integer(utc(tracker)[4])
    minute.add_updater(lambda mob: mob.set_value(utc(tracker)[4]))

    seconds = Integer(utc(tracker)[4])
    seconds.add_updater(lambda mob: mob.set_value(utc(tracker)[5]))

    label = VGroup(Tex('dy'), Tex('-'), Tex('hr'), Tex('-'), Tex('min'), Tex('-'), Tex('sec')).arrange(RIGHT)
    text = VGroup(Tex('UTC:  '), day, Tex('-'), hour, Tex('-'), minute, Tex('-'), seconds
                  ).arrange(RIGHT).scale(0.6)

    label.add_updater(lambda mob: mob.next_to(text[3], UP, buff=0.1).scale(0.47).shift(text.get_center() + 0.4 * RIGHT))

    date_list = [text, label]

    return [x.set_color(BLUE_C) for x in date_list]


class SV(Scene):

    def construct(self):

        # reading and write part starts here

        # Orbit Data
        path_to_rinex = ask_path()
        satellite_number = ask_satellite(path_to_rinex)

        # absorbs and writes orbital data
        orbit_data = absorb(path_to_rinex, satellite_number)
        write_orbit(orbit_data, satellite_number)

        # Animation begins starts here

        # Beginning Camara Orientation and Rotation
        self.camera.set_euler_angles(phi=PI / 2.4, theta=PI / 4)

        # Ambient Camera Rotation
        self.add(self.camera)

        self.add(self.camera.light_source)

        self.camera.add_updater(lambda mob, dt: mob.increment_theta(dt * 0.1))

        self.update_self(0.001)

        # Axis-Creation

        ax = ThreeDAxes(x_range=[-30, 30, 1], y_range=[-30, 30, 1], z_range=[-30, 30, 1], x_length=30, y_length=30,
                        z_length=30, tips=False,
                        stroke_width=1, axis_config={'include_ticks': False, 'stroke_width': 3}).set(
            color=BLUE_C).set_opacity(0.67)

        self.play(Create(ax))

        # Earth Centered Earth Fixed Coordinate Frame ---- Fixed Earth and Cartesian plane

        earth = Sphere(radius=R, resolution=(50, 50), color=BLUE,
                       )

        earth = OpenGLTexturedSurface(earth, 'images/day.jpg', 'images/night.jpg')

        self.play(SpinInFromNothing(earth))

        a = elliptial_parameter(orbit_data['semimajor'], orbit_data['eccentricity'])

        # Orbits
        orbital_path = Ellipse(**a, color=BLUE_C) \
            .set_opacity(0.66).set_fill(opacity=0)

        # Focal off-set

        orbital_path.shift(RIGHT * get_focus(orbital_path))

        self.play(Create(orbital_path))
        self.wait(0.5)

        # Orbital rotations from Keplerian elements

        path_group = VGroup(orbital_path, Vector(OUT).set_opacity(0), Vector(RIGHT).set_opacity(0),
                            Vector(UP).set_opacity(0))

        self.wait(1)

        # Angle of inclination about y-axis

        self.play(
            path_group.animate.rotate(angle=angular_correction(orbit_data['inclination']), axis=np.array([1, 0, 0]),
                                      about_point=ORIGIN))

        self.wait(1)

        # RANN rotation-- ascending node rotations
        self.play(
            path_group.animate.rotate(angle=angular_correction(orbit_data['acending_node']), axis=np.array([0, 0, 1]),
                                      about_point=ORIGIN))
        self.wait(1)

        # Angle of Perigee rotation #FIX the animation
        self.play(Rotate(path_group, angle=angular_correction(orbit_data['periapsis']),
                         axis=path_group[1].get_end(), about_point=ORIGIN), run_time=2)

        self.wait(1)

        # Satellite Part

        sat = Dot3D(radius=0.06, point=scaling_factor * np.array(orbit_data['position']), color=BLUE)

        self.play(SpinInFromNothing(sat))  # creation of Satellite

        self.wait(0.22)

        self.play(Indicate(mobject=sat, scale_factor=2, color=PURPLE))  # Indicate Animation

        self.wait(0.1)

        self.play(orbital_path.animate.set_opacity(0.2).set_fill(opacity=0), ax.animate.set_opacity(0))

        self.wait()

        # Display coordinate of the satellite

        init_text = Tex('Initial Location: ', color=BLUE_C, font_size=40, slant=ITALIC, weight=BOLD)

        coordinate_system = Tex('ECFC coordinates: ', color=BLUE_C, font_size=40, slant=ITALIC, weight=BOLD)

        x_var = Variable(var=(sat.get_center()[0] * inverse_scaling), label='X-coordinate: ', num_decimal_places=5,
                         var_type=DecimalNumber) \
            .set_color(BLUE_C)

        y_var = Variable(var=(sat.get_center()[1] * inverse_scaling), label=' Y-coordinate: ', num_decimal_places=5,
                         var_type=DecimalNumber) \
            .set_color(BLUE_C)
        z_var = Variable(var=(sat.get_center()[2] * inverse_scaling), label='Z-coordinate: ', num_decimal_places=5,
                         var_type=DecimalNumber) \
            .set_color(BLUE_C)

        text_group = VGroup(init_text, x_var, y_var, z_var).arrange_in_grid(4, 1).scale(0.4).to_edge(UR).shift(DOWN)

        coordinate_system.next_to(text_group, UP, buff=0.6).scale(0.5)
        text_group.fix_in_frame()
        coordinate_system.fix_in_frame()

        x_var.add_updater(lambda mob: mob.tracker.set_value(sat.get_center()[0] * inverse_scaling))
        y_var.add_updater(lambda mob: mob.tracker.set_value(sat.get_center()[1] * inverse_scaling))
        z_var.add_updater(lambda mob: mob.tracker.set_value(sat.get_center()[2] * inverse_scaling))

        self.play(AnimationGroup(Write(coordinate_system), Write(text_group), lag_ratio=0.5))

        self.wait()

        self.play(FadeOut(init_text))

        self.wait()

        # Date and time

        track_seconds = ValueTracker(0)

        time = orbit_data['UTC']

        # get labels from function as list
        label = date_label(track_seconds, time)

        for x in label:
            x.fix_in_frame()

        label[0].to_edge(DR)

        self.play(AnimationGroup(*[Write(x) for x in label], lag_ratio=0.5))

        self.wait()

        # Moving satellite animation -- Real trace is a custom animation class implemented below.

        self.play(Move_along_edge(sat, orbital_path, rate_func=linear),
                  track_seconds.animate.set_value(orbit_data['time_period'])
                  , run_time=10)

        self.wait(3)


class Move_along_edge(Animation):

    def __init__(
            self,
            mobject: Mobject,
            path: VMobject,
            suspend_mobject_updating: bool | None = False,
            **kwargs,
    ):
        super().__init__(mobject, path, suspend_mobject_updating, **kwargs, )
        self.path = path
        self.needed = None

    def begin(self) -> None:

        self.path: Mobject

        for i in np.linspace(0, 1, 3500):
            if abs(angle(self.path.point_from_proportion(i), self.mobject.get_center())) <= 0.08:
                self.needed = i
                break
        print(self.needed)
        super().begin()

    def interpolate_mobject(self, alpha: float) -> None:
        beta = self.needed + self.rate_func(alpha)
        if beta < 1:
            self.mobject.move_to(self.path.point_from_proportion(beta))
        else:
            self.mobject.move_to(self.path.point_from_proportion(beta - 1))





# Just Checking data for a RINEX file
# path_to_rinex = r'/home/hades/Desktop/NAV/AMC400USA_R_20220911900_01H_GN.rnx'

# satellite_number = 'G09'

# Ignore above
