__all__ = [
    "BasicSprite",
    "CircleSprite",
    "RectangleSprite",
    "SPRITE_GROUPS",
]

from collections import defaultdict
from math import sqrt
from typing import Dict, List, Optional, Tuple

import pygame
from pygame.locals import (
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_UP,
)

from ..settings import SCREEN_HEIGHT, SCREEN_WIDTH

SPRITE_GROUPS: Dict[str, pygame.sprite.Group] = defaultdict(pygame.sprite.Group)


class BasicSprite(pygame.sprite.Sprite):
    """
    A base class for all simple sprites
    They must have a location and speed

    Parameters
    ----------
    location: Optional[Tuple[float, float]] = None
        where in the game the sprite should be rendered
        this means slightly different things for each sprite atm
    speed: Optional[float] = None
        the top speed that the sprite can move in total

    Attributes
    ----------
    location: Tuple[float, float] = (250.0, 250.0)
        where in the game the sprite should be rendered
        this means slightly different things for each sprite atm
    rect: pygame.rect.RectType
        the underlying pygame rect for this sprite
    speed: float = 10.0
        the top speed that the sprite can move in total

    Methods
    -------
    draw(self, surface: pygame.SurfaceType) -> None
        implements rendering the sprite onto the given surface
        no need to call pygame.display.flip()
    move(self, pressed_keys: Dict[int, bool]) -> None
        implements movement of the sprite given the key-presses
        the distance moved is according to self.speed
    """

    location: Tuple[float, float] = (250.0, 250.0)
    rect: pygame.rect.RectType
    speed: float = 10.0

    def __init__(
        self,
        location: Optional[Tuple[float, float]] = None,
        speed: Optional[float] = None,
    ) -> None:
        super().__init__()
        if location is not None:
            self.location = location
        if speed is not None:
            self.speed = speed
        SPRITE_GROUPS[type(self)].add(self)

    def move(self, pressed_keys: Dict[int, bool]) -> None:
        """
        Implements movement of the sprite given the key-presses
        The distance moved is according to self.speed
        """
        if not self.speed:
            return

        xy: List[float, float] = [0.0, 0.0]
        if pressed_keys[K_UP]:
            xy[1] -= 1
        if pressed_keys[K_DOWN]:
            xy[1] += 1
        if pressed_keys[K_LEFT]:
            xy[0] -= 1
        if pressed_keys[K_RIGHT]:
            xy[0] += 1

        r: float = sqrt(sum(abs(x) ** 2 for x in xy))
        if r:
            xy = [xy[0] / r * self.speed, xy[1] / r * self.speed]

        self.rect.move_ip(xy[0], xy[1])

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class CircleSprite(BasicSprite):
    """
    A simple sprite in the shape of a circle

    Parameters
    ----------
    bg_color: Optional[Tuple[int, int, int]] = None
        the base background color to fill the screen with before drawing anything else
        in the format (r,g,b)
    color: Optional[Tuple[int, int, int]] = None
        the color to fill the sprite, in the format (r,g,b)
    location: Optional[Tuple[float, float]] = None
        where in the game the sprite should be rendered
        this means slightly different things for each sprite atm
    radius: Optional[float] = None
        the distance from the location that the circle should occupy
    rect: pygame.rect.RectType
        the underlying pygame rect for this sprite
    speed: Optional[float] = None
        the top speed that the sprite can move in total

    Attributes
    ----------
    bg_color: Tuple[int, int, int] = (255, 255, 255)
        the base background color to fill the screen with before drawing anything else
        in the format (r,g,b)
    color: Tuple[int, int, int] = (0, 0, 255)
        the color to fill the sprite, in the format (r,g,b)
    location: Tuple[float, float] = (250.0, 250.0)
        where in the game the sprite should be rendered
        this means slightly different things for each sprite atm
    radius: float = 75.0
        the distance from the location that the circle should occupy
    speed: float = 10.0
        the top speed that the sprite can move in total
    surf: pygame.Surface
        the underlying pygame surface of the sprite

    Methods
    -------
    draw(self, surface: pygame.SurfaceType) -> None
        implements rendering the sprite onto the given surface
        no need to call pygame.display.flip()
    move(self, pressed_keys: Dict[int, bool]) -> None
        implements movement of the sprite given the key-presses
        the distance moved is according to self.speed
    """

    bg_color: Tuple[int, int, int] = (255, 255, 255)  # (r,g,b)
    color: Tuple[int, int, int] = (0, 0, 255)
    radius: float = 75.0
    surf: pygame.Surface

    def __init__(
        self,
        bg_color: Optional[Tuple[int, int, int]] = None,  # (r,g,b)
        color: Optional[Tuple[int, int, int]] = None,
        location: Optional[Tuple[float, float]] = None,
        radius: Optional[float] = None,
        speed: Optional[float] = None,
    ) -> None:
        super().__init__(location=location, speed=speed)
        if bg_color is not None:
            self.bg_color = bg_color
        if color is not None:
            self.color = color
        if radius is not None:
            self.radius = radius

        self.surf = pygame.Surface(
            size=(self.radius * 2, self.radius * 2),
        )
        self.surf.fill(self.bg_color)
        self.surf.set_colorkey(self.bg_color, pygame.RLEACCEL)
        # Give the surface a color to separate it from the background
        self.rect = pygame.draw.circle(
            surface=self.surf,
            color=self.color,
            center=(self.radius, self.radius),
            radius=self.radius,
        )
        self.rect.move_ip(*self.location)


