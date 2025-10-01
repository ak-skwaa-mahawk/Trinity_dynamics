"""
Trinity Dynamics Simulation Framework
Author: John Carroll Jr. (Two Mile Solutions LLC, Alaska)
Date: 2025-10-01
License: CC BY 4.0
Signature: κ/π ≈ 1.01 stabilization principle
Description: Package initializer, rooted in Shinati-Itanihs and (Luke 17:21)'s inner truth.
"""
from .simulation import TrinitySimulation
from .metrics import compute_metrics
from .sensitivity import run_sensitivity
from .visualize import plot_trajectories_matplotlib, plot_dashboard_plotly
from .report import generate_report
from .main import main