"""
Entrypoint: orchestrates simulation, sensitivity, visualization, reporting
Author: John Carroll Jr. (Two Mile Solutions LLC, Alaska) | CC BY 4.0
Signature: κ/π ≈ 1.01
"""

from __future__ import annotations
import os
import numpy as np
import pandas as pd

from .config import DEFAULT_X0, DEFAULT_A, S_FACTOR, DT_BASE, STEPS
from .simulation import TrinitySimulation
from .metrics import compute_metrics
from .sensitivity import run_sensitivity
from .visualize import plot_trajectories_matplotlib, plot_dashboard_plotly
from .report import generate_report

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

def run_baseline_and_compare():
    """Runs baseline comparison with and without κ/π."""
    sim = TrinitySimulation(n_agents=3)

    # Without κ/π
    x_w = sim.run_simulation(DEFAULT_X0, DEFAULT_A, s_factor=1.0, dt=DT_BASE, steps=STEPS)
    # With κ/π
    x_c = sim.run_simulation(DEFAULT_X0, DEFAULT_A, s_factor=S_FACTOR, dt=DT_BASE, steps=STEPS)

    m_w = compute_metrics(x_w, DT_BASE) if x_w is not None else {}
    m_c = compute_metrics(x_c, DT_BASE) if x_c is not None else {}

    png_path = os.path.join(DATA_DIR, "comparison.png")
    try:
        plot_trajectories_matplotlib(x_w, x_c, dt=DT_BASE, out_png=png_path)
    except Exception as e:
        print(f"Matplotlib plot failed: {e}")
        png_path = None

    return (x_w, m_w), (x_c, m_c), png_path

def main():
    """Orchestrates the full Trinity Dynamics workflow."""
    print("🔹 Trinity Dynamics — Two Mile Solutions LLC (κ/π ≈ 1.01) 🔹")

    # Baseline comparison
    (x_w, m_w), (x_c, m_c), png_path = run_baseline_and_compare()
    if m_w and m_c:
        print("Baseline (no κ/π):", {k: m_w[k] for k in ["conv_time", "entropy", "energy"]})
        print("Baseline (with κ/π):", {k: m_c[k] for k in ["conv_time", "entropy", "energy"]})
    else:
        print("Baseline run failed; check simulation logs.")

    # Sensitivity sweeps
    print("Running sensitivity sweeps...")
    df = run_sensitivity(steps=STEPS)
    csv_path = os.path.join(DATA_DIR, "sensitivity_results.csv")
    try:
        df.to_csv(csv_path, index=False)
        print(f"Sensitivity CSV saved: {csv_path}")
    except Exception as e:
        print(f"CSV write failed: {e}")

    # Interactive dashboard
    try:
        fig = plot_dashboard_plotly(df)
        if fig is not None:
            html_path = os.path.join(DATA_DIR, "dashboard.html")
            fig.write_html(html_path, include_plotlyjs="cdn")
            print(f"Interactive dashboard saved: {html_path}")
    except Exception as e:
        print(f"Plotly dashboard failed: {e}")

    # PDF report
    pdf_path = os.path.join(DATA_DIR, "report.pdf")
    try:
        generate_report(m_c if m_c else {}, df if df is not None else None, pdf_path, png_path)
    except Exception as e:
        print(f"Report generation failed: {e}")

if __name__ == "__main__":
    main()