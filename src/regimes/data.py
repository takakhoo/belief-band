"""Monthly panel, July 1926 onward, with every column dated by when it was knowable.

Convention: row t is month-end t. Return columns are the realized return over
month t. Signal columns are what an investor could see at the close of month t,
so a decision made at row t earns row t+1's returns.
"""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"


def _french(name, daily=False):
    path = RAW / "french" / name
    lines = path.read_text(errors="ignore").splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith(",") and "Mkt-RF" in line or line.startswith(",Mom") or line.startswith(",WML"))
    header = [h.strip() for h in lines[start].split(",")]
    rows = []
    width = 8 if daily else 6
    for line in lines[start + 1:]:
        parts = [p.strip() for p in line.split(",")]
        if not parts[0].isdigit() or len(parts[0]) != width:
            if rows:
                break
            continue
        rows.append(parts)
    frame = pd.DataFrame(rows, columns=["date"] + header[1:]).set_index("date").astype(float) / 100
    fmt = "%Y%m%d" if daily else "%Y%m"
    frame.index = pd.to_datetime(frame.index, format=fmt)
    if not daily:
        frame.index = frame.index + pd.offsets.MonthEnd(0)
    return frame


def _goyal():
    frame = pd.read_excel(RAW / "goyal" / "GW2008_PredictorData_updated_2025.xlsx", sheet_name="Monthly")
    frame.index = pd.to_datetime(frame.pop("yyyymm").astype(int).astype(str), format="%Y%m") + pd.offsets.MonthEnd(0)
    return frame.apply(pd.to_numeric, errors="coerce")


def _fred(series):
    frame = pd.read_csv(RAW / "fred" / f"{series}.csv")
    frame.columns = ["date", series]
    frame["date"] = pd.to_datetime(frame["date"])
    return frame.set_index("date")[series].apply(pd.to_numeric, errors="coerce")


def build_panel():
    factors = _french("F-F_Research_Data_Factors.csv")
    daily = _french("F-F_Research_Data_Factors_daily.csv", daily=True)
    goyal = _goyal()

    panel = pd.DataFrame(index=factors.index)
    # Returns realized during month t (simple, decimal).
    panel["stock"] = factors["Mkt-RF"] + factors["RF"]
    panel["cash"] = factors["RF"]
    panel["bond"] = goyal["ltr"]
    panel["corp"] = goyal["corpr"]

    # Realized variance from daily returns inside month t: observable at its close.
    mkt = daily["Mkt-RF"] + daily["RF"]
    rv = (mkt ** 2).groupby(mkt.index.to_period("M")).sum()
    rv.index = rv.index.to_timestamp("M")
    panel["rv"] = rv.reindex(panel.index)
    neg = (mkt.clip(upper=0) ** 2).groupby(mkt.index.to_period("M")).sum()
    neg.index = neg.index.to_timestamp("M")
    panel["rv_down"] = neg.reindex(panel.index)

    # Rates and spreads are monthly averages of daily quotes, all known by the month's close.
    panel["tbl"] = goyal["tbl"]
    panel["lty"] = goyal["lty"]
    panel["term"] = goyal["lty"] - goyal["tbl"]
    panel["default"] = goyal["BAA"] - goyal["AAA"]
    # CPI for month t is released in the middle of month t+1: lag one month.
    panel["infl_lag"] = goyal["infl"].shift(1)
    # Dividends and earnings are reported with a delay; lag a quarter for safety.
    panel["log_dp"] = (np.log(goyal["D12"]) - np.log(goyal["Index"])).shift(3)
    panel["log_ep"] = (np.log(goyal["E12"]) - np.log(goyal["Index"])).shift(3)

    usrec = _fred("USREC")
    usrec.index = usrec.index + pd.offsets.MonthEnd(0)
    panel["nber"] = usrec.reindex(panel.index)  # Ex-post dating: evaluation only, never a signal.
    vix = _fred("VIXCLS").resample("ME").last()
    panel["vix"] = vix.reindex(panel.index)

    panel = panel.loc[: goyal["ltr"].last_valid_index()]
    return panel


if __name__ == "__main__":
    p = build_panel()
    print(p.describe().T[["count", "mean", "std", "min", "max"]])
    print(p.index[0], p.index[-1], len(p))
    print(p.isna().sum())
