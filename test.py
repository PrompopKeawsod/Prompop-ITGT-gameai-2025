import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Circle Disappear")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Circle properties
circle_pos = (WIDTH // 2, HEIGHT // 2)
circle_radius = 50
draw_circle = True # Flag to control drawing

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                draw_circle = not draw_circle # Toggle drawing on spacebar

    # Fill the background in each frame (clears previous drawings)
    screen.fill(WHITE)

    # Draw the circle only if the flag is True
    if draw_circle:
        pygame.draw.circle(screen, BLUE, circle_pos, circle_radius)

    # Update the display
    pygame.display.flip()

pygame.quit()