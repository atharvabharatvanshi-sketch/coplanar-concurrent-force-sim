from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class ForceVector:
    """Represents a single force in a coplanar concurrent force system."""
    label: str
    magnitude_n: float
    angle_deg: float  # Counter-clockwise from +x axis


def resolve_forces(forces: list[ForceVector]) -> dict[str, np.ndarray]:
    """Resolve all forces into Fx and Fy arrays (in Newtons)."""
    if not forces:
        empty = np.array([], dtype=float)
        return {"fx": empty, "fy": empty}

    magnitudes = np.array([f.magnitude_n for f in forces], dtype=float)
    angles_rad = np.deg2rad(np.array([f.angle_deg for f in forces], dtype=float))

    fx = magnitudes * np.cos(angles_rad)
    fy = magnitudes * np.sin(angles_rad)
    return {"fx": fx, "fy": fy}


def analyze_system(forces: list[ForceVector], tol: float = 1e-6) -> dict[str, object]:
    """
    Compute resultant force, equilibrant force, equilibrium status,
    and the single missing force needed to balance the system.
    """
    resolved = resolve_forces(forces)
    fx = resolved["fx"]
    fy = resolved["fy"]

    rx = float(np.sum(fx)) if fx.size else 0.0
    ry = float(np.sum(fy)) if fy.size else 0.0

    # Clean floating-point noise near zero
    if abs(rx) < tol:
        rx = 0.0
    if abs(ry) < tol:
        ry = 0.0

    r_mag = float(np.hypot(rx, ry))
    in_equilibrium = r_mag <= tol

    r_angle_deg = 0.0 if in_equilibrium else float(np.rad2deg(np.arctan2(ry, rx)))

    # Equilibrant F_eq = -R keeps the system in static equilibrium
    eq_x = -rx
    eq_y = -ry
    eq_mag = r_mag
    eq_angle_deg = 0.0 if in_equilibrium else float(np.rad2deg(np.arctan2(eq_y, eq_x)))

    return {
        "fx": fx,
        "fy": fy,
        "rx": rx,
        "ry": ry,
        "resultant_magnitude_n": r_mag,
        "resultant_angle_deg": r_angle_deg,
        "equilibrant_magnitude_n": eq_mag,
        "equilibrant_angle_deg": eq_angle_deg,
        "in_equilibrium": in_equilibrium,
    }


def format_steps(forces: list[ForceVector]) -> str:
    """Return a clean step-by-step mathematical breakdown of the resultant."""
    data = analyze_system(forces)
    lines = ["=== COPLANAR CONCURRENT FORCE SYSTEM: STEP-BY-STEP ==="]

    for idx, f in enumerate(forces, start=1):
        fx_i = data["fx"][idx - 1]
        fy_i = data["fy"][idx - 1]
        lines.append(
            f"{idx}. {f.label}: F = {f.magnitude_n:.4f} N at {f.angle_deg:.2f} deg "
            f"-> Fx = {fx_i:.4f} N, Fy = {fy_i:.4f} N"
        )

    rx = data["rx"]
    ry = data["ry"]
    r_mag = data["resultant_magnitude_n"]
    r_ang = data["resultant_angle_deg"]
    eq_mag = data["equilibrant_magnitude_n"]
    eq_ang = data["equilibrant_angle_deg"]

    lines.append(f"Sum of X-components (Rx): {rx:.4f} N")
    lines.append(f"Sum of Y-components (Ry): {ry:.4f} N")
    lines.append(f"Resultant Magnitude (R = sqrt(Rx^2 + Ry^2)): {r_mag:.4f} N")
    lines.append(f"Resultant Angle (atan2(Ry, Rx)): {r_ang:.4f} deg")

    if data["in_equilibrium"]:
        lines.append("Status: System is in STATIC EQUILIBRIUM (R = 0 N).")
    else:
        lines.append(
            f"Equilibrant Force to balance system: {eq_mag:.4f} N at {eq_ang:.4f} deg"
        )

    return "\n".join(lines)


if __name__ == "__main__":
    sample_forces = [
        ForceVector("F1", 120.0, 30.0),
        ForceVector("F2", 85.0, 135.0),
        ForceVector("F3", 60.0, 250.0),
    ]
    print(format_steps(sample_forces))