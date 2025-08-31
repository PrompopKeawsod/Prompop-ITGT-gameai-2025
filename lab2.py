import pygame
from pygame.draw import circle, line, rect
from pygame.math import Vector2
from agent import Agent

screen_width = 1280
screen_height = 720

class App:
    def __init__(self): #do once
        print("App is create")
        
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        
        self.running = True

        self.ball = Agent(position=Vector2(screen_width//2, screen_height//2), redius=100, color=(255,0,0)) #เรียกและส่งหน้าจอไปยังไฟล์ agent

        

    def handle_input(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

    def update(self, delta_time_ms):
        self.ball.update(delta_time_ms)

    def draw(self):
        self.screen.fill("grey")
        self.ball.draw(self.screen)
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