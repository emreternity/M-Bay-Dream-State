import pygame
from data import *


class SkillPlayer:
    def __init__(self, animPlay):
        self.animPlay = animPlay
        self.sounds = {
            'heal': pygame.mixer.Sound("sound\sfx\magic_black_defense_02.wav"),
            'hide': pygame.mixer.Sound("sound\sfx\magic_black_collapse_01.wav"),
            'appear':pygame.mixer.Sound("sound\sfx\magic_black_ghost_04.wav"),
            'nopot':pygame.mixer.Sound("sound\sfx\magic_black_squeal_02.wav")
        }

    def heal(self, player, strength, cost, groups):
        if player.energy >= cost and player.pot_amount != 0:
            self.sounds['heal'].play()
            player.hp += strength
            player.heartbeat_cd = 15 * (player.hp)
            player.energy -= cost
            player.pot_amount -= 1
            if player.hp >= player.stats["hp"]:
                player.hp = player.stats["hp"]
            self.animPlay.spawnParticles('heal',player.rect.center,groups)
        else:
            self.sounds['nopot'].play()


    def hide(self, player, strength, cost, groups):
        if player.isVisible == True and player.energy >= cost:
            player.isVisible = False
            self.sounds['hide'].play()
        else:
            self.sounds['appear'].play()
            player.isVisible = True
