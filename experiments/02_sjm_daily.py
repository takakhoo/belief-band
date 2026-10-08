"""Statistical jump model, daily, published protocol: replicate 1990-2023, then test 1950-1989 and 2024-2025."""
import json
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from regimes import sjm_daily as S  # noqa: E402

CACHE = ROOT / "results" / "sjm_cache"
CACHE.mkdir(parents=True, exist_ok=True)
START = "1934-01-01"


def one(lam):
    path = CACHE / f"labels_lam{lam:g}.npy"
    if path.exists():
        return lam, "cached"
    d = S.daily_returns()
    feats = S.features(d["ex"]).dropna()
    first = max(int(np.searchsorted(feats.index, np.datetime64(START))), 3000)
    t = time.time()
    np.save(path, S.label_series(feats, lam, first, d.loc[feats.index, "ex"]))
    return lam, f"{time.time() - t:.0f}s"


if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=10) as ex:
        for lam, msg in ex.map(one, S.LAMBDAS):
            print(f"lambda={lam:g}: {msg}", flush=True)
    out = {}
    for cost in (0.001, 0.0):
        df, _ = S.run(cost=cost, start=START, cache=CACHE)
        df.to_csv(ROOT / "results" / f"sjm_daily_cost{int(cost * 1e4)}bp.csv")
        out[f"{cost * 1e4:g}bp"] = {name: S.summarize(df, a, b) for name, (a, b) in {
            "paper window 1990-2023": ("1990-01-01", "2023-12-31"),
            "pre-sample 1950-1989": ("1950-01-01", "1989-12-31"),
            "post-publication 2024-2025": ("2024-01-01", "2025-12-31"),
            "full 1942-2025": ("1942-01-01", "2025-12-31"),
        }.items()}
    (ROOT / "results" / "02_sjm_daily.json").write_text(json.dumps(out, indent=2, default=float))
    print(json.dumps(out, indent=2, default=lambda x: round(float(x), 3)))
