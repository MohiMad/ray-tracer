import math
from typing import Tuple


"""
En 3D Vektor klass som kommer att representera nödvändiga vektorer i 'raytracer:n'. 
{x}: värdet i x-riktning
{y}: värdet i y-riktning
{z}: värdet i z-riktning

Klassen innehåller metoder som föreklar bearbetning av vektorerna, dels vanliga operatorer som +, -, * och division men också metoder som beräknar vanliga kvantitet.


OBS: Kommer att utvidgas med en numpy-vektor representation för förhoppningsvis snabbare kalkulationer
"""


class Vector:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    # beräknar magnituden av vektorn
    def magnitude(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    # normaliserar vektorn
    def normalize(self) -> "Vector":
        mag = self.magnitude()
        return Vector(self.x / mag, self.y / mag, self.z / mag)

    # definerar 'dot product' operation mellan två vektorer
    def dot_product(self, v: "Vector") -> "Vector":
        return self.x * v.x + self.y * v.y + self.z * v.z

    # definerar skalärmultipikation
    def multiply_by_scalar(self, scalar: int | float) -> "Vector":
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)

    # definerar kryssprodukten av två vektorer
    def cross_product(self, v: "Vector") -> "Vector":
        return Vector(
            self.y * v.z - self.z * v.y,
            self.z * v.x - self.x * v.z,
            self.x * v.y - self.y * v.x,
        )

    # addition av vektorer
    def __add__(self, v: "Vector") -> "Vector":
        return Vector(self.x + v.x, self.y + v.y, self.z + v.z)

    # subtraktion av vektorer
    def __sub__(self, v: "Vector") -> "Vector":
        return Vector(self.x - v.x, self.y - v.y, self.z - v.z)

    # multipikation av vektorer från vänster
    def __mul__(self, v: "Vector") -> "Vector":
        assert not isinstance(v, Vector)
        return Vector(self.x * v, self.y * v, self.z * v)

    # multipikation av vektorer från höger
    def __rmul__(self, other: "Vector") -> "Vector":
        return self.__mul__(other)

    # division av två vektorer
    def __truediv__(self, other: "Vector") -> "Vector":
        assert not isinstance(other, Vector)
        return Vector(self.x / other, self.y / other, self.z / other)

    # behövs för att formattera vektorn, kommer behövas för debugging
    def __str__(self) -> str:
        return f"({self.x}, {self.y}, {self.z})"

    # omvandling av vektorn till tupel-form
    def to_tuple(self) -> Tuple[int | float, int | float, int | float]:
        return (self.x, self.y, self.z)
