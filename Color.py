from Vector import Vector


class Color(Vector):
    """
    En färgklass, precis som en vektor, tar emot x,y,z som representerar (R, G, B) värden.
    """

    @classmethod
    def from_hex_to_vector(cls, hex="#000000") -> "Color":
        """
        En statisk metod som omvandlar hex-kod färg till (RGB) färg.
        IN:
            - hex: str - färgen i hex format
        OUT: Color
        """
        return cls(
            int(hex[1:3], 16) / 255.0,
            int(hex[3:5], 16) / 255.0,
            int(hex[5:7], 16) / 255.0,
        )

    # de tre metoderna nedan definerar användbara färger att ha med för att slippa upprepning

    @classmethod
    def white(cls) -> "Color":
        # returnerar en instans av klass Color
        return cls.from_hex_to_vector("#FFFFFF")

    @classmethod
    def red(cls) -> "Color":
        return cls.from_hex_to_vector("#FF0000")

    @classmethod
    def black(cls) -> "Color":
        return cls.from_hex_to_vector("#000000")
