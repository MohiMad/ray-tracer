from Color import Color


class Light:
    """
    En klass som representerar ljus i 3D rummet.
    Ljus har en position och färg.
    """

    def __init__(self, position, color=Color.white()):
        """
        position: Vector - ljusets position i 3D rummet
        color: Color - ljusets färg, vitt är default.
        """
        self.position = position
        self.color = color

    def get_light_point(self):
        return self.position
