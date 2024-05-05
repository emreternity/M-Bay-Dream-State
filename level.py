import pygame
from data import *
from object import Object
from player import Player
from random import choice, randint
from weapon import Weapon
from ui import UI
from hnpc import HostileNPC
from animparticles import AnimPlayer
from skill import SkillPlayer
from roulette import RouletteMan


class Level:
    def __init__(self, chosenChar):
        self.chosenChar = chosenChar
        self.isGamePaused = False
        self.display_surface = pygame.display.get_surface()
        self.vis_sprites = FollowingCamSys()
        self.obs_sprites = pygame.sprite.Group()
        self.curAtk = None
        self.atk_sprites = pygame.sprite.Group()
        self.atkable_sprites = pygame.sprite.Group()
        self.createMapCSV()
        self.ui = UI()
        self.animPlay = AnimPlayer()
        self.skillPlay = SkillPlayer(self.animPlay)

    def createMapCSV(self):
        layouts = {
            "mapBoundaries": import_csv_layout("csv\FirstMap_Sınır.csv"),
            # 'crate': import_csv_layout('crate.csv'),
            "objs": import_csv_layout("csv\FirstMap_Obje.csv"),
            "chars": import_csv_layout("csv\FirstMap_Canavar.csv"),
        }
        graphics = {
            # 'crate': import_folder('cratefolder'),
            "objs": import_folder("img\obj")
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != "-1":
                        x = col_index * 64
                        y = row_index * 64
                        if style == "mapBoundaries":
                            Object((x, y), [self.obs_sprites], "invisible")
                        if style == "crate":
                            random_grass_image = choice(graphics["crate"])
                            Object(
                                (x, y),
                                [
                                    self.vis_sprites,
                                    self.obs_sprites,
                                    self.atkable_sprites,
                                ],
                                "crate",
                                random_grass_image,
                            )
                        if style == "objs":
                            surf = graphics["objs"][int(col)]
                            Object(
                                (x, y),
                                [self.vis_sprites, self.obs_sprites],
                                "objs",
                                surf,
                            )
                        if style == "chars":
                            if col == "3":
                                self.player = Player(
                                    (x, y),
                                    [self.vis_sprites],
                                    self.obs_sprites,
                                    self.spawnAtk,
                                    self.despawnAtk,
                                    self.spawnSkill,
                                    self.chosenChar,
                                )
                            else:
                                if col == "1":
                                    hnpc_type = "earman"
                                    HostileNPC(
                                        hnpc_type,
                                        (x, y),
                                        [self.vis_sprites, self.atkable_sprites],
                                        self.obs_sprites,
                                        self.dmgPlayer,
                                        self.execDeathParticles,
                                        self.addXP,
                                    )
                                elif col == "0":
                                    hnpc_type = "eyeman"
                                    HostileNPC(
                                        hnpc_type,
                                        (x, y),
                                        [self.vis_sprites, self.atkable_sprites],
                                        self.obs_sprites,
                                        self.dmgPlayer,
                                        self.execDeathParticles,
                                        self.addXP,
                                    )
                                elif col == "2":
                                    RouletteMan(
                                        (x, y), [self.vis_sprites, self.obs_sprites]
                                    )
                    else:
                        pass

    def spawnAtk(self):
        self.curAtk = Weapon(self.player, [self.vis_sprites, self.atk_sprites])

    def despawnAtk(self):
        if self.curAtk:
            self.curAtk.kill()
        self.curAtk = None

    def spawnSkill(self, style, strength, cost):
        if style == "heal":
            self.skillPlay.heal(self.player, strength, cost, [self.vis_sprites])

        if style == "hide":
            self.skillPlay.hide(self.player, strength, cost, [self.vis_sprites])

    def checkHNPCHostility(self):
        if self.atk_sprites:
            for attack_sprite in self.atk_sprites:
                collision_sprites = pygame.sprite.spritecollide(
                    attack_sprite, self.atkable_sprites, False
                )
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == "crate":
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0, 75)
                            for crate_piece in range(randint(3, 6)):
                                self.animPlay.crateDestroyedParticles(
                                    pos - offset, [self.vis_sprites]
                                )
                            target_sprite.kill()
                        else:
                            target_sprite.takeDMG(
                                self.player, attack_sprite.sprite_type
                            )

    def dmgPlayer(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.hp -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            # self.animPlay.spawnParticles(attack_type,self.player.rect.center,[self.vis_sprites])

    def execDeathParticles(self, pos, particle_type):
        self.animPlay.spawnParticles(particle_type, pos, self.vis_sprites)

    def addXP(self, amount):
        self.player.xp += amount

    def checkIfPlayerDead(self,player):
        if player.hp <= 0:
            print('Ded x_x')
            exit()
    
    def checkIfLevelComplete(self,player):
        if player.xp == 350:
            player('Level completed! yay')
            exit()

    def run(self):
        self.vis_sprites.camFollowPlayer(self.player)
        self.vis_sprites.update()
        self.vis_sprites.hnpcUpdate(self.player)
        self.checkHNPCHostility()
        self.ui.display(self.player)
        self.checkIfPlayerDead(self.player)
        self.checkIfLevelComplete(self.player)


class FollowingCamSys(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        self.floor_surf = pygame.image.load(
            "img\map\Dream-State-First-Map.png"
        ).convert_alpha()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

    def camFollowPlayer(self, player):

        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def hnpcUpdate(self, player):
        enemy_sprites = [
            sprite
            for sprite in self.sprites()
            if hasattr(sprite, "sprite_type") and sprite.sprite_type == "enemy"
        ]
        for enemy in enemy_sprites:
            enemy.hnpcUpdate(player)
