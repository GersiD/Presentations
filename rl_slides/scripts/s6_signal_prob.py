"""P(group has a learning signal) = 1 - (1-p)^G - p^G, for several group sizes G."""
import numpy as np
import matplotlib.pyplot as plt
from style import C, setup, save

setup()
p = np.linspace(0, 1, 400)
fig, ax = plt.subplots(figsize=(4.3, 2.3))
for G, col, lw in [(4, C["human"], 1.6), (8, C["agent"], 2.4), (16, C["value"], 1.6)]:
    ax.plot(p, 1 - (1 - p) ** G - p**G, color=col, lw=lw, label=f"$G={G}$")
ps = 0.05
ax.plot([ps], [1 - (1 - ps) ** 8 - ps**8], "o", color=C["agent"], ms=5)
ax.annotate("$p=0.05$, $G=8$:\nonly 34% of groups\nteach anything", xy=(ps, 1 - (1 - ps) ** 8 - ps**8),
            xytext=(0.2, 0.3), fontsize=8, color=C["ink"], arrowprops=dict(arrowstyle="-", color=C["ink"], lw=0.8))
ax.set_xlabel("per-sample success rate $p$")
ax.set_ylabel("P(group has signal)")
ax.set_xlim(0, 1); ax.set_ylim(0, 1.02)
ax.legend(loc="lower center", fontsize=8, ncol=3, columnspacing=1.0, handlelength=1.2)
save(fig, "s6-signal-prob")
