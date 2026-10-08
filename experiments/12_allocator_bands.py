"""Exact no-trade bands for the daily equity regime signal at the one-way cost of each asset class.
The HMM is fit on the 3,000 trading days to the end of 2004 (a refit whose belief diffusion and
utility slope sit near the median of all 186 refits); the DP is solved at each cost; switches per
year are counted by running the band policy along the real-time belief path, 1942-2025."""
import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from regimes import pomdp  # noqa: E402
from regimes.hmm_daily import GRID  # noqa: E402
from regimes.models import hmm  # noqa: E402
from regimes.sjm_daily import daily_returns  # noqa: E402

COSTS = [("E-mini S&P 500 futures", 0.16e-4), ("SPY ETF", 0.065e-4), ("10-year Treasury (interdealer)", 0.89e-4),
         ("US large-cap stocks, institutional", 8.9e-4), ("US equities, 2001-2025 schedule", 10e-4),
         ("Investment-grade corporates", 38e-4), ("High-yield corporates", 51e-4), ("IG corporates, crisis", 71e-4),
         ("US equities, 1953-75", 100e-4), ("Buyout fund stake, secondary 2025", 0.08),
         ("Venture fund stake, secondary 2025", 0.22), ("PE stake, secondary 2009", 0.456)]

d = daily_returns()
end = int(np.searchsorted(d.index, pd.Timestamp("2005-01-01")))
x = d["ex"].to_numpy()[end - 3000:end, None]
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    model, _ = hmm.fit(x, 2, restarts=5, seed=0)
resp = hmm.smoothed(model, x)
mus = np.array([[np.average(x[:, 0], weights=resp[:, s])] for s in range(2)])
covs = np.array([[[np.average((x[:, 0] - mus[s, 0]) ** 2, weights=resp[:, s])]] for s in range(2)])
A = model.transmat_
K = pomdp.belief_kernel(A, model.means_, hmm._covars(model), GRID, n_nodes=48)
acts = np.array([[0.0], [1.0]])
R = pomdp.mixture_reward(GRID, A, mus, covs, acts, 2.0)
beliefs = pd.read_csv(ROOT / "results" / "hmm_daily_beliefs_25bp.csv", index_col=0, parse_dates=True)["belief"].loc["1942":"2025"].dropna()
idx = np.clip(np.round(beliefs.to_numpy() * (len(GRID) - 1)).astype(int), 0, len(GRID) - 1)
years = len(beliefs) / 252
rows = []
for name, c in COSTS:
    sol = pomdp.solve(K, R, acts, c, beta=np.exp(-1 / (252 * 10)), grid=GRID, max_iter=200000, tol=1e-12)
    pol = sol.policy
    enter = GRID[pol[:, 0] == 1].max() if (pol[:, 0] == 1).any() else None   # buy equity when belief below this
    leave = GRID[pol[:, 1] == 0].min() if (pol[:, 1] == 0).any() else None   # sell equity when belief above this
    held, sw = 1, 0
    for i in idx:
        new = pol[i, held]
        sw += new != held
        held = new
    rows.append({"asset": name, "one_way_cost": c, "buy_equity_below": enter, "sell_equity_above": leave, "switches_per_year": sw / years})
    print(f"{name:38s} {c * 1e4:9.2f} bp  buy<{enter if enter is None else round(enter, 3)}  sell>{leave if leave is None else round(leave, 3)}  switches/yr {sw / years:5.2f}", flush=True)
myo = GRID[np.argmin(np.abs(R[:, 1] - R[:, 0]))]
(ROOT / "results" / "12_allocator_bands.json").write_text(json.dumps({"myopic_threshold": float(myo), "rows": rows}, indent=2, default=float))
print("myopic threshold", round(float(myo), 3))
