
from pygame.draw import circle, line
from pygame.math import Vector2

class Agent:
    def __init__(self, position, radius, color):
        self.screen_width = 1280
        self.screen_height = 720
        self.radius = radius
        self.cycle_color = color
        self.position = position
        self.vel = Vector2(0,0)
        self.acc = Vector2(0,0)
        self.mass = 1.0
        self.EYE_SIGHT = 100
        self.STOP_DIST = 5
        self.detect_distance = 300
        self.safe_distance = 500
        self.target = Vector2(0,0)
        self.gravity = Vector2(0,0)
        self.center_of_mass = Vector2(0,0)
    
    def seek_to(self, target_pos):
        MAX_FORCE = 5
        d = target_pos - self.position
        if d.length_squared() == 0:
            return
        
        desired = d.normalize() * MAX_FORCE
        steering = desired - self.vel 
        if steering.length() > MAX_FORCE: 
            steering.scale_to_length(MAX_FORCE)

        self.apply_force(steering)

    def arrive_to(self, target_pos):
        '''add arriving bahavior here'''
        self.target = target_pos
        MAX_FORCE = 2

        d = target_pos - self.position

        if d.length_squared() == 0:
            return True
        
        dist = d.length() # square root is expensive in games
        if dist < self.STOP_DIST:
            desired = Vector2(0,0)

        elif dist < self.EYE_SIGHT:
            # slowing down forces
            desired = d.normalize() * (MAX_FORCE*(dist/self.EYE_SIGHT))
        else:
            desired = d.normalize() * MAX_FORCE

        steering = desired - self.vel 
        if steering.length() > MAX_FORCE: 
            steering.scale_to_length(MAX_FORCE)
        
        self.apply_force(steering)

    def flee_from(self, target_pos):
        MAX_FORCE = 5

        d = target_pos - self.position
        dist = d.length()
        if d.length_squared() == 0:
            return
        
        if dist > self.safe_distance:
            desired = Vector2(0,0)
        elif dist < self.detect_distance:
            desired = d.normalize() * (MAX_FORCE*(self.detect_distance/dist))*-1
        else:
            desired = Vector2(0,0)

        steering = desired - self.vel 
        if steering.length() > MAX_FORCE: 
            steering.scale_to_length(MAX_FORCE)
        
        self.apply_force(steering)

    def apply_force(self, force):
        self.acc += force / self.mass

    def set_gravity(self, gravity):
        self.gravity = gravity
    
    def get_cohesion_force(self, agents):
        count = 0
        center_of_mass = Vector2(0,0)
        for agent in agents:
            dist = (agent.position - self.position).length_squared()
            if 0 < dist < 400 * 400:
                center_of_mass += agent.position
                count += 1
        
        if count > 0:
            center_of_mass /= count

            d = center_of_mass - self.position
            d.scale_to_length(2)

            self.center_of_mass = center_of_mass

            return d
        return Vector2()
    
    def get_separation_force(self, agents):
        s = Vector2()
        count = 0
        for agent in agents:
            dist = (agent.position - self.position).length_squared()
            if dist < 100*100 and dist != 0:
                d = self.position - agent.position
                s += d
                count += 1

        if count > 0:
            s.scale_to_length(2)
            return s
        return Vector2()
    
    def get_align_force(self, agents):
        s = Vector2()
        count = 0
        for agent in agents:
            dist = (agent.position - self.position).length_squared()
            if dist < 500*500 and dist != 0:
                s += agent.vel
                count += 1

        if count > 0 and s != Vector2():
            s /= count
            s.scale_to_length(2)
            return s
        return Vector2()
    
    def bound_check(self, agent):
        if agent.position.x < -30:
            agent.position.x = self.screen_width + 30
        elif agent.position.x > self.screen_width + 30:
            agent.position.x = -20
        if agent.position.y < -10:
            agent.position.y = self.screen_height + 30
        elif agent.position.y > self.screen_height + 30:
            agent.position.y = -20
            
    def update(self, delta_time_s):
        self.vel = self.vel + self.acc + self.gravity
        self.vel *= 0.95
        self.position = self.position + self.vel
        self.acc.x = 0
        self.acc.y = 0

    def draw(self,screen):
        line(screen, (100, 100, 100), self.position, self.center_of_mass)
        circle(screen, self.cycle_color, 
               self.position, self.radius)
    