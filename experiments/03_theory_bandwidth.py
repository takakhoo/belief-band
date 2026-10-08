"""Check the asymptotic no-trade law against exact belief-space DP.

Two regimes with a weakly informative signal each period (so the belief moves almost
diffusively), equity-or-cash actions, proportional cost c per switch. Proposition 2 predicts
the hysteresis half-width delta = (3 c s^2 / (2 g))^(1/3), where s^2 is the per-period
variance of the belief increment at the myopic indifference point and g is the slope of the
utility gain of equity over cash in the belief.
"""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from regimes import pomdp  # noqa: E402

G = 801
grid = np.linspace(0, 1, G)
p_switch = 0.003
A = np.array([[1 - p_switch, p_switch], [p_switch, 1 - p_switch]])
rows = []
for sep in (0.10, 0.20):
    means = np.array([[sep / 2], [-sep / 2]])
    covs = np.array([[[1.0]], [[1.0]]])
    K = pomdp.belief_kernel(A, means, covs, grid, n_nodes=64)
    mus = np.array([[0.0004], [-0.0006]])          # daily excess return in the good and bad regimes
    rcov = np.array([[[0.008 ** 2]], [[0.02 ** 2]]])
    actions = np.array([[0.0], [1.0]])
    R = pomdp.mixture_reward(grid, A, mus, rcov, actions, gamma=2.0)
    gain = R[:, 1] - R[:, 0]
    i_star = int(np.argmin(np.abs(gain)))
    b_star = grid[i_star]
    g = -np.gradient(gain, grid)[i_star]          # gain falls as P(bad) rises
    mean_next = K @ grid
    s2 = (K @ grid ** 2 - mean_next ** 2)[i_star]  # one-period belief variance at b*
    for c in (1e-5, 2e-5, 5e-5, 1e-4, 2e-4, 5e-4, 1e-3):
        sol = pomdp.solve(K, R, actions, c, beta=0.9995, grid=grid)
        keep_cash = sol.policy[:, 0] == 0
        keep_eq = sol.policy[:, 1] == 1
        enter = grid[~keep_cash].max() if (~keep_cash).any() else np.nan   # buy equity below this P(bad)
        leave = grid[~keep_eq].min() if (~keep_eq).any() else np.nan       # sell equity above this P(bad)
        delta = (leave - enter) / 2
        pred = (3 * c * s2 / (2 * g)) ** (1 / 3)
        rows.append({"signal_sep": sep, "cost": c, "b_star": b_star, "enter_below": enter, "leave_above": leave,
                     "half_width_dp": delta, "half_width_law": pred, "ratio": delta / pred})
        print(f"sep={sep:.2f} c={c:.0e} b*={b_star:.3f} band=[{enter:.3f},{leave:.3f}] "
              f"half-width DP={delta:.4f} law={pred:.4f} ratio={delta / pred:.2f}", flush=True)
(ROOT / "results").mkdir(exist_ok=True)
(ROOT / "results" / "03_theory_bandwidth.json").write_text(json.dumps(rows, indent=2))
for sep in (0.10, 0.20):
    sub = [r for r in rows if r["signal_sep"] == sep and np.isfinite(r["half_width_dp"]) and r["half_width_dp"] > 0]
    slope = np.polyfit(np.log([r["cost"] for r in sub]), np.log([r["half_width_dp"] for r in sub]), 1)[0]
    print(f"sep={sep}: fitted log-log slope of DP half-width on cost = {slope:.3f} (law: 1/3)")
