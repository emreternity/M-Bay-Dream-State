import pygame

class TextEng:
    def __init__(self, pos, surface, speed, char,messages,fontsize):
        self.pos = pos
        self.surface = surface
        self.font = pygame.font.Font("other\ealagard.ttf", fontsize)
        self.timer = pygame.time.Clock()
        self.messages = messages
        self.snip = self.font.render('',True,'white')
        self.counter = 0
        self.speed = speed
        self.active_message = 0
        self.message = self.messages[self.active_message] 
        self.done = False
        self.timer.tick(60)
        self.rect = pygame.Rect(self.pos[0],self.pos[1],720,100)
        self.char = char
        self.textbox = pygame.image.load("other/textbox.png").convert_alpha()
        if char == "willie" or char == "lisa":
            self.textsfx = pygame.mixer.Sound("sound/text\willietext.wav")
        elif char == "gameover":
            self.textsfx = pygame.mixer.Sound("sound/text\gameover.wav")
        else:
            pass
        

    def spawnText(self):
        if len(self.messages)-1 != self.active_message and self.char != "gameover":
            if self.messages[self.active_message] != " ":
                self.surface.blit(self.textbox,(0,0))
        if self.counter < self.speed * len(self.message):
            self.counter += 1
            if self.counter % self.speed == 0:  # Set the volume to full
                self.textsfx.play()
                self.textsfx.set_volume(0.5)
        elif self.counter >= self.speed * len(self.message):
            self.done = True
        self.rect = self.snip.get_rect(topleft=self.rect.topleft)
        self.snip = self.font.render(self.message[0:self.counter // self.speed], True, 'white')
        self.surface.blit(self.snip,(self.pos))


    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN] and self.done and self.active_message < len(self.messages) - 1:
            self.counter = 0
            self.active_message += 1
            if self.active_message == len(self.messages):
                self.active_message = len(self.messages)
            self.message = self.messages[self.active_message]
            self.done = False

    def update(self):
        self.spawnText()
        self.input()

