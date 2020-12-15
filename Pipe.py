import pygame
from pygame.locals import *
import random


class Pipe:
    def __init__(self, screen, y=0): # sets y to 1 for consistent first pipe placement
        self.sprite = pygame.image.load('C:/Users/Alexander/PycharmProjects/Flappy_Bird/pipe.png').convert()
        self.sprite.set_colorkey(self.sprite.get_at((0, 0)))
        # print(self.sprite.get_at((1,1)))
        self.width = 60
        self.screen = screen
        self.x = 600
        if y == 0:
            self.y1 = random.randint(0, 450)
        else:
            self.y1 = 225
        # print(y)
        self.y2 = self.y1 + 100
        self.rect1 = pygame.Rect((self.x, 0), (self.width, self.y1))
        self.rect2 = pygame.Rect((self.x, self.y2), (self.width, 600))

    def move(self):
        self.x -= 1

    def edge(self):
        if self.x+self.sprite.get_width() < 0:
            return True
        else:
            return False

    def draw(self):
        self.rect1 = pygame.Rect((self.x, 0), (self.width, self.y1))
        self.rect2 = pygame.Rect((self.x, self.y2), (self.width, 600))
        self.screen.blit(self.sprite, (self.x, self.y2))  # + self.sprite.get_height()))
        self.screen.blit(pygame.transform.flip(self.sprite, False, True), (self.x, self.y1 - self.sprite.get_height()))
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect1, 1)
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect2, 1)

    def collide(self, colrect):
        if colrect.colliderect(self.rect1):
            return True
        elif colrect.colliderect(self.rect2):
            return True
        else:
            return False

    def scoreup(self, birdx, score):
        if birdx == self.x:
            # print(score)
            return 1
        else:
            return 0
