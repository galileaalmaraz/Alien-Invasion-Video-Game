import sys
from time import sleep

import pygame

from repeated_timer import RepeatedTimer

from graph import create_graphs

from pygame_textinput import TextInput
from text_message import Message

from button import Button
from bullet import Bullet
from alien import Alien
from asteroid import Asteroid


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(
    ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, asteroids
):
    """Respond to keypresses and mouse events."""

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stats.close_asteroids_timer()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # debugging
            if event.key == pygame.K_k:
                ship_hit(
                    ai_settings, screen, stats, sb, ship, aliens, bullets, asteroids
                )
            # debugging
            if event.key == pygame.K_n:
                aliens.empty()
                check_bullet_alien_collisions(
                    ai_settings, screen, stats, sb, ship, aliens, bullets, asteroids
                )
            # debugging
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(
                ai_settings,
                screen,
                stats,
                sb,
                play_button,
                ship,
                aliens,
                bullets,
                asteroids,
                mouse_x,
                mouse_y,
            )


def check_play_button(
    ai_settings,
    screen,
    stats,
    sb,
    play_button,
    ship,
    aliens,
    bullets,
    asteroids,
    mouse_x,
    mouse_y,
):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings.
        ai_settings.initialize_dynamic_settings()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

        # Reset the game statistics.
        stats.reset_stats()
        stats.game_active = True

        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()
        asteroids.empty()

        stats.set_asteroids_timer(
            start_asteroid_creation_timer(
                ai_settings, screen, stats, sb, ship, asteroids
            )
        )

        # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet, if limit not reached yet."""
    # Create a new bullet, add to bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def draw_home_page(screen):
    home_image = pygame.image.load("./assets/home.png")
    screen.blit(home_image, (0, 0))


def draw_gameover_page(screen):
    gameover_image = pygame.image.load("./assets/game_over.png")
    screen.blit(gameover_image, (0, -150))


def draw_levelup_page(screen):
    levelup_image = pygame.image.load("./assets/level_up.png")
    screen.blit(levelup_image, (0, 0))


def draw_background_image(screen):
    bg_image = pygame.image.load("./assets/stars.png")
    screen.blit(bg_image, (0, 0))


def draw_saveusername_page(screen):
    saveusername_image = pygame.image.load("./assets/save_username.png")
    saveusername_image = pygame.transform.scale(saveusername_image, (800, 400))
    screen.blit(saveusername_image, (320, 200))


def draw_missioncomplete_page(screen):
    missioncomplete_image = pygame.image.load("./assets/mission_complete.png")
    screen.blit(missioncomplete_image, (0, 0))


def display_mission_complete(screen, stats):
    draw_background_image(screen)

    next_level_button = Button(None, screen, "Next Level")
    next_level_button.rect.x = 620
    next_level_button.rect.y = 620

    while True:
        draw_missioncomplete_page(screen)
        event = pygame.event.poll()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            button_clicked = next_level_button.rect.collidepoint(mouse_x, mouse_y)
            if button_clicked:
                break
        elif event.type == pygame.QUIT:
            stats.close_asteroids_timer()
            sys.exit()

        next_level_button.draw_button()
        pygame.display.flip()

    draw_background_image(screen)
    pygame.display.flip()


def update_screen(
    ai_settings, screen, stats, sb, ship, aliens, bullets, asteroids, play_button
):
    """Update images on the screen, and flip to the new screen."""
    # Redraw the screen, each pass through the loop.
    # screen.fill(ai_settings.bg_color)

    # Redraw all bullets, behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    if stats.game_active:
        ship.blitme()
        aliens.draw(screen)
        asteroids.draw(screen)

    # Draw the score information.
    sb.show_score()

    # Draw the play button if the game is inactive.
    if not stats.game_active:
        if stats.games_count == 0:
            draw_home_page(screen)
        else:
            draw_gameover_page(screen)
            if not stats.is_new_game:
                pygame.display.flip()
                sleep(2)
                username = ask_player_for_username(screen, stats)
                stats.set_username(username)
                stats.end_game()
                create_graphs()
                show_user_scores(screen, stats)
        play_button.draw_button()

    # Make the most recently drawn screen visible.
    pygame.display.flip()


def show_user_scores(screen, stats):
    draw_background_image(screen)
    continue_button = Button(None, screen, "Continue")
    continue_button.rect.x = 620
    continue_button.rect.y = 620
    draw_yourscore_page(screen)
    draw_score(screen, stats)

    while True:
        event = pygame.event.poll()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            button_clicked = continue_button.rect.collidepoint(mouse_x, mouse_y)
            if button_clicked:
                break
        elif event.type == pygame.QUIT:
            stats.close_asteroids_timer()
            sys.exit()

        continue_button.draw_button()
        pygame.display.flip()

    draw_background_image(screen)
    pygame.display.flip()


def draw_yourscore_page(screen):
    yourscore_image = pygame.image.load("./assets/score_panel.png")
    screen.blit(
        yourscore_image,
        (0, 0),
    )


