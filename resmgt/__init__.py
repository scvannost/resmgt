__all__ = [
    "BasicSprite",
    "CircleSprite",
    "Game",
    "RectangleSprite",
    "SCREEN_HEIGHT",
    "SCREEN_WIDTH",
]

from .game import Game
from .settings import SCREEN_HEIGHT, SCREEN_WIDTH
from .sprites.base_sprites import BasicSprite, CircleSprite, RectangleSprite

__author__: str = "SC van Nostrand"
__email__: str = "scvannost@gmail.com"
__version__: str = "0.0.0"
