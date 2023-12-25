from Light import Light
from Scene import Scene


class Ray:
    """
    Representerar ett ljusstråle som har en ursprung (origin) och riktning (direction)
    origin: Point|Vector
    direction: Vector
    """

    def __init__(self, origin, direction):
        """
        origin: Vector|Point - strålens position
        direction: Vector|Point - strålens riktning
        """
        self.origin = origin
        self.direction = direction.normalize()

    def is_in_shadow(self, light: Light, scene: Scene) -> bool:
        """
        Avgör om strålen ligger i skugga-området genom att checka om det finns ett objekt mellan strålens origin och ljuskällan
        IN:
            - light: ljuskällan
            - scene: scenen med alla objekt
        OUT: boolean - om strålen ligger i skugga-området
        """
        light_distance = (light.position - self.origin).magnitude()

        for obj in scene.objects:
            hit_dist = obj.ray_intersection_distance(self)
            if hit_dist and hit_dist < light_distance:
                return True
        return False