class RectangleSprite(BasicSprite):
    """
    A simple sprite in the shape of a rectangle

    Parameters
    ----------
    color: Optional[Tuple[int, int, int]] = None
        the color to fill the sprite, in the format (r,g,b)
    location: Optional[Tuple[float, float]] = None
        where in the game the sprite should be rendered
        this means slightly different things for each sprite atm
    size: Tuple[float, float] = (50.0, 50.0)
        the width and height the rectangle should occupy
        the top-left corner is at the given location
    speed: Optional[float] = None
        the top speed that the sprite can move in total

    Attributes
    ----------
    color: Tuple[int, int, int] = (0, 0, 255)
        the color to fill the sprite, in the format (r,g,b)
    location: Tuple[float, float] = (250.0, 250.0)
        where in the game the sprite should be rendered
        this means slightly different things for each sprite atm
    rect: pygame.rect.RectType
        the underlying pygame rect for this sprite
    size: Tuple[float, float] = (50.0, 50.0)
        the width and height the rectangle should occupy
        the top-left corner is at the given location
    speed: float = 10.0
        the top speed that the sprite can move in total
    surf: pygame.Surface
        the underlying pygame surface of the sprite

    Methods
    -------
    draw(self, surface: pygame.SurfaceType) -> None
        implements rendering the sprite onto the given surface
        no need to call pygame.display.flip()
    move(self, pressed_keys: Dict[int, bool]) -> None
        implements movement of the sprite given the key-presses
        the distance moved is according to self.speed
    """

    color: Tuple[int, int, int] = (0, 0, 255)
    size: Tuple[float, float] = (50.0, 50.0)
    surf: pygame.Surface

    def __init__(
        self,
        location: Optional[Tuple[float, float]] = None,
        color: Optional[Tuple[int, int, int]] = None,
        size: Optional[Tuple[float, float]] = None,
        speed: Optional[float] = None,
    ) -> None:
        super().__init__(location=location, speed=speed)
        if color is not None:
            self.color = color
        if size is not None:
            self.size = size

        self.surf = pygame.Surface(size=self.size)
        # Give the surface a color to separate it from the background
        self.rect = self.surf.fill(color=(0, 0, 0))
        self.rect.move_ip(*self.location)
        self.image = self.surf


# set up types for sprite rendering order
for sprite_type in [
    BasicSprite,
    CircleSprite,
    RectangleSprite,
]:
    SPRITE_GROUPS[sprite_type]
