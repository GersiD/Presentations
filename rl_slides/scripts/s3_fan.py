"""Fan of many possible shots from the tee (illustrative)."""
import numpy as np

from s3_hole import TEE, draw_hole, new_fig
from style import C, save

rng = np.random.default_rng(3)
# 14 clubs, maximum carry in yards (illustrative)
CLUBS = np.linspace(260, 70, 14)

fig, ax = new_fig()
draw_hole(ax, labels=False)
n = 130
for _ in range(n):
    club = rng.choice(CLUBS)
    strength = rng.uniform(0.6, 1.0)
    theta = np.deg2rad(rng.uniform(-24, 24))
    dist = club * strength
    land = TEE + dist * np.array([np.cos(theta), np.sin(theta)]) + rng.normal(0, 0.05 * dist, 2)
    # slightly curved flight path (quadratic bezier in the plane)
    mid = (TEE + land) / 2 + rng.normal(0, 0.05 * dist) * np.array([0, 1])
    t = np.linspace(0, 1, 30)[:, None]
    path = (1 - t) ** 2 * TEE + 2 * (1 - t) * t * mid + t**2 * land
    ax.plot(path[:, 0], path[:, 1], color=C["agent"], lw=0.5, alpha=0.28, zorder=5)
    ax.plot(*land, "o", ms=2.2, color=C["agent"], alpha=0.8, mew=0, zorder=6)
save(fig, "s3-fan")
