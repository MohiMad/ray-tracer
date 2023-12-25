import pygame
import numpy as np
from Color import Color
from Light import Light
from SphereType import SphereType
from Scene import Scene
from Vector import Vector
from Image import Image
from Color import Color
from Point import Point
from Sphere import Sphere
from Scene import Scene
from Engine import Engine
from Ray import Ray


class GameEngine:
    """
    En klass som sköter hela användargränssnittet. Tar hand om uppladdning av text och grafik samt andra användarintegreringar med programmet.
    IN:
        - scene: Scene - scenen som innehåller alla objekt etc.
        - engine: Engine - Ray-Tracing engine som sköter belysningsalgoritmen
        - caption: str - Vilken rubrik pygame programmet ska ha.
    """

    def __init__(self, scene: Scene, engine: Engine, caption: str):
        self.scene = scene
        self.engine = engine
        self.caption = caption
        # starta pygame
        pygame.init()
        self.font = pygame.font.SysFont("Arial", 20)
        self.screen = pygame.display.set_mode((self.scene.width, self.scene.height))

        pygame.display.set_caption(caption)

        self.running = True
        # is_calculating_rays används för att förhindra spam
        self.is_calculating_rays = False
        self.text_surface, self.text_rect = self.render_text("Loading...")
        # generera 'loading' text
        self.blit_text_and_flip(self.text_surface, self.text_rect)
        # hämta första 'bilden' av 3D rummet
        self.image = self.get_image()
        self.text = "Click on sphere to move light position, one click at a time."
        self.text_surface, self.text_rect = self.render_text(self.text)
        # hämta pygame image formatet
        self.pygame_image = self.generate_pygame_image(self.image)
        # starta huvud loopen för pygame
        self.main_loop()

    def get_light(self):
        # hämtar ljuset från scenen.
        return self.scene.lights[0]

    def update_light(self, light_point: Point) -> None:
        """
        Uppdaterar ljuset i scenen
        """
        light = Light(light_point, Color.white())
        lights = [light]

        self.scene.set_lights(lights)

    def get_image(self) -> np.array:
        """
        Ladda upp den nya bilden av scenen beroende på ljuskällans nya position.
        OUT: np.array som representerar alla pixlar i formatet som matchar pygame
        """
        # försök inte uppdatera bilden om den håller på att uppdateras
        if self.is_calculating_rays:
            return None

        # sätt till true innan vi börjar kalkylera
        self.is_calculating_rays = True

        # self.update_light(self.scene.lights[0])
        new_image = self.engine.render()

        return new_image

    def render_text(self, text: str) -> None:
        """
        Laddar upp text i övre vänstra hörnet av användargränssnittet.
        IN:
            - font: Vilken font som textstilen ska ha.
            - text: str - Texten som ska laddas upp.
        OUT: tuple - ger text_surface och text_rect som används för att rita text i pygame.
        """
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.bottomleft = (10, 25)
        return (text_surface, text_rect)

    def draw_black_rectangle(self) -> None:
        """
        Ritar en svart rektangel i området där text ska laddas upp.
        Behövs för att 'gömma' den tidigare-skriven texten från att överlappa med den nya.
        """
        pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, self.scene.width, 25))

    def generate_pygame_image(self, image):
        # skapar en ny pygame surface av den genererade bilden
        return pygame.surfarray.make_surface(image)

    def main_loop(self) -> None:
        """
        Huvud-loopen i pygame som checkar efter events och uppdaterar användargränssnittet
        """
        while self.running:
            self.run_event_loop()
            self.screen.blit(self.pygame_image, (0, 0))
            self.screen.blit(self.text_surface, self.text_rect)
            pygame.display.flip()
            # här reset:ar vi cooldown:en eftersom vi har nyligen laddat upp en ny bild!
            self.is_calculating_rays = False
        self.quit()

    def run_event_loop(self) -> None:
        """
        Event-loopen i pygame: checkar efter events som att trycka på 'x' knappen, trycka på ESC knappen och trycka på skärmen/sfären.
        """
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    # stäng programmet ifall man trycker på 'x' knappen
                    self.quit()
                case pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # ifall man trycker på 'esc' stäng av programmet
                        self.quit()
                case pygame.MOUSEBUTTONDOWN:
                    # ifall man trycker på skärmen med musen
                    self.handle_mousedown(event)

    def handle_mousedown(self, event) -> None:
        """
        Sköter clicks på skärmen.
        Om man trycker på en sfär uppdaterar den ljusets källa och laddar upp en ny bild av 3D rummet.

        IN: event - event-objektet från pygame
        """
        screen_point = self.engine.screen_pos_to_point(event.pos[0], event.pos[1])
        cursor_ray = self.engine.screen_pos_to_ray(screen_point)
        # om knappen är lika med 1, då är det en left-klick.
        # kolla om positionen från vilken användaren tryckte på genererar en stråle som träffar den gröna (eller en av) sfärerna.
        if not (event.button == 1 and self.any_sphere_intersection(cursor_ray)):
            return

        # ta bort tidigare text och informera användare om att vi laddar en ny bild
        self.draw_black_rectangle()
        text_surface, text_rect = self.render_text("Loading...")
        self.blit_text_and_flip(text_surface, text_rect)
        light_point = self.get_light().get_light_point()

        # justera ljuskällans x och y position beroende på vart användare tryckte
        light_point.x = screen_point.x * light_point.magnitude() * 10
        light_point.y = screen_point.y * light_point.magnitude() * 10
        # light_point.z = 0

        self.update_light(light_point)

        image = self.get_image()
        # om bilden är None, då håller användaren på att spamma left-click :/
        if image is not None:
            # generera text och bild
            self.pygame_image = self.generate_pygame_image(image)
            self.text_surface, self.text_rect = self.render_text(self.text)

    def any_sphere_intersection(self, ray: Ray) -> float | None:
        """
        Itererar igenom alla sfärer i scenen och returnerar True om en av sfärerna inte är av typen "GROUND" och skär strålen som genererades av cursor-positionen som användaren tryckte på.
        IN: ray - strålen som genererades av click:et
        OUT: bool - om någon av sfärerna (som inte är marken) träffades av strålen
        """
        return any(
            sphere.ray_intersection_distance(ray) and sphere.type != SphereType.GROUND
            for sphere in self.scene.objects
        )

    def blit_text_and_flip(self, text_surface, text_rect) -> None:
        """
        Genererar ny text på skärmen
        IN:
            text_surface, text_rect - textrelaterade instanser som genereras av self.render_text funktionen.
        """

        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()

    def quit(self) -> None:
        # avslutar både pygame och python CLI
        pygame.quit()
        quit()
