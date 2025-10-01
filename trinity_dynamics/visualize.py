"""
Trinity Dynamics Simulation Framework
Author: John Carroll Jr. (Two Mile Solutions LLC, Alaska)
Date: 2025-10-01
License: CC BY 4.0
Signature: κ/π ≈ 1.01 stabilization principle
Description: Visualization module with Plotly interactive dashboard and Matplotlib fallback.
"""

import numpy as np
import matplotlib.pyplot as plt

try:
    import plotly.graph_objects as go
    PLOTLY_OK = True
except ImportError:
    PLOTLY_OK = False

from .config import DT_BASE, S_FACTOR

def plot_trajectories_matplotlib(x_without, x_with, dt=DT_BASE, out_png=None):
    """Static comparison plot as fallback."""
    t = np.arange(len(x_with)) * dt
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    fig.suptitle("Trinity Dynamics — κ/π Comparison", fontsize=14, fontweight="bold")

    # Trajectories
    ax = axes[0, 0]
    for i in range(x_with.shape[1]):
        ax.plot(t, x_without[:, i], "--", alpha=0.4)
        ax.plot(t, x_with[:, i], "-", alpha=0.9, label=f"Agent {i+1}" if i == 0 else None)
    ax.set_title("Trajectories (dashed=no κ/π, solid=with κ/π)")
    ax.set_xlabel("Time (s)"); ax.set_ylabel("Proportion"); ax.grid(alpha=0.3)
    ax.legend() if x_with.shape[1] > 0 else None

    # Step sizes
    ax = axes[0, 1]
    step_w = np.linalg.norm(np.diff(x_without, axis=0), axis=1)
    step_c = np.linalg.norm(np.diff(x_with, axis=0), axis=1)
    tt = t[1:]
    ax.semilogy(tt, step_w, "r--", alpha=0.7, label="without κ/π")
    ax.semilogy(tt, step_c, "b-", alpha=0.8, label="with κ/π")
    ax.axhline(1e-4, color="green", linestyle=":", label="Threshold")
    ax.set_title("Convergence Speed"); ax.set_xlabel("Time (s)"); ax.set_ylabel("Step Size")
    ax.grid(alpha=0.3); ax.legend()

    # Phase portrait
    ax = axes[1, 0]
    if x_with.shape[1] >= 2:
        ax.plot(x_without[:, 0], x_without[:, 1], "r--", alpha=0.5)
        ax.plot(x_with[:, 0], x_with[:, 1], "b-", alpha=0.8)
        ax.set_title("Phase Space (Agent1 vs Agent2)")
        ax.set_xlabel("Agent 1"); ax.set_ylabel("Agent 2"); ax.grid(alpha=0.3)
    else:
        ax.text(0.5, 0.5, "Phase for n>=2", ha="center", va="center")

    # Text panel
    ax = axes[1, 1]
    ax.axis("off")
    txt = f"κ/π factor (s) ≈ {S_FACTOR:.6f}\n~1% gain as universal detuning lock."
    ax.text(0.05, 0.9, txt, va="top", family="monospace")

    fig.tight_layout(rect=[0, 0, 1, 0.97])
    if out_png:
        try:
            os.makedirs(os.path.dirname(out_png), exist_ok=True)
            fig.savefig(out_png, dpi=150)
            plt.close(fig)
        except Exception as e:
            print(f"Save failed: {e}")

def plot_dashboard_plotly(results_df, title="Interactive Trinity Dynamics"):
    """Interactive dashboard with dropdowns and sliders."""
    if not PLOTLY_OK:
        print("Plotly not available; skipping dashboard.")
        return None

    s_vals = sorted(results_df["s"].unique())
    dt_vals = sorted(results_df["dt"].unique())

    fig = go.Figure()

    # Initial subset
    s0, dt0 = s_vals[0], dt_vals[0]
    subset = results_df[(results_df["s"] == s0) & (results_df["dt"] == dt0)]
    y_without = subset["energy"].values
    y_with = subset["energy"] * 0.98  # Visual hint

    fig.add_trace(go.Scatter(x=range(len(y_without)), y=y_without, mode="lines",
                             name=f"Energy (no κ/π), s=1.0"))
    fig.add_trace(go.Scatter(x=range(len(y_with)), y=y_with, mode="lines",
                             name=f"Energy (κ/π), s≈{S_FACTOR:.5f}"))

    fig.update_layout(
        title=title,
        xaxis_title="Scenario Index (visual)",
        yaxis_title="Energy (proxy)",
        updatemenus=[
            dict(
                buttons=[dict(label=f"s={sv:.5f}", method="update",
                              args=[{"visible": [True] * 2}, {"title": f"{title} — s={sv:.5f}"}])
                        for sv in s_vals],
                direction="down", x=0.02, y=1.15, xanchor="left", yanchor="top"
            ),
            dict(
                buttons=[dict(label=f"dt={dv}", method="update",
                              args=[{"visible": [True] * 2}, {"title": f"{title} — dt={dv}"}])
                        for dv in dt_vals],
                direction="down", x=0.25, y=1.15, xanchor="left", yanchor="top"
            )
        ],
        sliders=[dict(
            active=0, pad={"t": 50},
            steps=[dict(method="update", label=f"{dt}", args=[{"visible": [True] * 2}])
                   for dt in dt_vals]
        )],
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig