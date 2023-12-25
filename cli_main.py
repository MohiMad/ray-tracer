import math
import os


class Sphere:
    """
    Representerar en sfär som har radie (r) och x0, y0, z0 (mittpunkten).
    """

    def __init__(self, r, x0, y0):
        self.x0 = x0
        self.y0 = y0
        self.r = r
        self.z0 = self.calculate_z(x0, y0)

    def get_z_distance(self, x, y):
        """
        Beräknar z avståndet beroende på x,y och r värdena.
        IN:
            x: x-koordinat
            y: y-koordinat
        OUT: int|float - z avståndet
        """
        z_dist = self.r**2 - x**2 - y**2
        # returnerar 0 om avståndet är negativ!
        return 0 if z_dist < 0 else z_dist

    def calculate_z(self, x, y):
        """
        Beräknar z beroende på x,y värdena.
        IN:
            x: x-koordinat
            y: y-koordinat
        OUT: float - z-koordinaten
        """
        return math.sqrt(self.get_z_distance(x, y))

    def is_point_inside_sphere(self, x, y):
        """
        Avgör om en punkt ligger i sfären genom att kolla om summan av koordinaten är större än radien.
        IN:
            x: x-koordinat
            y: y-koordinat
        OUT: bool
        """
        return x**2 + y**2 < self.r**2


class Scene:
    """
    Innehåller alla pixlar och operationer för att lagra pixlar.
    """

    def __init__(self):
        self.pixels = []

    def add_row(self, row):
        # lägger till en row i pixels listan
        # IN: row - list
        # OUT: None
        self.pixels.append(row)


class Engine:
    """
    Behandlar visualisationen och beräkningar
    """

    def __init__(self, sphere, scene, steps):
        self.sphere = sphere
        self.scene = scene
        self.steps = steps

    def get_character_intensity(self, i):
        """
        Hämtar vilken karaktär som motsvarar respektive ljusintensitetsnivå.
        IN: i - intensiteten
        OUT: string - karaktär som motsvarar respektive ljusintensitetsnivå
        """
        if i <= 0:
            return "M"
        elif 0 < i <= 0.3:
            return "*"
        elif 0.3 < i <= 0.5:
            return "+"
        elif 0.5 < i <= 0.7:
            return "-"
        elif 0.7 < i <= 0.9:
            return "."
        else:
            return " "

    def calculate_intensity(self, x, y):
        """
        Beräknar ljusintensistet enligt metoden givet i uppgiftbeskrivningen.
        IN:
            - x: x-koordinaten
            - y: y-koordinaten
        OUT: float - ljusintensistet
        """
        z = self.sphere.calculate_z(x, y)
        b = (
            x * self.sphere.x0 + y * self.sphere.y0 + z * self.sphere.z0
        ) / self.sphere.r**2
        return b

    def is_in_shadow(self, x, y):
        """
        Avgör om en punkt ligger i skugga. Under antagandet att ljuskällan befinner sig till höger och upp.
        IN:
            - x: x-koordinaten
            - y: y-koordinaten
        OUT: bool - Om punkten befinner sig i skuggan
        """
        return (x < 0 and y > 0) and not self.sphere.is_point_inside_sphere(x, y)

    def generate_light(self):
        # skapar ljusmönster
        y_step = int((self.sphere.r / self.steps) * 2) + 1
        x_step = int(self.sphere.r / self.steps) + 1

        for y in range(-self.sphere.r, self.sphere.r, y_step):
            row = []
            for x in range(
                -self.sphere.r,
                self.sphere.r,
            ):
                if self.is_in_shadow(x, y):
                    row.append("#")  # Shadow character
                else:
                    i = self.calculate_intensity(x, y)
                    row.append(self.get_character_intensity(i))
            self.scene.add_row(row)

    def display_scene(self):
        # ritar ut 'scenen' genom att skriva ut alla 'pixlar' i pixels
        for row in self.scene.pixels:
            print("".join(row))


def ask_input_and_check(msg, checker_func=None):
    """
    Frågar användaren för input i all oändlighet ti
    """
    x = input(msg)
    try:
        num = int(x)
        if checker_func is not None:
            (bool_value, output_msg) = checker_func(num)
            if bool_value == True:
                return num
            else:
                ask_input_and_check(output_msg + msg, checker_func)
        else:
            return num
    except ValueError:
        ask_input_and_check("Invalid input. " + msg)


def check_radius(r):
    return (True, 0) if r > 0 else (False, "Radien får ej vara negativ!\n")


def check_distance(r, x, y):
    # checkar om avståndet är större än radie -> resulterar i negativ z!
    """
    IN: radien (int), x-koord (int), y-koord(int)
    OUT: bool. Om värdena resulterar i negativ z.
    """
    return x**2 + y**2 >= r**2


def main():
    r = ask_input_and_check("Ange radien: ", check_radius)
    x = ask_input_and_check("Ange x-koordinaten för sfären: ")
    y = ask_input_and_check("Ange y-koordinaten för sfären: ")
    steps = 70

    while check_distance(r, x, y):
        print("Dina x och y värden ger negativa z! Testa igen.")
        x = ask_input_and_check("Ange x-koordinaten för sfären: ")
        y = ask_input_and_check("Ange y-koordinaten för sfären: ")

    sphere = Sphere(r, x, y)

    scene = Scene()
    engine = Engine(sphere, scene, steps)
    engine.generate_light()
    engine.display_scene()


main()
