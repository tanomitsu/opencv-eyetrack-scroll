import numpy as np
from numpy.typing import NDArray
from typing import Any

Mat = NDArray[np.uint32]


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"Position ({self.x}, {self.y})"

    def to_tuple(self) -> tuple[int, int]:
        return (self.x, self.y)

    def __add__(self, other: Any) -> "Point":
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        elif isinstance(other, int):
            return Point(self.x + other, self.y + other)
        else:
            raise TypeError(f"You cannot add Point with {type(other)}.")

    def __iadd__(self, other: Any) -> "Point":
        new_point = self + other
        self.x = new_point.x
        self.y = new_point.y
        return self

    def __sub__(self, other: "Point") -> "Point":
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other: int) -> "Point":
        return Point(self.x * other, self.y * other)

    def __floordiv__(self, other: int) -> "Point":
        if other == 0:
            raise ValueError("You cannot divide by zero.")
        return Point(self.x // other, self.y // other)
