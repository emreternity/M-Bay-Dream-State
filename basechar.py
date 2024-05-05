import pygame
from math import sin


class CharacterBase(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.framei = 0
        self.anim_speed = 0.15
        self.direction = pygame.math.Vector2()

    def charMove(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.checkCollision("horizontal")
        self.hitbox.y += self.direction.y * speed
        self.checkCollision("vertical")
        self.rect.center = self.hitbox.center

    def checkCollision(self, direction):
        if direction == "horizontal":
            for sprite in self.obs_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == "vertical":
            for sprite in self.obs_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def sinWaveAnim(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 150
