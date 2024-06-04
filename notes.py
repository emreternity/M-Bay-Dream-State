import pygame
from data import *

class Note:
    def __init__(self, level, pos, surface, player, image, sound="sound\sfx\magic_spell_scroll_04.wav"):
        offset = HITBOX_OFFSET["notes"]
        self.image = image
        self.soundTxt = sound
        self.sound = pygame.mixer.Sound(sound)
        self.redscr = pygame.image.load("img/red.png").convert_alpha()
        self.redscr.set_alpha(128)
        self.surface = surface
        self.status = "idle"
        self.isDone = False
        self.player = player
        self.rect = self.image.get_rect(topleft=(pos[0], pos[1]+90))
        self.hitbox = self.rect.inflate(offset)
        self.soundPlayed = False
        self.level = level

    def comparePlayerNoteDist(self, player):
        note_vec = pygame.math.Vector2(self.rect.topleft)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - note_vec).magnitude()
        if distance > 20:
            return distance
        else:
            if not self.isDone:
                self.status = "read"
                if self.soundPlayed == False:
                    self.sound.play()
                    self.soundPlayed = True
                self.surface.blit(self.redscr, (0, 0))
                if self.soundTxt == "sound\sfx\magic_spell_scroll_04.wav":
                    self.surface.blit(self.image, (500, 15))
                else:
                    self.surface.blit(self.image, (0, 0))
                

    def update(self):
        self.comparePlayerNoteDist(self.player)
        
        keys = pygame.key.get_pressed()
        if self.status == "read":
            if keys[pygame.K_RETURN]:
                self.isDone = True
            if keys[pygame.K_BACKSPACE]:
                self.level.isreadingNote = False


