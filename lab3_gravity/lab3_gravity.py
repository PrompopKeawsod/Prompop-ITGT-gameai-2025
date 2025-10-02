import pygame
#import pygame_gui
from pygame.draw import circle, line, rect
from pygame.math import Vector2
from lab3_gravity_agent import Agent
import random, math

screen_width = 1280
screen_height = 720

class App:
    def __init__(self): #do once
        print("App is create")

        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        
        self.running = True
        self.CHAGE_DIR = pygame.USEREVENT +1
        pygame.time.set_timer(self.CHAGE_DIR, 2000)
        self.timer = 0
        #self.manager = pygame_gui.UIManager((800, 600))

        self.ball = Agent(position=Vector2(screen_width//2, screen_height//2), redius=50, color=(255,0,0)) #เรียกและส่งหน้าจอไปยังไฟล์ agent

        self.agents = []

        for i in range(5):
            agent = Agent(position=Vector2(random.randint(10,screen_width), random.randint(10,screen_height)), redius=10, color=((random.randint(0,255), random.randint(0,255), random.randint(0,255))))
            agent.mass = 10
            self.agents.append(agent)




    def handle_input(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
        #mouse_x, mouse_y = pygame.mouse.get_pos()
        #self.target = Vector2(mouse_x,mouse_y)


    def bound_check(self, agent):
        if agent.position.x < -10:
            agent.position.x = screen_width + 10
        elif agent.position.x > screen_width + 10:
            agent.position.x = -10
        if agent.position.y < -10:
            agent.position.y = screen_height + 10
        elif agent.position.y > screen_height + 10:
            agent.position.y = -10



    def update(self, delta_time_s):

        for i,agent in enumerate(self.agents): #

            cohesion_f = agent.get_cohesion_force(self.agents)
            agent.apply_force(cohesion_f)

            seperation_f = agent.get_seperation_force(self.agents)
            agent.apply_force(seperation_f)

            align_f = agent.get_align_force(self.agents)
            agent.apply_force(align_f)
            self.bound_check(agent)
            agent.update(delta_time_s)


    def draw(self):
        self.screen.fill("grey")
        
        for agent in self.agents:
            agent.draw(self.screen)

        #self.manager.draw_ui(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:        
            delta_time_s = self.clock.tick(60) / 1000
            self.handle_input()
            self.update(delta_time_s)
            self.draw()

            

def main():
    app = App()
    app.run()

if __name__ == "__main__":
    main()