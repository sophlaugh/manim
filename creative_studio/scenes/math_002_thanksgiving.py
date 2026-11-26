"""MATH-002: Happy Thanksgiving | Native Manim creative scene.

Original stylized maple leaf defined by a positive radial polygon.
One arc-length parameter drives outline, red-orange fill, and moving tip.
No AOI imports, paths, or production records are used.
"""
from manim import *
import numpy as np
import manimpango

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 8
config.frame_height = 128/9
config.frame_rate = 30
config.background_color = "#0B101B"

# Symmetric autumn maple contour. Each angle/radius pair is a vertex;
# the intermediate outline is piecewise linear in Cartesian coordinates.
HALF = np.array([
    [-90,.60],[-77,.85],[-64,1.38],[-53,1.15],
    [-43,1.74],[-33,1.39],[-23,2.24],[-12,1.91],
    [-2,2.32],[9,1.99],[19,1.36],[29,1.69],
    [40,2.48],[50,2.00],[58,2.12],[65,1.48],
    [72,1.25],[78,2.08],[84,1.91],[90,2.70],
], dtype=float)

def leaf_geometry():
    a = np.vstack([HALF, np.column_stack([180-HALF[-2::-1,0], HALF[-2::-1,1]])])
    theta, radius = np.deg2rad(a[:,0]), a[:,1]
    vertices = np.column_stack([radius*np.cos(theta),radius*np.sin(theta)])
    vertices[-1] = vertices[0]
    # Every consecutive edge has positive oriented area relative to the origin.
    # Therefore all fan triangles fit within the radial polygon.
    cross = vertices[:-1,0]*vertices[1:,1]-vertices[:-1,1]*vertices[1:,0]
    assert np.all(cross > 0), "Contour must be strictly radial"
    assert np.allclose(vertices[0], vertices[-1]), "Contour is not closed"
    area = .5*cross.sum()
    lengths = np.linalg.norm(np.diff(vertices,axis=0),axis=1)
    cumulative = np.r_[0,np.cumsum(lengths)]
    print(f"MATH-002: {len(vertices)-1} edges; area={area:.6f}; perimeter={cumulative[-1]:.6f}; radial fan validated")
    return vertices, cumulative

class ThanksgivingLeaf(Scene):
    def construct(self):
        vertices, cumulative = leaf_geometry()
        available = set(manimpango.list_fonts())
        serif = next((f for f in ("Times New Roman","Liberation Serif","Serif") if f in available),"serif")
        kicker = Text("M A T H E M A T I C S   /   0 0 2",font_size=23,color="#A8B1C2").move_to(UP*5.42)
        title = Text("The geometry of autumn",font=serif,font_size=43,color="#FFF0DA").move_to(UP*4.62)
        equation = MathTex(r"\mathbf{p}_i=r_i(\cos\theta_i,\sin\theta_i)",font_size=35,color="#F2BC8A").move_to(UP*3.83)
        plane = NumberPlane(x_range=[-3,3,1],y_range=[-3,3,1],
            x_length=6.7,y_length=6.7,faded_line_ratio=0,
            background_line_style={"stroke_color":"#364257","stroke_opacity":.36,"stroke_width":1},
            axis_config={"stroke_color":"#788499","stroke_opacity":.58,"stroke_width":1.25,"include_tip":False}).move_to(DOWN*.20)
        pts = np.array([plane.c2p(x,y) for x,y in vertices])
        O = plane.c2p(0,0)
        progress = ValueTracker(0)
        def prefix():
            d = np.clip(progress.get_value(),0,1)*cumulative[-1]
            i = min(len(pts)-2,int(np.searchsorted(cumulative,d,side="right")-1))
            alpha = (d-cumulative[i])/(cumulative[i+1]-cumulative[i])
            tip = (1-alpha)*pts[i]+alpha*pts[i+1]
            return np.vstack([pts[:i+1],tip])
        def partial_path():
            pp = prefix()
            return VGroup(*[VMobject().set_points_as_corners(pp).set_stroke(c,w,opacity=o)
                for c,w,o in [("#F65420",22,.07),("#F86A29",14,.15),("#FF9A38",8,.35),("#FFD17C",3,1)]])
        trace = always_redraw(partial_path)
        # Progressive fan fill. Warm gradient is evaluated separately on each
        # completed triangle. The final partial triangle shares the exact tip.
        def fan_fill():
            pp = prefix()
            fill = VGroup()
            for j in range(len(pts)-1):
                a = pts[j]
                b = pp[j+1] if j+1 < len(pp) else a
                mid = (a+b)/2
                weight = np.clip((mid[0]+2.5)/5,0,1)
                col = interpolate_color(ManimColor("#E23D1D"),ManimColor("#FFA32B"),weight)
                tri = Polygon(O,a,b,stroke_width=.1,stroke_opacity=float(np.linalg.norm(b-a)>1e-9),stroke_color=col,fill_color=col,fill_opacity=float(np.linalg.norm(b-a)>1e-9))
                fill.add(tri)
            return fill
        fill = always_redraw(fan_fill)
        lead = VGroup(Dot(radius=.11,color="#A74522"),Dot(radius=.064,color="#FFD69F"),Dot(radius=.032,color=WHITE))
        lead.add_updater(lambda m:m.move_to(prefix()[-1]))
        lead.move_to(pts[0])
        stem = CubicBezier(plane.c2p(0,-1.65),plane.c2p(-.12,-1.28),plane.c2p(-.04,-.85),pts[0]).set_stroke("#D68A39",7)
        # Veins are radial and remain in the filled blade; add after the sweep.
        veins = VGroup()
        for j in [6,12,19,26,32]:
            p=pts[j]
            veins.add(Line(O,O+(p-O)*.86,stroke_color="#8C321B",stroke_width=2.2,stroke_opacity=.55))
        mid = Line(pts[0],plane.c2p(0,2.42),stroke_color="#A73A17",stroke_width=3,stroke_opacity=.65)
        signature = Text("Soph Laugh",font=serif,font_size=22,color="#C8B5A6").to_corner(DR,buff=.65)
        caption = Text("Happy Thanksgiving!",font=serif,font_size=55,color="#FFD087").move_to(DOWN*4.65)
        caption.scale_to_fit_width(min(caption.width,7.0))
        sub = Text("Wishing you a beautiful autumn day.",font=serif,font_size=27,color="#F2DEC6").move_to(DOWN*5.35)
        self.add(kicker,title,equation,plane,signature,fill,trace,lead)
        self.play(Create(stem),run_time=.65)
        self.play(progress.animate.set_value(1),rate_func=linear,run_time=9.35)
        fill.clear_updaters()
        trace.clear_updaters()
        lead.clear_updaters()
        self.remove(lead)
        self.play(Create(mid),Create(veins),FadeIn(caption,shift=UP*.10),run_time=1)
        self.play(FadeIn(sub),run_time=.6)
        self.wait(2.4)
