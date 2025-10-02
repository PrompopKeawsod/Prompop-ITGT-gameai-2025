import pygame,time
from pygame.draw import circle, line, rect
from pygame.math import Vector2
from ant_agent import Agent

screen_width = 1280
screen_height = 720

class App:
    def __init__(self): #do once
        print("App is create")
        
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        
        self.running = True

        self.predator_pos = Vector2(0,0)
        self.ant_colony_pos = Vector2(0,screen_height)
        self.food_pos = Vector2(screen_width-100,100)

        self.agent_num = 5
        self.agents = []

        #Way point
        self.waypoint = [self.ant_colony_pos, self.food_pos]
        self.currant_waypoints = []
        self.targets = []

        self.add_agent(self.agent_num)

    def add_agent(self, num):
        for agent in range(num):
            spawnpoint = (agent + 1) * 100
            self.agents.append(Agent(position=Vector2(0, screen_height + spawnpoint), redius=10, color=(255,0,0)))
            self.currant_waypoints.append(0)
            self.targets.append(self.waypoint[self.currant_waypoints[agent]])

    def handle_input(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.predator_pos = Vector2(mouse_x,mouse_y)


    def update(self, delta_time_ms):
        for i,agent in enumerate(self.agents): #
            d = agent.position - self.targets[i]
            dist = d.length()

            if dist < 5:
                self.currant_waypoints[i] += 1
                
                if self.currant_waypoints[i] == 1:
                    agent.color = (255,0,0)
                else:
                    agent.color = (255,105,180)

                if self.currant_waypoints[i] >= len(self.waypoint):
                    self.currant_waypoints[i] = 0
            self.targets[i] = self.waypoint[self.currant_waypoints[i]]

            agent.seek_to(self.targets[i])
            agent.fee_form(self.predator_pos)
            agent.update(delta_time_ms)
        

    def draw(self):
        self.screen.fill("grey")
        
        circle(self.screen, (255,182,193), self.food_pos, 50)
        for agent in self.agents:
            agent.draw(self.screen)
        
        circle(self.screen, (205,133,63), self.ant_colony_pos, 200)
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