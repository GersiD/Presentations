"""Value V(s) = -(expected strokes to hole out) over the hole, shown as value boxes on the plain course. Illustrative."""
from s3_hole import draw_hole, new_fig, value_fn
from style import C, save

fig, ax = new_fig()
# plain course; value shown only as labelled boxes at a few telling spots
draw_hole(ax, scale=False, golfer=True, base=True, outlines_only=False, labels=False)


def tag(x, y, dx=0, dy=0):
    v = float(value_fn(x, y))
    ax.text(x + dx, y + dy, f"{v:.1f}".replace("-", "\u2212"), fontsize=8, ha="center", va="center", zorder=10,
            color=C["ink"], fontweight="bold", bbox=dict(fc="white", ec=C["ink"], lw=0.6, pad=1.5, boxstyle="round,pad=0.25"))


tag(0, 0, 0, 14)           # tee
tag(110, 0)                # mid fairway
tag(180, 0)                # just short of the pond
tag(225, 0)                # water
tag(262, 0)                # past the pond
tag(300, 0, 29, 0)         # hole
tag(130, 45)               # bunker
tag(110, -70)              # rough

save(fig, "s3-value")
