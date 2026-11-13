"""Mid-round: two shots played, rewards so far, and V at the tee vs V where the ball is now. Illustrative.

s3-mid-a: trajectory tee -> s1 -> s2, each shot tagged with its reward (-1)
s3-mid-b: + V(s0) at the tee  ("how well I should do")
s3-mid-c: + V(s2) at the ball ("how well I am doing" = rewards so far + V(s2))
"""
import matplotlib.patheffects as pe
import numpy as np

from s3_hole import TEE, draw_hole, new_fig, value_fn
from style import C, save

S1 = np.array([160.0, 6.0])   # drive: safe, short of the pond
S2 = np.array([290.0, 3.0])   # second shot: carries the pond, on the green
PATH = [TEE, S1, S2]
V0, V2 = (float(value_fn(*p)) for p in (TEE, S2))
print(f"V(s0)={V0:.2f}  V(s2)={V2:.2f}  so far+V(s2)={-2 + V2:.2f}  gap={-2 + V2 - V0:+.2f}")

WHITE = [pe.withStroke(linewidth=2.5, foreground="white")]


def num(v):
    return f"{v:.1f}".replace("-", "−")


def vbox(ax, xy, label, v, dx, dy):
    ax.text(xy[0] + dx, xy[1] + dy, f"{label} = {num(v)}", fontsize=8.5, ha="center", va="center", zorder=10,
            color=C["value"], fontweight="bold",
            bbox=dict(fc="white", ec=C["value"], lw=0.7, boxstyle="round,pad=0.3"))


def draw(stage, name):
    fig, ax = new_fig()
    draw_hole(ax, scale=False, golfer=False, labels=False)
    # shots played so far
    for i, (a, b) in enumerate(zip(PATH[:-1], PATH[1:])):
        ax.annotate("", xy=b, xytext=a, zorder=5,
                    arrowprops=dict(arrowstyle="-|>", mutation_scale=9, color=C["agent"], lw=1.6,
                                    shrinkA=3, shrinkB=3, connectionstyle="arc3,rad=-0.18"))
        mid = (a + b) / 2
        ax.text(mid[0], mid[1] + 24, f"$r_{i + 1}$ = −1", fontsize=8.5, ha="center", va="center", zorder=9,
                color=C["reward"], fontweight="bold",
                bbox=dict(fc="white", ec=C["reward"], lw=0.7, boxstyle="round,pad=0.25"))
    # where the ball has been (hollow) and where it is now (solid, "you")
    for p in (TEE, S1):
        ax.plot(*p, "o", ms=5, mfc="white", mec=C["agent"], mew=1.1, zorder=8)
    ax.plot(*S2, "o", ms=6, color=C["agent"], mec="white", mew=0.9, zorder=8)
    for p, lab in ((TEE, "$s_0$"), (S1, "$s_1$"), (S2, "$s_2$ (you)")):
        ax.text(p[0], p[1] - 13, lab, fontsize=10, color=C["agent"], ha="center", va="center", zorder=9,
                path_effects=WHITE)
    if stage in ("b", "c"):
        vbox(ax, TEE, "$V(s_0)$", V0, 8, -38)
    if stage == "c":
        vbox(ax, S2, "$V(s_2)$", V2, -8, -42)
    save(fig, name)


W = np.array([220.0, 5.0])    # the other trajectory: second shot falls short, in the pond
VW = float(value_fn(*W))
print(f"water: V(s2)={VW:.2f}  so far+V(s2)={-2 + VW:.2f}  gap={-2 + VW - V0:+.2f}")


def draw_water(name):
    """s3-mid-d: same drive, but the second shot splashes; the green trajectory stays, faded, for comparison."""
    fig, ax = new_fig()
    draw_hole(ax, scale=False, golfer=False, labels=False)
    faded = (*__import__("matplotlib").colors.to_rgb(C["agent"]), 0.3)
    ax.annotate("", xy=S2, xytext=S1, zorder=5,
                arrowprops=dict(arrowstyle="-|>", mutation_scale=9, color=faded, lw=1.4,
                                shrinkA=3, shrinkB=3, connectionstyle="arc3,rad=-0.18"))
    ax.plot(*S2, "o", ms=5, color=faded, mec="none", zorder=8)
    for i, (a, b) in enumerate(((TEE, S1), (S1, W))):
        ax.annotate("", xy=b, xytext=a, zorder=6,
                    arrowprops=dict(arrowstyle="-|>", mutation_scale=9, color=C["agent"], lw=1.6,
                                    shrinkA=3, shrinkB=3, connectionstyle="arc3,rad=-0.18"))
        mid = (a + b) / 2
        ax.text(mid[0], mid[1] + (24 if i == 0 else 18), f"$r_{i + 1}$ = −1", fontsize=8.5, ha="center",
                va="center", zorder=9, color=C["reward"], fontweight="bold",
                bbox=dict(fc="white", ec=C["reward"], lw=0.7, boxstyle="round,pad=0.25"))
    for p in (TEE, S1):
        ax.plot(*p, "o", ms=5, mfc="white", mec=C["agent"], mew=1.1, zorder=8)
    ax.plot(*W, "o", ms=6, color=C["agent"], mec="white", mew=0.9, zorder=8)
    for p, lab in ((TEE, "$s_0$"), (S1, "$s_1$"), (W, "$s_2$ (you)")):
        ax.text(p[0], p[1] - 13, lab, fontsize=10, color=C["agent"], ha="center", va="center", zorder=9,
                path_effects=WHITE)
    vbox(ax, TEE, "$V(s_0)$", V0, 8, -38)
    vbox(ax, W, "$V(s_2)$", VW, 0, -68)
    save(fig, name)


draw("a", "s3-mid-a")
draw("b", "s3-mid-b")
draw("c", "s3-mid-c")
draw_water("s3-mid-d")
