"""
Trinity Dynamics Simulation Framework
Author: John Carroll Jr. (Two Mile Solutions LLC, Alaska)
Date: 2025-10-01
License: CC BY 4.0
Signature: κ/π ≈ 1.01 stabilization principle
Description: Core simulation module for N-agent Trinity dynamics, with error handling,
             noise injection, and generalization. Rooted in Shinati-Itanihs (*Chiz'yaa*).
"""

import numpy as np
from config import NOISE_LEVEL, SEED

class TrinitySimulation:
    """Manages N-agent Trinity dynamics simulation."""
    
    def __init__(self, n_agents=3):
        """Initialize with number of agents."""
        self.n_agents = n_agents
        np.random.seed(SEED)

    def trinity_dynamics(self, x, A, s=1.0):
        """
        Computes rate of change for N-agent replicator dynamics.
        Args:
            x (np.array): Current state vector (n_agents,)
            A (np.array): Interaction matrix (n_agents, n_agents)
            s (float): Scaling factor (default 1.0, κ/π ≈ 1.01)
        Returns:
            dx (np.array): Rate of change
        Raises:
            ValueError: If dimensions mismatch
        """
        if len(x) != self.n_agents or A.shape != (self.n_agents, self.n_agents):
            raise ValueError(f"Dimension mismatch: x={len(x)}, A={A.shape}, n_agents={self.n_agents}")
        Ax = A @ x
        mean_feedback = np.dot(x, Ax)
        dx = s * x * (Ax - mean_feedback)
        return dx + np.random.normal(0, NOISE_LEVEL, self.n_agents)  # Noise

    def run_simulation(self, x0, A, s_factor, dt=0.01, steps=2000):
        """
        Runs simulation with given parameters.
        Args:
            x0 (np.array): Initial conditions
            A (np.array): Interaction matrix
            s_factor (float): Scaling factor
            dt (float): Time step
            steps (int): Number of iterations
        Returns:
            x (np.array): Time series of agent proportions
        Raises:
            ValueError: If inputs are invalid
        """
        if len(x0) != self.n_agents or A.shape != (self.n_agents, self.n_agents):
            raise ValueError("Initial conditions or matrix dimensions mismatch")
        if not (0 < dt <= 1.0 and steps > 0):
            raise ValueError("Invalid dt or steps")

        x = np.zeros((steps, self.n_agents))
        x[0] = x0
        try:
            for t in range(1, steps):
                dx = self.trinity_dynamics(x[t-1], A, s=s_factor)
                x[t] = x[t-1] + dt * dx
            return np.abs(x) / np.sum(np.abs(x), axis=1, keepdims=True)  # Normalize
        except Exception as e:
            print(f"Simulation error at step {t}: {e}")
            return None