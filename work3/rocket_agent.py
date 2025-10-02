import math
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
        self.STOP_DIST = 5
        self.IsShoot = False
        self.target = Vector2(0,0)
        self.timer = 0
        self.gravity = Vector2(0,1)

    def shoot_from_cannon(self,target_pos):
        if self.IsShoot:
            MAXFORCE = 6
            d = target_pos - self.position
            if d.length_squared() == 0:
                return
            
            desired = d.normalize() * MAXFORCE
            steering = desired - self.vel
            if steering.length() > MAXFORCE:
                steering.scale_to_length(MAXFORCE)

            self.apply_force(steering)

    def seek_to(self):
        MAXFORCE = 15
        d = self.target - self.position
        if d.length_squared() == 0:
            return
            
        dist = d.length() 
        if dist < self.STOP_DIST:
            desired = Vector2(0,0)
            self.color = (212,212,212) #(190,190,190)
            self.timer = 0
            self.IsShoot = False
        else:
            desired = d.normalize() * MAXFORCE
        
        steering = desired - self.vel
        if steering.length() > MAXFORCE:
            steering.scale_to_length(MAXFORCE)

        self.apply_force(steering)

    def set_gravity(self, gravity):
        self.gravity = gravity

    def get_cohesion_force(self, agents):

        center_of_mass = Vector2(0,0)
        for agent in agents:
            center_of_mass += agent.position

        center_of_mass /= len(agents)

        d = center_of_mass - self.position
        d.scale_to_length(2)

        return d

    def apply_force(self, force):
        self.acc += force/ self.mess

    def update(self, delta_time_ms, delay):
        self.vel = self.vel + self.acc + self.gravity

        self.position = self.position + self.vel
        self.acc = Vector2(0, 0)
        if not self.IsShoot:
            self.vel = Vector2(0, 0)

    def draw(self, screen):
        #circle(screen, (100,100,0), self.position, self.EYE_SIGHT, width = 1)
        circle(screen, self.color, self.position, self.circle_redius)