import math
import pytest

from solver import ForceVector, analyze_system, resolve_forces


def test_perpendicular_forces():
    forces = [ForceVector("F1", 100.0, 0.0), ForceVector("F2", 100.0, 90.0)]
    data = analyze_system(forces)

    assert data["rx"] == pytest.approx(100.0)
    assert data["ry"] == pytest.approx(100.0)
    assert data["resultant_magnitude_n"] == pytest.approx(100.0 * math.sqrt(2.0))
    assert data["resultant_angle_deg"] == pytest.approx(45.0)
    assert data["equilibrant_angle_deg"] == pytest.approx(-135.0)
    assert data["in_equilibrium"] is False


def test_equilibrium_system():
    # Equal and opposite forces cancel out
    forces = [ForceVector("F1", 75.0, 0.0), ForceVector("F2", 75.0, 180.0)]
    data = analyze_system(forces)

    assert data["resultant_magnitude_n"] == pytest.approx(0.0)
    assert data["in_equilibrium"] is True


def test_resolve_forces_empty():
    resolved = resolve_forces([])
    assert resolved["fx"].size == 0
    assert resolved["fy"].size == 0