"""Paper figures. Each figure reads only saved results."""
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.dates  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
R, F = ROOT / "results", ROOT / "figures"
F.mkdir(exist_ok=True)
plt.rcParams.update({"font.family": "serif", "font.size": 8, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.linewidth": 0.6, "xtick.major.width": 0.6, "ytick.major.width": 0.6, "legend.frameon": False,
                     "savefig.bbox": "tight", "savefig.dpi": 300})
COL = {"Buy and hold": "#7a7a7a", "Myopic HMM": "#c0392b", "Belief band": "#1f5fa8", "Jump model": "#d68910"}


def save(fig, name):
    fig.savefig(F / f"{name}.pdf")
    fig.savefig(F / f"{name}.png")
    plt.close(fig)


def hero():
    hm = pd.read_csv(R / "hmm_daily_jones.csv", index_col=0, parse_dates=True).loc["1942":"2025"]
    jm = pd.read_csv(R / "sjm_daily_jones.csv", index_col=0, parse_dates=True).loc["1942":"2025"]
    df = pd.DataFrame({"Buy and hold": hm["bh"], "Myopic HMM": hm["myopic"], "Belief band": hm["band"], "Jump model": jm["jm"]}).dropna()
    w = (1 + df).cumprod()
    fig, (a, b) = plt.subplots(2, 1, figsize=(7.0, 3.6), sharex=True, gridspec_kw={"height_ratios": [2.2, 1]})
    for k in ["Buy and hold", "Jump model", "Belief band", "Myopic HMM"]:
        a.plot(w.index, w[k], color=COL[k], lw=1.1 if k == "Belief band" else 0.8, label=k)
        b.plot(w.index, w[k] / w[k].cummax() - 1, color=COL[k], lw=0.6)
    a.set_yscale("log")
    a.set_ylabel("Growth of $1 (log)")
    a.legend(ncol=4, loc="upper left", fontsize=7)
    b.set_ylabel("Drawdown")
    b.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
    a.set_title("US equities, daily, real time, one-day delay, historical one-way costs (Jones 2002 anchors)", fontsize=8, loc="left")
    save(fig, "fig1_wealth_jones")


def theory():
    rows = json.loads((R / "03_theory_bandwidth.json").read_text())
    ref = json.loads((R / "03b_theory_refinement.json").read_text())
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.0, 2.5))
    for sep, mk in ((0.10, "o"), (0.20, "s")):
        sub = [r for r in rows if r["signal_sep"] == sep]
        c = np.array([r["cost"] for r in sub])
        a.loglog(c, [r["half_width_dp"] for r in sub], mk, ms=3.5, color="#1f5fa8", label=f"exact DP, signal {sep:.2f}")
        a.loglog(c, [r["half_width_law"] for r in sub], "-", lw=0.8, color="#7a7a7a", label="cube-root law" if sep == 0.10 else None)
    a.set_xlabel("Cost per switch $c$")
    a.set_ylabel(r"Band half-width $\delta$ (belief)")
    a.legend(fontsize=6.5)
    for c, mk in ((1e-4, "o"), (5e-4, "s")):
        sub = [r for r in ref if r["cost"] == c]
        dt = np.array([r["dt"] for r in sub])
        b.semilogx(dt, [r["half_width_dp"] / r["half_width_law"] for r in sub], mk + "-", ms=3.5, lw=0.8, color="#1f5fa8", label=f"DP / law, $c$={c:g}")
        b.semilogx(dt, [r["law_minus_correction"] / r["half_width_law"] for r in sub], mk + "--", ms=3, lw=0.8, color="#d68910",
                   label=r"(law $-\,0.583\,s\sqrt{\Delta t}$) / law" if c == 1e-4 else None)
    b.axhline(1, color="#7a7a7a", lw=0.6)
    b.set_xlabel(r"Decision interval $\Delta t$")
    b.set_ylabel("Ratio to continuous-time law")
    b.invert_xaxis()
    b.legend(fontsize=6.5)
    save(fig, "fig2_theory")


