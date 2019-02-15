import pygame
import random
import sys
import os

pygame.init()
size = width, height = 1024, 401
screen = pygame.display.set_mode(size)
pygame.draw.rect(screen, pygame.Color('white'), (0, 0, width, height), 0)
pygame.display.flip()
image = pygame.Surface([100, 100])
clock = pygame.time.Clock()
v = 0.2
pygame.display.update()
running = True
is_running = False
x = 50
pause = False
all_sprites = pygame.sprite.Group()


def terminate():
    pygame.quit()
    sys.exit()


monsters = []


def start_screen():
    intro_text = ["НАЧАТЬ ИГРУ",
                  "ПРАВИЛА ИГРЫ",
                  "НАСТРОЙКИ",
                  "УРОВЕНЬ",
                  "ВЫХОД"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
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


def load_image(name):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
        return image
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


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


class Monster(AnimatedSprite):
    def __init__(self, sheet, columns, rows, x, y, k1=-1, k2=-1, is_moving=False, v=5):
        self.frames = []
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        self.hp = 50
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

    def update(self):
        if self.r == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)

            self.image = self.frames[self.cur_frame]

        else:
            self.cur_frame = (self.cur_frame + 1) % self.r

            self.image = self.frames[self.cur_frame + self.k1]
        if self.is_moving:
            self.rect[0] -= self.v


class Bear:
    global pause

    def __init__(self):
        self.hp = 100
        self.bear = AnimatedSprite(load_image("Bear.png"), 8, 8, 50, 50)
        self.bear_run = AnimatedSprite(load_image("Bear.png"), 8, 8, 50, 50, 10, 22)
        self.bear_hit = AnimatedSprite(load_image("Bear.png"), 8, 8, 50, 50, 23, 31)
        self.bear_jump = AnimatedSprite(load_image("Bear.png"), 8, 8, 50, 50, 42, 51)

    def run(self):
        global running
        global pause
        for i in range(22 - 10):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:

                        if pause:
                            pause = False
                        else:
                            pause = True
                    if not pause:
                        if event.key == pygame.K_UP:
                            meathead.jump()
                        if event.key == pygame.K_q:
                            meathead.hit()

            if not pause:
                self.bear_run.update()
                screen.blit(fon, (0, 0, width, height))
                if not pause:

                    for i in monsters:
                        i.update()
                    for i in monsters:
                        screen.blit(i.image, i.rect)
                    screen.blit(self.bear_run.image, self.bear_run.rect)
                    clock.tick(15)
                    pygame.display.update()

    def jump(self):
        for i in range(51 - 42):
            for i in range(100000):
                pass
            screen.blit(fon, (0, 0, width, height))
            screen.blit(self.bear_jump.image, self.bear_jump.rect)
            for i in monsters:
                i.update()
            for i in monsters:
                screen.blit(i.image, i.rect)
            self.bear_jump.update()
            clock.tick(10)
            pygame.display.update()
        screen.blit(fon, (0, 0, width, height))
        if not pause:

            for i in monsters:
                i.update()
            for i in monsters:
                screen.blit(i.image, i.rect)
            screen.blit(self.bear.image, self.bear.rect)
            pygame.display.update()

    def hit(self):
        for i in range(31 - 23):
            screen.blit(fon, (0, 0, width, height))
            screen.blit(self.bear_hit.image, self.bear_hit.rect)
            for i in monsters:
                i.update()
            for i in monsters:
                screen.blit(i.image, i.rect)
            self.bear_hit.update()
            clock.tick(15)
            pygame.display.update()
        screen.blit(fon, (0, 0, width, height))
        if not pause:

            for i in monsters:
                i.update()
            for i in monsters:
                screen.blit(i.image, i.rect)
            screen.blit(self.bear.image, self.bear.rect)
            pygame.display.update()


fon = load_image('fon.jpg')

meathead = Bear()

camera = Camera()

screen.blit(fon, (0, 0, width, height))

what_time_i_need = 0


def which_one():
    global what_time_i_need
    z = random.choice(['mon', 'f_mon'])
    if z == 'mon':
        sprite = Monster(load_image("monster_1.png"), 8, 3, 1024, 80, is_moving=True)
        what_time_i_need = 15
        monsters.append(sprite)
    else:
        sprite = Monster(pygame.transform.scale(load_image("flying_monster.png"), (384, 288)), 4, 3, 1024, 230,
                         is_moving=True, v=20)
        what_time_i_need = 7
        monsters.append(sprite)


pygame.display.flip()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:

                if pause:
                    pause = False
                else:
                    pause = True

            if not pause:
                if event.key == pygame.K_UP:
                    meathead.jump()

                if event.key == pygame.K_q:
                    meathead.hit()

    if not pause:
        if what_time_i_need == 0:
            which_one()
        what_time_i_need -= 1

        meathead.run()
        pygame.display.flip()

pygame.quit()
