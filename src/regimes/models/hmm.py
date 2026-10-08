"""Gaussian hidden Markov models with causal (filtered) and smoothed inference."""
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from scipy.special import logsumexp
from scipy.stats import multivariate_normal


def fit(X, k, restarts=8, seed=0, covariance="full"):
    """Best-of-restarts Baum-Welch fit. States are ordered by the variance of column 0."""
    best, best_ll = None, -np.inf
    rng = np.random.default_rng(seed)
    for _ in range(restarts):
        model = GaussianHMM(n_components=k, covariance_type=covariance, n_iter=500, tol=1e-6,
                            random_state=int(rng.integers(1 << 31)), min_covar=1e-4)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                model.fit(X)
                ll = model.score(X)
            except (ValueError, np.linalg.LinAlgError):
                continue
        if np.isfinite(ll) and ll > best_ll and np.all(np.isfinite(model.transmat_)):
            best, best_ll = model, ll
    if best is None:
        raise RuntimeError("no restart converged")
    order = np.argsort(_covars(best)[:, 0, 0])
    return _reorder(best, order), best_ll


def _covars(model):
    c = model.covars_
    return c if c.ndim == 3 else np.stack([np.diag(v) for v in c])


def _reorder(model, order):
    model.startprob_ = model.startprob_[order]
    model.transmat_ = model.transmat_[np.ix_(order, order)]
    model.means_ = model.means_[order]
    if model.covariance_type == "full":
        model.covars_ = model.covars_[order]
    else:
        model.covars_ = _covars(model)[order].diagonal(axis1=1, axis2=2)
    return model


def log_emissions(model, X):
    cov = _covars(model)
    return np.column_stack([multivariate_normal.logpdf(X, model.means_[s], cov[s], allow_singular=True)
                            for s in range(model.n_components)])


def filtered(model, X, prior=None):
    """P(s_t | x_1..x_t) for every t. Uses nothing after t."""
    logb = log_emissions(model, X)
    logA = np.log(np.clip(model.transmat_, 1e-300, None))
    k = model.n_components
    alpha = np.empty_like(logb)
    prev = np.log(model.startprob_ if prior is None else prior)
    for t in range(len(X)):
        pred = prev if t == 0 else logsumexp(prev[:, None] + logA, axis=0)
        a = pred + logb[t]
        alpha[t] = a - logsumexp(a)
        prev = alpha[t]
    return np.exp(alpha)


def smoothed(model, X):
    """P(s_t | x_1..x_T): two-sided, for in-sample estimation and look-ahead comparisons only."""
    return model.predict_proba(X)


def bic(model, X):
    k, d = model.n_components, X.shape[1]
    n_params = (k - 1) + k * (k - 1) + k * d + k * d * (d + 1) / 2
    return -2 * model.score(X) + n_params * np.log(len(X))
