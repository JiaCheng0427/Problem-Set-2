"""Experiment portfolio and decision rules."""

from __future__ import annotations
import numpy as np
import pandas as pd
from scipy import stats

def simulate_portfolio(n: int, seed: int) -> pd.DataFrame:
    """Simulate experiments with true effects."""
    rng = np.random.default_rng(seed)
    real = rng.random(n) < 0.20
    true = np.where(real, rng.normal(0.15, 0.05, size=n), 0.0)
    size = rng.integers(80, 1601, size=n)
    se = np.sqrt(2 / size)
    est = true + rng.normal(0, se)
    return pd.DataFrame({"true": true, "n": size, "se": se, "est": est})


def apply_rule(log: pd.DataFrame, rule: str) -> pd.Series:
    """Select experiments under a decision rule."""
    p = pd.Series(
        2 * stats.norm.sf(np.abs(log["est"] / log["se"])),
        index=log.index
    )

    if rule == "old":
        return p < 0.05
    if rule == "new":
        return (p < 0.01) & (log["est"] > 0)
    if rule == "power_floor":
        power = stats.norm.sf(1.96 - 0.15 / log["se"]) + stats.norm.cdf(-1.96 - 0.15 / log["se"])
        return (p < 0.05) & (log["est"] > 0) & (power >= 0.80)

    raise ValueError("Unknown rule")


def evaluate(log: pd.DataFrame, rule: str) -> dict:
    """Calculate true return, ship count and false-ship rate."""
    selected = apply_rule(log, rule)
    w = log.loc[selected]
    return {
        "true_return": float(w["true"].sum()),
        "n_shipped": int(selected.sum()),
        "false_ship_rate": float((w["true"] == 0).mean()) if len(w) else 0.0
    }


if __name__ == "__main__":
    demo = simulate_portfolio(200, 42)

    assert len(demo) == 200
    assert (demo["se"] > 0).all()
    assert apply_rule(demo, "new").sum() <= apply_rule(demo, "old").sum()
    assert evaluate(demo, "old")["n_shipped"] == apply_rule(demo, "old").sum()

    print("All tests passed.")
