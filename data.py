from csv import reader
from os import walk
import pygame


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
        "attack_sound": "sfx\player\walk2.mp3",
        "speed": 7,
        "knockback": 1,
        "dmg_rad": 130,
        "chase_rad": 250,
    },
    "eyeman": {
        "hp": 100,
        "xp": 100,
        "damage": 25,
        "attack_type": "rot",
        "attack_sound": "sfx\player\walk1.mp3",
        "speed": 5,
        "knockback": 0.01,
        "dmg_rad": 70,
        "chase_rad": 350,
    },
}
