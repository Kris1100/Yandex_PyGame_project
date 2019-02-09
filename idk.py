import pygame
import random
import os
import sys

FPS = 50
all_sprites = pygame.sprite.Group()
pygame.init()
size = WIDTH, HEIGHT = 1200, 675
screen = pygame.display.set_mode(size)
pygame.draw.rect(screen, pygame.Color('white'), (0, 0, WIDTH, HEIGHT), 0)
pygame.display.flip()
running = True
image = pygame.Surface([100, 100])


def load_image(name):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
        return image
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)


def terminate():
    pygame.quit()
    sys.exit()


clock = pygame.time.Clock()


def start_screen():
    intro_text = ["НАЧАТЬ ИГРУ",
                  "ПРОДОЛЖИТЬ ИГРУ",
                  "ПРАВИЛА ИГРЫ",
                  "НАСТРОЙКИ",
                  "УРОВЕНЬ",
                  "ТАБЛИЦА РЕЗУЛЬТАТОВ",
                  "ВЫХОД"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 200
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pass
        pygame.draw.rect(screen, pygame.Color('white'), (0, 0, WIDTH, HEIGHT), 0)
        start_screen()
        clock.tick(10)
    pygame.display.update()
pygame.quit()
