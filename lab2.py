import pygame
from pygame.draw import circle, line, rect
from pygame.math import Vector2

screen_width = 1280
screen_height = 720

class App:
    def __init__(self): #do once
        print("App is create")
        
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        
        self.running = True

        self.color_red = (255,0,0)
        self.circle_redius = 100
        self.position = Vector2(screen_width//2, screen_height//2)


        self.vel = Vector2(0, 0)

        self.acc = Vector2(0, 0)
        self.acc.x = 1
        self.acc.y = 1

    def handle_input(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

    def update(self):
        self.vel = self.vel + self.acc

        self.position = self.position + self.vel

        self.acc.x = 0
        self.acc.y = 0

    def draw(self):
        self.screen.fill("grey")
        circle(self.screen, self.color_red, self.position, self.circle_redius)
        pygame.display.flip()

    def run(self):
        while self.running:            
            self.handle_input()
            self.update()
            self.draw()

            self.clock.tick(60)

def main():
    app = App()
    app.run()

if __name__ == "__main__":
    main()