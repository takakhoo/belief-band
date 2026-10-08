"""Daily two-state Gaussian HMM on equity excess returns (the benchmark of Shu, Yu and Mulvey 2024),
executed three ways: myopic (switch on the filtered belief), and the cost-aware belief-space
policy of Proposition 2 solved by exact dynamic programming. Same rolling 3,000-day window,
six-month refits, one-day delay and cost as the jump-model protocol."""
import warnings

import numpy as np
import pandas as pd

from . import pomdp
from .models import hmm
from .sjm_daily import daily_returns

GRID = np.linspace(0, 1, 401)


def run(cost=0.001, delay=1, start="1934-01-01", actions=(0.0, 1.0), gamma=2.0, horizon_years=10.0,
        refit_days=126, window=3000, restarts=5, seed=0, market="US"):
    d = daily_returns(market)
    ex, rf = d["ex"].to_numpy(), d["rf"].to_numpy()
    n = len(d)
    first = max(int(np.searchsorted(d.index, pd.Timestamp(start))), window)
    acts = np.array(actions, float)[:, None]
    beta = np.exp(-1 / (252 * horizon_years))
    belief = np.full(n, np.nan)
    pol_myopic = np.full(n, np.nan)
    pol_band = np.full(n, np.nan)
    tables = []
    t0 = first
    held = 0
    while t0 < n:
        lo = max(0, t0 - window)
        x = ex[lo:t0, None]
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            model, _ = hmm.fit(x, 2, restarts=restarts, seed=seed, covariance="full")
        resp = hmm.smoothed(model, x)
        mus = np.array([[np.average(ex[lo:t0], weights=resp[:, s])] for s in range(2)])
        covs = np.array([[[np.average((ex[lo:t0] - mus[s, 0]) ** 2, weights=resp[:, s])]] for s in range(2)])
        A = model.transmat_
        K = pomdp.belief_kernel(A, model.means_, hmm._covars(model), GRID, n_nodes=48)
        R = pomdp.mixture_reward(GRID, A, mus, covs, acts, gamma)
        c_now = float(cost) if np.isscalar(cost) else float(cost.iloc[t0])
        sol = pomdp.solve(K, R, acts, c_now, beta=beta, grid=GRID, max_iter=100000, tol=1e-12)
        hi = min(n, t0 + refit_days)
        post = hmm.filtered(model, ex[lo:hi, None])[:, 1]
        for t in range(t0, hi):
            b = post[t - lo]
            belief[t] = b
            i = int(round(b * (len(GRID) - 1)))
            pol_myopic[t] = acts[R[i].argmax(), 0]
            held = sol.policy[i, held]
            pol_band[t] = acts[held, 0]
        enter = GRID[sol.policy[:, 0] != 0].max() if (sol.policy[:, 0] != 0).any() else np.nan
        leave = GRID[sol.policy[:, -1] != len(acts) - 1].min() if (sol.policy[:, -1] != len(acts) - 1).any() else np.nan
        gain = R[:, -1] - R[:, 0]
        i_star = int(np.argmin(np.abs(gain)))
        m1 = K @ GRID
        s2 = float((K @ GRID ** 2 - m1 ** 2)[i_star])          # one-step belief variance at b*
        g = float(-np.gradient(gain, GRID)[i_star])               # utility slope in the belief
        kcost = c_now * abs(acts[-1, 0] - acts[0, 0])
        law = (3 * kcost * s2 / (2 * g)) ** (1 / 3) if g > 0 else np.nan
        tables.append({"date": d.index[t0], "enter_below": enter, "leave_above": leave,
                       "myopic_threshold": GRID[i_star], "s2": s2, "g": g, "cost": c_now,
                       "law_half_width": law, "law_corrected": law - 0.5826 * np.sqrt(s2),
                       "p_stay_calm": A[0, 0], "p_stay_turbulent": A[1, 1]})
        t0 = hi
    out = pd.DataFrame({"belief": belief, "myopic": pol_myopic, "band": pol_band}, index=d.index)
    res = {}
    for name in ("myopic", "band"):
        pos = out[name].shift(1 + delay).fillna(0.0)
        trades = pos.diff().abs().fillna(pos.abs())
        c_series = cost if np.isscalar(cost) else cost.reindex(d.index)
        res[name] = d["rf"] + pos * d["ex"] - c_series * trades
        res[name + "_pos"] = pos
    res["bh"] = d["rf"] + d["ex"]
    res["rf"] = d["rf"]
    frame = pd.DataFrame(res).loc[d.index[first]:]
    return frame, out.loc[d.index[first]:], pd.DataFrame(tables)


def summarize(df, a, b, cols=("myopic", "band", "bh")):
    seg = df.loc[a:b]
    out = {}
    for col in cols:
        ex = seg[col] - seg["rf"]
        wealth = (1 + seg[col]).cumprod()
        out[col] = {"sharpe": ex.mean() / ex.std() * np.sqrt(252),
                    "max_dd": (wealth / wealth.cummax() - 1).min(),
                    "cagr": wealth.iloc[-1] ** (252 / len(seg)) - 1}
        if col + "_pos" in seg:
            out[col]["switches_per_year"] = seg[col + "_pos"].diff().abs().sum() / (len(seg) / 252)
            out[col]["time_in_market"] = seg[col + "_pos"].mean()
    return out
