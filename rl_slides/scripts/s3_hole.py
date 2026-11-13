"""Shared golf-hole drawing + toy value model for section 3 (Value).

Everything here is ILLUSTRATIVE: a hand-made hole and a hand-made value function.
Importable helpers: new_fig, draw_hole, value_fn, terrain_masks, FLAG, TEE.
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Ellipse, Polygon

from style import C, setup

TEE = np.array([0.0, 0.0])
FLAG = np.array([300.0, 0.0])
XLIM = (-30, 342)
YLIM = (-92, 92)

# colours of the course
COL = {
    "rough": "#DCEBC6",
    "fairway": "#A9D68B",
    "green": "#7CC66B",
    "sand": "#F2E3AE",
    "sand_edge": "#CDB878",
    "water": "#9CCBEA",
    "water_edge": "#5C9CC9",
}

GREEN = dict(c=(300, 0), rx=21, ry=17)
WATER = dict(c=(225, 0), rx=19, ry=50)  # pond across the fairway, in front of the green
BUNKERS = [dict(c=(272, -27), rx=13, ry=8),
           dict(c=(281, 27), rx=12, ry=8),
           dict(c=(130, 45), rx=19, ry=8)]

VALUE_CMAP = LinearSegmentedColormap.from_list("value", ["#F6EAF5", "#D9A3D6", C["value"], "#4A0E48"])


def centerline(x):
    return 12 * np.sin(np.pi * np.clip(x, 0, 300) / 300)


def halfwidth(x):
    return 28 + 8 * np.sin(np.pi * (np.asarray(x) - 15) / 267)


def _sig(z):
    return 1 / (1 + np.exp(-np.clip(z, -30, 30)))


def _ell_sdf(x, y, e):
    cx, cy = e["c"]
    r = np.sqrt(((x - cx) / e["rx"]) ** 2 + ((y - cy) / e["ry"]) ** 2)
    return (1 - r) * min(e["rx"], e["ry"])  # >0 inside


def terrain_masks(x, y):
    """Soft masks (0..1) for fairway, green, water, bunker."""
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    fw_sdf = np.minimum(halfwidth(x) - np.abs(y - centerline(x)), np.minimum(x + 12, 285 - x))
    fairway = _sig(fw_sdf / 1.5)
    green = _sig(_ell_sdf(x, y, GREEN) / 1.5)
    water = _sig(_ell_sdf(x, y, WATER) / 1.5)
    bunker = np.zeros_like(x)
    for b in BUNKERS:
        bunker = np.maximum(bunker, _sig(_ell_sdf(x, y, b) / 1.5))
    return fairway, green, water, bunker


def value_fn(x, y):
    """Toy V(s) = -(expected strokes to hole out).  Illustrative, not data."""
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    d = np.hypot(x - FLAG[0], y - FLAG[1])
    base = np.where(d <= 20, 1 + 0.05 * d, 2 + 0.75 * np.log(np.maximum(d, 20) / 20))
    fairway, green, water, bunker = terrain_masks(x, y)
    rough = 1 - np.maximum(fairway, green)
    # water: penalty stroke + drop; plus a "must carry it" zone just short of the pond (sharp drop approaching it)
    wx, wy = WATER["c"]
    short = np.exp(-np.maximum(wx - WATER["rx"] - x, 0) / 18.0) * (x < wx) * _sig((WATER["ry"] - np.abs(y - wy)) / 3.0)
    pen = 0.35 * rough + 0.45 * bunker + 1.5 * water + 0.9 * short * (1 - water)
    return -(base + pen)


def new_fig():
    """Fixed-size, borderless axes so every overlay image has identical bounds."""
    setup()
    mpl.rcParams["savefig.bbox"] = "standard"
    w = 4.3
    h = w * (YLIM[1] - YLIM[0]) / (XLIM[1] - XLIM[0])
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(*XLIM)
    ax.set_ylim(*YLIM)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def _ell(ax, e, **kw):
    ax.add_patch(Ellipse(e["c"], 2 * e["rx"], 2 * e["ry"], **kw))


def draw_hole(ax, scale=True, golfer=True, flag=True, base=True, outlines_only=False, labels=False):
    """Top-down hole. With outlines_only=True only thin outlines are drawn (for use over a heatmap)."""
    xs = np.linspace(-10, 285, 200)
    c, w = centerline(xs), halfwidth(xs)
    poly = np.vstack([np.c_[xs, c + w], np.c_[xs[::-1], (c - w)[::-1]]])
    if base and not outlines_only:
        ax.add_patch(plt.Rectangle((XLIM[0], YLIM[0]), XLIM[1] - XLIM[0], YLIM[1] - YLIM[0],
                                   fc=COL["rough"], ec="none", zorder=0))
    fk = dict(fc="none", ec="#6E8F5B", lw=0.7) if outlines_only else dict(fc=COL["fairway"], ec="none")
    ax.add_patch(Polygon(poly, closed=True, zorder=1, **fk))
    gk = dict(fc="none", ec="#4F8F45", lw=0.8) if outlines_only else dict(fc=COL["green"], ec="#5FAE55", lw=0.8)
    _ell(ax, GREEN, zorder=2, **gk)
    for b in BUNKERS:
        bk = dict(fc="none", ec=COL["sand_edge"], lw=0.9) if outlines_only else dict(fc=COL["sand"], ec=COL["sand_edge"], lw=0.8)
        _ell(ax, b, zorder=3, **bk)
    wk = dict(fc="none", ec=COL["water_edge"], lw=0.9) if outlines_only else dict(fc=COL["water"], ec=COL["water_edge"], lw=0.8)
    _ell(ax, WATER, zorder=3, **wk)
    if labels:
        kw = dict(fontsize=6.5, ha="center", va="center", zorder=6, color="black")
        ax.text(*WATER["c"], "water", style="italic", **kw)
        ax.text(130, 45, "bunker", style="italic", **kw)
    if flag:
        fx, fy = FLAG
        ax.plot([fx, fx], [fy, fy + 17], color="black", lw=0.8, zorder=7)
        ax.add_patch(Polygon([[fx, fy + 17], [fx, fy + 10], [fx + 11, fy + 13.5]], fc=C["reward"], ec="none", zorder=7))
        ax.plot(fx, fy, "o", ms=2.6, color="#222222", zorder=7)
    # tee marker
    ax.add_patch(plt.Rectangle((-9, -6), 12, 12, fc="#F5F5F5", ec="#777777", lw=0.7, zorder=2))
    if golfer:
        ax.plot(TEE[0], TEE[1], "o", ms=5, color=C["agent"], mec="white", mew=0.8, zorder=8)
        ax.text(-3, 15, "you", fontsize=7.5, color=C["agent"], ha="center", va="bottom", zorder=8, fontweight="bold")
    if scale:
        y0 = -82
        ax.annotate("", xy=(300, y0), xytext=(0, y0),
                    arrowprops=dict(arrowstyle="<->", color="black", lw=0.8, shrinkA=0, shrinkB=0), zorder=6)
        ax.text(150, y0, "300 yd", fontsize=8, ha="center", va="center", color="black", zorder=7,
                bbox=dict(fc=COL["rough"], ec="none", pad=1.5))
        for xx in (0, 300):
            ax.plot([xx, xx], [y0 - 3, y0 + 3], color="black", lw=0.8, zorder=6)


if __name__ == "__main__":
    from style import save
    fig, ax = new_fig()
    draw_hole(ax, labels=True)
    save(fig, "s3-hole")
