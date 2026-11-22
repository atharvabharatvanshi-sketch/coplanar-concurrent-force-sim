import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
import numpy as np
import streamlit as st

from solver import ForceVector, analyze_system

st.set_page_config(
    page_title="Coplanar Concurrent Force Simulator", layout="wide"
)
st.title("Coplanar Concurrent Force System Simulator")

if "forces" not in st.session_state:
  st.session_state.forces = [
      ForceVector("F1", 120.0, 30.0),
      ForceVector("F2", 85.0, 135.0),
      ForceVector("F3", 60.0, 250.0),
  ]

with st.sidebar:
  st.header("Force Controls")
  idx = st.selectbox(
      "Select Force",
      options=range(len(st.session_state.forces)),
      format_func=lambda i: st.session_state.forces[i].label,
  )
  current = st.session_state.forces[idx]

  mag = st.slider(
      "Magnitude (N)",
      0.0,
      250.0,
      float(current.magnitude_n),
      step=1.0,
  )
  ang = st.slider(
      "Angle (deg)",
      -180.0,
      180.0,
      float(current.angle_deg),
      step=1.0,
  )

  st.session_state.forces[idx] = ForceVector(current.label, mag, ang)

  show_polygon = st.checkbox("Tip-to-Tail Polygon", value=True)
  show_components = st.checkbox("Rx / Ry Components", value=True)
  show_equilibrant = st.checkbox("Equilibrant (Feq)", value=True)

  if st.button("Reset Defaults"):
    st.session_state.forces = [
        ForceVector("F1", 120.0, 30.0),
        ForceVector("F2", 85.0, 135.0),
        ForceVector("F3", 60.0, 250.0),
    ]
    st.rerun()

forces = st.session_state.forces
data = analyze_system(forces)
fx, fy = data["fx"], data["fy"]
rx, ry = data["rx"], data["ry"]
r_mag, r_ang = data["resultant_magnitude_n"], data["resultant_angle_deg"]
eq_mag, eq_ang = data["equilibrant_magnitude_n"], data["equilibrant_angle_deg"]

col_plot, col_info = st.columns([2, 1])

with col_plot:
  max_reach = max(
      [150.0, r_mag * 1.25]
      + [f.magnitude_n * 1.2 for f in forces]
      + [abs(rx) * 1.25, abs(ry) * 1.25]
  )
  lim = float(np.ceil(max_reach / 25.0) * 25.0)

  fig, ax = plt.subplots(figsize=(6.5, 6.5))
  ax.set_xlim(-lim, lim)
  ax.set_ylim(-lim, lim)
  ax.set_aspect("equal", adjustable="box")
  ax.grid(True, linestyle=":", alpha=0.5)
  ax.axhline(0.0, color="#64748b", linewidth=1.0)
  ax.axvline(0.0, color="#64748b", linewidth=1.0)
  ax.set_xlabel("x-axis (N)")
  ax.set_ylabel("y-axis (N)")
  ax.set_title("Concurrent Forces at Origin (0, 0)")

  colors = ["#2563eb", "#0d9488", "#d97706"]

  def add_arrow(x0, y0, dx, dy, color, lw=2.2, ls="-", alpha=1.0):
    if np.hypot(dx, dy) < 1e-6:
      return
    ax.add_patch(
        FancyArrowPatch(
            (x0, y0),
            (x0 + dx, y0 + dy),
            arrowstyle="-|>,head_length=8,head_width=5",
            color=color,
            linewidth=lw,
            linestyle=ls,
            alpha=alpha,
        )
    )

  for i, f in enumerate(forces):
    c = colors[i % len(colors)]
    add_arrow(0.0, 0.0, fx[i], fy[i], c, lw=3.0 if i == idx else 2.0)
    ax.text(
        fx[i] * 1.06,
        fy[i] * 1.06,
        f"{f.label} ({f.magnitude_n:.0f}N, {f.angle_deg:.0f}°)",
        color=c,
        fontsize=9,
    )

  if show_polygon:
    px, py = 0.0, 0.0
    for i, f in enumerate(forces):
      c = colors[i % len(colors)]
      add_arrow(px, py, fx[i], fy[i], c, lw=1.4, ls="--", alpha=0.6)
      px += fx[i]
      py += fy[i]

  if show_components and not data["in_equilibrium"]:
    ax.plot([0.0, rx], [0.0, 0.0], color="#7c3aed", linestyle="--", lw=1.5)
    ax.plot([rx, rx], [0.0, ry], color="#7c3aed", linestyle=":", lw=1.5)

  if not data["in_equilibrium"]:
    add_arrow(0.0, 0.0, rx, ry, "#dc2626", lw=3.2)
    ax.text(
        rx * 1.06,
        ry * 1.06,
        f"R = {r_mag:.1f} N ({r_ang:.1f}°)",
        color="#dc2626",
        fontsize=9.5,
        fontweight="bold",
    )
    if show_equilibrant:
      add_arrow(0.0, 0.0, -rx, -ry, "#15803d", lw=2.2, ls="-.")
      ax.text(
          -rx * 1.06,
          -ry * 1.06,
          f"Feq = {eq_mag:.1f} N ({eq_ang:.1f}°)",
          color="#15803d",
          fontsize=9,
          fontweight="bold",
      )

  ax.scatter([0.0], [0.0], color="#0f172a", s=36)
  st.pyplot(fig)

with col_info:
  st.subheader("System Readout")
  st.metric("Net Fx (Rx)", f"{rx:.2f} N")
  st.metric("Net Fy (Ry)", f"{ry:.2f} N")
  if data["in_equilibrium"]:
    st.success("Static Equilibrium (R ≈ 0 N)")
  else:
    st.metric("Resultant R", f"{r_mag:.2f} N @ {r_ang:.2f}°")
    st.metric("Equilibrant Feq", f"{eq_mag:.2f} N @ {eq_ang:.2f}°")