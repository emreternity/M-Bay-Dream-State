import pygame
from data import *


class SkillPlayer:
    def __init__(self, animPlay):
        self.animPlay = animPlay

    def heal(self, player, strength, cost, groups):
        if player.energy >= cost and player.pot_amount != 0:
            player.hp += strength
            player.energy -= cost
            player.pot_amount -= 1
            if player.hp >= player.stats["hp"]:
                player.hp = player.stats["hp"]

    def hide(self, player, strength, cost, groups):
        if player.isVisible == True and player.energy >= cost:
            player.isVisible = False
        else:
            player.isVisible = True
