"""Robustness of the daily belief band: position grid, planning horizon, risk aversion. Each
variant is run at 25 bp and under the Jones schedule; all variants are reported."""
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from regimes import backtest, hmm_daily as H, sjm_daily as S  # noqa: E402

VARIANTS = {
    "base (0/1, H=10y, g=2)": dict(),
    "5 levels": dict(actions=(0.0, 0.25, 0.5, 0.75, 1.0)),
    "H=2y": dict(horizon_years=2.0),
    "H=30y": dict(horizon_years=30.0),
    "gamma=5": dict(gamma=5.0),
    "5 levels, gamma=5": dict(actions=(0.0, 0.25, 0.5, 0.75, 1.0), gamma=5.0),
}


def jones_daily():
    idx = S.daily_returns().index
    return pd.Series(backtest.jones_schedule(idx)["stock"].to_numpy(), index=idx)


def one(arg):
    name, cost_name = arg
    cost = jones_daily() if cost_name == "jones" else 0.0025
    df, beliefs, tables = H.run(cost=cost, **VARIANTS[name])
    tag = name.replace(" ", "_").replace(",", "").replace("(", "").replace(")", "").replace("/", "-").replace("=", "")
    df.to_csv(ROOT / "results" / f"robust_{tag}_{cost_name}.csv")
    tables.to_csv(ROOT / "results" / f"robust_bands_{tag}_{cost_name}.csv", index=False)
    return name, cost_name, H.summarize(df, "1942-01-01", "2025-12-31")


if __name__ == "__main__":
    out = {}
    with ProcessPoolExecutor(max_workers=4) as ex:
        for name, cost_name, r in ex.map(one, [(v, c) for v in VARIANTS for c in ("25bp", "jones")]):
            out[f"{name} | {cost_name}"] = r
            print(f"{name:26s} {cost_name:6s} band SR {r['band']['sharpe']:.2f} DD {r['band']['max_dd']:.2f} sw/yr {r['band']['switches_per_year']:.1f} | myopic SR {r['myopic']['sharpe']:.2f} | bh {r['bh']['sharpe']:.2f}", flush=True)
    (ROOT / "results" / "09_robustness.json").write_text(json.dumps(out, indent=2, default=float))
