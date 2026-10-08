import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from regimes import backtest, pomdp  # noqa: E402
from regimes.models import hmm, jump  # noqa: E402

GRID = np.linspace(0, 1, 201)
A = np.array([[0.99, 0.01], [0.02, 0.98]])


def small_problem(sep=0.5):
    K = pomdp.belief_kernel(A, np.array([[sep / 2], [-sep / 2]]), np.array([[[1.0]], [[1.0]]]), GRID, n_nodes=32)
    R = pomdp.mixture_reward(GRID, A, np.array([[0.001], [-0.002]]), np.array([[[1e-4]], [[4e-4]]]), np.array([[0.0], [1.0]]), 2.0)
    return K, R


def test_kernel_is_stochastic_and_martingale():
    K, _ = small_problem()
    assert np.allclose(K.sum(1), 1)
    pred = GRID * A[1, 1] + (1 - GRID) * A[0, 1]
    # The posterior is a martingale around the one-step prediction (up to grid interpolation).
    assert np.max(np.abs(K @ GRID - pred)) < 5e-3


def test_proposition_1_zero_cost_policy_is_myopic():
    K, R = small_problem()
    sol = pomdp.solve(K, R, np.array([[0.0], [1.0]]), 0.0, beta=0.99, grid=GRID)
    for prev in range(2):
        assert np.array_equal(sol.policy[:, prev], R.argmax(1))


def test_costly_policy_has_hysteresis_containing_myopic_threshold():
    K, R = small_problem()
    sol = pomdp.solve(K, R, np.array([[0.0], [1.0]]), 1e-3, beta=0.999, grid=GRID)
    enter = GRID[sol.policy[:, 0] == 1].max()
    leave = GRID[sol.policy[:, 1] == 0].min()
    myopic = GRID[np.argmin(np.abs(R[:, 1] - R[:, 0]))]
    assert enter < myopic < leave


def test_band_widens_with_cost():
    K, R = small_problem()
    widths = []
    for c in (1e-4, 1e-3, 5e-3):
        sol = pomdp.solve(K, R, np.array([[0.0], [1.0]]), c, beta=0.999, grid=GRID)
        widths.append(GRID[sol.policy[:, 1] == 0].min() - GRID[sol.policy[:, 0] == 1].max())
    assert widths[0] < widths[1] < widths[2]


def test_hmm_filter_is_causal():
    rng = np.random.default_rng(0)
    x = np.r_[rng.normal(0, 1, 300), rng.normal(0, 3, 100), rng.normal(0, 1, 100)][:, None]
    model, _ = hmm.fit(x, 2, restarts=2, seed=0)
    a = hmm.filtered(model, x)
    y = x.copy()
    y[400:] = rng.normal(5, 10, (100, 1))
    b = hmm.filtered(model, y)
    assert np.allclose(a[:400], b[:400])


def test_jump_online_labels_are_causal():
    rng = np.random.default_rng(1)
    x = np.r_[rng.normal(0, 1, (200, 2)), rng.normal(3, 1, (200, 2))]
    theta, _ = jump.fit(x, 2, lam=20.0, n_init=3)
    a = jump.online_states(x, theta, 20.0)
    y = x.copy()
    y[300:] += 50
    b = jump.online_states(y, theta, 20.0)
    assert np.array_equal(a[:300], b[:300])


def test_backtest_charges_both_legs_and_lags_weights():
    idx = pd.date_range("2000-01-31", periods=4, freq="ME")
    panel = pd.DataFrame({"stock": [0.0, 0.10, 0.0, 0.0], "bond": [0.0, 0.0, 0.05, 0.0], "cash": 0.0}, index=idx)
    w = pd.DataFrame({"stock": [1.0, 0.0, 0.0], "bond": [0.0, 1.0, 1.0]}, index=idx[:3])
    res = backtest.run(w, panel, 0.01)
    # Month 1: buy stock (1% cost), earn the 10% stock return of the next row.
    assert res["net"].iloc[0] == pytest.approx(0.99 * 1.10 - 1)
    # Month 2: sell stock and buy bonds, paying both legs (2%), earn the 5% bond return.
    assert res["net"].iloc[1] == pytest.approx(0.98 * 1.05 - 1)
    assert res["net"].iloc[2] == pytest.approx(0.0)
