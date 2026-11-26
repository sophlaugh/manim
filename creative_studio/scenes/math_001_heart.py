"""MATH-001 | An original mathematical heart animation.
Render: manim -qh --fps 30 -r 1080,1920 math_001_heart.py MathematicalHeart
Requires Manim Community Edition and NumPy.
"""
from manim import *
import numpy as np

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 8
config.frame_height = 128/9
config.frame_rate = 30
config.background_color = "#080B14"

PINK = "#FF5278"
RED = "#C5214C"

def heart_points(n=1601):
    """Solve r² - |cos θ|^(2/3) sin θ r^(5/3) - 1 = 0."""
    theta = np.linspace(-np.pi/2, 3*np.pi/2, n)
    k = np.abs(np.cos(theta))**(2/3)*np.sin(theta)
    lo, hi = np.full(n, .5), np.full(n, 2.5)
    for _ in range(55):
        r = (lo+hi)/2
        f = r*r-k*r**(5/3)-1
        lo = np.where(f <= 0, r, lo)
        hi = np.where(f > 0, r, hi)
    r = (lo+hi)/2
    points = np.column_stack((r*np.cos(theta),r*np.sin(theta)))
    # Resample to give the moving point a constant speed along the curve.
    s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(points,axis=0),axis=1))]
    q = np.linspace(0,s[-1],n)
    return np.column_stack([np.interp(q,s,points[:,i]) for i in range(2)])

class MathematicalHeart(Scene):
    def construct(self):
        kicker = Text("M A T H E M A T I C S   /   0 0 1", font_size=23, color="#8E9AB1").move_to(UP*5.4)
        title = Text("The mathematics of love", font="Liberation Serif", font_size=43, color="#F4EAF0").move_to(UP*4.72)
        equation = MathTex(r"(x^2+y^2-1)^3-x^2y^3=0", color="#F5DCE5", font_size=43).move_to(UP*3.8)
        equation.scale_to_fit_width(min(equation.width, 7))
        plane = NumberPlane(x_range=[-1.6,1.6,.4],y_range=[-1.6,1.6,.4],x_length=6.6,y_length=6.6,
            background_line_style={"stroke_color":"#314057","stroke_opacity":.5,"stroke_width":1},
            axis_config={"stroke_color":"#69778C","stroke_opacity":.7,"stroke_width":1.5,"include_tip":False},
            faded_line_ratio=0).move_to(DOWN*.1)
        xlab=Text("x",font_size=20,color="#97A3B6").next_to(plane.x_axis.get_right(),UP,buff=.12)
        ylab=Text("y",font_size=20,color="#97A3B6").next_to(plane.y_axis.get_top(),RIGHT,buff=.12)
        pts = np.array([plane.c2p(x,y) for x,y in heart_points()])
        curve = VMobject().set_points_as_corners(pts).set_stroke(PINK,5)
        glows = VGroup(*[curve.copy().set_stroke(PINK,w,opacity=o) for w,o in [(30,.035),(19,.06),(11,.14)]])
        lead = Dot(pts[0],radius=.065,color="#FFF1F4")
        track=ValueTracker(0)
        trace = always_redraw(lambda: curve.copy().pointwise_become_partial(curve,0, max(.0001,track.get_value())))
        lead.add_updater(lambda d:d.move_to(curve.point_from_proportion(track.get_value())))
        caption=Text("A mathematical way to say",font="Liberation Serif",font_size=32,color="#B9C0D0").move_to(DOWN*4.35)
        love=Text("I love you.",font="Liberation Serif",font_size=68,color="#FF829C").move_to(DOWN*5.15)
        signature = Text("Soph Laugh", font="Liberation Serif", font_size=22, color="#B7A7B8").move_to(RIGHT*3.15+DOWN*6.15)
        signature.align_to(RIGHT*3.35, RIGHT)
        self.add(signature)
        self.add(kicker,title,equation,plane,xlab,ylab,trace,lead)
        self.play(track.animate.set_value(1),rate_func=linear,run_time=10)
        lead.clear_updaters()
        self.remove(trace,lead)
        self.add(curve)
        self.play(FadeIn(caption),run_time=.65)
        self.play(FadeIn(love,shift=UP*.15),run_time=.65)
        self.wait(2.7)
