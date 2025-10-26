import pygame,math
from pygame.draw import circle, line, rect
from pygame.math import Vector2
from marblebag_random import MarbleBag
from progressive_random import ProgressProb
from predetermination_random import Predetermin
from fixed_limit_random import FixedLimit

screen_width = 1280
screen_height = 720

class App:
    def __init__(self):
        print("App is create")

        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.screen_color = [212,212,212]
        self.clock = pygame.time.Clock()
        
        self.running = True

        # random
        self.seed_num = 1
        self.marbleBag_dirt = MarbleBag(items=["iron", "gold", "diamond"], probs=[5, 3, 2], seed_num=self.seed_num)
        self.marbleBag_diamond = MarbleBag(items=["gold", "diamond"], probs=[3, 2], seed_num=self.seed_num)

        self.diamondChange = ProgressProb(rate=20, seed_num=self.seed_num)

        self.breakChance_dirt = Predetermin(max_attempt=10, seed_num=self.seed_num)
        self.breakChance_diamond = Predetermin(max_attempt=20, seed_num=self.seed_num)

        self.pity_dirt = FixedLimit(rate=30, limit=3, seed_num=self.seed_num)
        self.pity_diamond = FixedLimit(rate=60, limit=3, seed_num=self.seed_num)

        self.dirtPic = pygame.image.load("Assets/grass_block.png").convert_alpha()
        self.dirtPic = pygame.transform.scale(self.dirtPic, (300, 300))

        self.diamondPic = pygame.image.load("Assets/diamond_block.png").convert_alpha()
        self.diamondPic = pygame.transform.scale(self.diamondPic, (300, 300))

        self.isDiamondBlock = False
        self.isBreak = False
        
        self.blockCount = 0
        self.item = ""
        self.ironCount = 0
        self.goldCount = 0
        self.diamondCount = 0

        self.pityDirt = self.pity_dirt.attempt
        self.pityDiamond = self.pity_diamond.attempt

        self.pityLimit = self.pity_diamond.fixed_limit

        #font
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 24)
        self.fontBig = pygame.font.SysFont('Arial', 48)

        # animation
        self.hit_animation_timer = 0
        self.hit_offset = 0
        self.break_animation_timer = 0
        self.break_angle = 0

        self.text_item_timer = 0
        self.text_item_alpha = 0

    def checkBreak(self):
        if self.isDiamondBlock:
            self.isBreak = self.breakChance_diamond.check_predetermin()
        else:
            self.isBreak = self.breakChance_dirt.check_predetermin()

        if self.isBreak:
            self.blockCount += 1
            self.break_animation_timer = 500
            self.isBreak = False
            self.item = self.checkItem()
            self.text_item_timer = 1500
            self.text_item_alpha = 255
            self.checkChange()

    def checkChange(self):
        self.isDiamondBlock = self.diamondChange.chance()

    def checkItem(self):
        if self.isDiamondBlock:
            isDrop = self.pity_diamond.check_pity()
            self.pityDiamond = self.pity_diamond.attempt
            if isDrop:
                item = self.marbleBag_diamond.random_item()
                self.countItem(item)
                return item
            else:
                return "Nothing"
        else:
            isDrop = self.pity_dirt.check_pity()
            self.pityDirt = self.pity_dirt.attempt
            if isDrop:
                item = self.marbleBag_dirt.random_item()
                self.countItem(item)
                return item
            else:
                return "Nothing"

    def countItem(self, itemName):
        if itemName == "iron":
            self.ironCount += 1
        elif itemName == "gold":
            self.goldCount += 1
        elif itemName == "diamond":
            self.diamondCount += 1
        else:
            return

    def handle_input(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.break_animation_timer > 0:
                            return
                        block_rect = pygame.Rect((screen_width // 2) - 150, (screen_height // 2) - 150, 300, 300)
                        if block_rect.collidepoint(event.pos):
                            #print(f"Hit block at {event.pos}")
                            self.hit_animation_timer = 100
                            self.checkBreak()

    def update(self, delta_time_ms):

        # digging animation
        if self.hit_animation_timer > 0:
            self.hit_animation_timer -= delta_time_ms
            phase = math.sin((self.hit_animation_timer / 100) * math.pi)
            self.hit_offset = phase * 10
        else:
            self.hit_offset = 0

        # breaking animation
        if self.break_animation_timer > 0:
            self.break_animation_timer -= delta_time_ms
            swing_phase = math.sin((500 - self.break_animation_timer) / 500 * math.pi * 6)
            self.break_angle = swing_phase * 10
        else:
            self.break_angle = 0

        # text animation
        if self.text_item_timer > 0:
            self.text_item_timer -= delta_time_ms
            self.text_item_alpha = max(0, int((self.text_item_timer / 1500) * 255))
        else:
            self.text_item_alpha = 0

    def draw(self):
        self.screen.fill(self.screen_color)

        if self.isDiamondBlock:
            block = self.diamondPic
            #text_pity = self.fontBig.render(f"Diamond block's item drop pity {self.pityDiamond - 1} / {self.pityLimit}", True, (0, 0, 0))
        else:
            block = self.dirtPic
            #text_pity = self.fontBig.render(f"Grass block's item drop pity {self.pityDirt - 1} / {self.pityLimit}", True, (0, 0, 0))

        rotated_block = pygame.transform.rotate(block, self.break_angle)
        img = rotated_block.get_rect(center=(screen_width // 2, screen_height// 2 + int(self.hit_offset)))
        self.screen.blit(block, img.topleft)

        #text
        text_block_break = self.font.render(f"Block break : {self.blockCount}", True, (0, 0, 0))
        text_block_break_rect = text_block_break.get_rect(topleft=(20, 20))
        self.screen.blit(text_block_break, text_block_break_rect)

        text_iron = self.font.render(f"Iron : {self.ironCount}", True, (0, 0, 0))
        text_iron_rect = text_iron.get_rect(topleft=(20, 60))
        self.screen.blit(text_iron, text_iron_rect)

        text_gold = self.font.render(f"Gold : {self.goldCount}", True, (0, 0, 0))
        text_gold_rect = text_gold.get_rect(topleft=(20, 100))
        self.screen.blit(text_gold, text_gold_rect)

        text_diamond = self.font.render(f"Diamond : {self.diamondCount}", True, (0, 0, 0))
        text_diamond_rect = text_diamond.get_rect(topleft=(20, 140))
        self.screen.blit(text_diamond, text_diamond_rect)

        text_pity = self.fontBig.render(f"Diamond block's item drop pity {self.pityDiamond} / {self.pityLimit}", True, (0, 0, 0))
        text_pity_rect = text_pity.get_rect(center=(screen_width // 2, screen_height - 40))
        self.screen.blit(text_pity, text_pity_rect)

        text_pity = self.fontBig.render(f"Grass block's item drop pity {self.pityDirt} / {self.pityLimit}", True, (0, 0, 0))
        text_pity_rect = text_pity.get_rect(center=(screen_width // 2, screen_height - 110))
        self.screen.blit(text_pity, text_pity_rect)

        if self.text_item_alpha > 0 and self.item:
            text_item = self.fontBig.render(f"You got {self.item}!", True, (0, 0, 0))
            text_item.set_alpha(self.text_item_alpha)
            text_item_rect = text_item.get_rect(center=(screen_width // 2, 100))
            self.screen.blit(text_item, text_item_rect)

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