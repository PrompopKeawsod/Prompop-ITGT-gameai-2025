import pygame
from pygame.draw import circle, line, rect
from pygame.math import Vector2
from fish import Agent
from food import Food
from monster import Monster
import random, math

screen_width = 1280
screen_height = 720

class App:
    def __init__(self): #do once
        print("App is create")

        self.screen_xy = Vector2(screen_width,screen_height)
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load("Assets/bg.png").convert()
        self.background = pygame.transform.scale(self.background, (screen_width, screen_height))

        self.running = True
        self.CHAGE_DIR = pygame.USEREVENT +1
        pygame.time.set_timer(self.CHAGE_DIR, 2000)
        self.timer = 0

        self.image_x = 50
        self.image_y = 50

        self.agents = []
        self.max_agent = 6

        for i in range(self.max_agent):
            agent = Agent(position=Vector2(random.randint(self.image_x,screen_width//2), random.randint(self.image_y,screen_height)), redius=10, color=((random.randint(0,255), random.randint(0,255), random.randint(0,255))), Timer= random.randint(5, 20))
            agent.mass = 10
            self.agents.append(agent)

        self.group_target = self.get_random_position(self.agents[0].position)

        #food
        self.foods = []
        self.max_foods = self.max_agent
        self.stop_foods_dist = 20

        self.monster = Monster(position=Vector2(screen_width + 200, screen_height//2), redius=5, color="Red", screen_xy=self.screen_xy)

    def get_random_position(self, pos):
            new_pos = Vector2()
            if self.image_x <= pos.x <= screen_width//2 - self.image_x:
                new_pos.x = random.randint(screen_width//2, screen_width - self.image_x)
            else:
                new_pos.x = random.randint(self.image_x, screen_width//2 - self.image_x)
            
            if self.image_y <= pos.y <= screen_height//2 - self.image_y:
                new_pos.y = random.randint(screen_height//2, screen_height - 65 - self.image_x)
            else:
                new_pos.y = random.randint(self.image_y, screen_height//2 - self.image_y)

            return new_pos

    def handle_input(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    
                    if len(self.foods) < self.max_foods:
                        self.foods.append(Food(Vector2(mouse_x, mouse_y)))

    def bound_check(self, agent):
        if agent.position.x <= 30:
            agent.position.x = 30
            agent.vel.x *= -0.5   
        elif agent.position.x >= screen_width - 30:
            agent.position.x = screen_width - 30
            agent.vel.x *= -0.5

        if agent.position.y <= 30 + 65:
            agent.position.y = 30 + 65
            agent.vel.y *= -0.5
        elif agent.position.y >= screen_height - 95:
            agent.position.y = screen_height - 95
            agent.vel.y *= -0.5

    def update(self, delta_time_s):
        #fish
        for agent in self.agents:
            if agent.IsArrive and not agent.IsFound_food:
                self.group_target = self.get_random_position(agent.position)
                for a in self.agents:
                    a.IsArrive = False
                break

        for i,agent in enumerate(self.agents):

            if not agent.IsHungry:
                agent.HungryTimer += delta_time_s
            if agent.HungryTimer >= agent.max_HungryTimer:
                agent.IsHungry = True
                agent.HungryTimer = 0
                agent.search_target = None
                print("agent", i, "is Hungry")

            if agent.IsHungry:
                target_food = agent.find_food(self.foods)
                if target_food:
                    agent.IsFound_food = True
                    agent.seek_to(target_food.position, self.stop_foods_dist)

                    seperation_f = agent.get_seperation_force(self.agents)
                    agent.apply_force(seperation_f)

                else:
                    agent.IsFound_food = False
                    cohesion_f = agent.get_cohesion_force(self.agents)
                    agent.apply_force(cohesion_f)

                    seperation_f = agent.get_seperation_force(self.agents)
                    agent.apply_force(seperation_f)

                    agent.arrive_to(self.group_target)
            else:
                agent.IsFound_food = False
                cohesion_f = agent.get_cohesion_force(self.agents)
                agent.apply_force(cohesion_f)

                seperation_f = agent.get_seperation_force(self.agents)
                agent.apply_force(seperation_f)

                agent.arrive_to(self.group_target)

            # bound / update
            self.bound_check(agent)

            if self.monster.IsSwim:
                flee_f = agent.flee_from(self.monster.position)
                agent.apply_force(flee_f)
                
            agent.update(delta_time_s)

            # check eat (collision) AFTER agent moved
            if agent.IsHungry:
                for food in self.foods:
                    # ระยะกิน
                    if (agent.position - food.position).length_squared() < self.stop_foods_dist * self.stop_foods_dist:
                        food.IsEaten = True
                        agent.IsHungry = False
                        agent.HungryTimer = 0
                        agent.search_target = None
                        agent.IsFound_food = False
                        agent.max_HungryTimer = random.randint(5,20)
                        break
        
        #monster
        if not self.monster.IsSwim:
            self.monster.Timer += delta_time_s
            print(self.monster.Timer)
            if self.monster.Timer >= self.monster.max_Timer:
                self.monster.IsSwim = True
                self.monster.Timer = 0

        if self.monster.IsSwim:
            if self.monster.direction == -1:  # ขวา → ซ้าย
                self.monster.seek_to(Vector2(-200, self.monster.position.y))
            else:  # ซ้าย → ขวา
                self.monster.seek_to(Vector2(self.screen_xy.x + 200, self.monster.position.y))

        self.monster.update(delta_time_s)
        
        #food
        for food in self.foods:
            food.update(delta_time_s)

        new_foods = []
        for f in self.foods:
            if not f.IsEaten:
                new_foods.append(f)

        self.foods = new_foods

    def draw(self):
        self.screen.blit(self.background, (0,0))

        for food in self.foods:
            food.draw(self.screen)

        self.monster.draw(self.screen)
        
        for agent in self.agents:
            agent.draw(self.screen)

        #circle(self.screen, "red", self.group_target, 5)
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