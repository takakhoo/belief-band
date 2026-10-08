"""Allocation rules. Every function maps information available at t to weights for t+1."""
import itertools

import numpy as np


def action_grid(step=0.1):
    """Long-only stock/bond weights with cash as the remainder (no leverage)."""
    pts = np.round(np.arange(0, 1 + 1e-9, step), 10)
    return np.array([(s, b) for s, b in itertools.product(pts, pts) if s + b <= 1 + 1e-9])


def regime_moments(excess, resp):
    """Per-state mean and covariance of excess returns, weighted by state responsibilities."""
    k = resp.shape[1]
    mus, covs = [], []
    for s in range(k):
        w = resp[:, s] / resp[:, s].sum()
        mu = w @ excess
        d = excess - mu
        covs.append((d * w[:, None]).T @ d)
        mus.append(mu)
    return np.array(mus), np.array(covs)


def mixture(prob, mus, covs):
    mu = prob @ mus
    second = np.einsum("s,sij->ij", prob, covs + np.einsum("si,sj->sij", mus, mus))
    return mu, second - np.outer(mu, mu)


def mean_variance_scores(prob, mus, covs, actions, gamma):
    mu, cov = mixture(prob, mus, covs)
    return actions @ mu - 0.5 * gamma * np.einsum("ai,ij,aj->a", actions, cov, actions)


def myopic(prob, mus, covs, actions, gamma):
    return actions[np.argmax(mean_variance_scores(prob, mus, covs, actions, gamma))]