def sharpe_vs_cost():
    t = pd.read_csv(R / "08_daily_table.csv")
    t = t[t.era == "1942-2025"]
    order = ["5bp", "10bp", "25bp", "50bp", "jones"]
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.0, 2.4))
    for k in COL:
        s = t[t.strategy == k].set_index("cost").reindex(order)
        a.plot(range(len(order)), s["Sharpe"], "o-", ms=3, lw=0.9, color=COL[k], label=k)
        b.plot(range(len(order)), s["MaxDD"], "o-", ms=3, lw=0.9, color=COL[k])
    for ax in (a, b):
        ax.set_xticks(range(len(order)), ["5 bp", "10 bp", "25 bp", "50 bp", "Jones\nhistorical"])
    a.set_ylabel("Sharpe ratio, 1942-2025")
    b.set_ylabel("Maximum drawdown")
    b.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
    a.legend(fontsize=6.5)
    save(fig, "fig3_cost_curves")


def zooms():
    b = pd.read_csv(R / "hmm_daily_beliefs_25bp.csv", index_col=0, parse_dates=True)
    hm = pd.read_csv(R / "hmm_daily_25bp.csv", index_col=0, parse_dates=True)
    bands = pd.read_csv(R / "hmm_daily_bands_25bp.csv", parse_dates=["date"]).set_index("date")
    fig, axes = plt.subplots(2, 2, figsize=(7.0, 3.2), sharey="row")
    for j, (a0, a1, title) in enumerate((("2007-06", "2010-06", "2007-2010"), ("2019-10", "2021-03", "2019-2021"))):
        seg = b.loc[a0:a1]
        ax = axes[0, j]
        ax.plot(seg.index, seg["belief"], color="#555", lw=0.5, label="P(turbulent | data)")
        bd = bands.reindex(seg.index, method="ffill")
        ax.fill_between(seg.index, bd["enter_below"], bd["leave_above"], color="#1f5fa8", alpha=0.18, lw=0, label="no-trade band")
        ax.plot(seg.index, bd["myopic_threshold"], color="#c0392b", lw=0.6, ls="--", label="myopic threshold")
        ax.set_title(title, fontsize=8, loc="left")
        if j == 0:
            ax.set_ylabel("Belief")
            h, l = ax.get_legend_handles_labels()
            fig.legend(h, l, fontsize=6.5, loc="upper center", ncol=3, bbox_to_anchor=(0.5, 1.04))
        ax2 = axes[1, j]
        ax2.step(seg.index, hm.loc[a0:a1, "myopic_pos"].reindex(seg.index), color="#c0392b", lw=0.5, where="post", label="myopic")
        ax2.step(seg.index, hm.loc[a0:a1, "band_pos"].reindex(seg.index) * 0.94 + 0.03, color="#1f5fa8", lw=0.9, where="post", label="band")
        ax2.set_yticks([0, 1], ["T-bills", "equity"])
        if j == 0:
            ax2.set_ylabel("Position held")
            ax2.legend(fontsize=6, loc="center right", bbox_to_anchor=(1.0, 0.5))
        for axx in (ax, ax2):
            axx.xaxis.set_major_locator(matplotlib.dates.YearLocator())
            axx.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%Y"))
            axx.tick_params(axis="x", labelsize=6.5)
    save(fig, "fig4_zooms")


def eras():
    t = pd.read_csv(R / "08_daily_table.csv")
    t = t[t.cost == "jones"]
    eras = ["1950-1989 (pre-sample)", "1990-2023 (paper window)", "2024-2025 (post-publication)", "1942-2025"]
    fig, ax = plt.subplots(figsize=(7.0, 2.2))
    width = 0.2
    for i, k in enumerate(["Buy and hold", "Jump model", "Belief band", "Myopic HMM"]):
        vals = [t[(t.era == e) & (t.strategy == k)]["Sharpe"].squeeze() if len(t[(t.era == e) & (t.strategy == k)]) else np.nan for e in eras]
        ax.bar(np.arange(len(eras)) + (i - 1.5) * width, vals, width, color=COL[k], label=k)
    ax.axhline(0, color="#333", lw=0.5)
    ax.set_xticks(range(len(eras)), ["1950-1989\npre-sample", "1990-2023\npaper window", "2024-2025\npost-publication", "1942-2025\nfull period"])
    ax.set_ylabel("Sharpe ratio")
    ax.legend(ncol=4, fontsize=6.5, loc="lower center", bbox_to_anchor=(0.5, 1.0))
    save(fig, "fig6_eras")


if __name__ == "__main__":
    for fn in (hero, theory, sharpe_vs_cost, zooms, eras):
        try:
            fn()
            print("ok", fn.__name__)
        except Exception as e:  # keep going so partial results still plot
            print("skip", fn.__name__, type(e).__name__, e)
