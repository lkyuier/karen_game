import pygame
import sys

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Initialize pygame
pygame.init()

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Revised Pygame for Pygbag')

# Load font (using a built-in font)
font = pygame.font.Font(None, 72)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill screen with black
    screen.fill(BLACK)

    # Display a simple text with a background rectangle
    text_surface = font.render('Ready to start!', True, BLUE)  # Blue text
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    # Draw a rectangle around the text
    pygame.draw.rect(screen, GREEN, text_rect.inflate(20, 20))  # Green background with padding
    screen.blit(text_surface, text_rect)  # Draw the text

    # Update display
    pygame.display.flip()

# Quit pygame
pygame.quit()
sys.exit()
