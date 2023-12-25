from Object import Object
from Ray import Ray
from SphereType import SphereType
from math import sqrt


class Sphere(Object):
    """
    En klass som representerar en sfär i 3D rummet. Inherit:ar Object eftersom det är ett objekt i 3D rummet.
        IN:
            - center: Vector - Vart mittpunkten på sfären ligger.
            - radius: int/float - Radien
            - material: Material - Vilket 'material' sfären har.
            - type: SphereType (optional) - vilken typ av sfär
    """

    def __init__(self, center, radius, material, type=SphereType.SPHERE):
        # anropa initiate i Object klassen
        super().__init__(center, radius, material)
        # från Object sidlängd = radius
        self.radius = self.side_length
        self.type = type

    def ray_intersection_distance(self, ray: Ray) -> float | None:
        """
        Beräknar och returnerar avståndet från punkten på sfären som träffas av ray.
        Returnerar None om ray inte träffar sfären, annars avståndet (> 0)
        """
        obj_to_ray = ray.origin - self.center
        a = 1
        b = 2 * ray.direction.dot_product(obj_to_ray)
        c = obj_to_ray.dot_product(obj_to_ray) - (self.radius) ** 2
        discriminant = b**2 - 4 * c

        if discriminant >= 0:
            dist = (-b - sqrt(discriminant)) / 2
            if dist > 0:
                return dist
        return None
