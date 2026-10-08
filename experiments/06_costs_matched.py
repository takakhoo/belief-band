"""Jump model at 25 and 50 bp, and both the jump model and the daily HMM band under the
Jones (2002)-anchored historical cost schedule."""
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from regimes import backtest, hmm_daily as H, sjm_daily as S  # noqa: E402

WINDOWS = {"paper window 1990-2023": ("1990-01-01", "2023-12-31"),
           "pre-sample 1950-1989": ("1950-01-01", "1989-12-31"),
           "post-publication 2024-2025": ("2024-01-01", "2025-12-31"),
           "full 1942-2025": ("1942-01-01", "2025-12-31")}


def daily_jones():
    idx = S.daily_returns().index
    monthly = backtest.jones_schedule(idx)["stock"]
    return pd.Series(monthly.to_numpy(), index=idx)


def jm(cost_name):
    cost = daily_jones() if cost_name == "jones" else {"25bp": 0.0025, "50bp": 0.005}[cost_name]
    df, _ = S.run(cost=cost, cache=ROOT / "results" / "sjm_cache")
    df.to_csv(ROOT / "results" / f"sjm_daily_{cost_name}.csv")
    return f"JM {cost_name}", {w: S.summarize(df, a, b) for w, (a, b) in WINDOWS.items()}


def band(cost_name):
    df, beliefs, tables = H.run(cost=daily_jones())
    df.to_csv(ROOT / "results" / "hmm_daily_jones.csv")
    tables.to_csv(ROOT / "results" / "hmm_daily_bands_jones.csv", index=False)
    return "HMM jones", {w: H.summarize(df, a, b) for w, (a, b) in WINDOWS.items()}


def task(arg):
    kind, name = arg
    return jm(name) if kind == "jm" else band(name)


if __name__ == "__main__":
    out = {}
    with ProcessPoolExecutor(max_workers=4) as ex:
        for tag, res in ex.map(task, [("jm", "25bp"), ("jm", "50bp"), ("jm", "jones"), ("band", "jones")]):
            out[tag] = res
            for w, r in res.items():
                print(f"{tag:10s} {w:28s} " + " | ".join(f"{k} " + (f"SR {v['sharpe']:.2f} DD {v['max_dd']:.2f}" if isinstance(v, dict) else f"{v:.2f}") for k, v in r.items()), flush=True)
    (ROOT / "results" / "06_costs_matched.json").write_text(json.dumps(out, indent=2, default=float))
