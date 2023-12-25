from Color import Color


class Material:
    """
    Beskriver egenskaper och beteende hos ett material när det interagerar med ljus.
    """

    def __init__(self, color=Color.white(), ambient=0.05, diffuse=1.0, specular=1.0):
        """
        color: Color - Färgen som representerar materialet.
        ambient: float - Reflekterande konstant som styr hur mycket omgivande ljus materialet reflekterar.
        diffuse: float - Diffus reflektanskonstant som styr hur mycket diffus reflektion materialet ger.
        specular: float - Spekulär reflektanskonstant som styr hur glänsande materialet är.
        """
        self.color = color
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular

    def get_color(self) -> Color:
        """
        En getter funktion som returnerar materialets färg.
        """
        return self.color