def draw_score(screen, stats):
    myfont = pygame.font.SysFont("sans serif", 35)
    message = Message(
        (620, 380),
        f"Score: {stats.score}",
        myfont,
        color=pygame.Color("white"),
    )
    message2 = Message(
        (620, 400),
        f"High Score: {stats.high_score}",
        myfont,
        color=pygame.Color("white"),
    )
    message.blitme(screen)
    message2.blitme(screen)


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, asteroids):
    """Update position of bullets, and get rid of old bullets."""
    # Update bullet positions.
    bullets.update()

    # Get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(
        ai_settings, screen, stats, sb, ship, aliens, bullets, asteroids
    )
    check_bullet_asteroid_collisions(
        ai_settings, screen, stats, sb, ship, asteroids, bullets
    )


def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def check_bullet_alien_collisions(
    ai_settings, screen, stats, sb, ship, aliens, bullets, asteroids
):
    """Respond to bullet-alien collisions."""
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # If the entire fleet is destroyed, start a new level.
        bullets.empty()
        asteroids.empty()
        ai_settings.increase_speed()
        stats.close_asteroids_timer()
        stats.set_asteroids_timer(
            start_asteroid_creation_timer(
                ai_settings, screen, stats, sb, ship, asteroids
            )
        )

        # Increase level.
        stats.level += 1
        display_mission_complete(screen, stats)
        draw_levelup_page(screen)
        pygame.display.update()
        sleep(3)
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)


def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet, and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ask_player_for_username(screen, stats):
    fontsize = 35
    inputfield = TextInput(
        "USERNAME",
        font_family="Ariel",
        text_color=pygame.Color("white"),
        cursor_color=pygame.Color("red"),
        font_size=fontsize,
    )
    username = None
    myfont = pygame.font.SysFont("sans serif", fontsize)
    message = Message(
        (550, 550),
        "Type your name & press Enter",
        font=myfont,
        color=pygame.Color("green"),
    )

    while True:
        draw_background_image(screen)
        draw_saveusername_page(screen)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                stats.close_asteroids_timer()
                sys.exit()

        if inputfield.update(events):
            username = inputfield.get_text()
            break

        screen.blit(
            inputfield.get_surface(),
            (650, 500),
        )
        message.blitme(screen)
        pygame.display.update()
    return username


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, asteroids):
    """Respond to ship being hit by alien."""
    stats.close_asteroids_timer()
    stats.increase_game_count()
    if stats.ships_left > 0:
        # Decrement ships_left.
        stats.ships_left -= 1
        stats.set_asteroids_timer(
            start_asteroid_creation_timer(
                ai_settings, screen, stats, sb, ship, asteroids
            )
        )

        # Update scoreboard.
        sb.prep_ships()

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

    # Empty the list of aliens and bullets.
    aliens.empty()
    bullets.empty()
    asteroids.empty()

    # Create a new fleet, and center the ship.
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

    # Pause.
    sleep(0.5)


def check_aliens_bottom(
    ai_settings, screen, stats, sb, ship, aliens, bullets, asteroids
):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, asteroids)
            break


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, asteroids):
    """
    Check if the fleet is at an edge,
      then update the postions of all aliens in the fleet.
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, asteroids)

    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(
        ai_settings, screen, stats, sb, ship, aliens, bullets, asteroids
    )


def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = ai_settings.screen_height - (3 * alien_height) - ship_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien, and place it in the row."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens."""
    # Create an alien, and find number of aliens in a row.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Create the fleet of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def create_asteroid(ai_settings, screen, asteroids):
    """Create an asteroid and add it to the asteroids group"""
    asteroid = Asteroid(ai_settings, screen)
    asteroids.add(asteroid)


def check_asteroids_bottom(
    ai_settings, screen, stats, sb, ship, aliens, bullets, asteroids
):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for asteroid in asteroids.sprites():
        if asteroid.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, asteroids)
            break


def update_asteroids(ai_settings, screen, stats, sb, ship, aliens, bullets, asteroids):
    """A function that will update the position of the asteroids and randomly add them while the game is running."""
    asteroids.update()

    # Look for asteroid-ship collisions.
    if pygame.sprite.spritecollideany(ship, asteroids):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, asteroids)

    check_asteroids_bottom(
        ai_settings, screen, stats, sb, ship, aliens, bullets, asteroids
    )


def check_bullet_asteroid_collisions(
    ai_settings, screen, stats, sb, ship, asteroids, bullets
):
    """Respond to bullet-asteroid collisions."""
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, asteroids, True, True)

    if collisions:
        for asteroids in collisions.values():
            stats.score += ai_settings.asteroid_points * len(asteroids)
            sb.prep_score()
        check_high_score(stats, sb)


def start_asteroid_creation_timer(ai_settings, screen, stats, sb, ship, asteroids):
    if stats.level >= stats.MIN_HARD_LEVEL:
        timer = RepeatedTimer(
            ai_settings.base_asteroids_timer_interval / stats.level,
            create_asteroid,
            ai_settings,
            screen,
            asteroids,
        )
        timer.start()
        return timer
    return None
