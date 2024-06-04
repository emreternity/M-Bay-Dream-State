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
from cutscenes import Cutscene
from texteng import TextEng
from notes import Note


class LevelTwo:
    def __init__(self, chosenChar, current_state):
        self.noteList = []
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
        self.current_state = current_state
        msgepOne = [f"{chosenChar.capitalize()}: Burasi cehennem mi?"," "]
        self.epOneMsg = TextEng((410,580), self.display_surface, 5, chosenChar, msgepOne, 36)
        messageGameover = ["Ruhunu Kaybettin...","Tekrar Dene?"," "]
        self.gameoverMsg = TextEng((510, 310), self.display_surface, 5, "gameover", messageGameover,36)
        self.msgcutDoor = [f"{self.chosenChar.capitalize()}: Bu notlar..."," ",f"{self.chosenChar.capitalize()}: Anlamiyorum..."," ",
                      f"{self.chosenChar.capitalize()}:Neden buradayim? Burasi neresi?"," ",f"{self.chosenChar.capitalize()} acilan kapiya bakar."," ",
                      f"{self.chosenChar.capitalize()}: Tek yol...", f"{self.chosenChar.capitalize()}: Son sans..."," "]
        self.cutsceneDoor = Cutscene(cutsceneDoorImages, 200, "sound\music\doorcutscene.mp3",self.msgcutDoor,self.display_surface,self.chosenChar)
       
        self.crateSfx = pygame.mixer.Sound("sound\sfx\shield_wood_clash_B_19.wav")
        self.potFoundSfx = pygame.mixer.Sound("sound\sfx\magic_elemental_water_02.wav")
        self.papers = paperImages
        self.msgpotFound = [f"{chosenChar.capitalize()}: Bir iksir buldum!",""]
        self.notesFound = 0
        self.msgnoteFound = [f"{chosenChar.capitalize()}: Bir not buldum...","Notlar: %s/6" % (self.notesFound+3),""]
        self.noteFoundMsg = TextEng((410, 580), self.display_surface, 5, chosenChar, self.msgnoteFound, 36)
        self.potfoundMsg = TextEng((410, 580), self.display_surface, 5, chosenChar, self.msgpotFound, 36)
        self.ispotFound = False
        self.isreadingNote = False
        # self.firstNote = Note((0,0),self.display_surface,self.player,paperImages[0])
        # self.secondNote = Note((0, 0), self.display_surface, self.player, paperImages[1])
        # self.thirdNote = Note((0, 0), self.display_surface, self.player, paperImages[2])
        # self.fourthNote = Note((0, 0), self.display_surface, self.player, paperImages[3])
        # self.fifthNote = Note((0, 0), self.display_surface, self.player, paperImages[4])
        # self.sixthNote = Note((0, 0), self.display_surface, self.player, paperImages[5])
        # self.noteList = [self.firstNote, self.secondNote, self.thirdNote, self.fourthNote, self.fifthNote, self.sixthNote]
        self.notereadIndex = -1
        self.mimicSfx = pygame.mixer.Sound("sound\sfx\magic_spell_fire_15.wav")
        self.chestSfx = pygame.mixer.Sound("sound\sfx\chest_open_04.wav")
        self.mimickedMsgs = [f"{chosenChar.capitalize()}: Bu bir tuzak!",""]
        self.mimickedMsg = TextEng((410, 580), self.display_surface, 5, chosenChar, self.mimickedMsgs, 36)
        self.isMimicked = False


    def createMapCSV(self):
        layouts = {
            "mapBoundaries": import_csv_layout("csv\LevelTwo\LevelTwo_Sınır.csv"),
            'crate': import_csv_layout('csv\LevelTwo\LevelTwo_Crates.csv'),
            "objs": import_csv_layout("csv\LevelTwo\LevelTwo_Objs.csv"),
            "chars": import_csv_layout("csv\LevelTwo\LevelTwo_Canavar.csv"),
            "chests": import_csv_layout("csv\LevelTwo\LevelTwo_Chest.csv"),
            "notes": import_csv_layout("csv\LevelTwo\LevelTwo_Kağıt.csv"),
        }
        graphics = {
            'crate': import_folder('img\obj\crate42'),
            "objs": import_folder("img\objs42"),
            "chests": import_folder("img\obj\chest42"),
            "notes": import_folder("img\paper")
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != "-1":
                        x = col_index * 48  
                        y = row_index * 48
                        if style == "mapBoundaries":
                            Object((x, y), [self.obs_sprites], "invisible42")
                        if style == "crate":
                            crate_img = choice(graphics["crate"])
                            Object(
                                (x, y),
                                [
                                    self.vis_sprites,
                                    self.obs_sprites,
                                    self.atkable_sprites,
                                ],
                                "crate42",
                                crate_img,
                            )
                        if style == "chests":
                            surf = graphics["chests"][int(col)-949]
                            Object(
                                (x, y),
                                [self.vis_sprites, self.obs_sprites, self.atkable_sprites],
                                "chest42",
                                surf,
                            )
                        if style == "notes":
                            surf = graphics["notes"][int(col)-11]
                            if (int(col) - 11) == 3:
                                self.noteList.append(Note(self,(x,y),self.display_surface,self.player,jumpImg,"sound\sfx/recording-2-6-2024 19_28_21.wav"))
                            else:
                                self.noteList.append(Note(self,(x,y),self.display_surface,self.player,paperImages[int(col)-11]))
                            Object(
                                (x, y),
                                [
                                    self.vis_sprites,
                                    self.atkable_sprites,
                                ],
                                "notes",
                                surf,
                            )
                            
                        if style == "objs":
                            surf = graphics["objs"][int(col)]
                            Object(
                                (x, y),
                                [self.vis_sprites, self.obs_sprites],
                                "objs42",
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
                                elif col == "4":
                                    hnpc_type = "final-boss"
                                    HostileNPC(
                                        hnpc_type,
                                        (x, y),
                                        [self.vis_sprites, self.atkable_sprites],
                                        self.obs_sprites,
                                        self.dmgPlayer,
                                        self.execDeathParticles,
                                        self.addXP,
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

    def checkHNPCHostility(self,player):
        if self.atk_sprites:
            for attack_sprite in self.atk_sprites:
                collision_sprites = pygame.sprite.spritecollide(
                    attack_sprite, self.atkable_sprites, False
                )
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == "crate42":
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0, 75)
                            if randint(1,6) == 6 :
                                player.pot_amount += 1
                                self.potFoundSfx.play()
                                self.animPlay.spawnParticles(
                                    "spawn_pot", pos - offset, [self.vis_sprites]
                                )
                                self.ispotFound = True
                                self.potfoundMsg = TextEng((410, 580), self.display_surface, 5, self.chosenChar, self.msgpotFound, 36)
                            else:
                                self.ispotFound = False
                                self.potfoundMsg = None
                            for crate_piece in range(randint(3, 6)):
                                self.crateSfx.play()
                                self.animPlay.spawnParticles(
                                    "crate_piece", pos - offset, [self.vis_sprites]
                                )
                            target_sprite.kill()
                        elif target_sprite.sprite_type == "notes":
                            self.isreadingNote = True
                            self.notesFound += 1
                            self.notereadIndex += 1
                            self.msgnoteFound = [f"{self.chosenChar.capitalize()}: bir not buldum...","Notlar: %s/6" % (self.notesFound+3),""]
                            self.noteFoundMsg = TextEng((410, 580), self.display_surface, 5, self.chosenChar, self.msgnoteFound, 36)
                            target_sprite.kill()
                        elif target_sprite.sprite_type == "chest42":
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0, 75)
                            if randint(1,10) != 1:
                                player.pot_amount += 1
                                self.potFoundSfx.play()
                                self.animPlay.spawnParticles(
                                    "spawn_pot", pos - offset, [self.vis_sprites]
                                )
                                self.ispotFound = True
                                self.isMimicked = False
                                self.potfoundMsg = TextEng((410, 580), self.display_surface, 5, self.chosenChar, self.msgpotFound, 36)
                            else:
                                self.ispotFound = False
                                self.player.hp -= 50
                                self.mimicSfx.play()
                                self.animPlay.spawnParticles(
                                    "mimic", pos - offset, [self.vis_sprites]
                                )
                                self.isMimicked = True
                                self.mimickedMsg = TextEng((410, 580), self.display_surface, 5, self.chosenChar, self.mimickedMsgs, 36)
                            for crate_piece in range(randint(3, 6)):
                                self.crateSfx.play()
                                self.animPlay.spawnParticles(
                                    "crate_piece", pos - offset, [self.vis_sprites]
                                )
                            target_sprite.kill()
                        else:
                            target_sprite.takeDMG(
                                self.player, attack_sprite.sprite_type
                            )

    def dmgPlayer(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.hp -= amount
            self.player.heartbeat_cd = 15 * (self.player.hp)
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.animPlay.spawnParticles(attack_type,self.player.rect.center,[self.vis_sprites])

    def execDeathParticles(self, pos, particle_type):
        self.animPlay.spawnParticles(particle_type, pos, self.vis_sprites)


    def addXP(self, amount):
        self.player.xp += amount

    def checkIfPlayerDead(self,player):
        if player.hp <= 0:
            self.current_state = STATE_GAMEOVER
            
    def triggerStartCutscene(self):
        if self.current_state == STATE_BEFOREDOORCUTSCENE:
            self.cutsceneDoor.start()
            self.current_state = STATE_DOORCUTSCENE
            
        elif self.current_state == STATE_DOORCUTSCENE:
            self.cutsceneDoor.update()
            self.cutsceneDoor.draw(self.display_surface)
            if self.cutsceneDoor.is_finished():
                self.current_state = STATE_GAMEPLAYTWO
                pygame.mixer.music.load('sound\music\ep2theme.mp3')
                pygame.mixer.music.play(-1)

    def run(self):
        
        
        
        if self.current_state == STATE_GAMEPLAYTWO:
            
            self.vis_sprites.camFollowPlayer(self.player)
            self.vis_sprites.update()
            self.vis_sprites.hnpcUpdate(self.player)
            
            self.checkHNPCHostility(self.player)
            self.epOneMsg.update()
            self.obs_sprites.update()
            if self.ispotFound:
                self.potfoundMsg.update()
            if self.isMimicked:
                self.mimickedMsg.update()
            if self.isreadingNote:
                self.noteList[0].update()
                self.noteList[1].update()
                self.noteList[2].update()
                self.noteFoundMsg.update()
            else:
                self.noteFoundMsg = None
        
        if self.player.xp == 1250 and self.notesFound == 3:
            return "next"
            
            
        self.ui.deathDisplay(self.player)
        if self.current_state == STATE_GAMEPLAYTWO:
            self.ui.display(self.player)
        self.triggerStartCutscene()
        self.checkIfPlayerDead(self.player)
        if self.current_state == STATE_GAMEOVER:
            self.gameoverMsg.update()
            if self.gameoverMsg.active_message == len(self.gameoverMsg.messages)-1:
                return "dead"



class FollowingCamSys(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        self.floor_surf = pygame.image.load(
            "img\map\Final-Teslim.png"
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

