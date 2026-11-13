"""Advantages for a group of G=8 samples: all wrong (no signal) vs one correct."""
import numpy as np
import matplotlib.pyplot as plt
from style import C, setup, save

setup()
G = 8

def adv(r):
    r = np.asarray(r, float)
    return (r - r.mean()) / (r.std() + 1e-8)

cases = [("all 8 wrong", np.zeros(G)), ("1 of 8 correct", np.eye(G)[3])]
fig, axes = plt.subplots(1, 2, figsize=(4.3, 2.0), sharey=True)
for ax, (title, r) in zip(axes, cases):
    a = adv(r)
    x = np.arange(G)
    cols = [C["env"] if v > 0 else C["reward"] for v in a]
    ax.bar(x, a, color=cols, width=0.7)
    ax.axhline(0, color=C["ink"], lw=0.8)
    ax.set_ylim(-1.2, 3.2)
    ax.set_xticks(x)
    ax.set_xticklabels([r"$\checkmark$" if v else r"$\times$" for v in r], fontsize=10)
    for t, v in zip(ax.get_xticklabels(), r):
        t.set_color(C["env"] if v else C["reward"])
    ax.set_title(title, fontsize=8.5)
    ax.spines["bottom"].set_visible(False)
    ax.tick_params(axis="x", length=0, pad=2)
axes[0].set_ylabel("advantage $A_i$")
axes[0].text(3.5, 0.45, "$A_i = 0$ for all", ha="center", fontsize=8, color=C["reward"])
fig.tight_layout(w_pad=0.8)
save(fig, "s6-zero-adv")
