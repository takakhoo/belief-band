"""Tables for the daily study: belief band vs myopic HMM vs jump model vs buy-and-hold, across costs
and eras, with stationary-bootstrap tests on monthly-compounded returns and spanning regressions."""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from regimes import stats  # noqa: E402
from regimes.data import build_panel  # noqa: E402

R = ROOT / "results"
ERAS = {"1942-2025": ("1942-01-01", "2025-12-31"), "1950-1989 (pre-sample)": ("1950-01-01", "1989-12-31"),
        "1990-2023 (paper window)": ("1990-01-01", "2023-12-31"), "2024-2025 (post-publication)": ("2024-01-01", "2025-12-31")}
COSTS = {"5bp": "5bp", "10bp": "10bp", "25bp": "25bp", "50bp": "50bp", "jones": "jones"}


def monthly(daily):
    return (1 + daily).groupby(daily.index.to_period("M")).prod() - 1


def load(cost):
    hm = pd.read_csv(R / f"hmm_daily_{cost}.csv", index_col=0, parse_dates=True)
    jm_file = {"10bp": "sjm_daily_cost10bp.csv", "5bp": None}.get(cost, f"sjm_daily_{cost}.csv")
    df = pd.DataFrame({"Belief band": hm["band"], "Myopic HMM": hm["myopic"], "Buy and hold": hm["bh"], "rf": hm["rf"]})
    if jm_file and (R / jm_file).exists():
        jm = pd.read_csv(R / jm_file, index_col=0, parse_dates=True)
        df["Jump model"] = jm["jm"].reindex(df.index)
    pos = {"Belief band": hm["band_pos"], "Myopic HMM": hm["myopic_pos"]}
    return df, pos


def summary(m, rf):
    ex = m - rf
    w = (1 + m).cumprod()
    out = {"Sharpe": ex.mean() / ex.std() * np.sqrt(12), "CAGR": w.iloc[-1] ** (12 / len(m)) - 1,
           "MaxDD": (w / w.cummax() - 1).min()}
    for g in (2, 5, 10):
        out[f"CE{g}"] = float(stats.ce(m.to_numpy(), g))
    return out


if __name__ == "__main__":
    tables, tests = {}, {}
    for cost in COSTS:
        if not (R / f"hmm_daily_{cost}.csv").exists():
            continue
        df, pos = load(cost)
        for era, (a, b) in ERAS.items():
            seg = df.loc[a:b].dropna(axis=1, how="all").dropna()
            mon = seg.apply(monthly)
            rf = mon.pop("rf")
            tables[(cost, era)] = {k: summary(mon[k], rf) for k in mon}
            for k, p in pos.items():
                ps = p.loc[a:b]
                tables[(cost, era)][k]["switches/yr"] = float(ps.diff().abs().sum() / (len(ps) / 252))
            comp = {}
            for other in [c for c in mon.columns if c != "Belief band"]:
                comp[other] = stats.compare(mon["Belief band"], mon[other], rf, n_boot=5000, mean_block=12)
            tests[(cost, era)] = comp
    rows = []
    for (cost, era), strategies in tables.items():
        for name, m in strategies.items():
            row = {"cost": cost, "era": era, "strategy": name, **m}
            if name != "Belief band":
                t = tests[(cost, era)][name]
                row.update({"band_minus_this_sharpe": t["sharpe"]["diff"], "p_sharpe": t["sharpe"]["p"],
                            "band_minus_this_ce5": t["ce"]["diff"], "p_ce5": t["ce"]["p"]})
            rows.append(row)
    out = pd.DataFrame(rows)
    out.to_csv(R / "08_daily_table.csv", index=False)
    pd.set_option("display.width", 250)
    for era in ERAS:
        print(f"\n=== {era}")
        sub = out[out.era == era].set_index(["cost", "strategy"])
        print(sub[["Sharpe", "CE5", "CE10", "MaxDD", "switches/yr", "band_minus_this_sharpe", "p_sharpe", "band_minus_this_ce5", "p_ce5"]].round(3).to_string())

    # Spanning: does the band's monthly excess return have alpha beyond the market, a vol-managed
    # market and a 10-month trend rule (all built in real time on the same data)?
    panel = build_panel()
    df, _ = load("10bp")
    mon = df.loc["1942-01-01":"2025-12-31"].dropna().apply(monthly)
    mon.index = mon.index.to_timestamp("M")
    rf = mon["rf"]
    main = pd.read_csv(R / "main" / "net_returns.csv", header=[0, 1], index_col=0, parse_dates=True) if (R / "main" / "net_returns.csv").exists() else None
    fac = pd.DataFrame({"MKT": mon["Buy and hold"] - rf})
    if main is not None:
        for col, name in ((("flat10", "Vol-managed"), "VOL"), (("flat10", "Trend 10m (cash)"), "TREND")):
            if col in main.columns:
                fac[name] = main[col].reindex(fac.index) - panel["cash"].reindex(fac.index)
    span = {k: stats.spanning(mon[k] - rf, fac.dropna()) for k in ("Belief band", "Jump model", "Myopic HMM") if k in mon}
    (R / "08_spanning.json").write_text(json.dumps(span, indent=2, default=float))
    for k, v in span.items():
        print(f"spanning {k}: alpha {v['alpha_ann']:.4f}/yr t={v['t_alpha']:.2f} R2={v['r2']:.2f} betas {{{', '.join(f'{a}: {b:.2f}' for a, b in v['betas'].items())}}}")
