import pygame
import random
from pygame import draw
import os


def load_image(name):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
        return image
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)


all_sprites = pygame.sprite.Group()
pygame.init()


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, k1=-1, k2=-1):
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.k1 = k1
        self.k2 = k2
        if self.k1 != -1 and (self.k2 != -1):
            self.r = self.k2 - self.k1
        else:
            self.r = 0
        if self.k1 == -1:
            self.k1 = 0
        if self.k2 == -1:
            self.k2 = x * y - 1

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        if self.r == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]

        else:
            self.cur_frame = (self.cur_frame + 1) % self.r
            self.image = self.frames[self.cur_frame + self.k1]


size = width, height = 1024, 401

screen = pygame.display.set_mode(size)
pygame.draw.rect(screen, pygame.Color('white'), (0, 0, width, height), 0)

pygame.display.flip()
image = pygame.Surface([100, 100])
bear = AnimatedSprite(load_image("Bear.png"), 8, 8, 50, 50)
screen.blit(bear.image, bear.rect)
bear_run = AnimatedSprite(load_image("Bear.png"), 8, 8, 50, 50, 10, 22)

bear_hit = AnimatedSprite(load_image("Bear.png"), 8, 8, 50, 50, 23, 31)

bear_jump = AnimatedSprite(load_image("Bear.png"), 8, 8, 50, 50, 42, 51)

clock = pygame.time.Clock()
v = 0.2
all_sprites.draw(screen)
pygame.display.update()
running = True
evtype = 0
x = 50
evkey = 0
while running:
    while evtype == pygame.KEYDOWN and evkey == pygame.K_RIGHT:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYUP and (event.key == pygame.K_RIGHT):
                evtype = 0
                evkey = 0
                pygame.draw.rect(screen, pygame.Color('white'), (0, 0, width, height), 0)
                screen.blit(bear.image, bear.rect)
                pygame.display.update()
                is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key != pygame.K_RIGHT:
                    is_running = False
                    break
            if event.type == pygame.KEYDOWN:
                is_running = False
                break
        if not is_running:
            break
        for i in range(22 - 10):
            bear_run.update()
            pygame.draw.rect(screen, pygame.Color('white'), (0, 0, width, height), 0)
            screen.blit(bear_run.image, bear_run.rect)
            clock.tick(15)
            pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                for i in range(51 - 42):
                    pygame.draw.rect(screen, pygame.Color('white'), (0, 0, width, height), 0)
                    screen.blit(bear_jump.image, bear_jump.rect)
                    bear_jump.update()
                    clock.tick(15)
                    pygame.display.update()
                pygame.draw.rect(screen, pygame.Color('white'), (0, 0, width, height), 0)
                screen.blit(bear.image, bear.rect)
                pygame.display.update()

            if event.key == pygame.K_q:
                for i in range(31 - 23):
                    pygame.draw.rect(screen, pygame.Color('white'), (0, 0, width, height), 0)
                    screen.blit(bear_hit.image, bear_hit.rect)
                    bear_hit.update()
                    clock.tick(15)
                    pygame.display.update()
                pygame.draw.rect(screen, pygame.Color('white'), (0, 0, width, height), 0)
                screen.blit(bear.image, bear.rect)
                pygame.display.update()
            evtype = event.type
            evkey = event.key
        if event.type == pygame.KEYUP and (event.key == pygame.K_RIGHT):
            evtype = 0
            evkey = 0
            pygame.draw.rect(screen, pygame.Color('white'), (0, 0, width, height), 0)
            screen.blit(bear.image, bear.rect)
            pygame.display.update()
            is_running = False
        if evtype == pygame.KEYDOWN and evkey == pygame.K_RIGHT:
            is_running = True



pygame.quit()
