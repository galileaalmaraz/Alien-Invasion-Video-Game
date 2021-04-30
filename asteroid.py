import pygame
from pygame.sprite import Sprite
from random import randint


class Asteroid(Sprite):
    """A class to manage the asteroids that will fall randomly."""

    def __init__(self, ai_settings, screen):
        """Create an asteroid object, at the top of the screen."""
        super(Asteroid, self).__init__()
        self.screen = screen

        # Load the asteroid image, and set its rect attribute.
        self.image = pygame.image.load("./assets/asteroid.bmp")
        self.rect = self.image.get_rect()

        # Position the asteroid rect as a random horizontal position at the beginning of the screen
        self.rect.x = self._get_random_x_pos()
        self.rect.y = 0

        # Store a decimal value for the asteroid's position.
        self.y = float(self.rect.y)

        self.speed_factor = ai_settings.asteroid_speed_factor

    def _get_random_x_pos(self):
        w, _ = pygame.display.get_surface().get_size()
        min_x = self.rect.width
        max_x = w - self.rect.width
        return randint(min_x, max_x)

    def update(self):
        """Move the asteroid up the screen."""
        # Update the decimal position of the asteroid.
        self.y += self.speed_factor
        # Update the rect position.
        self.rect.y = self.y

    def blitme(self):
        """Draw the alien at its current location."""
        self.screen.blit(self.image, self.rect)
