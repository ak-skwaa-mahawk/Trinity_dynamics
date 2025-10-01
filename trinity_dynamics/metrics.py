"""
Trinity Dynamics Simulation Framework
Author: John Carroll Jr. (Two Mile Solutions LLC, Alaska)
Date: 2025-10-01
License: CC BY 4.0
Signature: κ/π ≈ 1.01 stabilization principle
Description: Metrics module for Trinity dynamics, computing convergence, entropy,
             oscillation, stability, and energy with robustness tests.
"""

import numpy as np
from scipy.signal import find_peaks

def _safe_entropy(p, eps=1e-12):
    """Safe Shannon entropy calculation in bits."""
    q = np.clip(p, eps, 1.0)
    q = q / np.sum(q)
    return float(-np.sum(q * np.log2(q)))

def compute_metrics(x, dt):
    """
    Computes core metrics with robustness checks.
    Args:
        x (np.ndarray): Simulation time series
        dt (float): Time step
    Returns:
        dict: Metrics including convergence time, entropy, oscillation frequency,
              stability (variance), energy, and final state
    """
    if x is None or len(x) < 2:
        return {
            "conv_time": float("inf"), "entropy": 0.0, "osc_freq": 0.0,
            "stability": float("inf"), "energy": float("inf"), "final_state": None
        }

    diffs = np.diff(x, axis=0)
    step_sizes = np.linalg.norm(diffs, axis=1)

    # Convergence time
    threshold = 1e-4
    idx = np.where(step_sizes < threshold)[0]
    conv_time = float(idx[0] * dt) if len(idx) else float("inf")

    # Final state and entropy
    final_state = x[-1]
    entropy = _safe_entropy(final_state)

    # Oscillation frequency
    peaks, _ = find_peaks(step_sizes)
    osc_freq = float(len(peaks) / (len(step_sizes) * dt)) if len(step_sizes) else 0.0

    # Stability (variance over last 10% or 100 steps)
    tail_len = max(100, len(x) // 10)
    tail = x[max(0, len(x) - tail_len):]
    stability = float(np.mean(np.var(tail, axis=0))) if len(tail) else float("inf")

    # Energy (total movement)
    energy = float(np.sum(step_sizes))

    return {
        "conv_time": conv_time, "entropy": entropy, "osc_freq": osc_freq,
        "stability": stability, "energy": energy, "final_state": final_state
    }