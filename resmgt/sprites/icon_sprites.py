__all__ = [
    "IconSprite",
    "VillagerIconSprite",
]

from typing import Dict, Optional, Tuple

import pygame

from ..db.database import Database
from ..db.models import Villager
from .base_sprites import SPRITE_GROUPS, BasicSprite
from .img import sprite_image_filepath


class IconSprite(BasicSprite):
    """
    A simple sprite that contains a picture
    They must have an image path

    Parameters
    ----------
    image_filepath: str
        the filepath of the image to load
        e.g from the output of .img.sprite_image_filepath()
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

    image: pygame.Surface
    size: Tuple[float, float] = (50.0, 50.0)

    def __init__(
        self,
        image_filepath: str,
        location: Optional[Tuple[float, float]] = None,
        size: Optional[Tuple[float, float]] = None,
        speed: Optional[float] = None,
    ) -> None:
        super().__init__(location=location, speed=speed)
        if size is not None:
            self.size = size

        image = pygame.image.load(image_filepath)
        self.image = pygame.transform.scale(image, (size[0], size[1]))

        self.rect = self.image.get_rect()
        self.rect.move_ip(*self.location)


class VillagerIconSprite(IconSprite):
    """
    A simple sprite representing a villager

    Parameters
    ----------
    location: Optional[Tuple[float, float]] = None
        where in the game the sprite should be rendered
        this means slightly different things for each sprite atm
    size: Optional[Tuple[float, float]] = None
        the width and height the rectangle should occupy
        the top-left corner is at the given location
        if None, uses (64.0, 64.0)
    speed: Optional[float] = None
        the top speed that the sprite can move in total
    img_filename: str = "robot.png"
        the filename from .img to load
        one of the values from .img.get_supported_img_filenames()
    db: Optional[Database] = None
        the database to hold the Villager data for this sprite
    insert: bool = True
        whether or not to insert the new Villager on init
    **kwargs
        passed into db.Villager
        along with x=location[0], y=location[1]

    Attributes
    ----------
    location: Tuple[float, float] = (250.0, 250.0)
        where in the game the sprite should be rendered
        this means slightly different things for each sprite atm
    size: Optional[Tuple[float, float]] = (64.0, 64.0)
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

    db: Optional[Database]
    image: pygame.Surface
    model: Villager
    size: Tuple[float, float] = (64.0, 64.0)

    def __init__(
        self,
        location: Optional[Tuple[float, float]] = None,
        size: Optional[Tuple[float, float]] = None,
        speed: Optional[float] = None,
        img_filename: str = "robot.png",
        db: Optional[Database] = None,
        insert: bool = True,
        **kwargs
    ) -> None:
        if size is not None:
            self.size = size
        super().__init__(
            image_filepath=sprite_image_filepath(filename=img_filename),
            location=location,
            size=self.size,
            speed=speed,
        )
        kwargs.update(
            {
                "x": self.location[0],
                "y": self.location[1],
            }
        )
        self.model = Villager(**kwargs)

        if db is not None:
            self.db = db
            if insert:
                self.insert()

    def insert(self, db: Database = None):
        if db:
            self.db = db
        self.db.add(self.model)

    def move(self, pressed_keys: Dict[int, bool]) -> None:
        super().move(pressed_keys)

        self.model.x, self.model.y = self.location
        self.db.merge(self.model)


# set up types for sprite rendering order
for sprite_type in [
    IconSprite,
    VillagerIconSprite,
]:
    SPRITE_GROUPS[sprite_type]
