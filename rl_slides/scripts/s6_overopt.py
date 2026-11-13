"""Schematic: proxy reward keeps rising while gold reward rises then falls (shape of Gao et al., 2023)."""
import numpy as np
import matplotlib.pyplot as plt
from style import C, setup, save

setup()
fig, ax = plt.subplots(figsize=(4.3, 2.4))
d = np.linspace(0, 1, 200)
proxy = 1.6 * d**0.8
gold = 1.6 * d - 1.5 * d**2
ax.plot(d, proxy, color=C["reward"], label="proxy reward (what the verifier says)")
ax.plot(d, gold, color=C["env"], label="true reward (what we want)")
k = np.argmax(gold)
ax.plot(d[k], gold[k], "o", color=C["env"], ms=5)
ax.annotate("true reward\npeaks, then falls", xy=(d[k], gold[k]), xytext=(0.62, 0.12),
            fontsize=8, color=C["env"], ha="left",
            arrowprops=dict(arrowstyle="-", color=C["env"], lw=1))
ax.set_xlabel("optimization pressure  $\\rightarrow$")
ax.set_ylabel("reward")
ax.set_xticks([]); ax.set_yticks([])
ax.set_xlim(0, 1); ax.set_ylim(-0.1, 1.75)
ax.legend(loc="upper left", fontsize=7.5)
save(fig, "s6-overopt")
