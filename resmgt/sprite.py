__all__ = [
    "BasicSprite",
    "CircleSprite",
    "RectangleSprite",
]

from typing import Dict, List, Optional, Tuple
import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
)

from .settings import SCREEN_HEIGHT, SCREEN_WIDTH


class BasicSprite(pygame.sprite.Sprite):
    """
    A base class for all simple sprites
    They must have a color, location, and speed

    Parameters
    ----------
    color: Optional[Tuple[int, int, int]] = None
        the color to fill the sprite, in the format (r,g,b)
    location: Optional[Tuple[float, float]] = None
        where in the game the sprite should be rendered
        this means slightly different things for each sprite atm
    speed: Optional[float] = None
        the top speed that the sprite can move in total

    Attributes
    ----------
    color: Tuple[int, int, int] = (0, 0, 255)
        the color to fill the sprite, in the format (r,g,b)
    location: Tuple[float, float] = (250.0, 250.0)
        where in the game the sprite should be rendered
        this means slightly different things for each sprite atm
    speed: float = 5.0
        the top speed that the sprite can move in total

    Methods
    -------
    draw(self, surface: pygame.SurfaceType) -> None
        a function to implement rendering the sprite onto the given surface
        no need to call pygame.display.flip()
    move(self, pressed_keys: Dict[int, bool]) -> None
        a function to implement movement of the sprite given the key-presses
        the distance moved is according to the speed of the sprite
        skipped if not self.speed
    """

    color: Tuple[int, int, int] = (0, 0, 255)
    location: Tuple[float, float] = (250.0, 250.0)
    rect: pygame.rect.RectType
    speed: float = 5.0
    surf: pygame.SurfaceType

    def __init__(
        self,
        color: Optional[Tuple[int, int, int]] = None,
        location: Optional[Tuple[float, float]] = None,
        speed: Optional[float] = None,
    ) -> None:
        super().__init__()
        if color is not None:
            self.color = color
        if location is not None:
            self.location = location
        if speed is not None:
            self.speed = speed

    def draw(self, screen: pygame.SurfaceType) -> None:
        """
        Draw the top-left corner of the rectangle at self.location
        """
        screen.blit(self.surf, self.rect)

    def move(self, pressed_keys: Dict[int, bool]) -> None:
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

        r: float = sum(abs(x) for x in xy)
        if r:
            xy = [xy[0] / r * self.speed, xy[1] / r * self.speed]

        self.rect.move_ip(xy[0], xy[1])

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class CircleSprite(BasicSprite):
    """
    A simple sprite in the shape of a circle
    They must have a color, location, and radius

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
    speed: Optional[float] = None
        the top speed that the sprite can move in total

    Attributes
    ----------
    color: Tuple[int, int, int] = (0, 0, 255)
        the color to fill the sprite, in the format (r,g,b)
    location: Tuple[float, float] = (250.0, 250.0)
        where in the game the sprite should be rendered
        this means slightly different things for each sprite atm
    radius: float = 75.0
        the distance from the location that the circle should occupy
    speed: float = 5.0
        the top speed that the sprite can move in total

    Methods
    -------
    draw(self, surface: pygame.SurfaceType) -> None
        a function to implement rendering the sprite onto the given surface
        no need to call pygame.display.flip()
    move(self, pressed_keys: Dict[int, bool]) -> None
        a function to implement movement of the sprite given the key-presses
        the distance moved is according to the speed of the sprite
        skipped if not self.speed just in case
    """

    bg_color: Tuple[int, int, int] = (255, 255, 255)  # (r,g,b)
    radius: float = 75.0

    def __init__(
        self,
        bg_color: Optional[Tuple[int, int, int]] = None,  # (r,g,b)
        color: Optional[Tuple[int, int, int]] = None,
        location: Optional[Tuple[float, float]] = None,
        radius: Optional[float] = None,
        speed: Optional[float] = None,
    ) -> None:
        super().__init__(color=color, location=location, speed=speed)
        if radius is not None:
            self.radius = radius
        if bg_color is not None:
            self.bg_color = bg_color

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
    They must have a color, location, and size

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
    size: Optional[Tuple[float, float]] = None
        the width and height the rectangle should occupy
        the top-left corner is at the given location
    speed: float = 5.0
        the top speed that the sprite can move in total

    Methods
    -------
    draw(self, surface: pygame.SurfaceType) -> None
        a function to implement rendering the sprite onto the given surface
        no need to call pygame.display.flip()
    move(self, pressed_keys: Dict[int, bool]) -> None
        a function to implement movement of the sprite given the key-presses
        the distance moved is according to the speed of the sprite
        skipped if not self.speed
    """

    size: Tuple[float, float] = (50.0, 50.0)

    def __init__(
        self,
        location: Tuple[float, float],
        color: Optional[Tuple[int, int, int]] = None,
        size: Optional[Tuple[float, float]] = None,
        speed: Optional[float] = None,
    ) -> None:
        super().__init__(color=color, location=location, speed=speed)
        if size is not None:
            self.size = size

        self.surf = pygame.Surface(size=self.size)
        # Give the surface a color to separate it from the background
        self.rect = self.surf.fill(color=(0, 0, 0))
        self.rect.move_ip(*self.location)