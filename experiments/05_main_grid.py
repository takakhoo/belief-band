"""Main monthly study, 1947-2025, strictly real time. Saves every strategy's weights and net returns
under a flat 10 bp cost and under the Jones (2002)-anchored historical schedule."""
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from regimes import backtest, engine  # noqa: E402
from regimes.data import build_panel  # noqa: E402

START = "1946-12-31"
OUT = ROOT / "results" / "main"
OUT.mkdir(parents=True, exist_ok=True)
PANEL = build_panel()
COSTS = {"flat10": 0.001, "jones": backtest.jones_schedule(PANEL.index)}


def configs():
    for feats in ("rv", "rv_term", "rv_term_def", "macro4", "returns"):
        for k in (2, 3, "bic"):
            for policy in ("myopic", "switch"):
                yield dict(features=feats, k=k, policy=policy)
        for cost_name in COSTS:
            yield dict(features=feats, k=2, policy="band", cost_name=cost_name)
    for feats in ("rv_term_def", "returns"):
        for mode in ("full_smoothed", "full_filtered"):
            yield dict(features=feats, k=2, policy="myopic", mode=mode)


def label(c):
    tag = f"HMM[{c['features']},K={c['k']},{c['policy']}"
    if c.get("cost_name"):
        tag += f",{c['cost_name']}"
    tag += "]"
    if c.get("mode"):
        tag += " " + c["mode"]
    return tag


def run_one(c):
    c = dict(c)
    cost_name = c.pop("cost_name", None)
    name = label({**c, "cost_name": cost_name})
    cache = OUT / "cache" / (name.replace("/", "_").replace(" ", "_") + ".csv")
    if cache.exists():
        return name, pd.read_csv(cache, index_col=0, parse_dates=True)
    strat = engine.HMMStrategy(**c, cost=COSTS[cost_name] if cost_name else 0.001)
    w = engine.walk_forward(PANEL, strat, START)
    cache.parent.mkdir(exist_ok=True)
    w.to_csv(cache)
    return name, w


def baselines():
    return {
        "60/40": engine.static(PANEL, START, 0.6, 0.4),
        "100% stock": engine.static(PANEL, START, 1.0, 0.0),
        "Unconditional MV": engine.unconditional_mv(PANEL, START),
        "Vol-managed": engine.vol_managed(PANEL, START),
        "Trend 10m (cash)": engine.trend(PANEL, START),
        "Trend 10m (bonds)": engine.trend(PANEL, START, defensive="bond"),
        "TSMOM 12m": engine.tsmom(PANEL, START),
        "Risk parity": engine.risk_parity(PANEL, START),
    }


def jump_monthly():
    """Month-end label of the daily jump model (penalty chosen in real time) -> next month."""
    sjm = pd.read_csv(ROOT / "results" / "sjm_daily_cost10bp.csv", index_col=0, parse_dates=True)
    sig = sjm["signal"].dropna().resample("ME").last()
    sig = sig.reindex(PANEL.loc[START:].index[:-1]).ffill()
    return {
        "JM (equity/cash)": pd.DataFrame({"stock": sig, "bond": 0.0}),
        "JM (60/40 or cash)": pd.DataFrame({"stock": 0.6 * sig, "bond": 0.4 * sig}),
    }


if __name__ == "__main__":
    weights = baselines()
    weights.update(jump_monthly())
    with ProcessPoolExecutor(max_workers=8) as ex:
        for name, w in ex.map(run_one, list(configs())):
            weights[name] = w
            print("done", name, flush=True)
    rows, nets = {}, {}
    for cost_name, cost in COSTS.items():
        for name, w in weights.items():
            if "band" in name and cost_name not in name:
                continue
            w = w.dropna()
            res = backtest.run(w, PANEL, cost)
            m = backtest.metrics(res["net"], res["rf"])
            m["turnover_yr"] = res["turnover"].mean() * 12
            m["avg_stock"] = res["w_stock"].mean()
            rows[(cost_name, name.replace(",flat10", "").replace(",jones", ""))] = m
            nets[(cost_name, name.replace(",flat10", "").replace(",jones", ""))] = res["net"]
    table = pd.DataFrame(rows).T
    table.index.names = ["cost", "strategy"]
    table.to_csv(OUT / "metrics.csv")
    pd.DataFrame(nets).to_csv(OUT / "net_returns.csv")
    pd.concat({k: v for k, v in weights.items()}, axis=1).to_csv(OUT / "weights.csv")
    PANEL.loc[START:, ["cash", "stock", "bond", "nber"]].to_csv(OUT / "panel_eval.csv")
    pd.set_option("display.width", 250)
    for cost_name in COSTS:
        print("\n==", cost_name)
        print(table.loc[cost_name].sort_values("ce_g5", ascending=False).round(3).to_string())
