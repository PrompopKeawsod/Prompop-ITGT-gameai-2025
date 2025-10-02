import pygame
#import pygame_gui
from pygame.draw import circle, line, rect
from pygame.math import Vector2
from lab3_agent import Agent
import random, math

screen_width = 1280
screen_height = 720

class App:
    def __init__(self): #do once
        print("App is create")

        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        
        self.running = True
        self.timer = 0
        #self.manager = pygame_gui.UIManager((800, 600))

        self.ball = Agent(position=Vector2(screen_width//2, screen_height//2), redius=50, color=(255,0,0)) #เรียกและส่งหน้าจอไปยังไฟล์ agent

        self.agents = [
            Agent(position=Vector2(100, screen_height//2), redius=50, color=(255,0,0)),
            Agent(position=Vector2(500, screen_height//2), redius=30, color=(242,127,0)),
            Agent(position=Vector2(screen_width//2, 300), redius=10, color=(0,75,100))
        ]

        for agent in self.agents:
            agent.vel = Vector2(1, 0)

        #Way point
        self.waypoint = [Vector2(100,100), Vector2(100,600), Vector2(1000,600), Vector2(1000, 100)]

        self.currant_waypoints = [0, 0, 0]
        self.targets = [
            self.waypoint[self.currant_waypoints[0]],
            self.waypoint[self.currant_waypoints[1]],
            self.waypoint[self.currant_waypoints[2]]
        ]

    def handle_input(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
        #mouse_x, mouse_y = pygame.mouse.get_pos()
        #self.target = Vector2(mouse_x,mouse_y)


    def update(self, delta_time_s):
        self.timer += delta_time_s

        for i,agent in enumerate(self.agents): #
            target = agent.position + (agent.vel.normalize() * 100)
            if self.timer > 1:
                theta = random.randint(-100,100)
                target += Vector2(math.cos(theta), math.sin(theta)) * 50

            agent.seek_to(target)
            agent.update(delta_time_s)

        if self.timer > 1:
            self.timer = 0

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