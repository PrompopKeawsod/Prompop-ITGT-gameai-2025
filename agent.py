from pygame.draw import circle, line, rect
from pygame.math import Vector2

class Agent:
    def __init__(self, position, redius, color):
        self.color = color
        self.circle_redius = redius
        self.vel = Vector2(0, 0)
        self.position = position
        self.acc = Vector2(0, 0)
        self.acc.x = 1
        self.acc.y = 1

    def update(self, delta_time_ms):
        self.vel = self.vel + self.acc

        self.position = self.position + self.vel

        self.acc.x = 0
        self.acc.y = 0

    def draw(self, screen):
        circle(screen, self.color, self.position, self.circle_redius)