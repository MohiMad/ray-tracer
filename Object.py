from math import sqrt
from Point import Point


class Object:
    """
    Representerar ett objekt i 3D rummet.
       IN:
            - center: Vector - Vart mittpunkten på objektet ligger.
            - side_length: int/float - sidlängd, t.ex sidlängden på en kub.
            - material: Material - Vilket 'material' objektet ska ha.
    """

    def __init__(self, center, side_length, material):
        self.center = center
        self.side_length = side_length
        self.material = material

    def normal(self, surface_point: Point) -> float:
        """
        Beräknar normalen från en punkt på ytan och objektets mittpunkt.
        """
        return (surface_point - self.center).normalize()
