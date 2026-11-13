"""Schematic: performance vs compute for human-knowledge methods vs search/learning (Sutton's bitter lesson).

Writes two PDFs with identical geometry so they can be swapped with \\only<..>:
  s0-bitter-curve-human.pdf  (human-knowledge curve only; other curve drawn with alpha=0 to keep the bbox)
  s0-bitter-curve.pdf        (both curves)
"""
import numpy as np
import matplotlib.pyplot as plt

from style import C, setup, save

setup()
x = np.linspace(0, 1, 400)
human = 0.62 * (1 - np.exp(-9 * x)) + 0.06            # fast rise, then plateau
search = 0.02 + 0.98 * (np.log1p(6 * x) / np.log1p(6)) * (0.25 + 0.75 * x)
# crossover
i = np.argmax(search > human)


def draw(both):
    fig, ax = plt.subplots(figsize=(4.3, 2.5))
    ax.plot(x, human, color=C["human"], lw=2.6)
    a = 1.0 if both else 0.0
    ax.plot(x, search, color=C["search"], lw=2.6, alpha=a)
    ax.text(0.3, human[-1] + 0.05, "human knowledge", color=C["ink"], ha="left", va="bottom", fontsize=9, fontweight="bold")
    ax.text(0.97, search[-1] + 0.03, "search + learning", color=C["search"], ha="right", va="bottom", fontsize=9,
            fontweight="bold", alpha=a)
    ax.plot([x[i]], [human[i]], "o", color=C["ink"], ms=4, alpha=a)
    ax.annotate("overtakes", (x[i], human[i]), (x[i] + 0.06, human[i] - 0.38), fontsize=8, color=C["ink"], alpha=a,
                arrowprops=dict(arrowstyle="-", color=C["ink"], lw=0.8, alpha=a), ha="center")
    ax.set_xlim(0, 1.0)
    ax.set_ylim(0, 1.3)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("compute  (time, data, search)  " + r"$\rightarrow$")
    ax.set_ylabel("performance  " + r"$\rightarrow$")
    return fig


save(draw(False), "s0-bitter-curve-human")
save(draw(True), "s0-bitter-curve")
