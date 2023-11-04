import pygame, sys


class Bombero(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.animation_right = []
        self.animation_right.append(pygame.image.load('Sprites/right1.png'))
        self.animation_right.append(pygame.image.load('Sprites/right2.png'))
        self.animation_right.append(pygame.image.load('Sprites/right3.png'))
        self.animation_right.append(pygame.image.load('Sprites/right4.png'))
        self.animation_left = []
        self.animation_left.append(pygame.image.load('Sprites/left1.png'))
        self.animation_left.append(pygame.image.load('Sprites/left2.png'))
        self.animation_left.append(pygame.image.load('Sprites/left3.png'))
        self.animation_left.append(pygame.image.load('Sprites/left4.png'))
        self.bucket_right = []
        self.bucket_right.append(pygame.image.load('Sprites/bucketR1.png'))
        self.bucket_right.append(pygame.image.load('Sprites/bucketR2.png'))
        self.bucket_right.append(pygame.image.load('Sprites/bucketR3.png'))
        self.bucket_right.append(pygame.image.load('Sprites/bucketR4.png'))
        self.bucket_left = []
        self.bucket_left.append(pygame.image.load('Sprites/bucketL1.png'))
        self.bucket_left.append(pygame.image.load('Sprites/bucketL2.png'))
        self.bucket_left.append(pygame.image.load('Sprites/bucketL3.png'))
        self.bucket_left.append(pygame.image.load('Sprites/bucketL4.png'))
        self.counter = 0
        self.position = position
        self.image = self.animation_right[self.counter]
        self.rect = self.image.get_rect()
        self.rect.topleft = [position[0], position[1]]

    def update(self, direccion):
        self.counter += 1
        if direccion == 'derecha':
            if self.counter >= len(self.animation_right):
                self.counter = 0
            self.image = self.animation_right[self.counter]
        if direccion == 'izquierda':
            if self.counter >= len(self.animation_left):
                self.counter = 0
            self.image = self.animation_left[self.counter]
        if direccion == 'derecha balde':
            if self.counter >= len(self.bucket_right):
                self.counter = 0
            self.image = self.bucket_right[self.counter]
        if direccion == 'izquierda balde':
            if self.counter >= len(self.bucket_left):
                self.counter = 0
            self.image = self.bucket_left[self.counter]






