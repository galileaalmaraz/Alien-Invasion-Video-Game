import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
import game_functions as gf


def run_game():
    # Initialize pygame, settings, and screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height)
    )

    pygame.display.set_caption("Alien Invasion")

    # Create an instance to store game statistics, and a scoreboard.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Set the background
    bg_image = pygame.image.load("./assets/stars.png")
    i = 0
    image_width = 1440

    # Make a ship, a group of bullets, and a group of aliens.
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    asteroids = Group()

    # Create the fleet of aliens.
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Start the main loop for the game.
    while True:
        # screen.fill(0, 0, 0)
        screen.blit(bg_image, (i, 0))
        screen.blit(bg_image, (image_width + i, 0))
        if i == -image_width:
            screen.blit(bg_image, (image_width + i, 0))
            i = 0

        i -= 1

        # Make the Play button.
        play_button = Button(ai_settings, screen, "PLAY")

        if play_button.screen_rect:
            gf.check_events(
                ai_settings,
                screen,
                stats,
                sb,
                play_button,
                ship,
                aliens,
                bullets,
                asteroids,
            )
            if stats.game_active:
                ship.update()
                gf.update_bullets(
                    ai_settings, screen, stats, sb, ship, aliens, bullets, asteroids
                )
                gf.update_aliens(
                    ai_settings, screen, stats, sb, ship, aliens, bullets, asteroids
                )
                gf.update_asteroids(
                    ai_settings, screen, stats, sb, ship, aliens, bullets, asteroids
                )

            gf.update_screen(
                ai_settings,
                screen,
                stats,
                sb,
                ship,
                aliens,
                bullets,
                asteroids,
                play_button,
            )


run_game()