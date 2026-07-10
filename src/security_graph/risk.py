"""Transparent MVP risk scoring for findings and reachable assets."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RiskFactors:
    severity: float
    exploitability: float
    exposure: float
    asset_criticality: float
    identity_reach: float
    control_reduction: float = 0.0


def score_risk(factors: RiskFactors) -> float:
    """Return a bounded 0-100 score with an explicit control reduction."""
    values = (
        factors.severity,
        factors.exploitability,
        factors.exposure,
        factors.asset_criticality,
        factors.identity_reach,
        factors.control_reduction,
    )
    if any(value < 0 or value > 1 for value in values):
        raise ValueError("risk factors must be between 0 and 1")

    inherent = (
        0.25 * factors.severity
        + 0.20 * factors.exploitability
        + 0.20 * factors.exposure
        + 0.25 * factors.asset_criticality
        + 0.10 * factors.identity_reach
    )
    residual = inherent * (1 - 0.60 * factors.control_reduction)
    return round(max(0.0, min(100.0, residual * 100)), 1)
