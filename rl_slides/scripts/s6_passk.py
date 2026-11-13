"""Schematic pass@k shape: RL model wins at small k, base model catches up / overtakes at large k.
Shape only (cf. Yue et al., 2025); per-problem success rates p are drawn from a Beta distribution,
'RL' sharpens them (logit p -> a*logit p + b), pass@k = E[1-(1-p)^k]."""
import numpy as np
import matplotlib.pyplot as plt
from style import C, setup, save

setup()
rng = np.random.default_rng(0)
p_base = rng.beta(0.3, 1.0, 20000)
a, b = 1.8, 1.5
lg = np.log(p_base / (1 - p_base))
p_rl = 1 / (1 + np.exp(-(a * lg + b)))
ks = np.unique(np.round(np.logspace(0, 3, 40)).astype(int))
def passk(p):
    return np.array([np.mean(1 - (1 - p) ** k) for k in ks])
fig, ax = plt.subplots(figsize=(4.3, 2.4))
ax.plot(ks, passk(p_base), color=C["human"], label="base model")
ax.plot(ks, passk(p_rl), color=C["search"], label="after RLVR")
ax.set_xscale("log")
ax.set_xlabel("$k$ (samples per problem)")
ax.set_ylabel("pass@$k$")
ax.set_ylim(0, 1.0)
ax.set_yticks([0, 0.5, 1.0])
ax.legend(loc="lower right")
save(fig, "s6-passk")
print("pass@1", passk(p_base)[0], passk(p_rl)[0], "pass@1000", passk(p_base)[-1], passk(p_rl)[-1])
