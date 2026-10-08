"""Inference for strategy comparisons: stationary block bootstrap, deflated Sharpe ratio,
and spanning regressions with Newey-West errors."""
import numpy as np
import pandas as pd
from scipy import stats as st


def stationary_bootstrap_indices(n, mean_block, n_boot, seed=0):
    """Politis and Romano (1994) stationary bootstrap index paths."""
    rng = np.random.default_rng(seed)
    p = 1.0 / mean_block
    idx = np.empty((n_boot, n), dtype=np.int64)
    idx[:, 0] = rng.integers(n, size=n_boot)
    restart = rng.random((n_boot, n)) < p
    fresh = rng.integers(n, size=(n_boot, n))
    for t in range(1, n):
        idx[:, t] = np.where(restart[:, t], fresh[:, t], (idx[:, t - 1] + 1) % n)
    return idx


def sharpe(ex, periods=12):
    return ex.mean(-1) / ex.std(-1, ddof=1) * np.sqrt(periods)


def ce(ret, gamma=5.0, periods=12):
    return np.mean((1 + ret) ** (1 - gamma), axis=-1) ** (periods / (1 - gamma)) - 1


def compare(ret_a, ret_b, rf, n_boot=10000, mean_block=12, seed=0, gamma=5.0):
    """Difference A - B in Sharpe and CRRA certainty equivalent, with a two-sided bootstrap
    p-value computed by recentering the bootstrap distribution at zero."""
    a, b, r = (np.asarray(x, float) for x in (ret_a, ret_b, rf))
    idx = stationary_bootstrap_indices(len(a), mean_block, n_boot, seed)
    out = {}
    for name, fn in (("sharpe", lambda x, f: sharpe(x - f)), ("ce", lambda x, f: ce(x, gamma))):
        obs = fn(a, r) - fn(b, r)
        boot = fn(a[idx], r[idx]) - fn(b[idx], r[idx])
        se = boot.std(ddof=1)
        p = np.mean(np.abs(boot - boot.mean()) >= abs(obs))
        lo, hi = np.percentile(boot, [2.5, 97.5])
        out[name] = {"diff": obs, "se": se, "p": p, "ci95": (lo, hi)}
    return out


def deflated_sharpe(sr_obs, sr_trials, n_obs, skew, kurt, periods=12):
    """Bailey and López de Prado (2014). Sharpe ratios are annualized on input and converted to
    per-period for the test. sr_trials: annualized Sharpe ratios of all configurations tried."""
    sr = sr_obs / np.sqrt(periods)
    trials = np.asarray(sr_trials) / np.sqrt(periods)
    n_trials = len(trials)
    var_trials = trials.var(ddof=1) if n_trials > 1 else 0.0
    gamma_e = 0.5772156649
    z1 = st.norm.ppf(1 - 1 / n_trials) if n_trials > 1 else 0.0
    z2 = st.norm.ppf(1 - 1 / (n_trials * np.e)) if n_trials > 1 else 0.0
    sr0 = np.sqrt(var_trials) * ((1 - gamma_e) * z1 + gamma_e * z2)
    num = (sr - sr0) * np.sqrt(n_obs - 1)
    den = np.sqrt(1 - skew * sr + (kurt - 1) / 4 * sr ** 2)
    return float(st.norm.cdf(num / den)), float(sr0 * np.sqrt(periods))


def newey_west(y, X, lags=12):
    """OLS with Newey-West (Bartlett) standard errors. X should include a constant."""
    y, X = np.asarray(y, float), np.asarray(X, float)
    XtX_inv = np.linalg.inv(X.T @ X)
    beta = XtX_inv @ X.T @ y
    u = y - X @ beta
    S = (X * u[:, None]).T @ (X * u[:, None])
    for L in range(1, lags + 1):
        w = 1 - L / (lags + 1)
        G = (X[L:] * u[L:, None]).T @ (X[:-L] * u[:-L, None])
        S += w * (G + G.T)
    cov = XtX_inv @ S @ XtX_inv
    se = np.sqrt(np.diag(cov))
    return beta, se, beta / se


def spanning(strategy_ex, factors_ex, lags=12, periods=12):
    """Regress a strategy's excess return on benchmark excess returns. Returns annualized alpha,
    its t-stat, betas and R^2."""
    df = pd.concat([strategy_ex.rename("y"), factors_ex], axis=1).dropna()
    X = np.column_stack([np.ones(len(df)), df[factors_ex.columns].to_numpy()])
    beta, se, t = newey_west(df["y"].to_numpy(), X, lags)
    resid = df["y"].to_numpy() - X @ beta
    r2 = 1 - resid.var() / df["y"].var()
    return {"alpha_ann": beta[0] * periods, "t_alpha": t[0],
            "betas": dict(zip(factors_ex.columns, beta[1:])), "t_betas": dict(zip(factors_ex.columns, t[1:])), "r2": r2,
            "n": len(df)}
