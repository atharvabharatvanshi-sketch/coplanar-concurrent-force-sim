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
## Demo

![Coplanar Concurrent Force System Simulator desktop window, showing a Cartesian force diagram and controls. The plot has title Concurrent Forces at Origin (0, 0), axes x-axis (N) and y-axis (N), and a range of -150 to 150 N on both axes. Three blue, teal, and orange force arrows extend from the origin and represent F1 at 120 N and 30 degrees, F2 at 85 N and 135 degrees, and F3 at 60 N and 250 degrees. A red resultant arrow is labeled R = 67.8 N (69.9 degrees), dashed component lines mark its components, and an orange equilibrant arrow is labeled Feq = 67.8 N (110.8 degrees). Dotted cyan tip-to-tail segments connect the forces. A right-side panel transcribes the system readout: sumFx (Rx) = 23.30 N, sumFy (Ry) = 63.72 N, Resultant R = 67.85 N at 69.92 degrees, and Equilibrant = 67.85 N at -110.08 degrees. It also lists F1: 120.0 N at 30.0 degrees (+103.9, +60.0), F2: 85.0 N at 135.0 degrees (-60.1, +60.1), and F3: 60.0 N at 250.0 degrees (-20.5, -56.4). The controls include a force selector, magnitude and angle sliders, checkboxes for Tip-to-tail, Equilibrant, and Rx / Ry, and a Reset button. The neutral, technical desktop application is set against a light gray background.](demo.png) 