from manim import *
import numpy as np

class PathHomotopyOnTorus(ThreeDScene):
    def construct(self):
        # Torus parameters
        R = 2  # Major radius
        r = 0.7  # Minor radius

        # Create the torus
        torus = Surface(
            lambda u, v: np.array([
                (R + r * np.cos(v)) * np.cos(u),
                (R + r * np.cos(v)) * np.sin(u),
                r * np.sin(v),
            ]),
            u_range=[0, TAU],
            v_range=[0, TAU],
            resolution=(50, 50),
        )
        torus.set_style(fill_color=BLUE, stroke_color=WHITE)
        torus.set_opacity(0.1)

        R = 2.01  # Major radius
        r = 0.701  # Minor radius

        def path_homot(t, i):
            i = i * 0.01

            u_2 = t*TAU
            v_2 = t*TAU + TAU/4

            u_1 = t*TAU
            v_1 = t*TAU + TAU + 6 * np.sin(t * TAU)

            u = (u_2)*i + (u_1)*(1-i)
            v = (v_2)*i + (v_1)*(1-i)
            return np.array([
                (R + r * np.cos(v)) * np.cos(u),
                (R + r * np.cos(v)) * np.sin(u),
                r * np.sin(v),
            ])

        c1_points = np.array([path_homot(t, 0) for t in np.linspace(0, 1, 100)])
        curve1 = Polygon(*c1_points)
        curve1.set_color(YELLOW)

        c2_points = np.array([path_homot(t, 99) for t in np.linspace(0, 1, 100)])
        curve2 = Polygon(*c2_points)
        curve2.set_color(ORANGE)

        # create group for 2d objects needed in 3d
        line_group = VGroup()
        
        line_group.add(curve1)
        line_group.add(curve2)
        curves = []

        for i in range(0, 100, 5):
            h_points = np.array([path_homot(t, i) for t in np.linspace(0, 1, 100)])
            curves.append(Polygon(*h_points).set_color(YELLOW))
            line_group.add(curves[-1])

        curves.append(curve2)

        # increase granularity if you still see "popping" but 20 should be enough
        granularity_3d = 100

        # step through group items and make mobjects needed for propper alpha hiding
        for line_group_3d in line_group:
            line_group_3d.pieces = VGroup(
                *line_group_3d.get_pieces(granularity_3d)
            )
            line_group_3d.add(line_group_3d.pieces)
            line_group_3d.set_stroke(width=0, family=False)
            line_group_3d.set_shade_in_3d(True)

        # Add paths to the scene
        self.add(curve1)
        self.add(curve2)
        self.add(torus)

        # Rotate the camera for a better view
        self.move_camera(zoom = 2, phi=75 * DEGREES, theta=15 * DEGREES, run_time=3)

        for curve in curves:
            #h_points = np.array([path_homot(t, i) for t in np.linspace(0, 1, 100)])
            self.play(Transform(curve1, curve, run_time=0.2, rate_func=linear))
        self.play(Transform(curve1, curve2, run_time=0.25, rate_func=linear))

        # Pause to display the final state
        self.wait(2)
