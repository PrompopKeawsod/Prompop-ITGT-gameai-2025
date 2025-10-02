import pygame
from pygame.draw import circle, line, rect
from pygame.math import Vector2

class Food:
    def __init__(self, pos):
        self.position = pos
        self.vel = Vector2(0, 0)
        self.acc = Vector2(0, 0)
        self.mess = 1.0
        self.gravity = Vector2(0,0)
        self.IsEaten = False
        self.speed = 50
        self.angle = 0
        self.rotate_speed = 90
        self.alpha = 255
        self.on_ground = False

        self.image = pygame.image.load("Assets/fish_food.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))

    def apply_force(self, force):
        self.acc += force/ self.mess

    def set_gravity(self, gravity):
        self.gravity = gravity

    def update(self, delta_time_s):
        if not self.on_ground:
            self.position.y += self.speed * delta_time_s
            self.angle += self.rotate_speed * delta_time_s
            self.angle %= 360

            if self.position.y >= 655:
                self.on_ground = True
        else:
            self.alpha -= 1000 * delta_time_s
            if self.alpha <= 0:
                self.IsEaten = True

    def draw(self, screen):
        rotated_img = pygame.transform.rotate(self.image, self.angle)
        rotated_img.set_alpha(max(0, int(self.alpha)))  # apply alpha

        rect = rotated_img.get_rect(center=(int(self.position.x), int(self.position.y)))
        screen.blit(rotated_img, rect.topleft)
        #circle(screen, "green", self.position, 5)
    