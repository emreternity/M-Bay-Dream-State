import pygame, sys
from level import Level
from data import *
from cutscenes import Cutscene
from leveltwo import LevelTwo


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.bg = pygame.image.load("img\map\eopj2hiyutg11.png").convert()
        self.chosenChar = None
        pygame.display.set_caption("M-Bay: Dream State")
        self.clock = pygame.time.Clock()
        self.level = None
        self.levelTwo = None
        # self.levelTwo = LevelTwo("willie",STATE_BEFOREDOORCUTSCENE)
   
        # self.cutsceneEnd = Cutscene(cutsceneEndImages, 200, "sound\music\endingtheme.mp3",self.msgcutEnd,self.screen,"willie")
                            
       
        
        
       

    def run(self):
        global current_state
        pygame.mixer.music.load("sound\music\menutheme.mp3")
        pygame.mixer.music.play(1)
        start_sfx = pygame.mixer.Sound("sound\sfx/fnt_ui_select_click_14.wav")
        charchoose_sfx = pygame.mixer.Sound("sound\sfx\medwpn_scrape_hit_flesh_10.wav")
        

        charchoosebg = pygame.image.load("img\menu\charchoose.png").convert()
        menu = pygame.image.load("img\menu\sonhalgibibisi.png").convert()
        start = pygame.image.load("img\menu\start.png").convert()
        lisapic = pygame.image.load("other\Lisa-kucuk-on.png").convert_alpha()
        williepic = pygame.image.load("other\Willie-kucuk-on.png").convert_alpha()
        while True:
            
            self.screen.fill("black")
            self.screen.blit(self.bg, [0, 0])
            if current_state == STATE_STARTSCREEN:

                self.screen.blit(menu, (0, 0))
                b = self.screen.blit(start, [406, 288])
                
            elif current_state == STATE_CHARCHOOSE:
                self.screen.blit(charchoosebg, (0, 0))
                lisa = self.screen.blit(lisapic, (259, 360))
                willie = self.screen.blit(williepic, (900, 360))

            if current_state == STATE_BEFORECUTSCENEONE:
                runResult = self.level.run()
                if runResult == "next":
                    current_state = STATE_BEFOREDOORCUTSCENE
                elif runResult == "dead":
                     current_state = STATE_BEFORECUTSCENEONE
                     chosenChar = self.level.chosenChar
                     self.level = Level(chosenChar,current_state)
                     

            if current_state == STATE_BEFOREDOORCUTSCENE:
                runResult = self.levelTwo.run()
                if runResult == "next":
                    current_state = STATE_BEFOREFINALCUTSCENE
                elif runResult == "dead":
                     current_state = STATE_BEFOREDOORCUTSCENE
                     chosenChar = self.level.chosenChar
                     self.levelTwo = LevelTwo(chosenChar,current_state)

            if current_state == STATE_BEFOREFINALCUTSCENE:
                    self.cutsceneEnd.start()
                    current_state = STATE_FINALCUTSCENE
            elif current_state == STATE_FINALCUTSCENE:
                self.cutsceneEnd.update()
                self.cutsceneEnd.draw(self.screen)
                if self.cutsceneEnd.is_finished():
                    exit()
                    

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and current_state == STATE_STARTSCREEN:
                        pos = pygame.mouse.get_pos()
                        if b.collidepoint(pos):
                            start_sfx.play()
                            current_state = STATE_CHARCHOOSE

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and current_state == STATE_CHARCHOOSE:
                        lisa = self.screen.blit(lisapic, (259, 360))
                        willie = self.screen.blit(williepic, (900, 360))
                        pos = pygame.mouse.get_pos()
                        if lisa.collidepoint(pos):
                            charchoose_sfx.play()
                            self.chosenChar = "lisa"
                            current_state = STATE_BEFORECUTSCENEONE
                            self.level = Level(self.chosenChar,current_state)
                            self.levelTwo = LevelTwo(self.chosenChar,STATE_BEFOREDOORCUTSCENE)
                            self.msgcutEnd = ["Lisa aciyla kivranir..."," ","Hemsire: Sonunda uyandin."," ","Lisa: N-Ne... Neredeyim?","Hemsire: Seni buraya beyaz tenli... "," ","...gri gozlu..."," ","...kisa boylu birisi getirdi.","Hemsire: Burasi hastane."," ","Lisa yavasca gozlerini aralar."," ","Polis: Ve gorunen o ki..."," ","...sen Rockford Beach'i patlatan cocuksun.", "Lisa: Olamaz..."," "]
                            self.cutsceneEnd = Cutscene(cutsceneEndImages, 200, "sound\music\endingtheme.mp3",self.msgcutEnd,self.screen,self.chosenChar)
                            pygame.mixer.music.stop()
                            
                        elif willie.collidepoint(pos):
                            charchoose_sfx.play()
                            self.chosenChar = "willie"
                            current_state = STATE_BEFORECUTSCENEONE
                            self.level = Level(self.chosenChar,current_state)
                            self.levelTwo = LevelTwo(self.chosenChar,STATE_BEFOREDOORCUTSCENE)
                            self.msgcutEnd = ["Willie aciyla kivranir..."," ","Hemsire: Sonunda uyandin."," ","Willie: N-Ne... Neredeyim?","Hemsire: Seni buraya beyaz tenli... "," ","...gri gozlu..."," ","...kisa boylu birisi getirdi.","Hemsire: Burasi hastane."," ","Willie yavasca gozlerini aralar."," ","Polis: Ve gorunen o ki..."," ","...sen Rockford Beach'i patlatan cocuksun.", "Willie: Olamaz..."," "]
     
                            self.cutsceneEnd = Cutscene(cutsceneEndImages, 200, "sound\music\endingtheme.mp3",self.msgcutEnd,self.screen,self.chosenChar)
                            # current_state = STATE_BEFORECUTSCENEONE
                            pygame.mixer.music.stop()

                            
            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()
