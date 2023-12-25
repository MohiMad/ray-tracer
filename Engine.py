import numpy as np
from Image import Image
from Ray import Ray
from Point import Point
from Color import Color
from Utility import Utility
from Object import Object
from typing import Tuple


class Engine:
    """
    Implementerar ray-tracing algoritmen för att rita ut alla objekt på en scen.
    """

    def __init__(self, scene):
        """
        Scen: Scene - Scenen som innehåller allt. Används för att beräkna 'konstanter' med vilka man kan omvandla en koordinat i 3D-rum till en koordinat i pixel-format
        """
        # vi initierar dessa värden här för att kunna ha tillgång till dem utanför Engine klassen också
        self.scene = scene
        aspect_ratio = float(scene.width) / scene.height
        self.x_0 = -1.0
        x_1 = 1.0

        self.x_step = (x_1 - self.x_0) / (scene.width - 1)
        self.y_0 = -1.0 / aspect_ratio
        y_1 = 1.0 / aspect_ratio
        self.y_step = (y_1 - self.y_0) / (scene.height - 1)

    def render(self) -> np.array:
        """
        Genererar en np.array som används i pygame surface för att render:a 3D rummet.
        render funktionen 'ritar ut' 3D rummet och utför loop:en för att färgsätta varje pixel.
        OUT: np.array - listan som korresponderar till varje pixel på skärmen i lämplig format som passar pygame.
        """

        width, height = self.scene.width, self.scene.height

        camera = self.scene.camera
        pixels = Image(width, height)
        data = np.zeros((height, width, 3), dtype=np.uint8)

        for j in range(height):
            y = self.y_0 + j * self.y_step
            for i in range(width):
                x = self.x_0 + i * self.x_step
                ray = Ray(camera, Point(x, y) - camera)

                color = self.ray_trace_and_return_pixel_color(ray)

                data[j, i] = [
                    Utility.clamp(color.x),
                    Utility.clamp(color.y),
                    Utility.clamp(color.z),
                ]

        return np.transpose(
            data, (1, 0, 2)
        )  # Transponera för att matcha 'pygames surface format'

    def screen_pos_to_point(self, screen_x: int, screen_y: int) -> Point:
        """
        Omvandlar en pixel-koordinat till en '3D' koordinat i vårt 3D rum.
        IN:
            - screen_x: int - x-pixel-koordinaten
            - screen_y: int - y-pixel-koordinaten
        OUT: Point - Koordinaten i 3D-punktsformat.
        """
        x = self.x_0 + screen_x * self.x_step
        y = self.y_0 + screen_y * self.y_step
        return Point(x, y)

    def screen_pos_to_ray(self, screen_point: Point) -> Ray:
        """
        Skapar en stråle av 3D-punktskoordinaten.
        IN:
            - screen_point: Point - koordinaten i 3D
        OUT: Ray - En stråle skapad av punktskoordinaten given.
        """
        ray_direction = screen_point - self.scene.camera

        return Ray(self.scene.camera, ray_direction.normalize())

    def ray_trace_and_return_pixel_color(self, ray: Ray) -> Color:
        """
        Räknar ut vilken färg en viss stråle resulterar i för den närmast-träffat objekt.
        IN: ray: Ray - strålen i fråga
        OUT: Color - färgen som strålen resulterar i för det närmast träffade objektet på skärmen.
        """
        # initialvärde = svart
        color = Color.black()

        # hitta närmaste objektet som strålen träffar
        dist_hit, obj_hit = self.find_nearest_and_return_distance_and_hit_object(ray)
        # returnerar svart om strålen träffar ingenting
        if obj_hit is None:
            return color

        hit_pos = ray.origin + ray.direction * dist_hit
        hit_normal = obj_hit.normal(hit_pos)
        color += self.color_at(obj_hit, hit_pos, hit_normal)
        return color

    def find_nearest_and_return_distance_and_hit_object(
        self, ray: Ray
    ) -> Tuple[float | None, Object | None]:
        """
        Itererar igenom alla objekt och returnerar avståndet samt det närmaste objektet som blev träffad.
        IN:
            - ray: Ray - strålen som ska undersökas
        OUT: Tupel som innehåller det minsta avståndet (eller None) från strålen till objektet samt objektet som träffades (eller None ifall den inte träffar något)
        """
        dist_min = None
        obj_hit = None

        for obj in self.scene.objects:
            dist = obj.ray_intersection_distance(ray)
            if dist is not None and (obj_hit is None or dist < dist_min):
                dist_min = dist
                obj_hit = obj
        return (dist_min, obj_hit)

    def color_at(self, obj_hit: Object, hit_pos: Point, normal: float) -> Color:
        """
        Beräknar vilken färg en viss punkt på ett objekt kommer att ha beroende på objektets material
        """
        material = obj_hit.material
        obj_color = material.get_color()
        to_cam = self.scene.camera - hit_pos
        specular_k = 50
        color = material.ambient * Color.white()

        # Vi beräknar hur ljuset påverkar färgen på objektet i en viss koordinat
        for light in self.scene.lights:
            to_light = Ray(hit_pos, light.position - hit_pos)
            light_dir = (light.position - hit_pos).normalize()

            # skapa en stråle som befinner sig en liten bit framför träffytan så den inte kolliderar med objektet redan vid start
            shadow_ray = Ray(hit_pos + normal * 0.001, light_dir)

            # Om 'skuggstrålen' är i skuggområdet, applicera inte diffuse och specular
            if shadow_ray.is_in_shadow(light, self.scene):
                continue

            # Diffuse shading (Lambert)
            color += (
                obj_color
                * material.diffuse
                * max(normal.dot_product(to_light.direction), 0)
            )
            # Specular shading (Blinn-Phong)
            half_vector = (to_light.direction + to_cam).normalize()
            color += (
                light.color
                * material.specular
                * max(normal.dot_product(half_vector), 0) ** specular_k
            )
        return color
