import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from matplotlib.widgets import Button, CheckButtons, RadioButtons, Slider
import numpy as np

from solver import ForceVector, analyze_system


def build_simulation() -> None:
    # Initial 3-force coplanar concurrent system
    state = {
        "forces": [
            ForceVector("F1", 120.0, 30.0),
            ForceVector("F2", 85.0, 135.0),
            ForceVector("F3", 60.0, 250.0),
        ],
        "selected_idx": 0,
        "show_polygon": True,
        "show_equilibrant": True,
        "show_components": True,
    }

    plt.rcParams["toolbar"] = "none"
    fig = plt.figure(figsize=(11, 7.2))
    fig.canvas.manager.set_window_title(
        "Coplanar Concurrent Force System Simulator"
    )

    # Main vector plot on the left
    ax = fig.add_axes([0.07, 0.12, 0.56, 0.80])
    # Readout panel on the top right
    info_ax = fig.add_axes([0.67, 0.54, 0.30, 0.38])
    info_ax.axis("off")

    # Controls below readout panel
    ax_sel = fig.add_axes([0.67, 0.42, 0.30, 0.09])
    ax_mag = fig.add_axes([0.74, 0.35, 0.22, 0.035])
    ax_ang = fig.add_axes([0.74, 0.29, 0.22, 0.035])
    ax_chk = fig.add_axes([0.67, 0.13, 0.18, 0.12])
    ax_rst = fig.add_axes([0.87, 0.16, 0.10, 0.05])

    radio = RadioButtons(
        ax_sel,
        labels=[f.label for f in state["forces"]],
        active=0,
        activecolor="#2563eb",
    )

    current_f = state["forces"][0]
    slider_mag = Slider(
        ax=ax_mag,
        label="Mag (N)",
        valmin=0.0,
        valmax=250.0,
        valinit=current_f.magnitude_n,
        valstep=1.0,
    )
    slider_ang = Slider(
        ax=ax_ang,
        label="Angle (°)",
        valmin=-180.0,
        valmax=180.0,
        valinit=current_f.angle_deg,
        valstep=1.0,
    )

    checks = CheckButtons(
        ax_chk,
        labels=["Tip-to-Tail", "Equilibrant", "Rx / Ry"],
        actives=[
            state["show_polygon"],
            state["show_equilibrant"],
            state["show_components"],
        ],
    )
    btn_reset = Button(ax_rst, "Reset")

    force_colors = ["#2563eb", "#0d9488", "#d97706"]

    def draw_arrow(
        target_ax: plt.Axes,
        x0: float,
        y0: float,
        dx: float,
        dy: float,
        color: str,
        lw: float = 2.2,
        ls: str = "-",
        alpha: float = 1.0,
        zorder: int = 4,
    ) -> None:
        if np.hypot(dx, dy) < 1e-6:
            return
        arrow = FancyArrowPatch(
            (x0, y0),
            (x0 + dx, y0 + dy),
            arrowstyle="-|>,head_length=8,head_width=5",
            color=color,
            linewidth=lw,
            linestyle=ls,
            alpha=alpha,
            zorder=zorder,
        )
        target_ax.add_patch(arrow)

    def redraw() -> None:
        ax.clear()
        info_ax.clear()
        info_ax.axis("off")

        forces = state["forces"]
        data = analyze_system(forces)
        fx = data["fx"]
        fy = data["fy"]
        rx = data["rx"]
        ry = data["ry"]
        r_mag = data["resultant_magnitude_n"]
        r_ang = data["resultant_angle_deg"]
        eq_mag = data["equilibrant_magnitude_n"]
        eq_ang = data["equilibrant_angle_deg"]

        max_reach = max(
            [150.0, r_mag * 1.25]
            + [f.magnitude_n * 1.2 for f in forces]
            + [abs(rx) * 1.25, abs(ry) * 1.25]
        )
        lim = float(np.ceil(max_reach / 25.0) * 25.0)

        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_aspect("equal", adjustable="box")
        ax.grid(True, linestyle=":", alpha=0.5)
        ax.axhline(0.0, color="#64748b", linewidth=1.0, zorder=1)
        ax.axvline(0.0, color="#64748b", linewidth=1.0, zorder=1)
        ax.set_xlabel("x-axis (N)")
        ax.set_ylabel("y-axis (N)")
        ax.set_title("Concurrent Forces at Origin (0, 0)", pad=10)

        # 1. Plot concurrent forces from origin
        for i, f in enumerate(forces):
            col = force_colors[i % len(force_colors)]
            lw = 3.0 if i == state["selected_idx"] else 2.0
            draw_arrow(ax, 0.0, 0.0, fx[i], fy[i], color=col, lw=lw, zorder=4)
            ax.text(
                fx[i] * 1.06,
                fy[i] * 1.06,
                f"{f.label} ({f.magnitude_n:.0f}N, {f.angle_deg:.0f}°)",
                color=col,
                fontsize=9,
                fontweight="bold" if i == state["selected_idx"] else "normal",
            )

        # 2. Optional tip-to-tail force polygon
        if state["show_polygon"] and len(forces) > 0:
            px, py = 0.0, 0.0
            for i in range(len(forces)):
                col = force_colors[i % len(force_colors)]
                draw_arrow(
                    ax,
                    px,
                    py,
                    fx[i],
                    fy[i],
                    color=col,
                    lw=1.4,
                    ls="--",
                    alpha=0.55,
                    zorder=3,
                )
                px += fx[i]
                py += fy[i]

        # 3. Optional resultant Rx and Ry components
        if state["show_components"] and not data["in_equilibrium"]:
            ax.plot(
                [0.0, rx],
                [0.0, 0.0],
                color="#7c3aed",
                linestyle="--",
                linewidth=1.5,
                zorder=3,
            )
            ax.plot(
                [rx, rx],
                [0.0, ry],
                color="#7c3aed",
                linestyle=":",
                linewidth=1.5,
                zorder=3,
            )

        # 4. Plot Resultant R in crimson
        if not data["in_equilibrium"]:
            draw_arrow(
                ax, 0.0, 0.0, rx, ry, color="#dc2626", lw=3.2, zorder=6
            )
            ax.text(
                rx * 1.06,
                ry * 1.06,
                f"R = {r_mag:.1f} N ({r_ang:.1f}°)",
                color="#dc2626",
                fontsize=9.5,
                fontweight="bold",
            )

            # 5. Optional Equilibrant F_eq = -R in green
            if state["show_equilibrant"]:
                draw_arrow(
                    ax,
                    0.0,
                    0.0,
                    -rx,
                    -ry,
                    color="#15803d",
                    lw=2.2,
                    ls="-.",
                    zorder=5,
                )
                ax.text(
                    -rx * 1.06,
                    -ry * 1.06,
                    f"Feq = {eq_mag:.1f} N ({eq_ang:.1f}°)",
                    color="#15803d",
                    fontsize=9,
                    fontweight="bold",
                )

        ax.scatter([0.0], [0.0], color="#0f172a", s=36, zorder=7)

        status_line = (
            "Status: STATIC EQUILIBRIUM (R ≈ 0 N)"
            if data["in_equilibrium"]
            else f"Resultant R: {r_mag:.2f} N @ {r_ang:.2f}°"
        )
        eq_line = (
            "Equilibrant: Not needed"
            if data["in_equilibrium"]
            else f"Equilibrant: {eq_mag:.2f} N @ {eq_ang:.2f}°"
        )
        summary_text = (
            "SYSTEM READOUT\n"
            "──────────────────────────\n"
            f"ΣFx (Rx) : {rx:8.2f} N\n"
            f"ΣFy (Ry) : {ry:8.2f} N\n"
            f"{status_line}\n"
            f"{eq_line}\n\n"
            "INDIVIDUAL FORCES\n"
            "──────────────────────────\n"
            + "\n".join(
                f"{f.label}: {f.magnitude_n:5.1f} N @ {f.angle_deg:6.1f}° "
                f"({fx[i]:+6.1f}, {fy[i]:+6.1f})"
                for i, f in enumerate(forces)
            )
        )
        info_ax.text(
            0.0,
            0.98,
            summary_text,
            va="top",
            ha="left",
            family="monospace",
            fontsize=9.5,
            color="#0f172a",
        )

        fig.canvas.draw_idle()

    def on_select_force(label: str) -> None:
        for i, f in enumerate(state["forces"]):
            if f.label == label:
                state["selected_idx"] = i
                slider_mag.set_val(f.magnitude_n)
                slider_ang.set_val(f.angle_deg)
                redraw()
                break

    def on_slider_change(_val: float) -> None:
        idx = state["selected_idx"]
        old = state["forces"][idx]
        state["forces"][idx] = ForceVector(
            label=old.label,
            magnitude_n=float(slider_mag.val),
            angle_deg=float(slider_ang.val),
        )
        redraw()

    def on_check(label: str) -> None:
        if label == "Tip-to-Tail":
            state["show_polygon"] = not state["show_polygon"]
        elif label == "Equilibrant":
            state["show_equilibrant"] = not state["show_equilibrant"]
        elif label == "Rx / Ry":
            state["show_components"] = not state["show_components"]
        redraw()

    def on_reset(_event) -> None:
        state["forces"] = [
            ForceVector("F1", 120.0, 30.0),
            ForceVector("F2", 85.0, 135.0),
            ForceVector("F3", 60.0, 250.0),
        ]
        state["selected_idx"] = 0
        radio.set_active(0)
        slider_mag.set_val(120.0)
        slider_ang.set_val(30.0)
        redraw()

    radio.on_clicked(on_select_force)
    slider_mag.on_changed(on_slider_change)
    slider_ang.on_changed(on_slider_change)
    checks.on_clicked(on_check)
    btn_reset.on_clicked(on_reset)

    redraw()
    plt.show()


if __name__ == "__main__":
    build_simulation()