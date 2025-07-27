
import pygame
import sys

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Initialize pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Simplified Pygame for Pygbag')

# Load font (using relative path)
font = pygame.font.Font(None, 36)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill screen with black
    screen.fill(BLACK)

    # Display a simple text
    text_surface = font.render('Hello, Pygbag!', True, WHITE)
    screen.blit(text_surface, (100, 100))

    # Update display
    pygame.display.flip()

# Quit pygame
pygame.quit()
sys.exit()
