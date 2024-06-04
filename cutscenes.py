import pygame
from texteng import TextEng

class Cutscene:
    def __init__(self, images, duration, music, messages, screen, chosenChar):
        self.images = images  # List of images for the cutscene
        self.duration = duration  # Duration each image is shown
        self.current_index = 0
        self.current_time = None
        self.can_skip = False
        self.skip_time = None
        self.length = len(images)
        self.messages = messages
        self.music = music
        self.texts = TextEng((410,580),screen,3,chosenChar,messages,28)
        
    
    def start(self):
        self.skip_time = pygame.time.get_ticks()
        self.current_time = pygame.time.get_ticks()
        self.current_index = 0
        pygame.mixer.music.load(self.music)
        pygame.mixer.music.play(-1)
    
    def update(self):
        
        

        if self.current_time - self.skip_time >= 1000:
            self.can_skip = True
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.current_time = pygame.time.get_ticks() 
            if self.can_skip:
                self.skip_time = pygame.time.get_ticks()
                self.can_skip = False
                self.current_index += 1

    # def times(self):
    #     self.current_time = pygame.time.get_ticks()
                
    
    def draw(self, screen):
        if self.length != self.current_index:
            screen.blit(self.images[self.current_index], (0, 0))
            self.texts.update()

    def is_finished(self):
        if self.length == self.current_index:
            pygame.mixer.music.stop()
            return True