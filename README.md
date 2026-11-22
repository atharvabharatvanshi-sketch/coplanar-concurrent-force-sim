# Coplanar Concurrent Force System Simulator

An interactive Python simulation and analytical solver for **coplanar concurrent force systems** using NumPy and Matplotlib.

## Features
- Resolves multiple forces $(F_i, \theta_i)$ into orthogonal components $F_{ix} = F_i\cos\theta_i$ and $F_{iy} = F_i\sin\theta_i$.
- Computes net components ($R_x, R_y$), resultant magnitude $R = \sqrt{R_x^2 + R_y^2}$, and quadrant-safe angle $\theta_R = \operatorname{atan2}(R_y, R_x)$.
- Calculates and visualizes the **equilibrant force** ($\vec{F}_{\text{eq}} = -\vec{R}$) and **static equilibrium** state.
- Interactive controls to select forces, adjust magnitude and angle sliders, and toggle tip-to-tail polygon and component overlays.

## Setup & Run
```bash
pip install numpy matplotlib pytest
python solver.py
python app.py