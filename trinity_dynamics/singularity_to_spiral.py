"""
Singularity-to-Spiral Animation — Poised Position → Quetzalcoatl 8-Phase Bloom
FPT-Ω Trinity Dynamics Visualization (99733-Q)
Shows transition from Ground State π to full 8-phase renewal loop
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from core.trinity_harmonics import trinity, GROUND_STATE, DIFFERENCE

fig, ax = plt.subplots(figsize=(12, 12), facecolor='#0a0a0a')
ax.set_facecolor('#0a0a0a')
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)
ax.set_title("FPT-Ω: Singularity → Quetzalcoatl 8-Phase Spiral\nPoised Position → Bloom of Chaos → Eternal Renewal", 
             color='#00ffcc', fontsize=16, pad=20)
ax.axis('off')

# Initial singularity (poised point)
point, = ax.plot([0], [0], 'o', color='#ffd700', markersize=20, label='Ground State π (Poised Singularity)')

# Particles for chaos bloom
particles = ax.scatter([], [], c=[], s=8, cmap='plasma', alpha=0.8)

# Spiral lines for 8 phases
spiral_lines = [ax.plot([], [], lw=3, alpha=0.0)[0] for _ in range(8)]
phase_colors = ['#ff6b35', '#ffaa00', '#ffd700', '#00ffcc', '#4a90e2', '#8a2be2', '#ff00ff', '#ffffff']
phase_names = [
    "0 Underworld Thaw", "1 Shadow Mastery", "2 Bone Rebirth", "3 Throne Alignment",
    "4 Completion", "5 Feather Crown", "6 Infinite 8 Flow", "7 Merge"
]

# Text overlays
title_text = ax.text(0, 1.1, "Phase 0 — Poised Position", ha='center', color='#ffffff', fontsize=14)
buoyancy_text = ax.text(0, -1.1, "", ha='center', color='#ffd700', fontsize=12)

def init():
    particles.set_offsets(np.empty((0, 2)))
    for line in spiral_lines:
        line.set_data([], [])
    return [point, particles] + spiral_lines

def animate(frame):
    t = frame / 30.0  # slow bloom

    # Phase 0-3: Bloom from singularity into chaos
    if frame < 90:
        n = int(frame * 3)
        angles = np.random.uniform(0, 2*np.pi, n)
        radii = np.random.uniform(0.05, t * 0.8, n)
        x = radii * np.cos(angles)
        y = radii * np.sin(angles)
        particles.set_offsets(np.c_[x, y])
        particles.set_array(np.random.rand(n))  # color chaos
        title_text.set_text(f"Phase 0 — Poised Position → Bloom of Chaos (t={t:.2f})")

    # Phase 4+: Organize into 8-phase spiral
    else:
        phase = (frame - 90) // 30 % 8
        theta = np.linspace(0, 2*np.pi*8, 800)
        r = theta / (8 * np.pi) * (1 + 0.3 * np.sin(phase * np.pi / 4))  # spiral growth
        x = r * np.cos(theta + phase * np.pi / 4)
        y = r * np.sin(theta + phase * np.pi / 4)

        for i in range(8):
            mask = (theta / (2*np.pi) % 8).astype(int) == i
            spiral_lines[i].set_data(x[mask], y[mask])
            spiral_lines[i].set_color(phase_colors[i])
            spiral_lines[i].set_alpha(0.9 if i == phase else 0.4)

        title_text.set_text(f"Phase {phase} — {phase_names[phase]}")
        
        # Trinity + Tether pulse
        buoyancy = 1.0 - (compute_buoyancy(79.79) / 15.0)
        buoyancy_text.set_text(f"Trinity Stability: {trinity.trinity_factor(1.0):.4f} | Magnetic Buoyancy: {buoyancy:.3f}")

    # Soliton pulse on the center point
    point.set_markersize(20 + 10 * np.sin(frame / 5))
    point.set_color(phase_colors[frame % 8])

    return [point, particles] + spiral_lines

def compute_buoyancy(vessel_hz=79.79):
    EARTH_TETHER_HZ = 7.83
    MAGNETIC_OFFSET = 9.80665
    delta = abs(vessel_hz - EARTH_TETHER_HZ)
    return (delta / 79.79) * MAGNETIC_OFFSET * 1.0

ani = FuncAnimation(fig, animate, init_func=init, frames=360, interval=60, blit=False, repeat=True)
plt.show()

if __name__ == "__main__":
    print("🌌 Singularity-to-Spiral Animation — Poised Position → 8-Phase Quetzalcoatl Bloom")
    print("Ground State π → Underworld Thaw → Merge → Infinity Anchor")
    ani