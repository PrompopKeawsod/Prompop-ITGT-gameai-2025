
#lab2
import pygame
from pygame.draw import circle, line, rect
from pygame.math import Vector2

from agent import Agent
import random
import math

window_width = 1280
window_height = 720

class App:
    def __init__(self):
        print("Application is created.")
        pygame.init()
        
        self.timer = 0
        self.screen = pygame.display.set_mode((window_width, window_height))

        self.clock = pygame.time.Clock()
        self.CHANGE_DIR = pygame.USEREVENT +1
        pygame.time.set_timer(self.CHANGE_DIR, 2000)
        self.running = True
        
        self.agents = []
        self.food_list = []


        for i in range(10):
            agent = Agent(position = Vector2(random.randint(0,window_width), random.randint(0,window_height)), 
                          radius = 10, 
                          color = (random.randint(0,255),random.randint(0,255),random.randint(0,255)))
            agent.mass = 10
            self.agents.append(agent)

        self.target = Vector2(0, 0)
        self.current_waypoint = 0

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = Vector2(event.pos)
                self.food_list.append(pos)
                    

    def bound_check(self,agent):
        if agent.position.x < -10:
            agent.position.x = window_width + 30
        elif agent.position.x > window_width + 34:
            agent.position.x = -5 
        if agent.position.y < -10:
            agent.position.y = window_height + 30
        elif agent.position.y > window_height + 34:
            agent.position.y = -5 


    def update(self, delta_time_s):
        for agent in self.agents:
            cohesion_f = agent.get_cohesion_force(self.agents)
            separation_f = agent.get_separation_force(self.agents)
            align_f = agent.get_align_force(self.agents)
            wall_f = agent.avoid_walls(window_width, window_height) * 5.0
            wander_f = agent.wander() *2
            agent.apply_force(cohesion_f * 2.0)
            agent.apply_force(separation_f * 1.5)
            agent.apply_force(align_f * 1.5)
            agent.apply_force(wall_f * 5.0)
            agent.apply_force(wander_f * 0.2)
            agent.seek_food_direct(self.food_list)
            agent.update(delta_time_s, window_width,window_height)

            
            

        
    def draw(self):
        self.screen.fill("gray")
        for agent in self.agents:
            agent.draw(self.screen)
        for food in self.food_list:
            circle(self.screen, (255, 200, 0), food, 5)  #food

        pygame.display.flip()

    

    def run(self):
        while self.running:
            dt = self.clock.tick(60) /1000.0
            self.handle_input()
            self.update(dt)
            self.draw()


        pygame.quit()


def main():
    app = App()
    app.run()

if __name__ == "__main__":
    main()
