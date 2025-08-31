from pygame.draw import circle, line, rect
from pygame.math import Vector2

class Agent:
    def __init__(self, position, redius, color):
        self.color = color
        self.circle_redius = redius
        self.vel = Vector2(0, 0)
        self.position = position
        self.acc = Vector2(0, 0)
        self.mess = 1.0

    def seek_to(self, target_pos):
        MAXFORCE = 5
        d = target_pos - self.position
        if d.length_squared() == 0:
            return
        
        desired = d.normalize() * MAXFORCE
        steering = desired - self.vel
        if steering.length() > MAXFORCE:
            steering.scale_to_length(MAXFORCE)

        self.apply_force(steering)

    def apply_force(self, force):
        self.acc += force/ self.mess

    def update(self, delta_time_ms):
        self.vel = self.vel + self.acc

        self.position = self.position + self.vel

        self.acc = Vector2(0, 0)

    def draw(self, screen):
        circle(screen, self.color, self.position, self.circle_redius)