"""Shared matplotlib style for every generated figure in the deck.

Usage (from any script in scripts/):
    from style import C, setup, save
    setup()
    fig, ax = plt.subplots(figsize=(4.2, 2.6))
    ...
    save(fig, "my-figure")   # -> imgs/gen/my-figure.pdf

Run scripts with: ../gd-answers/assignment3/.venv/bin/python scripts/<name>.py  (from rl_slides/)
Colors mirror the \\colorlet{...} names in preamble.tex (dvipsnames values).
"""

import logging
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent.parent / "imgs" / "gen"

C = {
    "agent": "#006EB8",   # NavyBlue
    "env": "#009B55",     # ForestGreen
    "reward": "#B6321C",  # BrickRed
    "value": "#92268F",   # Plum
    "human": "#949698",   # Gray
    "search": "#006EB8",  # NavyBlue (same as agent; no orange in the deck)
    "ink": "#333333",
    "grid": "#E6E6E6",
}


CMU = "/usr/local/texlive/2026/texmf-dist/fonts/opentype/public/cm-unicode/"


def setup():
    # Computer Modern Sans = the Beamer body font, so figures match the slide text.
    from matplotlib import font_manager as fm
    for name in ("matplotlib.font_manager", "fontTools", "matplotlib.backends.backend_pdf"):
        logging.getLogger(name).setLevel(logging.ERROR)
    for f in ("cmunss.otf", "cmunsx.otf", "cmunsi.otf"):
        try:
            fm.fontManager.addfont(CMU + f)
        except Exception:
            pass
    mpl.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["CMU Sans Serif", "Helvetica", "DejaVu Sans"],
        "mathtext.fontset": "cm",  # professionalfonts keeps math in CM serif
        "axes.unicode_minus": True,
        "font.size": 9,
        "axes.titlesize": 9,
        "axes.labelsize": 9,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "legend.fontsize": 8,
        "legend.frameon": False,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.edgecolor": C["ink"],
        "axes.labelcolor": C["ink"],
        "xtick.color": C["ink"],
        "ytick.color": C["ink"],
        "axes.grid": False,
        "lines.linewidth": 2.0,
        "savefig.transparent": True,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.02,
        "pdf.fonttype": 42,
    })


def save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"{name}.pdf")
    plt.close(fig)
    print(f"wrote {OUT / name}.pdf")
