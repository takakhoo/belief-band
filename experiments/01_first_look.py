"""First pass: baselines and the default HMM under three information sets."""
import sys
import time
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from regimes import backtest, engine  # noqa: E402
from regimes.data import build_panel  # noqa: E402

START = "1946-12-31"
COST = 0.001

panel = build_panel()
strategies = {
    "60/40": engine.static(panel, START, 0.6, 0.4),
    "100% stock": engine.static(panel, START, 1.0, 0.0),
    "Unconditional MV": engine.unconditional_mv(panel, START),
    "Vol-managed": engine.vol_managed(panel, START),
    "Trend 10m": engine.trend(panel, START),
    "TSMOM 12m": engine.tsmom(panel, START),
    "Risk parity": engine.risk_parity(panel, START),
}
for mode in ["full_smoothed", "full_filtered", "realtime"]:
    for feats in ["rv_term_def", "returns"]:
        t = time.time()
        s = engine.HMMStrategy(features=feats, k=2, policy="myopic", mode=mode)
        strategies[f"{s.name} {mode}"] = engine.walk_forward(panel, s, START)
        print(f"{s.name} {mode}: {time.time() - t:.1f}s", flush=True)

rows = {}
for name, w in strategies.items():
    res = backtest.run(w, panel, COST)
    m = backtest.metrics(res["net"], res["rf"])
    m["turnover/yr"] = res["turnover"].mean() * 12
    m["avg stock"] = res["w_stock"].mean()
    rows[name] = m
table = pd.DataFrame(rows).T
pd.set_option("display.width", 200)
print(table.round(3))
Path(__file__).resolve().parents[1].joinpath("results").mkdir(exist_ok=True)
table.to_csv(Path(__file__).resolve().parents[1] / "results" / "01_first_look.csv")
