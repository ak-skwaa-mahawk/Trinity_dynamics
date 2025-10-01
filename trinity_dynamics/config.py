"""
Trinity Dynamics Simulation Framework
Author: John Carroll Jr. (Two Mile Solutions LLC, Alaska)
Date: 2025-10-01
License: CC BY 4.0
Signature: κ/π ≈ 1.01 stabilization principle
Description: Global configuration constants, inspired by Shinati-Itanihs (*Chiz'yaa*) stability.
"""

import numpy as np

# Mathematical and Custom Constants
PI = np.pi  # Standard mathematical constant (~3.14159)
KAPPA = 3.1730059  # Unique constant from Two Mile Solutions research
S_FACTOR = KAPPA / PI  # Scaling factor ≈ 1.01005, a ~1% correction

# Simulation Parameters
STEPS = 2000  # Number of time steps
DT_BASE = 0.01  # Base time step
SEED = 42  # Random seed for reproducibility
NOISE_LEVEL = 0.001  # Noise injection for realism

# Default Initial Conditions and Interaction Matrix
DEFAULT_X0 = np.array([0.33, 0.33, 0.34])  # Near-equal starting proportions
DEFAULT_A = np.array([[1.0, 0.5, 0.3],
                      [0.5, 1.0, 0.4],
                      [0.3, 0.4, 1.0]])  # Symmetric interaction matrix

# Sensitivity Ranges
X0_LIST = [
    np.array([0.33, 0.33, 0.34]),
    np.array([0.1, 0.1, 0.8]),
    np.array([0.5, 0.3, 0.2]),
    np.array([0.4, 0.4, 0.2])  # Added diversity
]
A_LIST = [
    np.array([[1.0, 0.5, 0.3], [0.5, 1.0, 0.4], [0.3, 0.4, 1.0]]),
    np.array([[1.0, 0.7, 0.3], [0.7, 1.0, 0.4], [0.3, 0.4, 1.0]]),
    np.array([[1.0, 0.3, 0.3], [0.3, 1.0, 0.4], [0.3, 0.4, 1.0]]),
    np.array([[1.0, 0.6, 0.2], [0.6, 1.0, 0.5], [0.2, 0.5, 1.0]])  # New variation
]
DT_LIST = [0.01, 0.005, 0.02, 0.015]  # Expanded
S_LIST = [1.0, 1.005, 1.01, 1.015, S_FACTOR, 1.02]  # Extended
SEEDS = [SEED + i for i in range(5)]  # Multiple seeds