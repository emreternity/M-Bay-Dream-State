import pygame, sys
from level import Level

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.bg = pygame.image.load("img\map\eopj2hiyutg11.png").convert()
        self.chosenChar = None
        pygame.display.set_caption("M-Bay: Dream State")
        self.clock = pygame.time.Clock()
        self.level = None

    def run(self):
        isRunning = False
        charChoose = False
        charchoosebg = pygame.image.load("img\menu\charchoose.png").convert()
        menu = pygame.image.load("img\menu\sonhalgibibisi.png").convert()
        start = pygame.image.load("img\menu\start.png").convert()
        lisapic = pygame.image.load("other\Lisa-kucuk-on.png").convert_alpha()
        williepic = pygame.image.load("other\Willie-kucuk-on.png").convert_alpha()

        while True:
            self.screen.fill("black")
            self.screen.blit(self.bg, [0, 0])
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if b.collidepoint(pos):
                        charChoose = True
                    elif lisa.collidepoint(pos):
                        self.chosenChar = "lisa"
                        self.level = Level(self.chosenChar)
                        isRunning = True
                        charChoose = False
                        
                    elif willie.collidepoint(pos):
                        self.chosenChar = "willie"
                        self.level = Level(self.chosenChar)
                        isRunning = True
                        charChoose = False
                        

            if isRunning == False:
                self.screen.blit(menu, (0, 0))
                b = self.screen.blit(start, [406, 288])
            if charChoose == True:
                self.screen.blit(charchoosebg, (0, 0))
                lisa = self.screen.blit(lisapic, (259, 360))
                willie = self.screen.blit(williepic, (900, 360))
            elif isRunning == True:
                self.level.run()
            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()
