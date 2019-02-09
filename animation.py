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
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


size = width, height = 1024, 401
screen = pygame.display.set_mode(size)
pygame.display.flip()
image = pygame.Surface([100, 100])

dragon = AnimatedSprite(load_image("Jumping sack_Walk.png"), 6, 4 , 50, 50)

clock = pygame.time.Clock()
v = 0.2
all_sprites.draw(screen)
all_sprites.update()
pygame.display.update()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    dragon.update()
    pygame.draw.rect(screen, pygame.Color('white'), (0, 0, width, height), 0)

    all_sprites.draw(screen)
    clock.tick(10)
    pygame.display.update()
pygame.quit()
