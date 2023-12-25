class Utility:
    """
    En klass som innehåller generella funktioner som kan vara användbara överallt och som inte är specifika till en viss klass.
    """

    @classmethod
    def clamp(cls, value: int | float) -> int | float:
        """
        Ser till att ett värde 'value' överskrider ej 255 vilket är gränsen för rgb värden.
        Input: 'value' (int) - det värde du vill 'clamp':a.
        Output: float|int - Det 'clamp':ade värdet.
        """
        return max(0, min(int(value * 255), 255))
