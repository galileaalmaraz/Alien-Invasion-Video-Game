import datetime
from score import GameScore


class GameStats:
    """Track statistics for Alien Invasion."""

    MIN_HARD_LEVEL = 2

    def __init__(self, ai_settings):
        """Initialize statistics."""
        self.ai_settings = ai_settings
        # A timer that will be responsible for creating asteroids on a specific time interval
        self.asteroids_timer = None

        self.reset_stats()

        # Start game in an inactive state.
        self.game_active = False

        # High score should never be reset.
        self.high_score = 0

        # A game count that will indicate whether the player has lost any games
        self.games_count = 0

    def get_level(self):
        return self._level

    def set_level(self, new_level):
        if hasattr(self, "_level"):
            self._level_end_time = datetime.datetime.now()
            self.record_level_data()
        self._level = new_level
        self._level_start_time = datetime.datetime.now()
        self._level_end_time = None
        self._level_score = 0

    level = property(get_level, set_level)

    def get_score(self):
        return self._score

    def set_score(self, new_score):
        if hasattr(self, "_score"):
            old_score = self._score
            diff = new_score - old_score
            self._level_score += diff
        self._score = new_score

    score = property(get_score, set_score)

    def get_level_times(self):
        return self._level_start_time, self._level_end_time

    def get_level_score(self):
        return self._level_score

    def record_level_data(self):
        start, end = self.get_level_times()
        self.current_game_score.add_level(
            self.level, start, end, self.get_level_score()
        )

    def increase_game_count(self):
        self.games_count += 1

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
        self.username = None
        self.current_game_score = GameScore(self.username)
        self.close_asteroids_timer()
        self.is_new_game = False

    def close_asteroids_timer(self):
        if self.asteroids_timer is not None:
            self.asteroids_timer.stop()
            self.asteroids_timer = None

    def set_asteroids_timer(self, timer):
        self.asteroids_timer = timer

    def set_username(self, username):
        self.username = username

    def end_game(self):
        assert self.username is not None
        self._level_end_time = datetime.datetime.now()
        self.record_level_data()
        self.current_game_score.username = self.username
        self.current_game_score.save()
        self.is_new_game = True
