"""Real numbers from Shao et al. 2025 (Spurious Rewards): Qwen2.5-Math-7B, MATH-500, GRPO."""
import matplotlib.pyplot as plt
from style import C, setup, save

setup()
fig, axes = plt.subplots(1, 2, figsize=(4.3, 2.3), gridspec_kw=dict(width_ratios=[1.15, 1]))
ax = axes[0]
labels = ["ground-truth\nreward", "random\nreward"]
vals = [29.1, 21.4]
bars = ax.bar(labels, vals, color=[C["env"], C["reward"]], width=0.6)
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.8, f"+{v}", ha="center", fontsize=9, color=C["ink"])
ax.set_ylim(0, 36)
ax.set_ylabel("MATH-500 gain (pts)")
ax.tick_params(axis="x", labelsize=7.5)
ax = axes[1]
bars = ax.bar(["before", "after"], [65, 90], color=[C["human"], C["search"]], width=0.6)
for b, t in zip(bars, ["~65%", ">90%"]):
    ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 2, t, ha="center", fontsize=9, color=C["ink"])
ax.set_ylim(0, 110)
ax.set_ylabel("responses with\n“code reasoning” (%)")
ax.set_title("under spurious rewards", fontsize=7.5, color=C["ink"])
fig.tight_layout(w_pad=1.5)
save(fig, "s6-spurious")
