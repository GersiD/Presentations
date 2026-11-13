"""Number of action sequences = (actions per shot)^(shots). Illustrative numbers."""
import matplotlib.pyplot as plt
import numpy as np

from style import C, save, setup

setup()
A = 14 * 30 * 20  # 8400, illustrative
n = np.arange(0, 26)
logv = n * np.log10(A)

fig, ax = plt.subplots(figsize=(4.3, 2.3))
ax.plot(n, logv, color=C["agent"], lw=1.8)
ax.axhline(80, color="black", lw=1.0, ls="--")
ax.text(0.3, 83, r"atoms in the universe $\approx 10^{80}$", color="black", fontsize=8.5, va="bottom")
ax.plot([4], [4 * np.log10(A)], "o", color=C["reward"], ms=6, zorder=5)
ax.annotate("one hole (4 shots)\n" + r"$\approx 5\times10^{15}$", xy=(4, 4 * np.log10(A)), xytext=(7.5, 8),
            fontsize=8.5, color=C["reward"], arrowprops=dict(arrowstyle="-", color=C["reward"], lw=0.8))
ax.tick_params(colors="black")
ax.xaxis.label.set_color("black"); ax.yaxis.label.set_color("black")
ax.set_xlim(0, 25)
ax.set_ylim(0, 100)
ax.set_xlabel("shots played")
ax.set_ylabel("possible shot sequences")
ax.set_yticks([0, 20, 40, 60, 80, 100])
ax.set_yticklabels(["1", r"$10^{20}$", r"$10^{40}$", r"$10^{60}$", r"$10^{80}$", r"$10^{100}$"])
save(fig, "s3-explosion")
