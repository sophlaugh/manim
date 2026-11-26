"""MATH-003: See the good — vector redraw of Soph's original sticker.

Coordinates are traced in the reference image's coordinate system and mapped
uniformly onto the Manim plane. No photograph or external assets are rendered.
"""
from manim import *
import numpy as np

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16
config.frame_rate = 30

INK = "#122027"
BLUE = "#20B4E6"
PINK = "#ED0050"
PAPER = "#FFFFFF"
ICING = "#F4C8C8"
SCALE = 0.0095


def pt(p):
    x, y = p
    return np.array([(x - 621) * SCALE, (756 - y) * SCALE, 0.0])


def curve(start, *segments, fill=None, width=3, color=INK):
    """Cubic Bezier segments, or a line when only an endpoint is supplied."""
    path = VMobject()
    path.start_new_path(pt(start))
    for seg in segments:
        if len(seg) == 2:
            path.add_line_to(pt(seg))
        else:
            path.add_cubic_bezier_curve_to(pt(seg[:2]), pt(seg[2:4]), pt(seg[4:6]))
    if fill is not None:
        if not np.allclose(path.get_end(), path.get_start()):
            path.add_line_to(path.get_start())
        path.set_fill(fill, opacity=1)
    else:
        path.set_fill(opacity=0)
    path.set_stroke(color, width=width)
    return path

LETTER_PATHS = [[[588,1100],[570,1101],[569,1102],[537,1103],[497,1108],[460,1110],[436,1112],[435,1113],[421,1113],[407,1115],[334,1118]],[[446,1198],[426,1213],[420,1219],[415,1228],[415,1232],[418,1235],[421,1237],[427,1238],[435,1237],[444,1232],[450,1226],[454,1219],[454,1209],[449,1198]],[[472,1158],[461,1156],[444,1158],[435,1163],[429,1170],[428,1174],[430,1178],[435,1185],[446,1196],[446,1198]],[[446,1198],[449,1198]],[[473,1184],[471,1184],[457,1192],[449,1198]],[[476,1177],[473,1184]],[[473,1184],[474,1188],[478,1192],[484,1194],[498,1192],[502,1189],[506,1188]],[[476,1175],[476,1173],[482,1167],[486,1167],[484,1173],[480,1177],[478,1177]],[[476,1175],[476,1177]],[[476,1175],[478,1177]],[[476,1177],[478,1177]],[[506,1185],[509,1184],[514,1178],[514,1172],[510,1172],[506,1176],[505,1178],[506,1185]],[[506,1185],[506,1188]],[[506,1188],[513,1192],[527,1192],[536,1190]],[[588,1100],[588,1106],[579,1145],[568,1206],[567,1230],[570,1238],[574,1238],[586,1222],[606,1180],[625,1133],[631,1121],[634,1120]],[[597,1058],[589,1100]],[[819,1098],[689,1097],[688,1098],[640,1098],[639,1099],[589,1100]],[[634,1120],[635,1122],[635,1136],[627,1176],[626,1190],[630,1190],[641,1183],[645,1183],[659,1191],[667,1191],[679,1182]],[[635,1117],[634,1120]],[[679,1178],[677,1178],[674,1173],[674,1165],[676,1160],[678,1159],[682,1160],[683,1162],[683,1170],[682,1174],[679,1178]],[[679,1178],[679,1182]],[[679,1182],[689,1188],[698,1190]],[[749,1210],[747,1210],[741,1218],[728,1243],[719,1271],[714,1301],[714,1319],[716,1326],[719,1329],[721,1329],[727,1325],[735,1309],[738,1300],[743,1275],[743,1267],[746,1251],[749,1216],[750,1215],[749,1210]],[[754,1168],[746,1170],[737,1178],[736,1182],[742,1183],[746,1180],[752,1178],[753,1180],[752,1192],[753,1196]],[[753,1196],[749,1210]],[[774,1176],[770,1177],[759,1192],[753,1196]],[[781,1168],[782,1187],[781,1191],[777,1194],[775,1194],[774,1192],[774,1176]],[[781,1168],[776,1170],[774,1173],[774,1176]],[[781,1168],[798,1171],[800,1172],[801,1176]],[[801,1176],[798,1191],[800,1197],[804,1197],[808,1192],[808,1182],[804,1177],[801,1176]],[[836,1174],[830,1172],[823,1176],[819,1182],[817,1188],[818,1190],[820,1192],[822,1192],[826,1189],[836,1175]],[[866,1106],[863,1111],[851,1145],[837,1174]],[[837,1175],[840,1176]],[[869,1107],[869,1115],[866,1129],[859,1191],[859,1205],[858,1207],[859,1242]],[[868,1103],[866,1104],[866,1106]],[[866,1106],[869,1107]],[[871,1090],[868,1103]],[[868,1103],[870,1104],[869,1107]]]


