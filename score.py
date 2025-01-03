import pygame.font
import os

class Scoreboard:
    """Class to report scoring information."""

    def __init__(self, screen):
        """Initialize score attributes."""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Set up font and color
        self.text_color = (251, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Initialize score, high score, and level
        self.score = 0
        self.high_score = self._load_high_score()  
        self.level = 1
        self.score_image = None
        self.high_score_image = None
        self.level_image = None
        self.update_scoreboard()

    def update_score(self, points):
        """Update the score with points."""
        self.score += points
        if self.score > self.high_score:  # Check if current score is higher than the high score
            self.high_score = self.score
            self._save_high_score()  # Save new high score to file
        self.update_scoreboard()

    def update_scoreboard(self):
        """Update the images of the score, high score, and level."""
        self.score_image = self.font.render(f"Score: {self.score}", True, self.text_color)
        self.high_score_image = self.font.render(f"High Score: {self.high_score}", True, self.text_color)
        self.level_image = self.font.render(f"Level: {self.level}", True, self.text_color)

        # Position the score at top-left with a margin
        self.score_rect = self.score_image.get_rect()
        self.score_rect.topleft = (20, 20)  
        
        # Position the high score at the center horizontally
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx  
        self.high_score_rect.top = 20  

        # Position the level below the high score (top-left aligned)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.topleft = (20, self.score_rect.bottom + 10)  

    def draw(self):
        """Draw the score, high score, and level on the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)

    def display_final_score(self):
        """Display the final score when the game is over."""
        final_score_image = self.font.render(f"Final Score: {self.score}", True, self.text_color)
        final_score_rect = final_score_image.get_rect()
        final_score_rect.center = self.screen_rect.center

        self.screen.blit(final_score_image, final_score_rect)
        pygame.display.flip()
        pygame.time.wait(2000)  # 2 seconds before quitting

    def reset_score(self):
        """Reset the score to 0."""
        self.score = 0
        self.update_scoreboard()

    def _load_high_score(self):
        """Load the high score from a file."""
        if os.path.exists("high_score.txt"):
            with open("high_score.txt", "r") as file:
                return int(file.read())
        else:
            return 0  # If no high score file exists, set to 0

    def _save_high_score(self):
        """Save the current high score to a file."""
        with open("high_score.txt", "w") as file:
            file.write(str(self.high_score))
