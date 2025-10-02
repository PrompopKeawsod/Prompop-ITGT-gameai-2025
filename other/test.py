import pygame
from pygame.draw import circle, lines, rect
from pygame.math import Vector2
from test_agent import Agent
import random
import math

screen_width = 1280
screen_height = 720

class App:
    def __init__(self):
        print("Application is created")
        pygame.init()
        
        self.running = True
        self.screen_width = 1280
        self.screen_height = 720
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.CHAGE_DIR = pygame.USEREVENT +1
        pygame.time.set_timer(self.CHAGE_DIR, 2000)
        self.timer = 0
        self.ball = Agent(position = Vector2(screen_width/2, screen_height/2), 
                          radius= 30, 
                          color= (100,0,0))
        """self.agents = [
            Agent(position = Vector2(100, 100), 
                          radius= 30, 
                          color= (100,0,0)),
            Agent(position = Vector2(300, 50), 
                          radius= 20, 
                          color= (100,0,0)),
            Agent(position = Vector2(600, 300), 
                          radius= 10, 
                          color= (100,0,0))]"""
        self.agents = []

        for agent in self.agents:
            agent.vel = Vector2(0,0)

        self.waypoints = [Vector2(100,0), Vector2(1000, 100), Vector2(0, 800)]
        self.current_waypoint_numbers = [0, 1, 2]  
        self.targets = [self.waypoints[self.current_waypoint_numbers[0]],
                        self.waypoints[self.current_waypoint_numbers[1]],
                        self.waypoints[self.current_waypoint_numbers[2]],
        ]

 

        for i in range(5):
            agent = Agent(position = Vector2(random.randint(100,screen_width), random.randint(100,screen_height)), 
                          radius= 20, 
                          color= (random.randint(0,255),random.randint(0,255),random.randint(0,255)))
            agent.mass = 10
            self.agents.append(agent)

        #self.agents[0].set_gravity(Vector2(0,3)) 
        #self.agents[1].set_gravity(Vector2(0,3)) 
        #self.agents[2].set_gravity(Vector2(0,3)) 
    
    def handle_input(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
    
    def update(self, delta_time_s):
        for i, agent in enumerate(self.agents):
            cohension_force = agent.get_cohesion_force(self.agents)
            agent.apply_force(cohension_force)

            separation_force = agent.get_separation_force(self.agents)
            agent.apply_force(separation_force)

            align_force = agent.get_align_force(self.agents)
            agent.apply_force(align_force)

            agent.bound_check(agent)
            agent.update(delta_time_s)
        

    def draw(self):
        self.screen.fill("grey")
        
        for agent in self.agents:
            agent.draw(self.screen)

        pygame.display.flip()

    def run(self):
        while self.running:
            delta_time_s = self.clock.tick(60)/1000
            self.handle_input()
            self.update(delta_time_s)
            self.draw()
 
        
        pygame.quit()

def main():
    app = App()
    app.run()

if __name__ == "__main__":
    main()