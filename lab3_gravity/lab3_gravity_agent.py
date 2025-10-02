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
        self.gravity = Vector2(0,0)
        self.center_of_mass = Vector2()

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

    def set_gravity(self, gravity):
        self.gravity = gravity

    def get_cohesion_force(self, agents):

        center_of_mass = Vector2(0,0)
        count = 0
        for agent in agents:

            dist = (agent.position - self.position).length_squared() #ทำเหมือน length แต่ไม่ใช้ square root ช่วยลดทรัพยากรเครื่อง
            if 0 < dist < 400*400: #eye sight
                center_of_mass += agent.position
                count += 1

        if count > 0:
            center_of_mass /= count
            d = center_of_mass - self.position
            d.scale_to_length(1)

            self.center_of_mass = center_of_mass

            return d
        
        return Vector2()
    
    def get_seperation_force(self, agents):
        s = Vector2()
        count = 0
        for agent in agents:
            dist = (agent.position - self.position).length_squared()
            if dist < 200*200 and dist != 0:
                d = self.position - agent.position
                s += d
                count += 1
        if count > 0:
            s.scale_to_length(1)
            return s

        return Vector2()
    
    def get_align_force(self, agents):
        s = Vector2()
        count = 0
        for agent in agents:
            dist = (agent.position - self.position).length_squared()
            if dist < 300*300 and dist != 0:
                s += agent.vel
                count += 1
        if count > 0 and s != Vector2():
            s /= count
            s.scale_to_length(0.5)
            return s

        return Vector2()

    def update(self, delta_time_ms):
        self.vel = self.vel + self.acc + self.gravity
        self.vel *= 0.8
        self.position = self.position + self.vel
        
        self.acc = Vector2(0, 0)

    def draw(self, screen):
        #circle(screen, (100,100,0), self.position, self.EYE_SIGHT, width = 1)
        line(screen,(100,0,0), self.position, self.center_of_mass)
        circle(screen, self.color, self.position, self.circle_redius)