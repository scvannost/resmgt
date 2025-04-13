__all__ = [
    "Game",
]

from typing import Dict, List, Optional, Tuple

import pygame
from pygame.locals import (
    K_ESCAPE,
)

from .db.database import Database, load_dotenv_config
from .settings import FPS, SCREEN_HEIGHT, SCREEN_WIDTH
from .sprite import SPRITE_GROUPS, BasicSprite, VillagerIconSprite


class Game:
    """
    The game, which has an underlying pygame display

    Parameters
    ----------
    bg_color: Tuple[int, int, int] = (255, 255, 255)
        the base background color to fill the screen with before drawing anything else
        in the format (r,g,b)
    size: Optional[Tuple[float, float]] = None
        the size of the underlying display to create
    player_sprite: Optional[BasicSprite] = None
        the movable sprite that the player controls
    other_sprites: List[BasicSprite] = []
        the other sprites to render that the player doesn't control
    start: bool = True
        whether to call self.start()

    Attributes
    ----------
    clock: pygame.time.Clock = None
        a timer to limit the update rate of the
        not None if between calls to self.start() and self.quit()
    player: VillagerIconSprite = VillagerIconSprite(location=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        the movable sprite representing the villager that the player controls
    running: bool = False
        whether the game is running or not
        set to False to prevent game from continuing
        can only change from True to False, other changes are nullpotent
    screen: Optional[pygame.SurfaceType] = None
        the underlying pygame.display
        created by calling self.start()
        removed by calling self.quit()
    size: Tuple[float, float] = (SCREEN_WIDTH, SCREEN_HEIGHT)
        the size of the underlying display to create
        can only be changed when self.screen is None
        other changes are nullpotent

    Methods
    -------
    quit() -> None
        calls pygame.quit() and resets self.screen and self.running
    run(quit: bool = True) -> None
        runs main game loop until not self.running
        will run infinitely until self.running is set to False
        calls self.quit() on finish if quit
        sets self.running to False when game window is quit by [x] or hitting ESCAPE
    start() -> None
        calls pygame.init(), sets up self.screen, and sets self.running = True
    """

    bg_color: Tuple[int, int, int] = (0, 154, 23)  # (r,g,b)
    db: Database = Database().connect(
        **load_dotenv_config(),
        create_db_if_not_exist=True,
    )
    clock: Optional[pygame.time.Clock] = None
    player: Optional[VillagerIconSprite] = None
    _running: bool = False
    sprites: pygame.sprite.Group = pygame.sprite.Group()
    _surface: Optional[pygame.SurfaceType] = None
    _size: Tuple[float, float] = (SCREEN_WIDTH, SCREEN_HEIGHT)  # (x,y)

    def __init__(
        self,
        bg_color: Optional[Tuple[int, int, int]] = None,  # (r,g,b)
        size: Optional[Tuple[float, float]] = None,
        player_sprite: Optional[VillagerIconSprite] = None,
        other_sprites: List[BasicSprite] = [],
        db: Database = None,
        start: bool = True,
    ) -> None:
        """
        Parameters
        ----------
        bg_color: Optional[Tuple[int, int, int]] = None
            the base background color to fill the screen with before drawing anything else
            in the format (r,g,b)
        size: Optional[Tuple[float, float]] = None
            the size of the underlying display to create
        player_sprite: Optional[VillagerIconSprite] = None
            the movable sprite that the player controls
        other_sprites: List[BasicSprite] = []
            the other sprites to render that the player doesn't control
        db: Database = None
            the database to use for running the game
        start: bool = True
            whether to call self.start()
        """
        if bg_color is not None:
            self.bg_color = bg_color
        if size is not None:
            self._size = size

        if db is not None:
            self.db = db
        if self.db.session is None:
            self.db.open_session()
        self.db.create_all_tables()

        if player_sprite is not None:
            self.player = player_sprite
        if self.player is not None:
            self.player.insert(self.db)
            self.sprites.add(self.player)

        for spr in other_sprites:
            self.sprites.add(spr)

        if start:
            self.start()

    def quit(self) -> None:
        """
        Quits pygame to be nice
        Resets self.screen and self.running
        """
        # Done! Time to quit.
        pygame.quit()
        # No longer keep the screen around
        self._surface = None
        # Just in case
        self._running = False

    def run(self, quit: bool = True) -> None:
        """
        Runs main game loop until not self.running
        Can call self.quit() on finish

        Parameters
        ----------
        quit: bool = True
            whether to call self.quit() after not self.running
        """
        while self.running:
            self.clock.tick(FPS)
            # Did the user click the window close button or hit the escape key?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Get all the keys currently pressed and
            # update the player sprite based on user keypresses
            pressed_keys: Dict[str, bool] = pygame.key.get_pressed()
            if pressed_keys[K_ESCAPE]:
                self.running = False
            self.player.move(pressed_keys=pressed_keys)

            # Fill the background with bg_color
            self.surface.fill(self.bg_color)

            # Draw all the objects
            group: pygame.sprite.Group
            for group in SPRITE_GROUPS.values():
                group.draw(self.surface)

            # Flip ie update the display
            pygame.display.flip()

        if quit:
            pygame.quit()

    @property
    def running(self) -> bool:
        """
        Whether the game is running or not
        Set to False to prevent game from continuing
        Can only change from True to False
        Other changes are nullpotent

        Is always False if self.screen is None ie self.quit() has been called
        If self.screen is not None:
            if self.running, then can call self.run() or self.quit()
            if not self.running, then can only call self.quit()
        """
        return self._running

    @running.setter
    def running(self, value: bool) -> None:
        """
        Can only change from True to False
        Other changes are nullpotent
        """
        if self.running and not value:
            self._running = False

    @property
    def size(self) -> Tuple[float, float]:
        """
        The size of the underlying display to create
        """
        return self._size

    @size.setter
    def size(self, val: Tuple[float, float]) -> None:
        """
        Can only be changed when self.screen is None
            each call to self.start() must be balanced with a self.quit()
        Other changes are nullpotent
        """
        if self.surface is None:
            self._size = val

    def start(self) -> None:
        """
        Starts pygame and sets up the screen
        If size is passed, overwrites current self.size before opening the display
        """
        # Set up the drawing window
        pygame.init()
        self._surface: pygame.SurfaceType = pygame.display.set_mode(size=self.size)
        self.clock = pygame.time.Clock()

        # Run until the user asks to quit
        self._running = True

    @property
    def surface(self) -> Optional[pygame.SurfaceType]:
        """
        The underlying pygame.display, if it exists
        """
        return self._surface
