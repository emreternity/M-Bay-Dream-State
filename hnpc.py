import pygame
from data import *
from basechar import CharacterBase

from random import randint


class HostileNPC(CharacterBase):
    def __init__(
        self, hnpc_type, pos, groups, obs_sprites, dmgPlayer, execDeathParticles, addXP
    ):
        super().__init__(groups)
        self.sprite_type = "enemy"
        self.importGraphics(hnpc_type)
        self.status = "idle"
        self.image = self.animations[self.status][self.framei]

        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-20, -20)
        self.obs_sprites = obs_sprites

        self.hnpc_type = hnpc_type
        hnpc_info = hnpc[self.hnpc_type]
        self.hp = hnpc_info["hp"]
        self.xp = hnpc_info["xp"]
        self.speed = hnpc_info["speed"]
        self.attack_damage = hnpc_info["damage"]
        self.knockback = hnpc_info["knockback"]
        self.dmg_rad = hnpc_info["dmg_rad"]
        self.chase_rad = hnpc_info["chase_rad"]
        self.attack_type = hnpc_info["attack_type"]
        self.addXP = addXP

        self.can_attack = True
        self.atk_time = None
        self.atk_cd = 400
        self.dmgPlayer = dmgPlayer
        self.execDeathParticles = execDeathParticles

        self.vulnerable = True
        self.hit_time = None
        self.invi_dur = 300

    def importGraphics(self, name):
        self.animations = {"idle": [], "move": [], "attack": [], "random": []}
        main_path = f"img\enemies/{name}/"
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def comparePlayerHNPCDist(self, player):
        hnpc_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - hnpc_vec).magnitude()
        if distance > 0:
            direction = (player_vec - hnpc_vec).normalize()
        else:
            direction = pygame.math.Vector2(0, 0)
        return (distance, direction)

    def getStatus(self, player):
        distance = self.comparePlayerHNPCDist(player)[0]
        if distance <= self.dmg_rad and self.can_attack and self.hnpc_type == "eyeman":
            if self.status != "attack":
                self.framei = 0
            self.status = "attack"
        elif (
            distance <= self.chase_rad
            and self.hnpc_type == "eyeman"
            and player.isVisible
        ):
            self.status = "move"
        elif (
            distance <= self.dmg_rad
            and self.can_attack
            and player.sound_made != 0
            and self.hnpc_type == "earman"
        ):
            if self.status != "attack":
                self.framei = 0
            self.status = "attack"
        elif (
            distance <= player.sound_made * self.chase_rad
            and self.hnpc_type == "earman"
        ):
            self.status = "move"
        elif self.hnpc_type == "earman":
            self.status = "random"
        else:
            self.status = "idle"

    def statusExecute(self, player):
        if self.status == "attack":
            self.atk_time = pygame.time.get_ticks()
            self.dmgPlayer(self.attack_damage, self.attack_type)
        elif self.status == "move":
            self.direction = self.comparePlayerHNPCDist(player)[1]
        elif self.status == "random":
            self.direction = pygame.math.Vector2((randint(-1, 1), randint(-1, 1)))
        else:
            self.direction = pygame.math.Vector2()

    def anim(self):
        animation = self.animations[self.status]
        self.framei += self.anim_speed
        if self.framei >= len(animation):
            if self.status == "attack":
                self.can_attack = False
            self.framei = 0
        self.image = animation[int(self.framei)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        if not self.vulnerable:
            alpha = self.sinWaveAnim()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    #cooldowns
    def cds(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.atk_time >= self.atk_cd:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invi_dur:
                self.vulnerable = True

    def takeDMG(self, player, attack_type):
        if self.vulnerable:
            self.direction = self.comparePlayerHNPCDist(player)[1]
            if attack_type == "weapon":
                self.hp -= player.takeWpnDMG()
            else:
                pass

        self.hit_time = pygame.time.get_ticks()
        self.vulnerable = False

    def checkIfDead(self):
        if self.hp <= 0:
            self.kill()
            self.execDeathParticles(self.rect.center, self.hnpc_type)
            self.addXP(self.xp)

    def hnpcKnockback(self):
        if not self.vulnerable:
            self.direction *= -self.knockback

    def update(self):
        self.hnpcKnockback()
        self.charMove(self.speed)
        self.anim()
        self.cds()
        self.checkIfDead()

    def hnpcUpdate(self, player):
        self.getStatus(player)
        self.statusExecute(player)
