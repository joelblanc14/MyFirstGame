import pygame
import pygame.freetype
import sys
import random

# Initialize pygame
pygame.init()

font = pygame.freetype.SysFont("Times New Roman", 12)

# Set up the game window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Shooter Simple")

# Set the frame rate
clock = pygame.time.Clock()

# Player settings
player_width = 50
player_height = 60
player_x = screen_width // 2 - player_width // 2
player_y = screen_height - player_height - 10
player_speed = 5

# Bullet settings
bullet_width = 5
bullet_height = 10
bullet_speed = 10
bullets = []

# Enemy settings
enemy_width = 50
enemy_height = 60
enemy_speed = 2
enemies = []

# Spawn enemy every 2 seconds
enemy_timer = 0
enemy_spawn_time = 2000

score = 0

# Collision detection function
def check_collision(rect1, rect2):
    return pygame.Rect(rect1).colliderect(pygame.Rect(rect2))

start_time = pygame.time.get_ticks()
# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Create a bullet in the current player position
                bullet_x = player_x + player_width // 2 - bullet_width // 2
                bullet_y = player_y 
                bullets.append(pygame.Rect(bullet_x, bullet_y, bullet_width, bullet_height))

    # Handle player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
        player_x += player_speed

    # Update bullet positions
    for bullet in bullets:
        bullet[1] -= bullet_speed
    # Remove bullets that are off-screen
    bullets = [bullet for bullet in bullets if bullet[1] > 0]

    # Update enemy positions and add new enemies
    current_time = pygame.time.get_ticks()
    if current_time - enemy_timer >= enemy_spawn_time:
        enemy_x = random.randint(0, screen_width - enemy_width)
        enemy_y = -enemy_height
        enemies.append(pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height))
        enemy_timer = current_time

    # Update enemy positions and remove enemies that are off-screen
    for enemy in enemies:
        enemy[1] += enemy_speed
    enemies = [enemy for enemy in enemies if enemy[1] < screen_height]

    # Check for bullet collisions 
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if check_collision((bullet[0], bullet[1], bullet_width, bullet_height),
                                (enemy[0], enemy[1], enemy_width, enemy_height)):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 1

    # Check for player collisions
    for enemy in enemies:
        if check_collision((player_x, player_y, player_width, player_height),
                            (enemy[0], enemy[1], enemy_width, enemy_height)):
            
            pygame.quit()
            sys.exit()

    # Fill the screen with black
    screen.fill((0,0,0))

    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000 # Convert to seconds

    time_surface, time_rect = font.render(f"Temps: {elapsed_time}s", (255, 255, 255), size=15)
    screen.blit(time_surface, (10, 10))

    score_surface, score_rect = font.render(f"Score: {score}", (255, 255, 255), size=15)
    screen.blit(score_surface, (720, 580))

    # Draw the player
    pygame.draw.rect(screen, (0, 128, 255), (player_x, player_y, player_width, player_height))

    # Draw the bullets
    for bullet in bullets:
        pygame.draw.rect(screen, (255, 255, 255), bullet)

    # Draw the enemies
    for enemy in enemies:
        pygame.draw.rect(screen, (255, 0, 0), enemy)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate at 60 FPS
    clock.tick(60)

