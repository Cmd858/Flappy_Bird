import pygame
from pygame.locals import *
from NN import *
import copy


class Bird:
    def __init__(self, screen, net=None):
        self.sprite = pygame.image.load('C:/Users/Alexander/PycharmProjects/Flappy_Bird/Bird.png').convert()
        self.sprite.set_colorkey(self.sprite.get_at((0, 0)))
        self.y = 200
        self.x = 50
        self.rect = (self.x, self.y, 30, 30)
        self.acc = 0
        self.screen = screen
        self.scr_w = screen.get_width()
        self.scr_h = screen.get_height()
        self.events = []
        self.score = 0
        self.topy = None
        self.bottomy = None  # pipe y (top and bottom)
        # TODO: fix draw breaking on hidden nodes

        if net == None:
            self.net = Network(2, 1, 0.05, 0.25, 0.5, 0.1, (-2, 0), 5)  # edit net values in population
            self.net.mutate()

        else:
            self.net = copy.deepcopy(net)
            # print('mutating')
            # self.net.mutate()

    def move(self):
        # for event in self.events:
        #     if event.type == KEYDOWN:
        #         if event.key == K_SPACE:
        self.net.getinput([self.distytop, self.distybottom])
        self.net.run()
        self.jump = self.net.getoutput()[0]
        if self.jump > 0.5:
            self.acc = -6
        # print(self.jump)
        self.y += self.acc
        self.acc += 0.5
        if self.acc > 10:
            self.acc = 10
        self.rect = (self.x, self.y, 30, 30)

    def draw(self):
        self.screen.blit(self.sprite, (self.x, self.y))
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect, 1)

    def collide(self):
        if self.y + 30 > self.scr_w or self.y < 0:
            return True

    def getevents(self, events):
        self.events = events

    def getrect(self):
        return Rect(self.rect)

    def getpipey(self, topy, bottomy):
        self.topy = topy
        self.bottomy = bottomy
        self.distytop = self.topy - self.y
        self.distybottom = self.y - self.bottomy

    def tick(self):
        self.score += 1
        # print(self.score)

    def reset(self):
        self.y = 200
        self.x = 50
        self.events = []
        self.score = 0