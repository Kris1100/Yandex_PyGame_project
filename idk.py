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
    def __init__(self, sheet, columns, rows, x, y, k1=-1, k2=-1, is_moving=False, v=5):
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.k1 = k1

        self.v = v
        self.is_moving = is_moving
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
        if self.is_moving:
            self.rect[0] -= self.v


size = width, height = 1024, 401
screen = pygame.display.set_mode(size)
pygame.draw.rect(screen, pygame.Color('white'), (0, 0, width, height), 0)
pygame.display.flip()
running = True
image = pygame.Surface([100, 100])

mon = AnimatedSprite(load_image("monster_1.png"), 8, 3, 1024, 50, is_moving=True)

f_mon = AnimatedSprite(load_image("flying_monster.png"), 4, 3, 1024, 200, is_moving=True, v=10)

clock = pygame.time.Clock()
v = 0.2
all_sprites.draw(screen)
all_sprites.update()
pygame.display.update()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    mon.update()
    f_mon.update()
    pygame.draw.rect(screen, pygame.Color('white'), (0, 0, width, height), 0)

    screen.blit(mon.image, mon.rect)
    screen.blit(f_mon.image, f_mon.rect)
    clock.tick(10)
    pygame.display.update()
pygame.quit()
