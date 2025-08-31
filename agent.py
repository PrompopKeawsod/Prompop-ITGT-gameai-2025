from pygame.draw import circle, line, rect
from pygame.math import Vector2

class Agent:
    def __init__(self):
        self.color_red = (255,0,0)
        self.circle_redius = 100
        self.vel = Vector2(0, 0)
        self.position = Vector2(200, 200)
        self.acc = Vector2(0, 0)
        self.acc.x = 1
        self.acc.y = 1

    def update(self):
        self.vel = self.vel + self.acc

        self.position = self.position + self.vel

        self.acc.x = 0
        self.acc.y = 0

    def draw(self, screen):
        circle(screen, self.color_red, self.position, self.circle_redius)