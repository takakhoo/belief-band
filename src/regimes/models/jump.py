"""Statistical jump model (Nystrup, Lindström and Madsen 2020; Shu, Yu and Mulvey 2024).

Minimize  sum_t ||x_t - theta_{s_t}||^2 + lam * #{t : s_t != s_{t-1}}
by alternating a dynamic program over the state path and centroid updates.
"""
import numpy as np
from numba import njit


@njit(cache=True)
def _viterbi(X, theta, lam):
    n, k = X.shape[0], theta.shape[0]
    loss = np.empty((n, k))
    for t in range(n):
        for s in range(k):
            acc = 0.0
            for j in range(X.shape[1]):
                d = X[t, j] - theta[s, j]
                acc += d * d
            loss[t, s] = acc
    value = loss[0].copy()
    back = np.zeros((n, k), dtype=np.int64)
    new = np.empty(k)
    for t in range(1, n):
        for s in range(k):
            best, arg = np.inf, 0
            for r in range(k):
                v = value[r] + (0.0 if r == s else lam)
                if v < best:
                    best, arg = v, r
            new[s] = best + loss[t, s]
            back[t, s] = arg
        value[:] = new
    path = np.empty(n, dtype=np.int64)
    path[n - 1] = np.argmin(value)
    for t in range(n - 1, 0, -1):
        path[t - 1] = back[t, path[t]]
    return path, value.min()


@njit(cache=True)
def _online(X, theta, lam, start):
    n, k = X.shape[0], theta.shape[0]
    value = np.zeros(k)
    out = np.full(n, -1, dtype=np.int64)
    new = np.empty(k)
    for t in range(n):
        for s in range(k):
            acc = 0.0
            for j in range(X.shape[1]):
                d = X[t, j] - theta[s, j]
                acc += d * d
            if t == 0:
                new[s] = acc
            else:
                best = np.inf
                for r in range(k):
                    v = value[r] + (0.0 if r == s else lam)
                    if v < best:
                        best = v
                new[s] = best + acc
        m = new.min()
        for s in range(k):
            value[s] = new[s] - m
        if t >= start:
            out[t] = np.argmin(value)
    return out


def _kmeanspp(X, k, rng):
    centers = [X[rng.integers(len(X))]]
    for _ in range(1, k):
        d = np.min(((X[:, None] - np.array(centers)[None]) ** 2).sum(-1), axis=1)
        centers.append(X[rng.choice(len(X), p=d / d.sum())])
    return np.array(centers, dtype=float)


def fit(X, k=2, lam=50.0, n_init=10, max_iter=50, seed=0):
    X = np.ascontiguousarray(X, dtype=float)
    rng = np.random.default_rng(seed)
    best = (np.inf, None, None)
    for _ in range(n_init):
        theta = _kmeanspp(X, k, rng)
        prev = None
        for _ in range(max_iter):
            path, obj = _viterbi(X, theta, float(lam))
            if prev is not None and np.array_equal(path, prev):
                break
            prev = path
            for s in range(k):
                if np.any(path == s):
                    theta[s] = X[path == s].mean(0)
        if obj < best[0]:
            best = (obj, theta.copy(), path.copy())
    return best[1], best[2]


def online_states(X, theta, lam, start=0):
    """Label at each t >= start: the last state of the optimal path over X[:t+1] (knowable at t)."""
    return _online(np.ascontiguousarray(X, dtype=float), np.ascontiguousarray(theta, dtype=float), float(lam), int(start))
