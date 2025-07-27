import pygame
import sys

# Initialize Pygamel
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("My Pygbag Game")

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with white color
    screen.fill((255, 255, 255))

    # Draw a red rectangle
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(30, 30, 60, 60))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
