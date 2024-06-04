from csv import reader
from os import walk
import pygame

STATE_GAMEPLAY = 'gameplay'
STATE_CUTSCENE = 'cutscene'
STATE_CHARCHOOSE = 'charchoose'
STATE_STARTSCREEN = 'startscreen'
STATE_CUTSCENEONE = 'cutsceneone'
STATE_BEFORECUTSCENEONE = 'beforecutsceneone'
STATE_GAMEOVER = 'gameover'
STATE_DOORCUTSCENE = 'doorcutscene'
STATE_GAMEPLAYTWO = 'gameplaytwo'
STATE_BEFOREDOORCUTSCENE = 'beforedoorcutscene'
STATE_FINALCUTSCENE = 'finalcutscene'
STATE_BEFOREFINALCUTSCENE = 'beforefinalcutscene'

current_state = STATE_STARTSCREEN

HITBOX_OFFSET = {
    "player": (-64, -84),
    "earman": (0,  0),
    "eyeman": (0,  0),
    "objs": (-30,  -30),
    "invisible": (-50,  -50),
    "crate": (0,0),
    "chest": (0, 0),
    "notes": (-10, 0),
    "objs42": (0,0),
    "invisible42": (-25,-25),
    "crate42": (0,0),
    "chest42": (0,0)
}

def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter=",")
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map


def import_folder(path):
    surface_list = []

    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + "/" + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list

music_tracks = {
    'background': 'background_music.mp3',
    'battle': 'battle_music.mp3',
    'victory': 'victory_music.mp3'
}

items = {
    "small_hp_potion": {
        "cooldown": 1000,
        "start_amount": 3,
        "strength": 30,
        "design": "img\items\small_hp_potion",
    }
}

weapons = {
    "sword": {"cooldown": 100, "damage": 15, "design": "img\weapons\sword\efull.png"}
}

skills = {
    "heal": {"strength": 20, "cost": 25, "design": "img\items\small_hp_potion/1.png"},
    "hide": {"strength": 5, "cost": 25, "design": "img\particles\hide.png"},
}

hnpc = {
    "earman": {
        "hp": 200,
        "xp": 250,
        "damage": 50,
        "attack_type": "scream",
        "attack_sound": "sound\sfx/blood_flesh_gore_B_27.wav",
        "speed": 7,
        "knockback": 0.01,
        "dmg_rad": 130,
        "chase_rad": 250,
    },
    "eyeman": {
        "hp": 100,
        "xp": 100,
        "damage": 25,
        "attack_type": "rot",
        "attack_sound": "sound\sfx/blood_flesh_gore_B_04.wav",
        "speed": 5,
        "knockback": 0.01,
        "dmg_rad": 70,
        "chase_rad": 350,
    },
    "final-boss": {
        "hp": 300,
        "xp":1000,
        "damage": 75,
        "attack_type": "slime",
        "attack_sound": "sound\sfx/blood_flesh_gore_long_A_20.wav",
        "speed": 3,
        "knockback": 1,
        "dmg_rad": 100,
        "chase_rad": 500,
    }
    
}

cutsceneOneImages = [pygame.image.load('img\cutscenes\start/4.png'),pygame.image.load('img\cutscenes\start/3.png'),pygame.image.load('img\cutscenes\start/2.png'),pygame.image.load('img\cutscenes\start/1.png'),pygame.image.load('img\cutscenes\start/5.png'),pygame.image.load('img\cutscenes\start/6.jpg'),pygame.image.load('img\cutscenes\start/7.jpg')]
cutsceneDoorImages = [pygame.image.load('img\cutscenes\door/1.png')]
cutsceneEndImages = [pygame.image.load('img\cutscenes\end/1.png'),pygame.image.load('img\cutscenes\end/2.png'),pygame.image.load('img\cutscenes\end/3.png')]


paperImages = [pygame.image.load('img\papers/paper1.png'),pygame.image.load('img\papers/paper2.png'),pygame.image.load('img\papers/paper3.png'),pygame.image.load('img\papers/paper4.png'),pygame.image.load('img\papers/paper5.png'),pygame.image.load('img\papers/paper6.png')]
jumpImg = pygame.image.load("img\jump.png")