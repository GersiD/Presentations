"""Illustrative before/after next-token distribution at the answer position."""
import numpy as np
import matplotlib.pyplot as plt
from style import C, setup, save

setup()
labels = ["408", "418", "398", "428", "other"]
before = np.array([0.375, 0.25, 0.15, 0.10, 0.125])
after = np.array([0.50, 0.19, 0.11, 0.07, 0.13])
good = [True, False, False, False, False]

fig, ax = plt.subplots(figsize=(4.3, 2.0))
x = np.arange(len(labels))
w = 0.36
ax.bar(x - w / 2, before, w, color=C["human"], alpha=0.45, label="before")
for i in range(len(x)):
    ax.bar(x[i] + w / 2, after[i], w, color=C["agent"] if good[i] else C["reward"])
ax.set_xticks(x)
ax.set_xticklabels(labels, family="monospace")
ax.set_xlabel("final answer token")
ax.set_ylabel(r"$\pi_\theta$(answer | prompt)")
ax.set_ylim(0, 0.62)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=C["human"], alpha=0.45, label="before"),
                   Patch(color=C["agent"], label="after, correct (A>0)"),
                   Patch(color=C["reward"], label="after, wrong (A<0)")],
          loc="upper right", handlelength=1.0, fontsize=7.5)
save(fig, "s4-prob-shift")
