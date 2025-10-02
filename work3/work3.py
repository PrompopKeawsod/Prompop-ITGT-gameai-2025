import pygame,math
from pygame.draw import circle, line, rect
from pygame.math import Vector2
from rocket_agent import Agent

screen_width = 1280
screen_height = 720

class App:
    def __init__(self): #do once
        print("App is create")

        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.screen_color = [212,212,212]
        self.clock = pygame.time.Clock()
        
        self.running = True

        self.timer_delay = 0.05

        #Cannon
        self.basegun_radius = 60
        self.basegun_pos = Vector2(screen_width//2, screen_height - (self.basegun_radius//2))

        self.cannon_size = 20
        self.cannon_pos = Vector2(self.basegun_pos.x - self.basegun_radius, self.basegun_pos.y)
        self.cannon_rotate_speed = 0.01
        self.cannon_current_angle = 0
        self.canon_rotate_backward = False
        self.cannon_dir = Vector2(0,0)

        #Ammo
        self.agents = [
            Agent(self.basegun_pos, redius=10, color=self.screen_color),
            Agent(self.basegun_pos, redius=10, color=self.screen_color),
            Agent(self.basegun_pos, redius=10, color=self.screen_color),
            Agent(self.basegun_pos, redius=10, color=self.screen_color),
            Agent(self.basegun_pos, redius=10, color=self.screen_color),
            Agent(self.basegun_pos, redius=10, color=self.screen_color),
            Agent(self.basegun_pos, redius=10, color=self.screen_color)
        ]
        self.round = 0
        self.max_rounds = len(self.agents)

    def rotateCanon(self,path_x,path_y,path_radius):

        new_x = path_x - path_radius * math.cos(self.cannon_current_angle)
        new_y = path_y - path_radius * math.sin(self.cannon_current_angle)

        self.cannon_pos.x, self.cannon_pos.y = new_x, new_y

        if(self.cannon_current_angle > math.pi):
            self.canon_rotate_backward = True
        elif(self.cannon_current_angle < 0):
            self.canon_rotate_backward = False

        #print(self.cannon_current_angle)

        if(self.canon_rotate_backward):
            self.cannon_current_angle -= self.cannon_rotate_speed
        else:
            self.cannon_current_angle += self.cannon_rotate_speed

    def shoot(self, round):
        if(self.agents[round].IsShoot):
            return
        else:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.agents[round].position = self.cannon_pos
            self.agents[round].color = [255,0,0]
            self.agents[round].target = Vector2(mouse_x,mouse_y)
            self.agents[round].IsShoot = True
            #self.agents[round].shoot_from_cannon(self.basegun_pos + (self.cannon_pos - self.basegun_pos).normalize() * 100)

            if round >= self.max_rounds - 1:
                self.round = 0
            else:
                self.round += 1

    def handle_input(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        #print("E key pressed!")
                        self.shoot(self.round)
        
        #self.target = Vector2(mouse_x,mouse_y)

    def update(self, delta_time_ms):
        self.rotateCanon(self.basegun_pos.x, self.basegun_pos.y, self.basegun_radius)

        for i,agent in enumerate(self.agents):
            if agent.IsShoot:
                agent.timer += delta_time_ms / 1000
                agent.shoot_from_cannon(self.basegun_pos + (self.cannon_pos - self.basegun_pos).normalize() * 2000)
            if agent.timer > self.timer_delay:
                agent.seek_to()
            agent.update(delta_time_ms, self.timer_delay)

    def draw(self):
        self.screen.fill(self.screen_color)
        for i,agent in enumerate(self.agents):
            agent.draw(self.screen)
            if agent.IsShoot:
                color = "red"
            else:
                color = "green"
            circle(self.screen, color, (30 + (60 * i), screen_height - 30), 20)

        current_x = 30 + (60 * self.round)

        x1 = current_x - 20
        x2 = current_x + 20
        y_line = screen_height - 5  

        line(self.screen, (75,75,75), (x1, y_line), (x2, y_line), 5)           
        
        circle(self.screen, (125, 125, 125), self.cannon_pos, self.cannon_size)
        circle(self.screen, (137, 81, 41), self.basegun_pos, self.basegun_radius)
        #line(self.screen,(100,0,0), self.basegun_pos, self.basegun_pos + (self.cannon_pos - self.basegun_pos).normalize()*100)
        

        pygame.display.flip()

    def run(self):
        while self.running:        
            delta_time_ms = self.clock.tick(60)    
            self.handle_input()
            self.update(delta_time_ms)
            self.draw()

            

def main():
    app = App()
    app.run()

if __name__ == "__main__":
    main()