import sys
import pygame
from game_bullets import Bullet
from settings import Settings
from ship import Ship
from alien_class import Alien
from button import Button
from score import Scoreboard

class AlienInvasion:
    """Manages game assets and behavior."""

    def __init__(self):
        """Initializes game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        
        # Load background image
        self.background_image = pygame.image.load(r"C:\Users\denmar\Downloads\field.jpg")
        
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.game_active = False
        self.play_button = Button(self, "Play")
        self.bg_color = self.settings.bg_color
        self.scoreboard = Scoreboard(self.screen)  
        self.lives_left = 3 

    def run_game(self):
        """Main game loop."""
        while True:
            self._check_events()
            
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                
                if len(self.aliens) == 0:  # If all aliens are defeated
                    self._level_up()  # Move to next level

            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """Handles events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit_game()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Starts new game."""        
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.game_active = True
            self.bullets.empty()
            self.aliens.empty()
            self._create_fleet()
            self.ship.center_ship()
            self.lives_left = 3  
            self.scoreboard.reset_score() 
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Handles key presses.""" 
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            self._quit_game()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Handles key releases.""" 
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Creates new bullet.""" 
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update bullet positions and handle collisions.""" 
        # Update bullet positions
        self.bullets.update()

        # Remove bullets that move off the screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # Check for collisions between bullets and aliens
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.scoreboard.update_score(len(aliens))  # The score will increase as the number of aliens hit

    def _update_aliens(self):
        """Updates alien positions.""" 
        self._check_fleet_edges()
        self.aliens.update()
        
        if pygame.sprite.spritecollideany(self.ship, self.aliens) or self._alien_reached_ship_level():
            self._ship_hit()

    def _alien_reached_ship_level(self):
        """Check if any alien has reached the ship's level.""" 
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.ship.rect.top:  # If alien has reached the ship's level
                return True
        return False

    def _ship_hit(self):
        """Handles the ship getting hit by an alien.""" 
        if self.lives_left > 1:
            self.lives_left -= 1
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            pygame.time.delay(500)  # Pause before continuing
        else:
            self.game_active = False  # Game Over when no lives are left
            pygame.mouse.set_visible(True)

    def _game_won(self):
        """Handles the game won scenario and displays the final score.""" 
        self.game_active = False  # Stop the game loop
        self.scoreboard.display_final_score()  # Show final score
        pygame.mouse.set_visible(True)  # Make the mouse visible after game over

    def _create_fleet(self):
        """Creates a fleet of aliens with customizable spacing.""" 
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        # Set the limits for the number of aliens per row and rows
        max_aliens_x = 8 
        max_aliens_y = 7  

        # Set custom spacing (change these values for more or less spacing)
        horizontal_spacing = 5  
        vertical_spacing = 1.5  

        # Calculate the initial position for creating aliens
        current_x = (self.settings.screen_width - (alien_width * max_aliens_x * horizontal_spacing)) // 2
        current_y = alien_height  # Start the fleet just below the top edge

        # Loop to create a fleet of aliens
        for row in range(max_aliens_y):
            for col in range(max_aliens_x):
                self._create_alien(current_x + col * alien_width * horizontal_spacing, 
                                   current_y + row * alien_height * vertical_spacing)

    def _create_alien(self, x_position, y_position):
        """Creates a single alien at the given position."""        
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """Checks fleet edges and moves the fleet down if necessary.""" 
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """Move the fleet down one step and change direction."""        
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.alien_drop_speed  # Move the fleet down
        self.settings.fleet_direction *= -1  # Reverse direction horizontally

    def _update_screen(self):
        """Redraw all visual elements.""" 
        self.screen.fill(self.bg_color)
        
        # Stretch the background to fill the screen
        background_scaled = pygame.transform.scale(self.background_image, (self.settings.screen_width, self.settings.screen_height))
        
        # Draw the scaled background image
        self.screen.blit(background_scaled, (0, 0))  # top-left corner
        
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        # Draw the scoreboard
        self.scoreboard.draw()

        # Display the lives left
        self._draw_lives()

        if not self.game_active:
            self.play_button.draw_button()
        
        pygame.display.flip()

    def _draw_lives(self):
        """Draws the number of lives remaining on the screen using an image.""" 
        life_icon = pygame.image.load(r"C:\Users\denmar\Downloads\card.jpg")  
        life_icon = pygame.transform.scale(life_icon, (75, 55)) #scale of card image to make it smaller
        life_icon_rect = life_icon.get_rect()  # Get the rect of the image for positioning

        # Adjusted spacing to make the lives appear shorter
        for i in range(self.lives_left):  # Card for each life left
            life_icon_rect.x = self.settings.screen_width - (80 * (i + 1))  # card spacing
            life_icon_rect.y = 10  # top of the screen
            self.screen.blit(life_icon, life_icon_rect)  # Blit the image on the screen

    def _quit_game(self):
        """Cleanly exit game."""        
        pygame.quit()
        sys.exit()

    def _level_up(self):
        """Increase the level and speed of the game."""
        self.scoreboard.level += 1  # Increase level
        self.settings.increase_alien_speed()  # Increase alien speed
        self._create_fleet()  # Create new fleet of aliens
        self.ship.center_ship()  # Reposition the ship
        self.scoreboard.update_scoreboard()  # Update the scoreboard to show new level
        
        # Reset the bullets at the beginning of the level
        self.bullets.empty()  # Remove all bullets after 1 level passed
    
        pygame.time.delay(500)  # Short pause before next level starts


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
