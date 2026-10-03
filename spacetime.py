"""Clock comparison and hypothetical wormhole chapters for the main film."""

from manim import *
import numpy as np


CYAN = "#55E8FF"
PURPLE = "#A58AFF"
GOLD = "#FFCE73"
BG = "#050914"


class SpacetimeMixin:
    def _st_label(self, text, size=25, color=CYAN):
        return Text(text, font="Microsoft YaHei", font_size=size, color=color)

    def time_chapter(self):
        self.section("03", "时间，竟然有不同的速度", "GRAVITATIONAL TIME DILATION")
        equation = self.formula("dτ/dt = √(1 − rₛ/r)", font_size=38)
        equation.move_to([0, 2.05, 0])
        condition = self._st_label("非旋转黑洞外 · 静止时钟 · 与远处比较", 19, PURPLE)
        condition.move_to([0, 1.48, 0])
        self.body.add(equation, condition)
        self.play(FadeIn(equation, shift=UP * .15), FadeIn(condition), run_time=1.6)
        self.caption("引力越强，时钟相对远处走得越慢")
        self.say("黑洞还会改变时间。这条公式比较非旋转黑洞外的静止时钟与远处时钟。距离越近，本地一秒，对应远处更多的时间。", duration=3)

        elapsed = ValueTracker(0)
        centers = [np.array([-3.05, -.05, 0]), np.array([3.05, -.05, 0])]
        clocks = VGroup()
        hands = VGroup()
        counts = VGroup()
        labels = VGroup()
        for center, rate, color, title in zip(
            centers, [1., .5], [CYAN, GOLD], ["远处时钟", "靠近黑洞的时钟"]
        ):
            face = Circle(radius=1.03, color=color, stroke_width=2).move_to(center)
            inner = Circle(radius=.91, color=color, stroke_opacity=.25).move_to(center)
            ticks = VGroup(*[
                Line(center + .92 * np.array([np.sin(a), np.cos(a), 0]),
                     center + 1.01 * np.array([np.sin(a), np.cos(a), 0]),
                     color=color, stroke_width=2)
                for a in np.arange(12) * TAU / 12
            ])
            hub = Dot(center, radius=.055, color=color)
            clocks.add(face, inner, ticks, hub)
            hand = always_redraw(lambda c=center, k=rate, col=color: Line(
                c, c + .78 * np.array([
                    np.sin(elapsed.get_value() * k * TAU / 8),
                    np.cos(elapsed.get_value() * k * TAU / 8), 0
                ]), color=col, stroke_width=4))
            hands.add(hand)
            counter = DecimalNumber(0, num_decimal_places=1, font_size=34, color=color)
            counter.move_to(center + DOWN * 1.53)
            counter.add_updater(lambda m, k=rate: m.set_value(elapsed.get_value() * k))
            counts.add(counter)
            labels.add(self._st_label(title, 26, color).move_to(center + UP * 1.16))

        units = VGroup(*[
            self._st_label("累计秒数", 18, PURPLE).move_to(c + DOWN * 1.98)
            for c in centers
        ])
        comparison = self.formula("r = 4rₛ/3  →  dτ/dt = 0.5", font_size=25)
        comparison.move_to([0, -2.58, 0])
        connector = DashedLine([-1.62, -.05, 0], [1.62, -.05, 0], color=PURPLE,
                               stroke_opacity=.5)
        self.body.add(clocks, hands, counts, labels, units, comparison, connector)
        self.play(Create(clocks), FadeIn(labels), FadeIn(counts), FadeIn(units),
                  Create(connector), Write(comparison), run_time=2)
        self.add(hands)
        elapsed.add_updater(lambda tracker, dt: tracker.increment_value(dt))
        self.add(elapsed)
        self.caption("理想例子：远处两秒，这里一秒")
        self.say("把时钟固定在史瓦西半径的三分之四处，走时比就是零点五。远处两秒，近处一秒。双方都觉得自己的手表正常，差别来自比较。", duration=3)
        self.caption("固定悬停只是理想模型，需极大加速度")
        self.say("这条公式适用于静止时钟。如此接近黑洞还要悬停，需要极大的加速度。这只是理想模型，实际旅行还要考虑速度和往返过程。", duration=3)
        elapsed.clear_updaters()
        for counter in counts:
            counter.clear_updaters()
        for hand in hands:
            hand.clear_updaters()
        self.remove(elapsed)

        arrow = CurvedArrow([-1.8, -.72, 0], [1.8, -.72, 0], angle=PI / 3,
                            color=PURPLE, stroke_width=3)
        reunion = self._st_label("重逢时：你经历的时间更少", 24, GOLD)
        reunion.move_to([0, .48, 0])
        self.body.add(arrow, reunion)
        self.play(FadeOut(connector), Create(arrow), FadeIn(reunion), run_time=1.6)
        self.caption("去未来：重逢时，彼此年龄出现差别")
        self.say("经历较慢走时的旅行者，之后与远处的人重逢，可能发现自己老得更少。这是相对论意义上的去未来，完整时间差必须计算整个旅程。", duration=3)

    def wormhole_chapter(self):
        self.section("04", "黑洞，是时空穿越的门吗？", "WORMHOLES · THEORY AND EVIDENCE")
        hypothesis = self._st_label("虫洞：理论猜想", 27, GOLD).move_to([0, 2.08, 0])
        self.body.add(hypothesis)
        self.play(FadeIn(hypothesis), run_time=.8)
        self.caption("虫洞设想：连接遥远区域的时空捷径")
        self.say("科幻里的时空隧道通常指虫洞。某些相对论模型允许连接遥远区域的几何结构。但数学允许讨论，并不代表宇宙已经造好了这条路。", duration=3)

        def flat(x, y):
            return np.array([x, y - .25, 0])

        def folded(x, y):
            theta = PI * x / 4
            return np.array([2 * np.sin(theta) + .13 * x,
                             1.05 * np.cos(theta) + .58 * y - .2, 0])

        sheet = VGroup()
        targets = []
        for y in np.linspace(-.85, .85, 9):
            line = ParametricFunction(lambda t, yy=y: flat(t, yy), t_range=[-4, 4, .06],
                                      color=CYAN, stroke_width=1.2, stroke_opacity=.55)
            sheet.add(line)
            targets.append(ParametricFunction(lambda t, yy=y: folded(t, yy),
                                              t_range=[-4, 4, .06], color=CYAN,
                                              stroke_width=1.2, stroke_opacity=.55))
        for x in np.linspace(-4, 4, 17):
            line = Line(flat(x, -.85), flat(x, .85), color=PURPLE,
                        stroke_width=1.2, stroke_opacity=.45)
            sheet.add(line)
            targets.append(Line(folded(x, -.85), folded(x, .85), color=PURPLE,
                                stroke_width=1.2, stroke_opacity=.45))
        point_a = Dot(flat(-4, 0), color=GOLD, radius=.1)
        point_b = Dot(flat(4, 0), color=GOLD, radius=.1)
        name_a = self._st_label("A", 25, GOLD).next_to(point_a, LEFT)
        name_b = self._st_label("B", 25, GOLD).next_to(point_b, RIGHT)
        route = Line(flat(-4, 0), flat(4, 0), color=GOLD, stroke_width=3)
        sheet_note = self._st_label("纸面折叠仅作类比，不是虫洞形成过程", 19, PURPLE)
        sheet_note.move_to([0, -2.57, 0])
        self.body.add(sheet, point_a, point_b, name_a, name_b, route, sheet_note)
        self.play(Create(sheet), FadeIn(point_a), FadeIn(point_b),
                  FadeIn(name_a), FadeIn(name_b), Create(route), FadeIn(sheet_note), run_time=2)
        self.play(*[Transform(line, target) for line, target in zip(sheet, targets)],
                  point_a.animate.move_to(folded(-4, 0)),
                  point_b.animate.move_to(folded(4, 0)),
                  name_a.animate.move_to(folded(-4, 0) + LEFT * .4),
                  name_b.animate.move_to(folded(4, 0) + RIGHT * .4),
                  Transform(route, ParametricFunction(lambda t: folded(t, 0),
                            t_range=[-4, 4, .04], color=GOLD, stroke_width=3)), run_time=3)
        bridge = Line(folded(-4, 0), folded(4, 0), color=GOLD, stroke_width=6)
        bridge_label = self._st_label("假想连接", 23, GOLD).move_to([0, -1.72, 0])
        self.body.add(bridge, bridge_label)
        self.play(Create(bridge), FadeIn(bridge_label), run_time=1)
        self.caption("可穿越虫洞是否存在，尚未得到证实")
        self.say("把空间想成纸，折叠后两点仿佛变近了。这只是类比。可穿越虫洞通常需要特殊条件维持，目前没有观测证据证明这种通道存在。", duration=3)

        distinction = self.formula("黑洞 ≠ 可穿越虫洞", font_size=38)
        distinction.move_to([0, 1.48, 0])
        self.body.add(distinction)
        self.play(Write(distinction), run_time=1.6)
        self.caption("没有穿过黑洞、回到过去的证据")
        self.say("黑洞不等于可穿越虫洞。进入事件视界就无法向外发送信号。穿过黑洞回到过去没有证据；奇点提示经典理论可能失效，不能当作传送门。", duration=3)

        old_geometry = VGroup(sheet, point_a, point_b, name_a, name_b,
                              route, bridge, bridge_label, sheet_note)
        self.play(FadeOut(old_geometry), FadeOut(distinction), FadeOut(hypothesis), run_time=1)
        grid = NumberPlane(x_range=[-6, 6, .5], y_range=[-2.3, 2.3, .4],
                           x_length=12, y_length=4.6,
                           background_line_style={"stroke_color": CYAN,
                               "stroke_width": 1, "stroke_opacity": .35},
                           axis_config={"stroke_opacity": 0})
        grid.prepare_for_nonlinear_transform(num_inserted_curves=30)
        central = Circle(radius=.5, stroke_color=PURPLE, stroke_width=3,
                         fill_color=BG, fill_opacity=1)
        ring = Circle(radius=.68, stroke_color=GOLD, stroke_opacity=.75, stroke_width=2)
        ending = self.formula("Gμν = (8πG/c⁴) Tμν", font_size=35).move_to([0, 2.12, 0])
        self.body.add(grid, central, ring, ending)
        self.play(Create(grid), FadeIn(central), Create(ring), Write(ending), run_time=2)

        def warp(p):
            radius = np.linalg.norm(p[:2])
            angle = .95 * np.exp(-radius / 2.2)
            shrink = 1 - .48 * np.exp(-radius * radius / 3)
            return shrink * np.array([p[0] * np.cos(angle) - p[1] * np.sin(angle),
                                       p[0] * np.sin(angle) + p[1] * np.cos(angle), 0])

        self.play(grid.animate.apply_function(warp), ring.animate.scale(1.2), run_time=3)
        self.caption("数学揭示时空，也提醒我们证据的边界")
        self.say("黑洞让抽象数学变成宇宙现象。引力弯曲时空，时钟改变步伐；关于穿越的想象，仍需要新的理论和证据来检验。", duration=3)
        self.play(Indicate(ending, color=GOLD, scale_factor=1.05),
                  Flash(central.get_center(), color=CYAN, flash_radius=.82,
                        line_length=.16, num_lines=24), run_time=1.5)
