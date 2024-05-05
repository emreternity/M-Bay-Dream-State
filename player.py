import pygame
from data import *
from basechar import CharacterBase


class Player(CharacterBase):
    def __init__(
        self, pos, groups, obs_sprites, spawnAtk, despawnAtk, spawnSkill, char
    ):
        super().__init__(groups)
        self.char_imgpath = f"img\char\{char}\down_idle\idle_down.png"
        self.image = pygame.image.load(self.char_imgpath).convert()
        self.rect = self.image.get_rect(topleft=pos)
        self.char = char
        self.hitbox = self.rect.inflate(-20, -20)
        self.loadPlayerFiles()
        self.status = "down"
        self.isAttacking = False
        self.atk_cd = 400
        self.atk_time = None
        self.spawnAtk = spawnAtk
        self.despawnAtk = despawnAtk
        self.obs_sprites = obs_sprites
        self.weaponi = 0
        self.weapon = list(weapons.keys())[self.weaponi]
        self.can_switch_weapon = True
        self.switch_duration_cooldown = 200
        self.weapon_switch_time = None
        self.slow_walking = False
        self.slow_time = None
        self.can_slow_walk = True
        self.isVisible = True
        self.items = {
            "small_hp_potion": {
                "cooldown": 1000,
                "start_amount": 3,
                "strength": 30,
                "design": "img\items\small_hp_potion",
            }
        }
        self.item_index = 0
        self.pot_amount = list(self.items.values())[self.item_index]["start_amount"]
        self.sound_made = 0
        self.pauseGame = False
        self.skilli = 0
        self.skill = list(skills.keys())[self.skilli]
        self.canSwitchSkill = True
        self.skillSwitchTime = None
        self.spawnSkill = spawnSkill

        self.stats = {
            "hp": 100,
            "energy": 60,
            "attack": 10,
            "skill": 4,
            "speed": 4,
            "sprint_speed": 6,
            "slow_speed": 2,
        }
        self.hp = self.stats["hp"]
        self.energy = self.stats["energy"]
        self.xp = 0
        self.speed = self.stats["speed"]

        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

    def loadPlayerFiles(self):
        character_path = f"img\char\{self.char}/"
        self.animations = {
            "up": [],
            "down": [],
            "left": [],
            "right": [],
            "right_idle": [],
            "left_idle": [],
            "up_idle": [],
            "down_idle": [],
            "right_attack": [],
            "left_attack": [],
            "up_attack": [],
            "down_attack": [],
        }
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        if not self.isAttacking:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_ESCAPE]:
                if self.pauseGame == False:
                    self.pauseGame == True
                else:
                    self.pauseGame == False

            if keys[pygame.K_x] and self.can_slow_walk:
                self.slow_time = pygame.time.get_ticks()
                self.can_slow_walk = False
                if not self.slow_walking:
                    self.slow_walking = True
                else:
                    self.slow_walking = False

            if (
                keys[pygame.K_UP]
                or keys[pygame.K_w]
                and keys[pygame.K_LSHIFT]
                and self.energy > 0
            ):
                self.direction.y = -1
                self.status = "up"
                self.sound_made = 3
                self.speed = self.stats["sprint_speed"]
                self.anim_speed = 0.25
                if self.energy > 0:
                    self.energy -= 0.15
            elif keys[pygame.K_UP] or keys[pygame.K_w] and self.slow_walking:
                self.direction.y = -1
                self.status = "up"
                self.sound_made = 0
                self.speed = self.stats["slow_speed"]
                self.anim_speed = 0.05
            elif keys[pygame.K_UP] or keys[pygame.K_w]:
                self.speed = self.stats["speed"]
                self.direction.y = -1
                self.status = "up"
                self.sound_made = 1
                self.anim_speed = 0.15

            elif (
                keys[pygame.K_DOWN]
                or keys[pygame.K_s]
                and keys[pygame.K_LSHIFT]
                and self.energy > 0
            ):
                self.direction.y = 1
                self.status = "down"
                self.sound_made = 3
                self.speed = self.stats["sprint_speed"]
                self.anim_speed = 0.25
                if self.energy > 0:
                    self.energy -= 0.15
            elif keys[pygame.K_DOWN] or keys[pygame.K_s] and self.slow_walking:
                self.direction.y = 1
                self.status = "down"
                self.sound_made = 0
                self.speed = self.stats["slow_speed"]
                self.anim_speed = 0.05

            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.speed = self.stats["speed"]
                self.direction.y = 1
                self.status = "down"
                self.sound_made = 1
                self.anim_speed = 0.15
            else:
                self.direction.y = 0
                self.sound_made = 0

            if (
                keys[pygame.K_RIGHT]
                or keys[pygame.K_d]
                and keys[pygame.K_LSHIFT]
                and self.energy > 0
            ):
                self.direction.x = 1
                self.status = "right"
                self.sound_made = 3
                self.anim_speed = 0.25
                self.speed = self.stats["sprint_speed"]
                if self.energy > 0:
                    self.energy -= 0.15

            elif keys[pygame.K_RIGHT] or keys[pygame.K_d] and self.slow_walking:
                self.direction.x = 1
                self.status = "right"
                self.sound_made = 0
                self.anim_speed = 0.05
                self.speed = self.stats["slow_speed"]

            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.speed = self.stats["speed"]
                self.direction.x = 1
                self.status = "right"
                self.sound_made = 1
                self.anim_speed = 0.15

            elif (
                keys[pygame.K_LEFT]
                or keys[pygame.K_a]
                and keys[pygame.K_LSHIFT]
                and self.energy > 0
            ):
                self.direction.x = -1
                self.status = "left"
                self.sound_made = 3
                self.anim_speed = 0.25
                self.speed = self.stats["sprint_speed"]
                if self.energy > 0:
                    self.energy -= 0.15

            elif keys[pygame.K_LEFT] or keys[pygame.K_a] and self.slow_walking:
                self.direction.x = -1
                self.status = "left"
                self.sound_made = 0
                self.anim_speed = 0.05
                self.speed = self.stats["slow_speed"]

            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.speed = self.stats["speed"]
                self.direction.x = -1
                self.status = "left"
                self.sound_made = 1
                self.anim_speed = 0.15
            else:
                self.direction.x = 0
                self.sound_made = 0

            if keys[pygame.K_SPACE]:
                if self.energy >= 20:
                    self.isAttacking = True
                    self.sound_made = 5
                    self.atk_time = pygame.time.get_ticks()
                    self.energy -= 20
                    self.spawnAtk()

            if keys[pygame.K_q]:
                self.isAttacking = True
                self.sound_made = 2
                self.atk_time = pygame.time.get_ticks()
                style = list(skills.keys())[self.skilli]
                strength = (
                    list(skills.values())[self.skilli]["strength"] + self.stats["skill"]
                )
                cost = list(skills.values())[self.skilli]["cost"]
                self.spawnSkill(style, strength, cost)

            if keys[pygame.K_r] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()
                if self.weaponi > 0:
                    self.weaponi -= 1
                    self.weapon = list(weapons.keys())[self.weaponi]
                else:
                    self.weaponi = len(list(weapons.keys())) - 1

            if keys[pygame.K_e] and self.canSwitchSkill:
                self.canSwitchSkill = False
                self.skillSwitchTime = pygame.time.get_ticks()
                if self.skilli > 0:
                    self.skilli -= 1
                    self.skill = list(skills.keys())[self.skilli]
                else:
                    self.skilli = len(list(skills.keys())) - 1

    def getStatus(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not "idle" in self.status and not "attack" in self.status:
                self.status = self.status + "_idle"

        if self.isAttacking:
            self.direction.x = 0
            self.direction.y = 0
            if not "attack" in self.status:
                if "idle" in self.status:
                    self.status = self.status.replace("_idle", "_attack")
                else:
                    self.status = self.status + "_attack"
        else:
            if "attack" in self.status:
                self.status = self.status.replace("_attack", "")

    def cds(self):
        current_time = pygame.time.get_ticks()
        if self.isAttacking:
            if (
                current_time - self.atk_time
                >= self.atk_cd + weapons[self.weapon]["cooldown"]
            ):
                self.isAttacking = False
                self.despawnAtk()

        if not self.can_slow_walk:
            if current_time - self.slow_time >= 200:
                self.can_slow_walk = True

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

        if not self.canSwitchSkill:
            if current_time - self.skillSwitchTime >= self.switch_duration_cooldown:
                self.canSwitchSkill = True

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

    def anim(self):
        animation = self.animations[self.status]
        self.framei += self.anim_speed
        if self.framei >= len(animation):
            self.framei = 0

        self.image = animation[int(self.framei)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        if not self.vulnerable:
            alpha = self.sinWaveAnim()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

        if not self.isVisible:
            self.image.set_alpha(50)
        else:
            self.image.set_alpha(255)

    def takeWpnDMG(self):
        base_damage = self.stats["attack"]
        weapon_damage = weapons[self.weapon]["damage"]
        return base_damage + weapon_damage

    def energy_recovery(self):
        if self.energy < self.stats["energy"]:
            self.energy += 0.01 * self.stats["skill"]
        else:
            self.energy = self.stats["energy"]

    def energy_deprive(self):
        if self.energy > 0 and self.isVisible == False:
            self.energy -= 0.05 * self.stats["skill"]

    def energy_depleted(self):
        if self.energy <= 1:
            self.isVisible = True

    def update(self):
        self.input()
        self.cds()
        self.getStatus()
        self.anim()
        self.charMove(self.speed)
        self.energy_recovery()
        self.energy_deprive()
        self.energy_depleted()
