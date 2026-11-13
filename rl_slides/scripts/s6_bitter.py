"""Schematic: bitter-lesson curves (same look as s0-bitter-curve) with an 'RLVR?' marker between them."""
import numpy as np
import matplotlib.pyplot as plt
from style import C, setup, save

setup()
x = np.linspace(0, 1, 400)
human = 0.62 * (1 - np.exp(-9 * x)) + 0.06
search = 0.02 + 0.98 * (np.log1p(6 * x) / np.log1p(6)) * (0.25 + 0.75 * x)

fig, ax = plt.subplots(figsize=(4.3, 2.1))
ax.plot(x, human, color=C["human"], lw=2.6)
ax.plot(x, search, color=C["search"], lw=2.6)
ax.text(0.3, human[-1] + 0.05, "human knowledge", color=C["ink"], ha="left", va="bottom", fontsize=9, fontweight="bold")
ax.text(0.97, search[-1] + 0.03, "search + learning", color=C["ink"], ha="right", va="bottom", fontsize=9, fontweight="bold")
# ambiguous marker: halfway between the two curves
xm = 0.28
ym = 0.5 * (np.interp(xm, x, human) + np.interp(xm, x, search))
ax.text(xm, ym + 0.03, "RLVR ?", ha="center", va="center", fontsize=10, fontweight="bold", color=C["ink"], zorder=6,
        bbox=dict(boxstyle="round,pad=0.28", fc="white", ec=C["ink"], lw=1.6))
ax.set_xlim(0, 1.0)
ax.set_ylim(0, 1.3)
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlabel("compute  (time, data, search)  " + r"$\rightarrow$")
ax.set_ylabel("performance  " + r"$\rightarrow$")
save(fig, "s6-bitter")
