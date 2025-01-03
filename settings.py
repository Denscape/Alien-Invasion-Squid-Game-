class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        # Ship settings
        self.ship_speed = 1.5

        # Bullet settings
        self.bullet_speed = 2.5
        self.bullet_width = 3
        self.bullet_height = 10
        self.bullet_color = (255, 255, 0)
        self.bullets_allowed = 25

        # Alien settings
        self.alien_speed = 1.0  # Initial speed
        self.fleet_direction = 2  # 2 represents right while the -1 represents left
        self.alien_drop_speed = 40  

    def increase_alien_speed(self):
        """Increase the speed of aliens after each level."""
        if self.alien_speed < 2.0:
            self.alien_speed *= 1.1  # Increase by 10% after each level
        elif self.alien_speed < 3.0:
            self.alien_speed *= 1.2  # Increase by 20% for level 2 and beyond
        else:
            self.alien_speed *= 1.1  # the speed increasing as level increases
