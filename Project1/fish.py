import pygame, random
from pygame.draw import circle, line, rect
from pygame.math import Vector2

class Agent:
    def __init__(self, position, redius, color, Timer):
        self.color = color
        self.circle_redius = redius
        self.vel = Vector2(0, 0)
        self.position = position
        self.acc = Vector2(0, 0)
        self.mess = 1.0
        self.EYE_SIGHT = 100
        self.EYE_SIGHT_flee = 200
        self.STOP_DIST = 100
        self.target = Vector2(0,0)
        self.gravity = Vector2(0,0)
        self.center_of_mass = Vector2()
        self.IsArrive = False
        self.turn_rate = 0.08
        self.facing_right = False

        self.HungryTimer = 0
        self.max_HungryTimer = Timer
        self.IsHungry = False

        self.search_food = None
        self.IsFound_food = False

        self.image = pygame.image.load("Assets/fish.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 70))

        self.image2 = pygame.image.load("Assets/fish_hungry.png").convert_alpha()
        self.image2 = pygame.transform.scale(self.image2, (100, 70))

    def seek_to(self, target_pos, stop_dist):
        self.target = target_pos
        MAXFORCE = 10
        d = target_pos - self.position
        if d.length_squared() == 0:
            return
        
        dist = d.length_squared()
        if dist < stop_dist * stop_dist:
            desired = Vector2(0,0)
            self.IsArrive = True
        else:
            desired = d.normalize() * MAXFORCE

        if self.vel.length_squared() > 0:
            desired = self.vel.lerp(desired, 0.2)

        steering = desired - self.vel
        if steering.length_squared() > MAXFORCE * MAXFORCE:
            steering.scale_to_length(MAXFORCE)

        self.apply_force(steering)

    def find_food(self, foods):
        if not foods:
            return None

        closest_food = None
        closest_dist = float('inf')

        for food in foods:
            if food.IsEaten:
                continue
            dist = (food.position - self.position).length_squared()
            if dist < closest_dist:
                closest_dist = dist
                closest_food = food

        return closest_food

    def arrive_to(self, target_pos):
        MAXFORCE = 3
        
        d = target_pos - self.position   

        if d.length_squared() == 0:
            return
        
        dist = d.length_squared()
        if dist < self.STOP_DIST * self.STOP_DIST:
            desired = Vector2(0,0)
            self.IsArrive = True
        elif dist < self.EYE_SIGHT * self.EYE_SIGHT:
            desired = d.normalize() * (MAXFORCE * (dist/self.EYE_SIGHT))
        else:
            desired = d.normalize() * MAXFORCE

        if self.vel.length_squared() > 0:
            desired = self.vel.lerp(desired, self.turn_rate)
        
        steering = desired - self.vel
        if steering.length() > MAXFORCE:
            steering.scale_to_length(MAXFORCE)

        self.apply_force(steering)

    def flee_from(self, target_pos):
        MAXFORCE = 8
        d = self.position - target_pos

        if d.length_squared() == 0:
            return

        dist = d.length_squared()
        if dist < self.EYE_SIGHT_flee*self.EYE_SIGHT_flee:
            strength = ((self.EYE_SIGHT_flee*self.EYE_SIGHT_flee) - dist) / self.EYE_SIGHT_flee
            desired = d.normalize() * (MAXFORCE * strength)
            steering = desired - self.vel
            if steering.length() > MAXFORCE:
                steering.scale_to_length(MAXFORCE)
            return steering

        return Vector2(0, 0)
    
    def apply_force(self, force):
        self.acc += force/ self.mess

    def set_gravity(self, gravity):
        self.gravity = gravity

    def get_cohesion_force(self, agents):

        center_of_mass = Vector2(0,0)
        count = 0
        for agent in agents:
            if agent is self or agent.IsFound_food:  # อย่าเอาตัวที่ไปกินอาหารมาคิด
                continue

            dist = (agent.position - self.position).length_squared() #ทำเหมือน length แต่ไม่ใช้ square root ช่วยลดทรัพยากรเครื่อง
            if 0 < dist < 300*300: #eye sight
                center_of_mass += agent.position
                count += 1

        if count > 0:
            center_of_mass /= count
            d = center_of_mass - self.position
            d.scale_to_length(0.5)

            self.center_of_mass = center_of_mass

            return d
        
        return Vector2()
    
    def get_seperation_force(self, agents):
        s = Vector2()
        count = 0
        for agent in agents:
            '''if self.IsFound_food or agent.IsFound_food:
                continue
'''
            dist = (agent.position - self.position).length_squared()
            if dist < 110*110 and dist != 0:
                d = self.position - agent.position
                s += d
                count += 1
        if count > 0:
            s.scale_to_length(1)
            return s

        return Vector2()

    def update(self, delta_time_ms):
        self.vel = self.vel + self.acc + self.gravity
        self.vel *= 0.8
        self.position = self.position + self.vel
        
        self.acc = Vector2(0, 0)

    def draw(self, screen):
        if self.vel.x > 0.4:       # ถ้าเคลื่อนไปขวาแรงพอ
            self.facing_right = True
        elif self.vel.x < -0.4:    # ถ้าเคลื่อนไปซ้ายแรงพอ
            self.facing_right = False

        if self.IsHungry:
            if self.facing_right:
                fish_img = pygame.transform.flip(self.image2, True, False)
            else:
                fish_img = self.image2
        else:
            if self.facing_right:
                fish_img = pygame.transform.flip(self.image, True, False)
            else:
                fish_img = self.image

        rect = fish_img.get_rect(center=(self.position.x, self.position.y))
        screen.blit(fish_img, rect.topleft)

        

        '''line(screen,(100,0,0), self.position, self.center_of_mass)
        circle(screen, self.color, self.position, self.circle_redius)'''