"""Walk-forward evaluation. A strategy is refit at each December and decides the following
twelve month-ends using only information dated at or before each decision."""
from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from . import policies, pomdp
from .models import hmm

BELIEF_GRID = np.linspace(0, 1, 201)

FEATURES = {
    "rv": ["log_rv"],
    "rv_term": ["log_rv", "term"],
    "rv_term_def": ["log_rv", "term", "default"],
    "macro4": ["log_rv", "term", "default", "infl_lag"],
    "returns": ["ex_stock", "ex_bond"],
}


def prepare(panel):
    p = panel.copy()
    p["log_rv"] = np.log(p["rv"])
    p["ex_stock"] = p["stock"] - p["cash"]
    p["ex_bond"] = p["bond"] - p["cash"]
    return p


def refit_dates(index, start, every=12):
    s = index.get_loc(pd.Timestamp(start))
    return index[s::every]


@dataclass
class HMMStrategy:
    features: str = "rv_term_def"
    k: int = 2            # number of states, or "bic" to pick 2-4 by BIC on each training window
    policy: str = "myopic"  # "myopic" mean-variance on beliefs, or "switch" on the most likely state
    gamma: float = 5.0
    mode: str = "realtime"  # "realtime", "full_filtered", "full_smoothed"
    cost: object = 0.001     # for the "band" policy: scalar, or dict of Series from backtest.jones_schedule
    horizon_years: float = 10.0
    restarts: int = 6
    seed: int = 0
    state: dict = field(default_factory=dict)

    @property
    def name(self):
        return f"HMM[{self.features},K={self.k},{self.policy}]"

    def _fit(self, p, train_end):
        cols = FEATURES[self.features]
        train = p.loc[:train_end]
        mu, sd = train[cols].mean(), train[cols].std()
        z_train = ((train[cols] - mu) / sd).to_numpy()
        if self.k == "bic":
            fits = [hmm.fit(z_train, k, self.restarts, self.seed) for k in (2, 3, 4)]
            model = min((f[0] for f in fits), key=lambda m: hmm.bic(m, z_train))
        else:
            model, _ = hmm.fit(z_train, self.k, self.restarts, self.seed)
        resp = hmm.smoothed(model, z_train)
        excess = train[["ex_stock", "ex_bond"]].to_numpy()
        mus, covs = policies.regime_moments(excess, resp)
        z_all = ((p[cols] - mu) / sd).to_numpy()
        return model, mus, covs, z_all

    def _cost_at(self, t):
        if np.isscalar(self.cost):
            return float(self.cost), float(self.cost)
        return float(self.cost["stock"].asof(t)), float(self.cost["bond"].asof(t))

    def decide(self, p, dates, train_end, actions):
        model, mus, covs, z_all = self._fit(p, train_end)
        if self.policy == "band":
            if model.n_components != 2:
                raise ValueError("the belief-space band is solved for two regimes")
            cs, cb = self._cost_at(train_end)
            cmat = cs * np.abs(actions[:, None, 0] - actions[None, :, 0]) + cb * np.abs(actions[:, None, 1] - actions[None, :, 1])
            K = pomdp.belief_kernel(model.transmat_, model.means_, hmm._covars(model), BELIEF_GRID)
            R = pomdp.mixture_reward(BELIEF_GRID, model.transmat_, mus, covs, actions, self.gamma)
            sol = pomdp.solve(K, R, actions, cmat, beta=np.exp(-1 / (12 * self.horizon_years)), grid=BELIEF_GRID, max_iter=200000)
            post = hmm.filtered(model, z_all)[:, 1]
            held = self.state.get("held", int(np.argmin(np.abs(actions).sum(1))))
            out = []
            for i in p.index.get_indexer(dates):
                g = int(round(post[i] * (len(BELIEF_GRID) - 1)))
                held = int(sol.policy[g, held])
                out.append(actions[held])
            self.state["held"] = held
            self.state[train_end] = {"transmat": model.transmat_, "mus": mus, "covs": covs}
            return pd.DataFrame(out, index=dates, columns=["stock", "bond"])
        if self.mode == "full_smoothed":
            post = hmm.smoothed(model, z_all)
            # Two-sided probability of next month's state: the look-ahead most papers plot.
            nxt = np.vstack([post[1:], post[-1:]])
        else:
            nxt = hmm.filtered(model, z_all) @ model.transmat_
        pos = p.index.get_indexer(dates)
        out = []
        for i in pos:
            prob = nxt[i]
            if self.policy == "myopic":
                out.append(policies.myopic(prob, mus, covs, actions, self.gamma))
            else:
                good = np.argmin(covs[:, 0, 0])
                out.append(np.array([1.0, 0.0]) if prob.argmax() == good else np.array([0.0, 0.0]))
        self.state[train_end] = {"transmat": model.transmat_, "mus": mus, "covs": covs}
        return pd.DataFrame(out, index=dates, columns=["stock", "bond"])


