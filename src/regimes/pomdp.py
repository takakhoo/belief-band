"""Exact belief-space dynamic programming for a two-regime allocation problem with
proportional transaction costs.

State: (b, a_prev), where b = P(regime 1 | information) and a_prev is the action held.
Action: a in a finite set of portfolios. Reward: mean-variance utility of next-period excess
return under the predicted regime mixture, minus c * one-way turnover. The belief evolves by
the Bayes filter of a Gaussian HMM; its transition kernel is computed by Gauss-Hermite
quadrature over the next observation, so the solution is exact up to grid interpolation.

Without costs, the continuation value does not depend on the action and the optimal policy is
the myopic one (Proposition 1). With costs, the policy has a no-trade region in belief space.
"""
from dataclasses import dataclass

import numpy as np
from scipy.stats import multivariate_normal


def hermite_nodes(n):
    x, w = np.polynomial.hermite_e.hermegauss(n)  # probabilists' Hermite: weight exp(-x^2/2)
    return x, w / w.sum()


def belief_kernel(transmat, means, covs, grid, n_nodes=24):
    """Row-stochastic matrix K[i, j] = P(b_{t+1} = grid[j] | b_t = grid[i]) for a 2-state HMM.

    For d-dimensional Gaussian emissions, the posterior depends on the observation only through
    the log-likelihood ratio, so we integrate over a tensor-free scheme: draw quadrature nodes in
    each regime's own coordinates along each axis of its Cholesky factor.
    """
    d = means.shape[1]
    x, w = hermite_nodes(n_nodes)
    if d == 1:
        offsets, weights = x[:, None], w
    else:
        rng = np.random.default_rng(0)
        # Quasi-Monte Carlo for d > 1: Gaussian draws from a scrambled Sobol sequence.
        from scipy.stats import qmc, norm
        u = qmc.Sobol(d, scramble=True, seed=rng).random(512)
        offsets, weights = norm.ppf(np.clip(u, 1e-9, 1 - 1e-9)), np.full(512, 1 / 512)
    obs, obs_w, obs_state = [], [], []
    for s in range(2):
        L = np.linalg.cholesky(covs[s])
        obs.append(means[s] + offsets @ L.T)
        obs_w.append(weights)
        obs_state.append(np.full(len(weights), s))
    obs = np.vstack(obs)
    obs_w = np.concatenate(obs_w)
    obs_state = np.concatenate(obs_state)
    loglik = np.column_stack([multivariate_normal.logpdf(obs, means[s], covs[s], allow_singular=True) for s in range(2)])
    G = len(grid)
    K = np.zeros((G, G))
    pred = grid * transmat[1, 1] + (1 - grid) * transmat[0, 1]  # P(s_{t+1} = 1)
    for i in range(G):
        p1 = pred[i]
        # Weight of each node: P(s_{t+1} = its regime) times its quadrature weight.
        wt = obs_w * np.where(obs_state == 1, p1, 1 - p1)
        log_post1 = np.log(max(p1, 1e-300)) + loglik[:, 1]
        log_post0 = np.log(max(1 - p1, 1e-300)) + loglik[:, 0]
        post = 1 / (1 + np.exp(np.clip(log_post0 - log_post1, -700, 700)))
        pos = np.clip(post * (G - 1), 0, G - 1 - 1e-12)
        lo = pos.astype(int)
        frac = pos - lo
        np.add.at(K[i], lo, wt * (1 - frac))
        np.add.at(K[i], lo + 1, wt * frac)
    return K / K.sum(1, keepdims=True)


@dataclass
class Solution:
    grid: np.ndarray
    actions: np.ndarray
    policy: np.ndarray       # [G, A_prev] -> action index
    value: np.ndarray
    myopic: np.ndarray       # [G] -> action index
    iterations: int


def solve(K, reward, actions, cost, beta=0.995, tol=1e-10, max_iter=20000, grid=None):
    """reward[i, a]: one-period utility at belief grid[i] of holding action a next period.
    actions: [A, n_assets] weights (cash is the remainder). cost: one-way proportional cost."""
    G, A = reward.shape
    if np.ndim(cost) == 2:
        turnover, cost = np.asarray(cost, float), 1.0  # a full [prev, new] trading-cost matrix
    else:
        full = np.hstack([actions, 1 - actions.sum(1, keepdims=True)])
        turnover = 0.5 * np.abs(full[:, None, :] - full[None, :, :]).sum(-1)  # [prev, new]
    V = np.zeros((G, A))
    for it in range(max_iter):
        cont = reward + beta * (K @ V)  # [G, a]: value of choosing a (then holding a as a_prev)
        Q = cont[:, None, :] - cost * turnover[None]  # [G, prev, new]
        newV = Q.max(-1)
        # Relative value iteration keeps numbers bounded when beta is close to 1.
        newV -= newV[0, 0]
        if np.max(np.abs(newV - V)) < tol:
            V = newV
            break
        V = newV
    cont = reward + beta * (K @ V)
    policy = (cont[:, None, :] - cost * turnover[None]).argmax(-1)
    # Ties (exact indifference) resolve to keeping the current holding.
    stay = np.arange(A)[None, :]
    best = (cont[:, None, :] - cost * turnover[None]).max(-1)
    keep_val = np.take_along_axis(cont - cost * np.diag(turnover)[None, :], np.arange(A)[None, :].repeat(G, 0), 1)
    policy = np.where(np.isclose(keep_val, best, rtol=0, atol=1e-15), stay, policy)
    grid = np.linspace(0, 1, G) if grid is None else grid
    return Solution(grid, actions, policy, V, reward.argmax(1), it + 1)


def mixture_reward(grid, transmat, mus, covs, actions, gamma):
    """Mean-variance utility of next-period excess returns under the predicted regime mixture."""
    pred1 = grid * transmat[1, 1] + (1 - grid) * transmat[0, 1]
    out = np.empty((len(grid), len(actions)))
    for i, p in enumerate(pred1):
        prob = np.array([1 - p, p])
        mu = prob @ mus
        second = np.einsum("s,sij->ij", prob, covs + np.einsum("si,sj->sij", mus, mus))
        cov = second - np.outer(mu, mu)
        out[i] = actions @ mu - 0.5 * gamma * np.einsum("ai,ij,aj->a", actions, cov, actions)
    return out


def no_trade_bands(sol):
    """For each previous action, the belief interval where the optimal choice is to keep it."""
    G = sol.policy.shape[0]
    grid = np.linspace(0, 1, G)
    bands = {}
    for a in range(sol.policy.shape[1]):
        keep = sol.policy[:, a] == a
        bands[a] = (grid[keep].min(), grid[keep].max()) if keep.any() else None
    return bands
