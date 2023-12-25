from Light import Light


class Scene:
    """
    En klass som representerar en 'scen'. Har en `objects` property som är en lista som innehåller alla objekt som existerar på scenen, exempelvis sfärer och ljuskällan.
    """

    def __init__(self, camera, objects, lights, width, height):
        """
        camera: Vector - En vektor som representerar vart 'kameran' ska befinna sig, d.v.s användarens POV.
        objects: list - En lista av olika objekt t.ex `Sphere` som befinner sig i scenen.
        lights: list - En lista av `Light` instanser som beskriver ljus, se beskrivning av Light klassen nedan.
        width: int/float - Bredden på användargränssnittet
        height: int/float - Höjden på användargränssnittet
        """
        self.camera = camera
        self.objects = objects
        self.lights = lights
        self.width = width
        self.height = height

    def set_lights(self, lights: list[Light]) -> None:
        self.lights = lights
