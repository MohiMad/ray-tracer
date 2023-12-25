from enum import Enum


class SphereType(Enum):
    """
    En Enum klass som används för att specifiera vilket typ en sfär är.
    Typerna är SPHERE = en sfär eller GROUND = marken.
    Denna klass används särskilt för att förhindra att marken blir klickbar.
    """

    SPHERE = 1
    GROUND = 2
