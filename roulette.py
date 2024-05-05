import pygame
from data import *
from basechar import CharacterBase
from random import randint


class RouletteMan(CharacterBase):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load("img/rulet-adam.png")
        self.rect = self.image.get_rect(midleft=pos)
        self.hitbox = self.rect.inflate(-50, -50)
        self.can_offer_roulette = True
        self.status = "idle"
