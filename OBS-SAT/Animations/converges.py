from manim import  *
import numpy as np


coord =[]
series =0
for i in range(10):
    series += 1+ 1/ ((i+1)**2)
    coord.append(spherical_to_cartesian([1.3,series,series*(i/100)]))

coord.reverse()


class Linear(ThreeDScene):

    def construct(self):

        self.renderer.camera.set_theta(np.pi/3)

        self.renderer.camera.set_phi(np.pi /8)


        #Axes
        axes = ThreeDAxes(x_range=[-30, 30, 1], y_range=[-30, 30, 1], z_range=[-30, 30, 1], x_length=30, y_length=30,
                        z_length=30, tips=False,
                        stroke_width=1, axis_config={'include_ticks': False, 'stroke_width': 3}).set(
            color=BLUE_C).set_opacity(0.67)


        # sphere
        earth = Sphere(radius=1.3, resolution=(50, 50), color=BLUE, opacity=1)

        #
        self.play(Create(axes))

        # Sphere
        self.play(Create(earth))

        # dot Animation
        tracker= ValueTracker(0)
        self.add(tracker)
        dot  = Dot3D(color=YELLOW, resolution=(20,20)).move_to(coord[0])
        dot.add_updater(lambda mob: mob.move_to(coord[int(tracker.get_value())]))

        group =Group()

        for i in range(4):
            line = Line3D(color=BLUE_D, start=spherical_to_cartesian([3,np.random.randint(1,100),np.random.random()*1.33]) , end= dot.get_center()).copy()

            group.add(line)
            group[i].add_updater(lambda mob: mob.become(Line3D(color=BLUE, start=mob.get_start(), end= dot.get_end())))


            del line


        self.begin_ambient_camera_rotation(0.03)




        self.play(Create(dot))
        self.play(Create(group))


        self.play(tracker.animate.set_value(9), run_time=4)


scene = Linear()
scene.render()



