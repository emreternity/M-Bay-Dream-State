import pygame
from pygame.sprite import Group
from random import choice
from data import *


class AnimPlayer:
    def __init__(self):
        self.frames = {
            "rot": import_folder("img\particles/rot"),
            "scream": import_folder("img\particles\scream"),
            "heal": import_folder("img\particles\heal/frames"),
            "eyeman": import_folder("img\particles\hnpc_death"),
            "earman": import_folder("img\particles\hnpc_death"),
        }

    def flipAnimIMGs(self, frames):
        new_frames = []
        for frame in frames:
            flipped_frame = pygame.transform.flip(frame, True, False)
            new_frames.append(flipped_frame)
        return new_frames

    def crateDestroyedParticles(self, pos, groups):
        anim_frames = choice(self.frames["crate_piece"])
        ParticleEffect(pos, anim_frames, groups)

    def spawnParticles(self, animation_type, pos, groups):
        anim_frames = self.frames[animation_type]
        ParticleEffect(pos, anim_frames, groups)


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, anim_frames, groups):
        super().__init__(groups)
        self.framei = 0
        self.anim_speed = 0.15
        self.frames = anim_frames
        self.image = self.frames[self.framei]
        self.rect = self.image.get_rect(center=pos)

    def anim(self):
        self.framei += self.anim_speed
        if self.framei >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.framei)]

    def update(self):
        self.anim()
