"""Daily statistical-jump-model protocol of Shu, Yu and Mulvey (2024), applied to CRSP value-weighted
US equities since 1926.

Protocol as published: features are the EWM downside deviation (10-day halflife) and EWM Sortino
ratios (20- and 60-day halflives) of daily excess returns; the model is refit every six months on a
rolling 3,000-day window; each month the jump penalty is the candidate whose 0/1 strategy had the
highest Sharpe over the preceding eight years; positions are 100% equity or 100% T-bills, entered
with a one-day delay, at 10 bp one-way.
"""
from pathlib import Path

import numpy as np
import pandas as pd

from .data import _french
from .models import jump

# The grid in Table 3 of the paper, on its scale (loss = 0.5 * squared distance).
LAMBDAS = (0.0, 5.0, 15.0, 35.0, 70.0, 150.0)


MARKETS = {"US": "F-F_Research_Data_Factors_daily.csv",
           "DevExUS": "Developed_ex_US_3_Factors_Daily.csv",
           "Developed": "Developed_3_Factors_Daily.csv",
           "Europe": "Europe_3_Factors_Daily.csv",
           "Japan": "Japan_3_Factors_Daily.csv",
           "AsiaPacExJapan": "Asia_Pacific_ex_Japan_3_Factors_Daily.csv",
           "NorthAmerica": "North_America_3_Factors_Daily.csv"}


def daily_returns(market="US"):
    d = _french(MARKETS[market], daily=True)
    return pd.DataFrame({"ex": d["Mkt-RF"], "rf": d["RF"]})


def features(ex):
    out = {}
    neg = np.minimum(ex, 0.0) ** 2
    for hl in (10, 20, 60):
        dd = np.sqrt(neg.ewm(halflife=hl).mean())
        if hl == 10:
            out["dd10"] = dd  # Table 2 of the paper: downside deviation in levels
        else:
            out[f"sortino{hl}"] = ex.ewm(halflife=hl).mean() / dd
    return pd.DataFrame(out).replace([np.inf, -np.inf], np.nan)


def bull_state(path, ex_train):
    """As in the reference code (sort_by="cumret"): the state with the higher in-sample cumulative return."""
    return int(np.argmax([ex_train[path == s].sum() if np.any(path == s) else -np.inf for s in (0, 1)]))


def label_series(feats, lam, first_test, ex=None, refit_days=126, window=3000, seed=0):
    """Online bull(1)/bear(0) labels from first_test onward for one penalty (paper scale)."""
    X = feats.to_numpy()
    exv = np.asarray(ex, float)
    n = len(X)
    labels = np.full(n, np.nan)
    t0 = first_test
    while t0 < n:
        lo = max(0, t0 - window)
        train = X[lo:t0]
        # Reference preprocessing: clip at +-3 training std, then standardize on the clipped data.
        mu, sd = np.nanmean(train, 0), np.nanstd(train, 0)
        lo_b, hi_b = mu - 3 * sd, mu + 3 * sd
        clipped = np.clip(train, lo_b, hi_b)
        cm, cs = clipped.mean(0), clipped.std(0)
        z = (np.clip(X[lo: min(n, t0 + refit_days)], lo_b, hi_b) - cm) / cs
        # Our objective uses the full squared distance; the paper's uses half, so double lambda.
        theta, path = jump.fit(z[: t0 - lo], k=2, lam=2 * lam, n_init=10, seed=seed)
        states = jump.online_states(z, theta, 2 * lam, start=t0 - lo)
        bull = bull_state(path, exv[lo:t0])
        seg = states[t0 - lo:]
        labels[t0: t0 + len(seg)] = (seg == bull).astype(float)
        t0 += refit_days
    return labels


def strategy_returns(ex, rf, signal, cost=0.001, delay=1):
    """Signal known at close of day t; position held from day t+1+delay onward."""
    pos = pd.Series(signal, index=ex.index).shift(1 + delay)
    pos = pos.fillna(0.0)
    trades = pos.diff().abs().fillna(pos.abs())
    c = cost if np.isscalar(cost) else pd.Series(cost).reindex(ex.index)
    ret = rf + pos * ex - c * trades
    return ret, pos


def run(cost=0.001, delay=1, start="1934-01-01", val_years=8, lambdas=LAMBDAS, cache=None, market="US"):
    d = daily_returns(market)
    feats = features(d["ex"]).dropna()
    d = d.loc[feats.index]
    first = int(np.searchsorted(feats.index, pd.Timestamp(start)))
    first = max(first, 3000)
    cand = {}
    for lam in lambdas:
        path = None if cache is None else Path(cache) / f"labels_lam{lam:g}.npy"
        if path is not None and path.exists():
            cand[lam] = np.load(path)
            continue
        cand[lam] = label_series(feats, lam, first, d["ex"])
        if path is not None:
            np.save(path, cand[lam])
    # Each candidate's 0/1 strategy, computed causally, for the validation choice.
    cand_ret = {lam: strategy_returns(d["ex"], d["rf"], np.nan_to_num(lab), cost, delay)[0] for lam, lab in cand.items()}
    months = d.index.to_period("M")
    chosen = pd.Series(np.nan, index=d.index)
    signal = pd.Series(np.nan, index=d.index)
    val = int(val_years * 252)
    month_starts = np.flatnonzero(np.r_[True, months[1:] != months[:-1]])
    for i, ms in enumerate(month_starts):
        if ms - val < first:
            continue
        me = month_starts[i + 1] if i + 1 < len(month_starts) else len(d)
        best, best_sr = None, -np.inf
        for lam, r in cand_ret.items():
            ex_r = (r.iloc[ms - val: ms] - d["rf"].iloc[ms - val: ms]).to_numpy()
            sr = ex_r.mean() / ex_r.std() if ex_r.std() > 0 else -np.inf
            if sr > best_sr:
                best, best_sr = lam, sr
        chosen.iloc[ms:me] = best
        signal.iloc[ms:me] = cand[best][ms:me]
    live = signal.notna()
    ret, pos = strategy_returns(d["ex"], d["rf"], signal.fillna(1.0).where(live, 1.0), cost, delay)
    out = pd.DataFrame({"jm": ret, "pos": pos, "bh": d["rf"] + d["ex"], "rf": d["rf"], "lam": chosen, "signal": signal})
    return out.loc[live[live].index[0]:], cand


def summarize(df, a, b):
    seg = df.loc[a:b]
    res = {}
    for col in ("jm", "bh"):
        ex = seg[col] - seg["rf"]
        wealth = (1 + seg[col]).cumprod()
        dd = wealth / wealth.cummax() - 1
        res[col] = {"sharpe": ex.mean() / ex.std() * np.sqrt(252), "max_dd": dd.min(),
                    "cagr": wealth.iloc[-1] ** (252 / len(seg)) - 1}
    res["time_in_market"] = seg["pos"].mean()
    res["switches_per_year"] = seg["pos"].diff().abs().sum() / (len(seg) / 252)
    return res
