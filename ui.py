import pygame
from data import *

class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font("other\ealagard.ttf", 18)

        self.hpRect = pygame.Rect(10, 10, 200, 20)
        self.nrgRect = pygame.Rect(10, 34, 200, 20)

        self.bloodyscr = pygame.image.load("img/bloody.png").convert_alpha()
        self.redscr = pygame.image.load("img/red.png").convert_alpha()
        


        self.wpnFiles = []
        for weapon in weapons.values():
            path = weapon["design"]
            weapon = pygame.image.load(path).convert_alpha()
            self.wpnFiles.append(weapon)
        self.skillFiles = []
        for skill in skills.values():
            path = skill["design"]
            skill = pygame.image.load(path).convert_alpha()
            self.skillFiles.append(skill)
        self.itemGrayscale = [
            pygame.image.load("img\items\small_hp_potion/0.png").convert_alpha()
        ]

    def spawnBar(self, current, max_amount, bg_rect, color):
        pygame.draw.rect(self.display_surface, "#1f0101", bg_rect)

        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, "#0a0000", bg_rect, 3)

    def spawnXPText(self, xp):
        text_sent = f"Mevcut Tecrube Puani: {str(int(xp))}"
        text_surf = self.font.render(text_sent, False, "#fc6d6d")
        text_rect = text_surf.get_rect(topleft=(20, 680))
        pygame.draw.rect(self.display_surface, "#1f0101", text_rect.inflate(20, 20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, "#0a0000", text_rect.inflate(20, 20), 3)

    def spawnPotText(self, skilli, pot_amount):
        if skilli == 0:
                text_sent = f"{str(int(pot_amount))}"
                text_surf = self.font.render(text_sent, False, "#fc6d6d")
                text_rect = text_surf.get_rect(topleft=(1160, 680))
                pygame.draw.rect(self.display_surface, "#1f0101", text_rect.inflate(20, 20))
                self.display_surface.blit(text_surf, text_rect)
                pygame.draw.rect(self.display_surface, "#0a0000", text_rect.inflate(20, 20), 3)

    def spawnBloodyScreen(self,hp):
        ratio = hp * 255 / 100
        if (hp != 100):
            self.redscr.set_alpha(255-ratio)
            self.bloodyscr.set_alpha(255-ratio)
            


    def activeBorder(self, left, top, has_switched):
        bg_rect = pygame.Rect(left, top, 80, 80)
        pygame.draw.rect(self.display_surface, "#1f0101", bg_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface, "#7a3314", bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, "#0a0000", bg_rect, 3)
        return bg_rect

    def weaponHUDimg(self, weaponi, has_switched):
        bg_rect = self.activeBorder(1180, 550, has_switched)
        weapon_surf = self.wpnFiles[weaponi]
        weapon_rect = weapon_surf.get_rect(center=bg_rect.center)
        self.display_surface.blit(weapon_surf, weapon_rect)

    def skillHUDimg(self, skilli, has_switched, pot_amount):
        bg_rect = self.activeBorder(1180, 635, has_switched)
        if skilli == 0 and pot_amount == 0:
            magic_surf = self.itemGrayscale[0]
        else:
            magic_surf = self.skillFiles[skilli]
        magic_rect = magic_surf.get_rect(center=bg_rect.center)
        self.display_surface.blit(magic_surf, magic_rect)


    def deathDisplay(self,player):
        self.display_surface.blit(self.redscr, (0, 0))
        self.redscr.set_alpha(0)
        self.display_surface.blit(self.bloodyscr, (0, 0))
        self.bloodyscr.set_alpha(0)
        self.spawnBloodyScreen(player.hp)

    def display(self, player):
        self.spawnBar(player.hp, player.stats["hp"], self.hpRect, "#7a1414")
        self.spawnBar(player.energy, player.stats["energy"], self.nrgRect, "#53147a")

        self.spawnPotText(player.skilli,player.pot_amount)

        

        self.weaponHUDimg(player.weaponi, not player.can_switch_weapon)
        self.skillHUDimg(player.skilli, not player.canSwitchSkill, player.pot_amount)