def traced_ink(paths, width):
    return VGroup(*[
        VMobject().set_points_as_corners([pt(p) for p in points])
        .set_stroke(INK, width=width)
        for points in paths if len(points) > 1
    ])


class SeeTheGood(Scene):
    def setup_coordinates(self):
        # Every unit is one genuine Manim coordinate unit; pt() maps
        # reference pixels to this Cartesian plane with equal x/y scales.
        grid_color = "#9AABBA"
        grid = VGroup()
        for x in range(-4, 5):
            grid.add(Line([x,-7,0],[x,7,0],color=grid_color,
                          stroke_width=1.9 if x == 0 else .8,
                          stroke_opacity=.58 if x == 0 else .28))
        for y in range(-7, 8):
            grid.add(Line([-4,y,0],[4,y,0],color=grid_color,
                          stroke_width=1.9 if y == 0 else .8,
                          stroke_opacity=.58 if y == 0 else .28))
        labels = VGroup()
        for x in range(-4,5):
            labels.add(Text(str(x),font="Times New Roman",font_size=18,
                            color="#C8D4DF").move_to([x,-7.27,0]))
        for y in range(-7,8):
            labels.add(Text(str(y),font="Times New Roman",font_size=18,
                            color="#C8D4DF").move_to([-4.25,y,0]))
        labels.add(Text("x",font="Times New Roman",font_size=22,
                        color="#C8D4DF").move_to([4.25,-7.27,0]))
        labels.add(Text("y",font="Times New Roman",font_size=22,
                        color="#C8D4DF").move_to([-4.25,7.3,0]))
        heading = Text("Bezier coordinates",font="Times New Roman",
                       font_size=28,color="#E4ECF3").move_to([0,7.6,0])
        self.coordinate_grid = VGroup(grid,labels,heading).set_z_index(10)
        self.active_path = None
        self.pen = Dot(pt((621,108)),radius=.055,color="#FFCE72")
        self.pen.set_stroke("#10151D",width=1.5).set_z_index(12)
        def follow_pen(dot):
            if self.active_path is not None and self.active_path.has_points():
                dot.move_to(self.active_path.get_end())
        self.pen.add_updater(follow_pen)
        x_num = DecimalNumber(0,num_decimal_places=2,include_sign=True,
                              font_size=27,color="#FFCE72")
        y_num = DecimalNumber(0,num_decimal_places=2,include_sign=True,
                              font_size=27,color="#FFCE72")
        x_label = Text("x =",font="Times New Roman",font_size=25,color="#E4ECF3")
        y_label = Text("y =",font="Times New Roman",font_size=25,color="#E4ECF3")
        x_label.move_to([-1.55,7.12,0])
        y_label.move_to([.65,7.12,0])
        x_num.next_to(x_label,RIGHT,buff=.13)
        y_num.next_to(y_label,RIGHT,buff=.13)
        def update_number(number,axis,label):
            number.set_value(float(self.pen.get_center()[axis]))
            number.next_to(label,RIGHT,buff=.13)
        x_num.add_updater(lambda m: update_number(m,0,x_label))
        y_num.add_updater(lambda m: update_number(m,1,y_label))
        self.coordinate_readout = VGroup(x_label,x_num,y_label,y_num).set_z_index(11)
        self.play(FadeIn(self.coordinate_grid),run_time=.8)
        self.add(self.pen,self.coordinate_readout)

    def hide_coordinates(self):
        self.pen.clear_updaters()
        for m in self.coordinate_readout:
            m.clear_updaters()
        self.play(FadeOut(self.coordinate_grid),FadeOut(self.pen),
                  FadeOut(self.coordinate_readout),run_time=1.0)

    def draw_fill(self, shape, seconds=1.3):
        # Trace the boundary first, then flood the closed region with color.
        self.active_path = shape
        color = shape.get_fill_color()
        shape.set_fill(opacity=0)
        self.play(Create(shape), run_time=seconds, rate_func=linear)
        self.play(shape.animate.set_fill(color, opacity=1), run_time=0.42)

    def construct(self):
        self.camera.background_color = "#10151D"
        self.setup_coordinates()
        border = curve((621,108),
            (690,106,709,141,744,166),
            (815,198,861,225,900,259),
            (964,327,1010,428,1032,533),
            (1048,646,1035,752,1016,800),
            (1004,827,992,849,994,857),
            (1010,928,1004,997,949,1065),
            (943,1102,939,1173,933,1259),
            (923,1303,880,1335,817,1310),
            (798,1342,794,1400,728,1405),
            (674,1408,647,1370,642,1332),
            (640,1314,642,1287,636,1289),
            (588,1328,554,1324,506,1284),
            (467,1318,424,1322,391,1303),
            (349,1280,333,1250,342,1196),
            (281,1194,242,1149,263,1100),
            (272,1080,285,1067,284,1058),
            (246,1013,240,959,277,915),
            (214,801,198,713,204,601),
            (197,536,213,480,226,450),
            (185,389,239,337,271,326),
            (278,311,298,290,300,281),
            (296,230,318,181,369,176),
            (397,176,416,184,431,192),
            (471,173,498,171,524,139),
            (551,113,587,107,621,108),
            fill=PAPER, width=1.2, color=PAPER)
        self.draw_fill(border, 1.5)
        oval = curve((618,217),
            (807,217,965,405,965,630),
            (965,852,815,1044,621,1044),
            (435,1044,279,860,279,629),
            (279,400,429,217,618,217),
            fill=BLUE,width=5)
        self.draw_fill(oval,2.0)

        left_arm = curve((472,497),
            (450,548,430,637,410,665),
            (387,684,384,598,389,534),
            (390,493,391,453,392,421),width=2.4)
        right_arm = curve((731,500),
            (742,550,750,643,766,695),
            (780,729,834,752,872,791),
            (907,828,931,891,927,939),
            (922,984,901,982,895,948),
            (889,912,896,872,906,847),width=2.6)
        neck = curve((601,360),(611,389,606,416,599,438),width=2.4)
        spine = curve((600,766),(597,793,600,819,600,839),width=2.6)
        self.active_path = left_arm
        self.play(Create(left_arm),Create(right_arm),Create(neck),Create(spine),
                  run_time=2.1,rate_func=linear)

        rear_foot = curve((500,922),
            (572,930,683,935,751,947),
            (799,946,839,963,838,983),
            (838,1006,778,1018,720,1007),
            (648,999,568,962,500,922),fill=PINK,width=3)
        self.draw_fill(rear_foot,1.1)
        lap = curve((600,839),
            (520,799,449,757,401,757),
            (353,750,333,783,354,820),
            (378,854,456,896,508,925),
            (575,938,666,942,725,942),
            (786,932,857,889,882,851),
            (901,814,874,786,835,779),
            (768,762,692,792,600,839),fill=PAPER,width=3.6)
        self.draw_fill(lap,1.8)
        front_foot = curve((760,936),
            (706,958,620,966,552,953),
            (485,940,423,932,382,939),
            (328,944,315,971,345,1003),
            (383,1035,480,1023,546,1008),
            (624,991,701,969,760,936),
            fill=PINK,width=3.3)
        self.draw_fill(front_foot,1.5)

        head = curve((621,181),
            (674,180,696,236,680,283),
            (668,317,621,363,587,364),
            (540,367,525,314,537,260),
            (545,216,573,181,621,181),
            fill=PAPER,width=3.4)
        self.draw_fill(head,1.3)

        heart = curve((599,436),
            (576,392,540,389,512,412),
            (474,436,460,479,478,521),
            (501,578,553,601,580,689),
            (591,718,596,746,600,770),
            (611,717,622,674,649,632),
            (682,584,724,546,735,507),
            (757,448,711,396,663,398),
            (633,397,611,414,599,436),
            fill=PINK,width=3.7)
        self.draw_fill(heart,2.2)

        plate = curve((392,393),
            (411,388,427,395,423,406),
            (418,419,398,428,382,427),
            (337,420,289,412,290,403),
            (290,393,347,391,392,393),fill=PAPER,width=2.6)
        self.draw_fill(plate,.7)
        wrapper = curve((341,369),(423,369),(410,407),(353,399),
                        (341,369),fill="#D5EAF0",width=2)
        self.draw_fill(wrapper,.65)
        ribs = VGroup(*[curve((x,372),(b,401+(b-353)*.13),width=1.1)
                       for x,b in zip(range(348,421,9),range(357,410,7))])
        self.active_path = ribs[-1]
        self.play(LaggedStart(*[Create(r) for r in ribs],lag_ratio=.13),run_time=.65)
        frosting = curve((344,371),
            (333,362,347,345,355,344),
            (350,335,363,330,371,331),
            (377,319,388,320,396,331),
            (413,331,419,342,414,348),
            (428,354,430,368,419,374),
            (401,380,360,376,344,371),fill=ICING,width=1.9)
        self.draw_fill(frosting,1.0)
        swirls = VGroup(
            curve((347,351),(345,361,365,372,391,366),(402,363,418,360,421,357),width=1.4),
            curve((355,340),(348,349,367,361,391,357),(402,356,411,350,414,348),width=1.4),
            curve((371,331),(362,344,385,352,401,344),width=1.4),
            curve((382,324),(376,333,390,342,399,337),width=1.2))
        self.active_path = swirls[-1]
        self.play(LaggedStart(*[Create(p) for p in swirls],lag_ratio=.2),run_time=.95)
        candle = curve((381,329),(383,290),(389,290),(388,329),(381,329),
                       fill="#F9D6D9",width=1.35)
        self.draw_fill(candle,.5)
        cherry = curve((395,324),(406,323,405,340,395,341),
                       (382,342,382,326,395,324),fill=PINK,width=1.5)
        self.draw_fill(cherry,.45)
        flame = curve((383,285),(371,278,376,265,379,251),
                      (381,265,392,274,386,283),(383,285),
                      fill="#F2E900",width=1.5)
        self.draw_fill(flame,.7)

        # Replace the indistinct photo-traced mark with a legible two-line
        # signature, in the same small white space beside the figure.
        signature_heart = curve((847,959),
            (842,951,836,957,841,963),
            (843,966,845,969,847,972),
            (850,968,854,963,854,960),
            (854,953,849,953,847,959),width=1.55)
        soph = Text("soph",font="Times New Roman",slant=ITALIC,color=INK)
        soph.scale_to_fit_height(.155).move_to(pt((877,971)))
        if soph.width > .40:
            soph.scale_to_fit_width(.40)
        laugh = Text("laugh",font="Times New Roman",slant=ITALIC,color=INK)
        laugh.scale_to_fit_height(.19).move_to(pt((865,994)))
        if laugh.width > .46:
            laugh.scale_to_fit_width(.46)
        signature_swirl = curve((891,999),
            (896,1005,906,1005,908,998),
            (911,990,901,985,898,992),
            (895,997,903,1000,904,994),width=1.55)
        self.active_path = signature_heart
        self.play(Create(signature_heart),run_time=.3)
        # Text is vector glyph geometry; Write draws the glyph contours.
        self.play(Write(soph),Write(laugh),run_time=.8)
        self.active_path = signature_swirl
        self.play(Create(signature_swirl),run_time=.35)

        # Keep the genuine handwriting but remove the die-cut border
        # fragments that were captured in the original crop.
        lettering=traced_ink(LETTER_PATHS,3.4)
        # Track each actual stroke as it is drawn; no artificial coordinates.
        for stroke in lettering:
            self.active_path = stroke
            self.play(Create(stroke),rate_func=linear,
                      run_time=max(.09,4.9*stroke.get_arc_length()/
                                   sum(p.get_arc_length() for p in lettering)))
        self.hide_coordinates()
        credit = Text("Soph Laugh",font_size=18,color="#B7C0CC").to_corner(DR,buff=.25)
        self.play(FadeIn(credit),run_time=.5)
        self.wait(3)
