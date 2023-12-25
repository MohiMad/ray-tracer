from GameEngine import GameEngine
from SphereType import SphereType
from Vector import Vector
from Image import Image
from Color import Color
from Point import Point
from Sphere import Sphere
from Scene import Scene
from Engine import Engine
from Light import Light
from Material import Material

# Användargränssnittets storlek justeras här
WIDTH = 320 * 2
HEIGHT = 200 * 2

# 'kameran', d.v.s vart användaren befinner sig i 3D rummet
camera = Vector(0, 0, -1.5)
# marken är en stor orange sfär, av sfärtypen 'GROUND'.
ground = Sphere(
    Point(0, 10000.25, 1),
    10000.0,
    Material(Color.from_hex_to_vector("#FF7F00"), diffuse=1),
    SphereType.GROUND,
)

green_sphere = Sphere(
    Point(0, 0, 0), 0.25, Material(Color.from_hex_to_vector("#50C878"))
)

# red_sphere = Sphere(Point(0.25, -0.25, 0), 0.15, Material(Color.red()))

objects = [ground, green_sphere]
# vart ljuskällan befinner sig när man först startar programmet
light_point = Point(4.5, -5, -10.0)
light = Light(light_point, Color.white())
lights = [light]

scene = Scene(camera, objects, lights, WIDTH, HEIGHT)
engine = Engine(scene)

# allt sköts av game engine
game_engine = GameEngine(scene, engine, "Belysning av klot med Ray Tracing")
