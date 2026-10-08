"""Monthly grid: look-ahead ladder, distribution of real-time configurations, deflated Sharpe,
bootstrap comparisons with 60/40, and the ladder figure."""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy import stats as st  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from regimes import stats  # noqa: E402

R = ROOT / "results"
m = pd.read_csv(R / "main" / "metrics.csv", index_col=[0, 1])
net = pd.read_csv(R / "main" / "net_returns.csv", header=[0, 1], index_col=0, parse_dates=True)
panel = pd.read_csv(R / "main" / "panel_eval.csv", index_col=0, parse_dates=True)
rf = panel["cash"].shift(-1).reindex(net.index) if False else None
out = {}
for cost in ("flat10", "jones"):
    t = m.loc[cost]
    rt = t[t.index.str.startswith("HMM") & ~t.index.str.contains("full_")]
    n = net[cost]
    rf = pd.Series(panel["cash"].to_numpy(), index=panel.index).reindex(n.index)
    srs = rt["sharpe"].to_numpy()
    best = rt["sharpe"].idxmax()
    r_best = n[best].dropna()
    ex = (r_best - rf.reindex(r_best.index)).to_numpy()
    dsr, sr0 = stats.deflated_sharpe(rt.loc[best, "sharpe"], srs, len(ex), st.skew(ex), st.kurtosis(ex, fisher=False))
    comp = stats.compare(n[best].dropna(), n["60/40"].reindex(n[best].dropna().index), rf.reindex(n[best].dropna().index), n_boot=5000)
    ladder = {k: {v: float(t.loc[k2, "sharpe"]) for v, k2 in (("smoothed, full-sample fit", f"HMM[{k},K=2,myopic] full_smoothed"),
                                                              ("filtered, full-sample fit", f"HMM[{k},K=2,myopic] full_filtered"),
                                                              ("real time", f"HMM[{k},K=2,myopic]"))} for k in ("returns", "rv_term_def")}
    out[cost] = {"n_realtime_configs": len(rt), "sharpe_min": float(srs.min()), "sharpe_median": float(np.median(srs)),
                 "sharpe_max": float(srs.max()), "best": best, "best_minus_6040_sharpe": comp["sharpe"]["diff"],
                 "p_best_vs_6040": comp["sharpe"]["p"], "deflated_sharpe_prob": dsr, "sr0_expected_max_under_null": sr0,
                 "beats_6040": int((srs > t.loc["60/40", "sharpe"]).sum()), "sharpe_6040": float(t.loc["60/40", "sharpe"]),
                 "band_vs_myopic": {f: [float(t.loc[f"HMM[{f},K=2,band]", "sharpe"]), float(t.loc[f"HMM[{f},K=2,myopic]", "sharpe"])]
                                    for f in ("rv", "rv_term", "rv_term_def", "macro4", "returns")},
                 "ladder": ladder}
(R / "11_monthly_analysis.json").write_text(json.dumps(out, indent=2, default=float))
print(json.dumps(out, indent=1, default=lambda x: round(float(x), 3)))

t = m.loc["flat10"]
fig, ax = plt.subplots(figsize=(3.4, 2.3))
steps = ["smoothed, full-sample fit", "filtered, full-sample fit", "real time"]
for k, col, lab in (("returns", "#c0392b", "HMM on returns"), ("rv_term_def", "#1f5fa8", "HMM on vol, term, default")):
    ax.plot(range(3), [out["flat10"]["ladder"][k][s] for s in steps], "o-", color=col, ms=3.5, lw=1, label=lab)
for name, ls in (("60/40", "--"), ("TSMOM 12m", ":")):
    ax.axhline(t.loc[name, "sharpe"], color="#555", lw=0.7, ls=ls)
    ax.text(2.05, t.loc[name, "sharpe"], name, fontsize=6.5, va="center")
ax.set_xticks(range(3), ["smoothed\n(two-sided)", "filtered,\nfull-sample fit", "real time"], fontsize=7)
ax.set_ylabel("Sharpe ratio, 1947-2025", fontsize=7.5)
ax.set_xlim(-0.2, 2.6)
ax.legend(fontsize=6.5, frameon=False)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
fig.savefig(ROOT / "figures" / "fig5_ladder.pdf", bbox_inches="tight")
fig.savefig(ROOT / "figures" / "fig5_ladder.png", bbox_inches="tight", dpi=300)
