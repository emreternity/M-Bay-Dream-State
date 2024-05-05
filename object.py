import pygame
from data import *


class Object(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=pygame.Surface((64, 64))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        if sprite_type == "objs":
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1]))
        else:
            self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-60, -60)
