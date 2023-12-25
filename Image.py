from Color import Color


class Image:
    """
    En klass som representerar en bild, d.v.s en snapshot av 3D rummet som ska rendreras i pygame senare.
    """

    def __init__(self, width, height):
        """
        width: bildens/scenens bredd
        height: bildens/scenens höjd
        """
        self.width = width
        self.height = height
        black = Color.black()
        # pixels egenskapen innehåller alla pixlar i bilden.
        self.pixels = [[black for _ in range(width)] for _ in range(height)]

    def set_pixel_column(self, x: int, y: int, col: list[int]) -> None:
        """
        Ändrar en specifik kolumn i `pixels` matrisen.
        IN:
            - x: int - vilken rad (index)
            - y: int - vilken kolumn (index)
            - col: list - den nya kolumnen
        OUT: None
        """
        self.pixels[y][x] = col
