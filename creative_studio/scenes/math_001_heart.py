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
RED = "#E52239"

def heart_points(n=2401):
    """Solve r² - |cos θ|^(2/3) sin θ r^(5/3) - 1 = 0."""
    theta = np.linspace(-np.pi/2, 3*np.pi/2, n)
    def solve(angles):
        k = np.abs(np.cos(angles))**(2/3)*np.sin(angles)
        lo, hi = np.full_like(angles,.5), np.full_like(angles,2.5)
        for _ in range(55):
            r = (lo+hi)/2
            f = r*r-k*r**(5/3)-1
            lo = np.where(f <= 0, r, lo)
            hi = np.where(f > 0, r, hi)
        r = (lo+hi)/2
        return np.column_stack((r*np.cos(angles),r*np.sin(angles)))
    points = solve(theta)
    # Resample to give the moving point a constant speed along the curve.
    s = np.r_[0, np.cumsum(np.linalg.norm(np.diff(points,axis=0),axis=1))]
    q = np.linspace(0,s[-1],n)
    # Re-solve after angular interpolation to keep each sampled vertex on F=0.
    points = solve(np.interp(q,s,theta))
    x,y = points.T
    residual = float(np.max(np.abs((x*x+y*y-1)**3-x*x*y**3)))
    print(f"MATH-001: {n} boundary samples; max |F(x,y)| = {residual:.3e}")
    assert residual < 1e-10, "Heart equation validation failed"
    assert np.linalg.norm(points[0]-points[-1]) < 1e-10, "Curve is not closed"
    return points

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
        layers = VGroup(*[curve.copy().set_stroke(PINK,w,opacity=o) for w,o in [(24,.05),(16,.12),(10,.25)]],curve)
        lead = VGroup(Dot(pts[0],radius=.105,color="#81314C"),Dot(pts[0],radius=.064,color="#FFD2DD"),Dot(pts[0],radius=.032,color=WHITE))
        track=ValueTracker(0)
        def partial_trace():
            result = VGroup()
            for layer in layers:
                segment = layer.copy()
                segment.pointwise_become_partial(layer,0,max(.0001,track.get_value()))
                result.add(segment)
            return result
        trace = always_redraw(partial_trace)
        origin = plane.c2p(0,0)
        def partial_fill():
            progress = track.get_value()
            if progress <= 0:
                return VMobject().set_points_as_corners([origin,origin,origin]).set_fill(RED,0).set_stroke(width=0)
            tip = curve.point_from_proportion(progress)
            idx = min(len(pts)-1,int(progress*(len(pts)-1)))
            # Radial sweep: every traced boundary segment fills inward to the origin.
            vertices = np.vstack([origin,pts[:idx+1],tip,origin])
            return VMobject().set_points_as_corners(vertices).set_fill(RED,.86).set_stroke(width=0)
        fill = always_redraw(partial_fill)
        lead.add_updater(lambda d:d.move_to(curve.point_from_proportion(track.get_value())))
        caption=Text("A mathematical way to say",font="Liberation Serif",font_size=32,color="#B9C0D0").move_to(DOWN*4.35)
        love=Text("I love you.",font="Liberation Serif",font_size=68,color="#FF829C").move_to(DOWN*5.15)
        signature = Text("Soph Laugh", font="Liberation Serif", font_size=22, color="#B7A7B8").move_to(RIGHT*3.15+DOWN*6.15)
        signature.to_corner(DR,buff=.65)
        self.add(signature)
        self.add(kicker,title,equation,plane,xlab,ylab,fill,trace,lead)
        self.play(track.animate.set_value(1),rate_func=linear,run_time=10)
        lead.clear_updaters()
        fill.clear_updaters()
        fill.become(VMobject().set_points_as_corners(pts).set_fill(RED,.86).set_stroke(width=0))
        self.remove(trace,lead)
        self.add(layers)
        self.play(FadeIn(caption),run_time=.65)
        self.play(FadeIn(love,shift=UP*.15),run_time=.65)
        self.wait(2.7)
