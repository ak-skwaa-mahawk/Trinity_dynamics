"""
Trinity Dynamics Simulation Framework
Author: John Carroll Jr. (Two Mile Solutions LLC, Alaska)
Date: 2025-10-01
License: CC BY 4.0
Signature: κ/π ≈ 1.01 stabilization principle
Description: Sensitivity analysis module for parameter sweeps, with CSV exports.
"""

import itertools
import numpy as np
import pandas as pd
from .config import X0_LIST, A_LIST, DT_LIST, S_LIST, SEEDS
from .simulation import TrinitySimulation
from .metrics import compute_metrics

def param_grid(x0_list=None, a_list=None, dt_list=None, s_list=None, seeds=None):
    """Generates parameter combinations for sensitivity analysis."""
    x0_list = x0_list or X0_LIST
    a_list = a_list or A_LIST
    dt_list = dt_list or DT_LIST
    s_list = s_list or S_LIST
    seeds = seeds or SEEDS
    return [dict(x0=x0, A=A, dt=dt, s=s, seed=seed)
            for x0, A, dt, s, seed in itertools.product(x0_list, a_list, dt_list, s_list, seeds)]

def run_sensitivity(steps=2000, grid=None, n_agents=3):
    """
    Runs parameter sweeps and returns a DataFrame with results.
    Args:
        steps (int): Number of simulation steps
        grid (list): Custom parameter grid (default from config)
        n_agents (int): Number of agents
    Returns:
        pd.DataFrame: Results with parameters and metrics
    """
    grid = grid or param_grid()
    sim = TrinitySimulation(n_agents=n_agents)
    rows = []

    for p in grid:
        np.random.seed(p["seed"])
        x = sim.run_simulation(p["x0"], p["A"], s_factor=p["s"], dt=p["dt"], steps=steps)
        if x is not None:
            m = compute_metrics(x, p["dt"])
            rows.append({
                "dt": p["dt"], "s": p["s"], "seed": p["seed"],
                "x0": tuple(p["x0"].round(3)), "A_tag": tuple(p["A"].round(3).flatten()),
                **{k: m[k] for k in m if k != "final_state"}
            })

    df = pd.DataFrame(rows)
    return df