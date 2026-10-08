"""Compact JSON for the interactive explorer (takakhoo.com and GitHub Pages)."""
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / "results"
OUT = ROOT / "site" / "data"
OUT.mkdir(parents=True, exist_ok=True)
COSTS = {"5bp": "5 bp", "10bp": "10 bp", "25bp": "25 bp", "50bp": "50 bp", "jones": "Historical"}
JM = {"10bp": "sjm_daily_cost10bp.csv", "25bp": "sjm_daily_25bp.csv", "50bp": "sjm_daily_50bp.csv", "jones": "sjm_daily_jones.csv"}


def r4(x):
    return [None if not np.isfinite(v) else float(f"{v:.4g}") for v in np.asarray(x, float)]


def stats(daily_ret, rf):
    m = (1 + daily_ret).groupby(daily_ret.index.to_period("M")).prod() - 1
    f = (1 + rf).groupby(rf.index.to_period("M")).prod() - 1
    ex = m - f
    w = (1 + m).cumprod()
    return {"sharpe": round(float(ex.mean() / ex.std() * np.sqrt(12)), 3), "cagr": round(float(w.iloc[-1] ** (12 / len(m)) - 1), 4),
            "maxdd": round(float((w / w.cummax() - 1).min()), 3)}


wealth = {}
months = None
for key, label in COSTS.items():
    hm = pd.read_csv(R / f"hmm_daily_{key}.csv", index_col=0, parse_dates=True).loc["1943":"2025"]
    df = pd.DataFrame({"band": hm["band"], "myopic": hm["myopic"], "bh": hm["bh"]})
    if key in JM:
        df["jm"] = pd.read_csv(R / JM[key], index_col=0, parse_dates=True)["jm"].reindex(df.index)
    df = df.dropna()
    w = (1 + df).cumprod().resample("ME").last()
    dd = ((1 + df).cumprod() / (1 + df).cumprod().cummax() - 1).resample("ME").min()
    months = [d.strftime("%Y-%m") for d in w.index]
    wealth[key] = {"label": label, "wealth": {c: r4(w[c]) for c in w}, "drawdown": {c: r4(dd[c]) for c in dd},
                   "stats": {c: stats(df[c], hm["rf"].reindex(df.index)) for c in df},
                   "switches": {c: round(float(hm[f"{c}_pos"].loc[df.index].diff().abs().sum() / (len(df) / 252)), 1) for c in ("band", "myopic")}}
json.dump({"months": months, "costs": wealth}, open(OUT / "wealth.json", "w"), separators=(",", ":"))

zooms = {}
for key in ("25bp", "jones"):
    b = pd.read_csv(R / "hmm_daily_beliefs_25bp.csv", index_col=0, parse_dates=True)  # beliefs do not depend on cost
    hm = pd.read_csv(R / f"hmm_daily_{key}.csv", index_col=0, parse_dates=True)
    bands = pd.read_csv(R / f"hmm_daily_bands_{key}.csv", parse_dates=["date"]).set_index("date")
    for name, (a, z) in {"2008": ("2007-06-01", "2010-06-30"), "2020": ("2019-10-01", "2021-03-31")}.items():
        seg = b.loc[a:z]
        bd = bands.reindex(seg.index, method="ffill")
        zooms[f"{key}_{name}"] = {"dates": [d.strftime("%Y-%m-%d") for d in seg.index], "belief": r4(seg["belief"]),
                                  "lo": r4(bd["enter_below"]), "hi": r4(bd["leave_above"]), "myopic_threshold": r4(bd["myopic_threshold"]),
                                  "pos_myopic": hm["myopic_pos"].reindex(seg.index).astype(int).tolist(),
                                  "pos_band": hm["band_pos"].reindex(seg.index).astype(int).tolist(),
                                  "price": r4((1 + hm["bh"].reindex(seg.index)).cumprod())}
json.dump(zooms, open(OUT / "zooms.json", "w"), separators=(",", ":"))

monthly = json.loads((R / "11_monthly_analysis.json").read_text())
intl = json.loads((R / "07_international.json").read_text())
alloc = json.loads((R / "12_allocator_bands.json").read_text())
theory = {"bandwidth": json.loads((R / "03_theory_bandwidth.json").read_text()),
          "refinement": json.loads((R / "03b_theory_refinement.json").read_text())}
daily = pd.read_csv(R / "08_daily_table.csv")
eras = daily[daily.cost == "jones"][["era", "strategy", "Sharpe", "MaxDD"]].round(3).to_dict(orient="records")
json.dump({"ladder": monthly["flat10"]["ladder"], "grid": {k: v for k, v in monthly["flat10"].items() if k != "ladder"},
           "intl": intl, "alloc": alloc, "theory": theory, "eras": eras}, open(OUT / "summary.json", "w"), indent=1, default=float)
for f in OUT.iterdir():
    print(f.name, f.stat().st_size // 1024, "KB")
