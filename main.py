import pygame
import random
import os
import time

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen
screen_width = 600
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("2D Shooter Game")

# Set up colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (5, 5, 5)

# Set up levels
level = 1
level_threshold = 0
level_speed_increase = 0

# Level indicator box
level_indicator_width = 50
level_indicator_height = 25
level_indicator = pygame.Rect(screen_width - level_indicator_width - 10, 10, level_indicator_width, level_indicator_height)

# Set up the player
player_width = 50
player_height = 50
player_image = pygame.image.load('images/player.png').convert_alpha()
player_image = pygame.transform.scale(player_image, (player_width, player_height))
player = pygame.Rect(screen_width // 2 - player_width // 2, screen_height - player_height, player_width, player_height)

# Set up bullets
bullet_width = 5
bullet_height = 15
bullet_color = WHITE
bullet_speed = 20
bullet_image = pygame.image.load('images/bullet.png').convert_alpha()
bullet_image = pygame.transform.scale(bullet_image, (bullet_width, bullet_height))
bullets = []

# Set up target
target_width = 40
target_height = 40
target_color = RED
target_counter = 0
target_break = 5
target_speed = 1
num_targets = 5
target_image = pygame.image.load('images/target.png').convert_alpha()
target_image = pygame.transform.scale(target_image, (target_width, target_height))
targets = []

# Sounds
reload_sound = pygame.mixer.Sound(os.path.join('sounds', 'reload.wav'))
hit_sound = pygame.mixer.Sound(os.path.join('sounds', 'hit.wav'))
shot_sound = pygame.mixer.Sound(os.path.join('sounds', 'shot.flac'))
gameplay_music = pygame.mixer.Sound(os.path.join('sounds', 'gameplay_music.wav'))

# Target class
class Target:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, target_width, target_height)
        self.x_speed = random.choice([-1, 1]) * (random.uniform(0.0, 3.0) + level_speed_increase)
        self.y_speed = random.choice([-1, 1]) * (random.uniform(0.0, 3.0) + level_speed_increase)
        print(self.x_speed, self.y_speed)

# Function to create targets
def create_targets():
    targets.clear()
    for _ in range(num_targets):
        target = Target(random.randint(0, screen_width - target_width), random.randint(0, screen_height // 2))
        targets.append(target)

# Create initial targets
create_targets()

# Set up font
font = pygame.font.Font(None, 20)

# Set up clock
clock = pygame.time.Clock()

# Start the music
gameplay_music.play()

# Timer variables
start_time = time.time()
elapsed_time = 0

# Game loop
running = True
while running:
    # Set the frame rate
    clock.tick(40)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            # Move the player with the mouse
            player.x = event.pos[0] - player_width // 2
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Shoot a bullet on left-click
            shot_sound.play()
            bullet = pygame.Rect(player.x + player_width * 0.865 - bullet_width // 2,
                                 player.y,
                                 bullet_width,
                                 bullet_height)
            bullets.append(bullet)

    # Update bullets
    for bullet in bullets[:]:
        bullet.y -= bullet_speed
        if bullet.y < 0:
            bullets.remove(bullet)

    # Check for collisions between bullets and targets
    for bullet in bullets[:]:
        for target in targets[:]:
            if bullet.colliderect(target.rect):
                hit_sound.play()
                bullets.remove(bullet)
                targets.remove(target)

                # Check if all targets are eliminated
                if len(targets) == 0:
                    level += 1
                    level_speed_increase += 0.5  # Increase speed for next level
                    reload_sound.play()
                    create_targets()
                    start_time = time.time()  # Reset start time for the new level

    # Update targets
    for target in targets:
        target.rect.x += target.x_speed
        target.rect.y += target.y_speed
        if target.rect.left <= 0 or target.rect.right >= screen_width:
            target.x_speed *= -1
        if target.rect.top <= 0 or target.rect.bottom >= (screen_height * 0.85):
            target.y_speed *= -1

    # Calculate elapsed time
    elapsed_time = time.time() - start_time

    # Draw the screen
    screen.fill((210, 210, 230))  # Clear the screen

    # Draw the player
    screen.blit(player_image, player)

    # Draw the bullets
    for bullet in bullets:
        screen.blit(bullet_image, bullet)

    # Draw the targets
    for target in targets:
        screen.blit(target_image, target.rect)

    # Draw level indicator box
    pygame.draw.rect(screen, WHITE, level_indicator)

    # Draw the current level inside the level indicator
    level_text = font.render("Level: " + str(level), True, BLACK)
    level_text_rect = level_text.get_rect(center=level_indicator.center)
    screen.blit(level_text, level_text_rect)

    # Display the elapsed time
    timer_text = font.render("Time: {:.2f}".format(elapsed_time), True, BLACK)
    screen.blit(timer_text, (10, 10))

    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()
