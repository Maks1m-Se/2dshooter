import pygame
import random

# Initialize Pygame
pygame.init()

### Screen ###
screen_width = 600
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("2D Shooter Game")

### Set up colors ###
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (5, 5, 5)

### Set up levels ##
level = 1
level_threshold = 0
level_speed_increase = 0

# level indicator box
level_indicator_width = 50
level_indicator_height = 25
level_indicator = pygame.Rect(screen_width - level_indicator_width - 10, 10, level_indicator_width, level_indicator_height)


### Set up the player ###
player_width = 50
player_height = 50
player_image = pygame.image.load('images/player.png').convert_alpha() # convert_alpha() function is used to optimize the image for better performance
player_image = pygame.transform.scale(player_image, (player_width, player_height)) # Resize the player image to match the player object dimensions
player = pygame.Rect(screen_width // 2 - player_width // 2, screen_height - player_height, player_width, player_height)

### Set up bullets ###
bullet_width = 5
bullet_height = 15
bullet_color = WHITE
bullet_speed = 20
bullet_image = pygame.image.load('images/bullet.png').convert_alpha() # convert_alpha() function is used to optimize the image for better performance
bullet_image = pygame.transform.scale(bullet_image, (bullet_width, bullet_height)) # Resize the bullet image to match the bullet object dimensions
bullets = []

### Set up target ###
target_width = 40
target_height = 40
target_color = RED
target_counter = 0 # counter to make target move slower
target_break = 5 # decides after how my game loops targets moves
target_speed = 1
num_targets = 5 #random.randint(5, 10)
target_image = pygame.image.load('images/target.png').convert_alpha() # convert_alpha() function is used to optimize the image for better performance
target_image = pygame.transform.scale(target_image, (target_width, target_height)) # Resize the target image to match the target object dimensions
targets = []

# Target class
class Target:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, target_width, target_height)
        self.x_speed = random.choice([-1, 1]) * (random.uniform(0.0, 3.) + level_speed_increase)
        self.y_speed = random.choice([-1, 1]) * (random.uniform(0.0, 3.) + level_speed_increase)
        print(self.x_speed, self.y_speed)

for _ in range(num_targets):
    target = Target(random.randint(0, screen_width - target_width), random.randint(0, screen_height // 2))
    targets.append(target)

# function creating targets
def create_targets():
    targets.clear()
    for _ in range(num_targets):
        target = Target(random.randint(0, screen_width - target_width), random.randint(0, screen_height // 2))
        targets.append(target)

# create initial targets
create_targets()

### Set up font ###
font = pygame.font.Font(None, 20)

### Set up clock ###
clock = pygame.time.Clock()

### Game loop ###
running = True
while running:
    # Set the frame rate to x fps
    clock.tick(40)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            # Move the player with the mouse
            player.x = event.pos[0] - player_width // 2
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Shoot a bullet on right-click
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
            if bullet.colliderect(target):
                bullets.remove(bullet)
                targets.remove(target)

                # Check if all targets are eliminated
                if len(targets) == 0:
                    level += 1
                    # Speed increase
                    level_speed_increase += .5  # Increase the speed for the next level
                    create_targets()

    # Update targets
    for target in targets:
        # Movement targets
        target.rect.x += target.x_speed
        target.rect.y += target.y_speed
        # Bounce off the walls
        if target.rect.left < 0 or target.rect.right > screen_width:
            target.x_speed *= -1
        if target.rect.top < 0 or target.rect.bottom > screen_height:
            target.y_speed *= -1

    target_counter += 1

    # Draw the screen
    screen.fill((210, 210, 230))  # Clear the screen

    # Draw the player
    screen.blit(player_image, player)
    # pygame.draw.rect(screen, WHITE, player) #draw white rectangle

    # Draw the bullets
    for bullet in bullets:
        screen.blit(bullet_image, bullet)
        #pygame.draw.rect(screen, bullet_color, bullet)

    # Draw the targets
    for target in targets:
        screen.blit(target_image, target)
        #pygame.draw.rect(screen, target_color, target)


    # Draw level indicator box
    pygame.draw.rect(screen, WHITE, level_indicator)

    # Draw the current level inside the level indicator
    level_text = font.render("Level: " + str(level), True, BLACK)
    level_text_rect = level_text.get_rect(center=level_indicator.center)
    screen.blit(level_text, level_text_rect)

    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()
