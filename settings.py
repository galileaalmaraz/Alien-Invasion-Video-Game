import pygame

class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings.
        self.screen_width = 1440
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        # Ship settings.
        self.ship_limit = 3

        # Bullet settings.
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 255, 0, 0
        self.bullets_allowed = 3

        # Asteroid settings
        self.asteroid_length = 20

        # Alien settings.
        self.fleet_drop_speed = 15

        # How quickly the game speeds up.
        self.speedup_scale = 5
        # How quickly the alien and asteroid point values increase.
        self.score_scale = 1.5

        # Asteroids creation settings
        self.base_asteroids_timer_interval = 10

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed_factor = 8
        self.bullet_speed_factor = 10
        self.alien_speed_factor = 1
        self.asteroid_speed_factor = 1

        # Scoring.
        self.alien_points = 50
        self.asteroid_points = 40

        # fleet_direction of 1 represents right, -1 represents left.
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.asteroid_speed_factor *= self.speedup_scale 

        self.alien_points = int(self.alien_points * self.score_scale)
        self.asteroid_points = int(self.asteroid_points * self.score_scale)