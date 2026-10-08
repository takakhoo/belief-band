"""Daily HMM, myopic vs cost-aware belief band, across eras and costs."""
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from regimes import hmm_daily as H  # noqa: E402

WINDOWS = {"paper window 1990-2023": ("1990-01-01", "2023-12-31"),
           "pre-sample 1950-1989": ("1950-01-01", "1989-12-31"),
           "post-publication 2024-2025": ("2024-01-01", "2025-12-31"),
           "full 1942-2025": ("1942-01-01", "2025-12-31")}


def one(cost):
    df, beliefs, tables = H.run(cost=cost)
    tag = f"{cost * 1e4:g}bp"
    df.to_csv(ROOT / "results" / f"hmm_daily_{tag}.csv")
    beliefs.to_csv(ROOT / "results" / f"hmm_daily_beliefs_{tag}.csv")
    tables.to_csv(ROOT / "results" / f"hmm_daily_bands_{tag}.csv", index=False)
    return tag, {w: H.summarize(df, a, b) for w, (a, b) in WINDOWS.items()}


if __name__ == "__main__":
    out = {}
    with ProcessPoolExecutor(max_workers=4) as ex:
        for tag, res in ex.map(one, (0.0005, 0.001, 0.0025, 0.005)):
            out[tag] = res
            for w, r in res.items():
                print(f"{tag:6s} {w:28s} " + " | ".join(
                    f"{k} SR {v['sharpe']:.2f} DD {v['max_dd']:.2f}" + (f" sw/yr {v['switches_per_year']:.1f}" if 'switches_per_year' in v else "")
                    for k, v in r.items()), flush=True)
    (ROOT / "results" / "04_hmm_daily_band.json").write_text(json.dumps(out, indent=2, default=float))
