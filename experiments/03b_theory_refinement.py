"""Two checks of Proposition 2.
(a) Time refinement: the same continuous-time model sampled at dt = 1, 1/4, 1/16, 1/64 (signal
    separation ~ sqrt(dt), switching hazard, drift and variance ~ dt, cost per switch fixed).
    The DP half-width should converge to the cube-root law as dt -> 0.
(b) Discrete-monitoring correction: at dt = 1, delta_DP ~ delta_law - beta* s, with s the
    one-step belief standard deviation and beta* = -zeta(1/2)/sqrt(2 pi) ~ 0.5826
    (Broadie, Glasserman and Kou 1997)."""
import json
import sys
from pathlib import Path

import numpy as np
from scipy.special import zeta

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from regimes import pomdp  # noqa: E402

BETA_STAR = -zeta(0.5) / np.sqrt(2 * np.pi)
G = 1201
grid = np.linspace(0, 1, G)


def band(dt, sep1, c, hazard=0.003, mu=(0.0004, -0.0006), sig=(0.008, 0.02), gamma=2.0, horizon=2000.0):
    p = hazard * dt
    A = np.array([[1 - p, p], [p, 1 - p]])
    sep = sep1 * np.sqrt(dt)
    K = pomdp.belief_kernel(A, np.array([[sep / 2], [-sep / 2]]), np.array([[[1.0]], [[1.0]]]), grid, n_nodes=80)
    mus = np.array([[mu[0] * dt], [mu[1] * dt]])
    rcov = np.array([[[sig[0] ** 2 * dt]], [[sig[1] ** 2 * dt]]])
    actions = np.array([[0.0], [1.0]])
    R = pomdp.mixture_reward(grid, A, mus, rcov, actions, gamma)
    gain = R[:, 1] - R[:, 0]
    i = int(np.argmin(np.abs(gain)))
    g = -np.gradient(gain, grid)[i] / dt               # per unit time
    m = K @ grid
    s2 = (K @ grid ** 2 - m ** 2)[i] / dt              # belief variance per unit time
    beta = np.exp(-dt / horizon)
    sol = pomdp.solve(K, R, actions, c, beta=beta, grid=grid, max_iter=200000)
    enter = grid[sol.policy[:, 0] != 0].max()
    leave = grid[sol.policy[:, 1] != 1].min()
    law = (3 * c * s2 / (2 * g)) ** (1 / 3)
    return {"dt": dt, "sep_per_unit_time": sep1, "cost": c, "half_width_dp": (leave - enter) / 2,
            "half_width_law": law, "one_step_sd": float(np.sqrt(s2 * dt)),
            "law_minus_correction": law - BETA_STAR * np.sqrt(s2 * dt)}


rows = []
for c in (1e-4, 5e-4):
    for dt in (1.0, 0.25, 1 / 16, 1 / 64):
        r = band(dt, 0.10, c)
        rows.append(r)
        print(f"c={c:.0e} dt={dt:<7.4f} DP={r['half_width_dp']:.4f} law={r['half_width_law']:.4f} "
              f"law-0.583s={r['law_minus_correction']:.4f} ratio DP/law={r['half_width_dp'] / r['half_width_law']:.3f}", flush=True)
(ROOT / "results" / "03b_theory_refinement.json").write_text(json.dumps(rows, indent=2))
