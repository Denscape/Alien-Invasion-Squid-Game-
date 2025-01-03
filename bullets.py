import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""

    def __init__(self, ai_game):
        """Initialize bullet properties."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Bullet properties
        self.color = self.settings.bullet_color
        self.width = self.settings.bullet_width
        self.height = self.settings.bullet_height

        # Create bullet rect and set its initial position
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Store the bullet's position as a float for precision
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet up the screen."""
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
