"""Group-relative advantages for the 8 rollouts of the running example (17 x 24 = 408)."""
import numpy as np
import matplotlib.pyplot as plt
from style import C, setup, save

setup()
# trajectories tau_1..tau_8 -> final answers (same list as sections/05-grpo.tex)
answers = [418, 408, 398, 428, 408, 418, 408, 388]
r = np.array([1.0 if a == 408 else 0.0 for a in answers])
A = (r - r.mean()) / r.std()   # population std (np default)

fig, ax = plt.subplots(figsize=(4.3, 1.9))
x = np.arange(len(r))
cols = [C["agent"] if a > 0 else C["reward"] for a in A]
ax.bar(x, A, width=0.62, color=cols)
ax.axhline(0, color=C["ink"], lw=1.0)
for xi, a in zip(x, A):
    ax.text(xi, a + (0.08 if a > 0 else -0.08), f"{a:+.2f}", ha="center",
            va="bottom" if a > 0 else "top", fontsize=8, color=C["ink"])
ax.set_xticks(x)
ax.set_xticklabels([f"$\\tau_{{{i+1}}}$\n$r={int(v)}$" for i, v in enumerate(r)])
ax.tick_params(axis="x", length=0)
ax.set_ylabel(r"advantage $\hat{A}_i$")
ax.set_ylim(-1.2, 2.0)
ax.text(7.45, 1.8, "zero = group mean", ha="right", va="center",
        fontsize=7.5, color=C["value"])
save(fig, "s4-advantage")
