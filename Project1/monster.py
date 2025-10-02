import pygame, random
from pygame.draw import circle, line, rect
from pygame.math import Vector2

class Monster:
    def __init__(self, position, redius, color, screen_xy):
        self.color = color
        self.circle_redius = redius
        self.vel = Vector2(0, 0)
        self.position = position
        self.acc = Vector2(0, 0)
        self.mess = 1.0
        self.EYE_SIGHT = 100
        self.STOP_DIST = 30
        self.facing_right = False
        self.Timer = 0
        self.max_Timer = 10
        self.IsSwim = False
        self.screenXY = screen_xy
        self.direction = -1

        self.image = pygame.image.load("Assets/monster.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (175, 150))

        self.image_warning = pygame.image.load("Assets/warning.png").convert_alpha()
        self.image_warning = pygame.transform.scale(self.image_warning, (100, 100))

    def seek_to(self, target_pos):
        MAXFORCE = 10
        d = target_pos - self.position
        if d.length_squared() == 0:
            return
        dist = d.length_squared()
        if dist < self.STOP_DIST * self.STOP_DIST:
            self.vel = Vector2(0,0)
            self.IsSwim = False

            self.direction *= -1

            possible_y = [
                int(200),
                int(self.screenXY.y / 2),
                int(self.screenXY.y - 200)
            ]
            new_y = random.choice(possible_y)

            if self.direction == -1:  # right -> left
                self.position = Vector2(self.screenXY.x + 200, new_y)
            else:                     # left -> right
                self.position = Vector2(-200, new_y)

        desired = d.normalize() * MAXFORCE
        steering = desired - self.vel
        if steering.length() > MAXFORCE:
            steering.scale_to_length(MAXFORCE)

        self.apply_force(steering)

    def apply_force(self, force):
        self.acc += force/ self.mess

    def update(self, delta_time_ms):
        if self.IsSwim:
            self.vel = self.vel + self.acc
            
            self.position = self.position + self.vel

            self.acc = Vector2(0, 0)

    def draw(self, screen):
        if self.vel.x > 0.5:       # ถ้าเคลื่อนไปขวาแรงพอ
            self.facing_right = True
        elif self.vel.x < -0.5:    # ถ้าเคลื่อนไปซ้ายแรงพอ
            self.facing_right = False

        if self.facing_right:
                fish_img = pygame.transform.flip(self.image, True, False)
        else:
            fish_img = self.image

        rect = fish_img.get_rect(center=(self.position.x, self.position.y))
        screen.blit(fish_img, rect.topleft)

        if self.max_Timer - self.Timer < 3:
            if self.direction == -1:
                rect2=self.image_warning.get_rect(center=(self.screenXY.x - 50, self.position.y))
                screen.blit(self.image_warning, rect2.topleft)
            else:
                rect2=self.image_warning.get_rect(center=(50, self.position.y))
                screen.blit(self.image_warning, rect2.topleft) 
        
        #circle(screen, self.color, (500, self.position.y), self.circle_redius)