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
        self.EYE_SIGHT = 100
        self.STOP_DIST = 5 #ระยะที่บอลต้องใกล้หยุด
        self.target = Vector2(0,0)

    def seek_to(self, target_pos):
        self.target = target_pos
        MAXFORCE = 2
        d = target_pos - self.position
        if d.length_squared() == 0:
            return
        
        desired = d.normalize() * MAXFORCE
        steering = desired - self.vel
        if steering.length() > MAXFORCE:
            steering.scale_to_length(MAXFORCE)

        self.apply_force(steering)

    def arrive_to(self, target_pos):
        MAXFORCE = 5
        
        d = target_pos - self.position   

        if d.length_squared() == 0:
            return
        
        dist = d.length() #การทำ squareroot จะกินระบบมาก ควรเรียกครั้งเดียว 
        if dist < self.STOP_DIST:
            desired = Vector2(0,0)
        elif dist < self.EYE_SIGHT:
            desired = d.normalize() * (MAXFORCE * (dist/self.EYE_SIGHT)) #มองเป็นพลังงาน ระยะมากยิ่งไว
        else:
            desired = d.normalize() * MAXFORCE
        
        steering = desired - self.vel
        if steering.length() > MAXFORCE:
            steering.scale_to_length(MAXFORCE)

        self.apply_force(steering)

    def fee_form(self, target_pos):
        MAXFORCE = 5
        d = (target_pos - self.position) * -1
        if d.length_squared() == 0:
            return
        
        dist = d.length()
        if dist > self.EYE_SIGHT:
            desired = Vector2(0,0)
        else:
            desired = d.normalize() * (MAXFORCE * ((self.EYE_SIGHT - dist)/self.EYE_SIGHT))


        steering = desired - self.vel
        if steering.length() > MAXFORCE:
            steering.scale_to_length(MAXFORCE)

        self.apply_force(steering)
    
    def patrol(self, target_pos):
        
        MAXFORCE = 5
        d = Vector2(100,200) - self.position
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
        #circle(screen, (100,100,0), self.position, self.EYE_SIGHT, width = 1)
        line(screen,(100,0,0), self.position, self.target)
        circle(screen, self.color, self.position, self.circle_redius)