import sys
import os
import math
import pytest

# Ensure src is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.backend.core.formation_manager import FormationManager

def test_circle_formation():
    center = (0.5, 0.5)
    scale = 0.3
    count = 100

    points = FormationManager._circle(count, center, scale)

    assert len(points) == count

    for x, y, color in points:
        assert color == "default"
        # Check distance from center matches scale (allow small float error)
        dist = math.sqrt((x - center[0])**2 + (y - center[1])**2)
        assert math.isclose(dist, scale, rel_tol=1e-5)

def test_circle_formation_small_count():
    center = (0.5, 0.5)
    scale = 0.3
    count = 1

    points = FormationManager._circle(count, center, scale)
    assert len(points) == 1

    x, y, _ = points[0]
    # For count=1, angle is 0. cos(0)=1, sin(0)=0.
    # x = 0.5 + 1 * 0.3 = 0.8
    # y = 0.5 + 0 * 0.3 = 0.5
    assert math.isclose(x, 0.8)
    assert math.isclose(y, 0.5)

def test_circle_formation_zero_count():
    center = (0.5, 0.5)
    scale = 0.3
    count = 0

    points = FormationManager._circle(count, center, scale)
    assert len(points) == 0
