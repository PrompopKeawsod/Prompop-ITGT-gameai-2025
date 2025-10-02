'''import pygame
import math

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Half-Circle Rect Movement")

# Colors
white = (255, 255, 255)
red = (255, 0, 0)

# Rect properties
rect_size = 50
rect = pygame.Rect(0, 0, rect_size, rect_size)

# Half-circle path parameters
circle_center_x = screen_width // 2
circle_center_y = screen_height // 2
radius = 200
current_angle = 0  # Start at 0 radians (rightmost point of horizontal half-circle)
angle_speed = 0.05  # How fast the rect moves along the arc

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Calculate new position based on current angle
    new_x = circle_center_x + radius * math.cos(current_angle)
    new_y = circle_center_y + radius * math.sin(current_angle)

    # Update the rect's center
    rect.center = (int(new_x), int(new_y))

    # Increment the angle for the next frame
    current_angle += angle_speed

    # Loop the movement if it reaches the end of the half-circle
    # For a half-circle from 0 to pi (180 degrees)
    if current_angle > math.pi:
        current_angle = 0 # Reset to start for continuous looping

    screen.fill(white)
    pygame.draw.rect(screen, red, rect)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()'''

'''import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Rotate Rectangle without Rotating Screen")

# Original rectangle properties
rect_color = (255, 0, 0)
rect_width = 100
rect_height = 50
original_rect_center = (400, 300)
angle = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                angle += 5
            if event.key == pygame.K_RIGHT:
                angle -= 5

    screen.fill((0, 0, 0)) # Clear the screen

    # Create and draw the rectangle on its own surface
    rect_surface = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
    pygame.draw.rect(rect_surface, rect_color, (0, 0, rect_width, rect_height))

    # Rotate the surface
    rotated_surface = pygame.transform.rotate(rect_surface, angle)

    # Get the new rect and set its center
    rotated_rect = rotated_surface.get_rect(center=original_rect_center)

    # Blit the rotated surface to the screen
    screen.blit(rotated_surface, rotated_rect)

    pygame.display.flip()

pygame.quit()'''

import pygame
import math

pygame.init()

# ตั้งค่าหน้าจอ
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rocket Following Curved Path")

# สี
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 100, 100)
GREEN = (0, 255, 0)

# จุดเริ่ม (กลางจอ)
origin = (WIDTH // 2, HEIGHT // 2)

# จุดเป้าหมาย (scale 20 → 200 เพื่อเห็นชัด)
targets = [(200, 200), (200, -200), (-200, -200), (-200, 200)]
target_index = 0  # เริ่มจากเป้าแรก

# easing function
def easing(t):
    return (1 - math.cos(math.pi * t)) / 2

def trajectory_point(xf, yf, t):
    """คืนจุด (x,y) ณ เวลาสัดส่วน t [0,1]"""
    Rf = math.hypot(xf, yf)
    theta_f = math.atan2(yf, xf)
    s = easing(t)
    r = Rf * s
    theta = theta_f * s
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    return origin[0] + int(x), origin[1] - int(y)

# state ของการบิน
t = 0.0
speed = 0.005  # ความเร็ว (ค่ามาก = ไปถึงไว)
flying = True

clock = pygame.time.Clock()
running = True

while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if flying:
        # คำนวณตำแหน่งจรวด
        tx, ty = targets[target_index]
        rocket_pos = trajectory_point(tx, ty, t)

        # วาดจรวด (วงกลมสีขาวแทน sprite)
        pygame.draw.circle(screen, WHITE, rocket_pos, 8)

        # วาด origin
        pygame.draw.circle(screen, GREEN, origin, 6)

        # วาดเป้าหมาย
        end_pos = (origin[0] + tx, origin[1] - ty)
        pygame.draw.circle(screen, RED, end_pos, 6)

        # update t
        t += speed
        if t >= 1.0:  # ถึงเป้าแล้ว
            t = 0.0
            target_index = (target_index + 1) % len(targets)  # ไปเป้าถัดไป
    else:
        # วาด origin
        pygame.draw.circle(screen, GREEN, origin, 6)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
