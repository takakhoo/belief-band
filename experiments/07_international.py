"""Jump model (published protocol) vs daily HMM with myopic and belief-band execution on four
non-US developed markets (Fama-French/Bloomberg daily market returns in USD, 1990-2026).
Common evaluation window: the first date at which the jump model's eight-year validation is
available, through August 2026."""
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from regimes import hmm_daily as H, sjm_daily as S  # noqa: E402

MARKETS = ("Europe", "Japan", "AsiaPacExJapan", "DevExUS")
COSTS = (0.001, 0.0025)


def one(arg):
    market, cost = arg
    cache = ROOT / "results" / f"sjm_cache_{market}"
    cache.mkdir(exist_ok=True)
    jm, _ = S.run(cost=cost, start="1990-01-01", cache=cache, market=market)
    hm, _, _ = H.run(cost=cost, start="1990-01-01", market=market)
    a, b = jm.index[0], jm.index[-1]
    tag = f"{market}_{cost * 1e4:g}bp"
    jm.to_csv(ROOT / "results" / f"intl_jm_{tag}.csv")
    hm.to_csv(ROOT / "results" / f"intl_hmm_{tag}.csv")
    res = {"window": [str(a.date()), str(b.date())], "jm": S.summarize(jm, a, b)["jm"]}
    res.update(H.summarize(hm, a, b))
    return tag, res


if __name__ == "__main__":
    out = {}
    with ProcessPoolExecutor(max_workers=4) as ex:
        for tag, r in ex.map(one, [(m, c) for m in MARKETS for c in COSTS]):
            out[tag] = r
            print(f"{tag:22s} {r['window']} JM SR {r['jm']['sharpe']:.2f} DD {r['jm']['max_dd']:.2f} | myopic SR {r['myopic']['sharpe']:.2f} DD {r['myopic']['max_dd']:.2f} | band SR {r['band']['sharpe']:.2f} DD {r['band']['max_dd']:.2f} | B&H SR {r['bh']['sharpe']:.2f} DD {r['bh']['max_dd']:.2f}", flush=True)
    (ROOT / "results" / "07_international.json").write_text(json.dumps(out, indent=2, default=float))
