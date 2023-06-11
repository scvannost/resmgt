__all__ = [
    "Game",
]

from typing import List, Optional, Tuple
import pygame
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
)

from .settings import SCREEN_HEIGHT, SCREEN_WIDTH
from .sprite import BasicSprite, RectangleSprite


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
    start: bool = True
        whether to call self.start()

    Attributes
    ----------
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

    bg_color: Tuple[int, int, int] = (255, 255, 255)  # (r,g,b)
    player: Optional[RectangleSprite] = RectangleSprite(
        location=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    )
    _running: bool = False
    sprites: pygame.sprite.Group = pygame.sprite.Group()
    _surface: Optional[pygame.SurfaceType] = None
    _size: Tuple[float, float] = (SCREEN_WIDTH, SCREEN_HEIGHT)  # (x,y)

    def __init__(
        self,
        bg_color: Optional[Tuple[int, int, int]] = None,  # (r,g,b)
        size: Optional[Tuple[float, float]] = None,
        sprites: List[BasicSprite] = [],
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
        start: bool = True
            whether to call self.start()
        """
        if bg_color is not None:
            self.bg_color = bg_color
        if size is not None:
            self._size = size

        for spr in sprites:
            self.sprites.add(spr)
        self.sprites.add(self.player)

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
            # Did the user click the window close button or hit the escape key?
            for event in pygame.event.get():
                if (
                    event.type == KEYDOWN and event.key == K_ESCAPE
                ) or event.type == pygame.QUIT:
                    self.running = False

            # Get all the keys currently pressed and
            # update the player sprite based on user keypresses
            self.player.move(pygame.key.get_pressed())

            # Fill the background with bg_color
            self.surface.fill(self.bg_color)

            # Draw all the objects
            spr: BasicSprite
            for spr in self.sprites:
                spr.draw(self.surface)

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

        # Run until the user asks to quit
        self._running = True

    @property
    def surface(self) -> Optional[pygame.SurfaceType]:
        """
        The underlying pygame.display, if it exists
        """
        return self._surface