def walk_forward(panel, strategy, start="1946-12-31", end=None, every=12, step=0.1):
    p = prepare(panel)
    actions = policies.action_grid(step)
    last = p.index[-2] if end is None else pd.Timestamp(end)
    decisions = p.loc[start:last].index
    if getattr(strategy, "mode", "realtime") != "realtime":
        return strategy.decide(p, decisions, p.index[-1], actions)
    chunks = []
    for t0 in refit_dates(p.index, start, every):
        if t0 > last:
            break
        window = decisions[(decisions >= t0) & (decisions < t0 + pd.DateOffset(months=every))]
        chunks.append(strategy.decide(p, window, t0, actions))
    return pd.concat(chunks)


# ---------- baselines (all causal) ----------

def static(panel, start, w_stock, w_bond, end=None):
    p = panel.loc[start:end].iloc[:-1] if end is None else panel.loc[start:end]
    return pd.DataFrame({"stock": w_stock, "bond": w_bond}, index=p.index)


def unconditional_mv(panel, start, gamma=5.0, step=0.1, every=12):
    p = prepare(panel)
    actions = policies.action_grid(step)
    out = {}
    for t0 in refit_dates(p.index, start, every):
        train = p.loc[:t0, ["ex_stock", "ex_bond"]].to_numpy()
        mus, covs = policies.regime_moments(train, np.ones((len(train), 1)))
        w = policies.myopic(np.ones(1), mus, covs, actions, gamma)
        for t in p.loc[t0:].index[:every]:
            out[t] = w
    df = pd.DataFrame(out, index=["stock", "bond"]).T
    return df.loc[: p.index[-2]]


def vol_managed(panel, start, gamma=5.0, cap=1.0, every=12):
    """Moreira-Muir scaling w = c / RV_t with c re-estimated only from past data (Cederburg et al. 2020)."""
    p = prepare(panel)
    out = {}
    for t0 in refit_dates(p.index, start, every):
        train = p.loc[:t0]
        mu = train["ex_stock"].mean()
        # c chosen so the average past weight equals the unconditional mean-variance weight.
        target = mu / (gamma * train["ex_stock"].var())
        c = target / (1 / train["rv"]).mean()
        for t in p.loc[t0:].index[:every]:
            out[t] = min(cap, max(0.0, c / p.at[t, "rv"]))
    s = pd.Series(out).loc[: p.index[-2]]
    return pd.DataFrame({"stock": s, "bond": 0.0})


def trend(panel, start, months=10, defensive="cash"):
    """Faber-style: hold stocks while the total-return index is above its trailing mean."""
    idx = (1 + panel["stock"]).cumprod()
    on = (idx > idx.rolling(months).mean()).astype(float)
    on = on.loc[start: panel.index[-2]]
    bond = (1 - on) if defensive == "bond" else 0.0
    return pd.DataFrame({"stock": on, "bond": bond})


def tsmom(panel, start, months=12, defensive="cash"):
    ex = (panel["stock"] - panel["cash"]).rolling(months).sum()
    on = (ex > 0).astype(float).loc[start: panel.index[-2]]
    bond = (1 - on) if defensive == "bond" else 0.0
    return pd.DataFrame({"stock": on, "bond": bond})


def risk_parity(panel, start, window=36):
    vol = panel[["stock", "bond"]].rolling(window).std()
    inv = 1 / vol
    w = inv.div(inv.sum(1), axis=0).loc[start: panel.index[-2]]
    return w
