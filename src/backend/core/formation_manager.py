import math
import random
from typing import List, Tuple, Optional

class FormationManager:
    """
    Generates coordinate sets for particle formations.
    Coordinates are normalized (0.0 to 1.0).
    """

    @staticmethod
    def get_formation(shape: str, count: int, center: Tuple[float, float] = (0.5, 0.5), scale: float = 0.3) -> List[Tuple[float, float, str]]:
        """
        Returns a list of (x, y, color_hint) tuples.
        """
        shape = shape.lower().strip()
        points = []

        if shape == "circle" or shape == "ring":
            points = FormationManager._circle(count, center, scale)
        elif shape == "square" or shape == "box":
            points = FormationManager._square(count, center, scale)
        elif shape == "line" or shape == "horizontal":
            points = FormationManager._line(count, center, scale)
        elif shape == "vertical":
            points = FormationManager._vertical_line(count, center, scale)
        elif shape == "spiral" or shape == "vortex":
            points = FormationManager._spiral(count, center, scale)
        elif shape == "cross" or shape == "x":
            points = FormationManager._cross(count, center, scale)
        else:
            # Default to random scatter (Nebula)
            points = FormationManager._scatter(count, center, scale)

        return points

    @staticmethod
    def _circle(count: int, center: Tuple[float, float], scale: float) -> List[Tuple[float, float, str]]:
        cx, cy = center
        points = []
        for i in range(count):
            angle = (i / count) * 2 * math.pi
            x = cx + math.cos(angle) * scale
            # Aspect ratio correction could be applied here if needed, but assuming square canvas for now
            y = cy + math.sin(angle) * scale
            points.append((x, y, "default"))
        return points

    @staticmethod
    def _square(count: int, center: Tuple[float, float], scale: float) -> List[Tuple[float, float, str]]:
        cx, cy = center
        points = []
        side = scale * 2
        per_side = count // 4
        # Top
        for i in range(per_side):
            x = cx - scale + (i / per_side) * side
            y = cy - scale
            points.append((x, y, "default"))
        # Right
        for i in range(per_side):
            x = cx + scale
            y = cy - scale + (i / per_side) * side
            points.append((x, y, "default"))
        # Bottom
        for i in range(per_side):
            x = cx + scale - (i / per_side) * side
            y = cy + scale
            points.append((x, y, "default"))
        # Left
        for i in range(count - 3 * per_side): # Remainder
            x = cx - scale
            y = cy + scale - (i / (count - 3 * per_side)) * side
            points.append((x, y, "default"))
        return points

    @staticmethod
    def _line(count: int, center: Tuple[float, float], scale: float) -> List[Tuple[float, float, str]]:
        cx, cy = center
        points = []
        start_x = cx - scale
        width = scale * 2
        for i in range(count):
            x = start_x + (i / count) * width
            y = cy
            points.append((x, y, "default"))
        return points

    @staticmethod
    def _vertical_line(count: int, center: Tuple[float, float], scale: float) -> List[Tuple[float, float, str]]:
        cx, cy = center
        points = []
        start_y = cy - scale
        height = scale * 2
        for i in range(count):
            x = cx
            y = start_y + (i / count) * height
            points.append((x, y, "default"))
        return points

    @staticmethod
    def _spiral(count: int, center: Tuple[float, float], scale: float) -> List[Tuple[float, float, str]]:
        cx, cy = center
        points = []
        rotations = 3
        for i in range(count):
            progress = i / count
            angle = progress * rotations * 2 * math.pi
            radius = progress * scale
            x = cx + math.cos(angle) * radius
            y = cy + math.sin(angle) * radius
            points.append((x, y, "default"))
        return points

    @staticmethod
    def _cross(count: int, center: Tuple[float, float], scale: float) -> List[Tuple[float, float, str]]:
        cx, cy = center
        points = []
        half = count // 2
        # Horizontal
        for i in range(half):
            x = (cx - scale) + (i / half) * (scale * 2)
            y = cy
            points.append((x, y, "default"))
        # Vertical
        remainder = count - half
        for i in range(remainder):
            x = cx
            y = (cy - scale) + (i / remainder) * (scale * 2)
            points.append((x, y, "default"))
        return points

    @staticmethod
    def _scatter(count: int, center: Tuple[float, float], scale: float) -> List[Tuple[float, float, str]]:
        cx, cy = center
        points = []
        for _ in range(count):
            # Random inside circle
            angle = random.random() * 2 * math.pi
            radius = math.sqrt(random.random()) * scale
            x = cx + math.cos(angle) * radius
            y = cy + math.sin(angle) * radius
            points.append((x, y, "default"))
        return points
