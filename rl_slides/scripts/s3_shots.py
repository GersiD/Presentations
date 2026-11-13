"""Candidate shots from the tee, landing spots s', their value, and the argmax. Illustrative."""
import matplotlib as mpl
import matplotlib.patheffects as pe
import numpy as np

from s3_hole import TEE, VALUE_CMAP, draw_hole, new_fig, value_fn
from style import C, save

rng = np.random.default_rng(7)
# (label, angle deg, distance yd)
CANDS = [("lay up", 9, 177), ("carry the pond", 0, 252), ("fall short, splash", -6, 223), ("around, right", 18, 240)]
R = -1.0  # reward per stroke


def landings(theta, dist, n=400):
    th = np.deg2rad(theta)
    u = np.array([np.cos(th), np.sin(th)])
    n_ = np.array([-np.sin(th), np.cos(th)])
    d = dist + rng.normal(0, 0.04 * dist, n)
    l = rng.normal(0, 0.06 * dist, n)
    return TEE[None] + d[:, None] * u + l[:, None] * n_


stats = []
for lab, th, dist in CANDS:
    pts = landings(th, dist)
    q = float(np.mean(R + value_fn(pts[:, 0], pts[:, 1])))
    mean = np.array([dist * np.cos(np.deg2rad(th)), dist * np.sin(np.deg2rad(th))])
    stats.append((lab, mean, pts[:25], q))
    print(f"{lab:15s} E[r+V(s')] = {q:.2f}")
best = int(np.argmax([s[3] for s in stats]))
qs = np.array([s[3] for s in stats])
norm = mpl.colors.Normalize(vmin=-6.2, vmax=-3.4)


def shade(q):
    return VALUE_CMAP(0.35 + 0.65 * norm(q))


# label offsets (dx, dy) in yards
OFF = [(0, 15), (0, 15), (0, -16), (21, 0)]


def draw(mode, name):
    fig, ax = new_fig()
    draw_hole(ax, scale=True, labels=False)
    for i, (lab, mean, pts, q) in enumerate(stats):
        faded = mode == "c" and i != best
        col = C["agent"] if mode == "a" else shade(q)
        alpha = 0.28 if faded else 1.0
        lw = 2.4 if (mode == "c" and i == best) else 1.3
        rgba = mpl.colors.to_rgba(col, alpha)
        ax.annotate("", xy=mean, xytext=TEE, zorder=5,
                    arrowprops=dict(arrowstyle="-|>", mutation_scale=9, color=rgba, lw=lw,
                                    shrinkA=3, shrinkB=0, connectionstyle="arc3,rad=0.0"))
        ax.plot(pts[:, 0], pts[:, 1], "o", ms=1.8, color=col, alpha=0.5 * alpha, mew=0, zorder=5)
        ax.plot(*mean, "o", ms=6 if not (mode == "c" and i == best) else 8, color=col, mec="white", mew=0.9,
                alpha=alpha, zorder=8)
        dx, dy = OFF[i]
        if mode == "a":
            ax.text(mean[0] + dx, mean[1] + dy, "s'", style="italic", fontsize=11, color=C["agent"], ha="center", va="center",
                    zorder=9, fontweight="bold", path_effects=[pe.withStroke(linewidth=2.5, foreground="white")])
        else:
            win = mode == "c" and i == best
            ax.text(mean[0] + dx, mean[1] + dy, f"{q:.1f}".replace("-", "\u2212"), fontsize=9 if win else 8.5, ha="center", va="center",
                    zorder=9, color="white" if win else C["value"], fontweight="bold",  # labels stay full color (no grey text)
                    bbox=dict(fc=C["value"] if win else "white", ec=C["value"], lw=0.7, pad=1.4,
                              boxstyle="round,pad=0.25"))
    save(fig, name)


draw("a", "s3-shots-a")
draw("b", "s3-shots-b")
draw("c", "s3-shots-c")
