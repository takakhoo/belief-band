"""Portfolio accounting with drift-aware turnover, plus summary metrics."""
import numpy as np
import pandas as pd

ASSETS = ["stock", "bond"]  # risky sleeves; the remainder sits in cash


def run(weights, panel, cost):
    """Weights decided at row t are held over row t+1.

    `weights`: DataFrame (index ⊂ panel.index) of stock/bond weights, cash = 1 - sum.
    `cost`: one-way proportional cost charged on |change| of each risky sleeve (cash trades
    free): a scalar, or a dict {"stock": c_s, "bond": c_b} of scalars or Series indexed like panel.
    Returns a DataFrame with gross and net simple returns, turnover and weights held.
    """
    idx = weights.index
    nxt = panel.index.get_indexer(idx) + 1
    ok = nxt < len(panel)
    idx, nxt = idx[ok], nxt[ok]
    w = weights.loc[idx, ASSETS].to_numpy(float)
    r = panel[ASSETS].to_numpy(float)[nxt]
    rf = panel["cash"].to_numpy(float)[nxt]
    def _as_array(c):
        return np.full(len(idx), float(c)) if np.isscalar(c) else pd.Series(c).reindex(idx).to_numpy(float)
    costs = {"stock": cost, "bond": cost} if np.isscalar(cost) else cost
    c = np.column_stack([_as_array(costs["stock"]), _as_array(costs["bond"])])

    held = np.zeros(2)  # start from cash
    gross, net, turnover = np.empty(len(idx)), np.empty(len(idx)), np.empty(len(idx))
    for i in range(len(idx)):
        trade = np.abs(w[i] - held)
        turnover[i] = (trade.sum() + abs(w[i].sum() - held.sum())) / 2  # one-way, cash included
        port = rf[i] + w[i] @ (r[i] - rf[i])
        gross[i] = port
        net[i] = (1 - c[i] @ trade) * (1 + port) - 1
        # Drift the weights through the month for the next trade.
        val = np.append(w[i] * (1 + r[i]), (1 - w[i].sum()) * (1 + rf[i]))
        held = val[:2] / val.sum()
    out_idx = panel.index[nxt]
    return pd.DataFrame({"gross": gross, "net": net, "turnover": turnover, "rf": rf,
                         "w_stock": w[:, 0], "w_bond": w[:, 1]}, index=out_idx)


def metrics(ret, rf, gamma=5.0, periods=12):
    ret, rf = np.asarray(ret, float), np.asarray(rf, float)
    ex = ret - rf
    years = len(ret) / periods
    wealth = np.cumprod(1 + ret)
    peak = np.maximum.accumulate(np.r_[1.0, wealth])[1:]
    dd = wealth / peak - 1
    # Certainty equivalent (annualized simple) for CRRA utility of monthly gross returns.
    if gamma == 1:
        ce = np.exp(np.mean(np.log1p(ret)) * periods) - 1
    else:
        ce = (np.mean((1 + ret) ** (1 - gamma)) ** (1 / (1 - gamma))) ** periods - 1
    srt = ex[ex < 0]
    return {
        "cagr": wealth[-1] ** (1 / years) - 1,
        "vol": ex.std(ddof=1) * np.sqrt(periods),
        "sharpe": ex.mean() / ex.std(ddof=1) * np.sqrt(periods),
        "sortino": ex.mean() / np.sqrt(np.mean(np.minimum(ex, 0) ** 2)) * np.sqrt(periods) if len(srt) else np.nan,
        "max_dd": dd.min(),
        "cvar5": np.mean(np.sort(ret)[: max(1, int(0.05 * len(ret)))]),
        f"ce_g{gamma:g}": ce,
    }


def jones_schedule(index, bond_ratio=0.5):
    """One-way equity costs anchored to Jones (2002): 0.84% average 1925-2000, at least 1.00% for
    1953-1975, below 0.50% since 1991. Piecewise: 0.84% before 1953, 1.00% for 1953-1975, linear to
    0.50% by 1991, 0.30% for 1991-2000, 0.10% from 2001 (decimalization and index futures/ETFs).
    Bond costs are an assumed fraction of equity costs."""
    yr = index.year + (index.month - 1) / 12
    eq = np.select([yr < 1953, yr < 1975.42, yr < 1991, yr < 2001],
                   [0.0084, 0.0100, 0.0100 - (yr - 1975.42) / (1991 - 1975.42) * 0.005, 0.0030], 0.0010)
    eq = pd.Series(eq, index=index)
    return {"stock": eq, "bond": eq * bond_ratio}
