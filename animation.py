import os
import random
import sys

import pygame

pygame.init()
dead = False

pygame.mixer.init()
score = 0
pygame.mixer.music.load('m.mp3')
pygame.mixer.music.play()
size = width, height = 1024, 576
screen = pygame.display.set_mode(size)
pygame.draw.rect(screen, pygame.Color('white'), (0, 0, width, height), 0)
pygame.display.flip()
image = pygame.Surface([100, 100])
clock = pygame.time.Clock()
v = 0.2
pygame.display.update()
running = True
start_of_game = False
is_running = False
x = 50
pause = False
all_sprites = pygame.sprite.Group()


def terminate():
    pygame.quit()
    sys.exit()


monsters = []


def load_image(name):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
        return image
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)


def scor():
    global score
    pygame.font.init()
    font = pygame.font.Font(None, 30)
    text = font.render("Счёт: " + str(score), 1, pygame.Color('white'))
    place = (0, 0)
    screen.blit(text, place)
    pygame.display.flip()


def start_screen():
    with open("score.txt", encoding='utf-8') as f:
        read_data = f.read()

    intro_text = ["НАЖМИТЕ S, ЧТОБЫ НАЧАТЬ ИГРУ",
                  "ПРАВИЛА ИГРЫ",
                  "Ваша задача убить всех монстров",
                  "Чтобы бить - нажмите Q",
                  "НАЖМИТЕ E, ЧТОБЫ ВЫЙТИ",
                  "РЕКОРД:", read_data]

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


def end_of_game():
    sprite = pygame.sprite.Sprite()
    sprite.image = load_image('gameover.png')
    sprite.image = pygame.transform.scale(sprite.image, (1024, 576))
    sprite.rect = sprite.image.get_rect()

    v = 0.2
    sprite.rect.x = 0
    sprite.rect.y = 0
    screen.blit(sprite.image, sprite.rect)
    pygame.display.update()


class Monster(AnimatedSprite):
    def __init__(self, sheet, columns, rows, x, y, k1=-1, k2=-1, is_moving=False, v=5):
        self.frames = []
        self.sheet = sheet
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        self.hp = 50
        self.x = x
        self.columns = columns
        self.rows = rows
        self.y = y
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
            self.x -= self.v


class Bear:
    global pause

    def __init__(self):
        self.hp = 100
        self.bear = AnimatedSprite(load_image("Bear.png"), 8, 8, 50, 150)
        self.bear_run = AnimatedSprite(load_image("Bear.png"), 8, 8, 50, 150, 10, 22)
        self.bear_hit = AnimatedSprite(load_image("Bear.png"), 8, 8, 50, 150, 23, 31)
        self.bear_jump = AnimatedSprite(load_image("Bear.png"), 8, 8, 50, 150, 42, 51)

    def run(self):
        global running
        global pause
        if start_of_game:
            scor()
            for i in range(22 - 10):
                scor()

                if not start_of_game:
                    break
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_e:
                            running = False
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
                    meathead.update()

                    self.bear_run.update()
                    scor()

                    screen.blit(fon, (0, 0, width, height))
                    if not pause:
                        for k in monsters:
                            k.update()
                        for k in monsters:
                            screen.blit(k.image, k.rect)
                        screen.blit(self.bear_run.image, self.bear_run.rect)
                        clock.tick(15)
                        pygame.display.update()

    def jump(self):
        scor()
        for i in range(51 - 42):
            scor()

            for j in range(100000):
                pass
            if i < (51 - 42) // 2:
                self.bear_jump.rect[1] -= 20
            else:
                self.bear_jump.rect[1] += 20

            screen.blit(fon, (0, 0, width, height))
            screen.blit(self.bear_jump.image, self.bear_jump.rect)
            for k in monsters:
                k.update()
            for k in monsters:
                screen.blit(k.image, k.rect)
            meathead.update()

            self.bear_jump.update()
            clock.tick(10)
            scor()

            pygame.display.update()
        screen.blit(fon, (0, 0, width, height))
        if not pause:

            for k in monsters:
                k.update()
            for k in monsters:
                screen.blit(k.image, k.rect)
            meathead.update()

            screen.blit(self.bear.image, self.bear.rect)
            scor()

            pygame.display.update()
        self.bear_jump.rect[1] -= 20

    def hit(self):
        if not pause:
            scor()
            self.bear_hit.rect[0] += 10
        for i in range(31 - 23):
            scor()

            screen.blit(fon, (0, 0, width, height))
            screen.blit(self.bear_hit.image, self.bear_hit.rect)
            for k in monsters:
                k.update()
            for k in monsters:
                screen.blit(k.image, k.rect)
            meathead.update()

            self.bear_hit.update()
            clock.tick(15)
            scor()

            pygame.display.update()
        screen.blit(fon, (0, 0, width, height))
        if not pause:

            for k in monsters:
                k.update()
            for k in monsters:
                screen.blit(k.image, k.rect)
            screen.blit(self.bear.image, self.bear.rect)
            pygame.display.update()
        if not pause:
            self.bear_hit.rect[0] -= 10

    def update(self):
        global running
        global score
        global dead
        global start_of_game
        for k in monsters:
            if self.bear_hit.rect[0] + self.bear_hit.rect[2] // 2 + 40 >= k.rect[0] and (
                    self.bear_hit.rect[0] != self.bear.rect[0]) and (k.v != 20) and (
                    self.bear_hit.rect[0] - k.rect[0] + k.rect[2]) <= 150:
                monsters.remove(k)
                score += 10
                fi = AnimatedSprite(load_image('fire.png'), 8, 4, k.rect[0], k.rect[1])
                for i in range(32):
                    screen.blit(fi.image, fi.rect)
                    fi.update()
                    pygame.display.flip()

            if (self.bear_jump.rect[1] + self.bear_jump.rect[3] // 2 + 40 >= k.rect[1]) and (k.v == 20) and (
                    self.bear_jump.rect[0] + self.bear_jump.rect[2] // 2 + 40 >= k.rect[0]) and (
                    self.bear_jump.rect[0] <= k.rect[0] + k.rect[2]):
                monsters.remove(k)
                score += 10
                fi = AnimatedSprite(load_image('fire.png'), 8, 4, k.rect[0], k.rect[1])
                for i in range(32):
                    screen.blit(fi.image, fi.rect)
                    fi.update()
                    pygame.display.flip()
            if self.bear.rect[0] >= k.rect[0] and (k.v == 20):
                start_of_game = False
                end_of_game()
                dead = True
                score = 0

                with open("score.txt", encoding='utf-8') as f:
                    read_data = f.read()

                if score > int(read_data):
                    d = open('score.txt', 'w')
                    d.write(str(score))
                    d.close()

            if self.bear.rect[0] + self.bear.rect[2] // 2 >= k.rect[0] and (k.v != 20):
                start_of_game = False
                end_of_game()
                dead = True
                score = 0

                with open("score.txt", encoding='utf-8') as f:
                    read_data = f.read()

                if score > int(read_data):
                    d = open('score.txt', 'w')
                    d.write(str(score))
                    d.close()


fon = load_image('fon.jpg')

meathead = Bear()

camera = Camera()

screen.blit(fon, (0, 0, width, height))

what_time_i_need = 0


def which_one():
    global what_time_i_need
    z = random.choice(['mon', 'f_mon'])
    if z == 'mon':
        sprite = Monster(load_image("monster_1.png"), 8, 3, 1024, 180, is_moving=True)
        what_time_i_need = 12
        monsters.append(sprite)
    else:
        sprite = Monster(pygame.transform.scale(load_image("flying_monster.png"), (384, 288)), 4, 3, 1024, 330,
                         is_moving=True, v=20)
        what_time_i_need = 6
        monsters.append(sprite)


pygame.display.flip()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                start_of_game = True
                monsters = []
            if event.key == pygame.K_e:
                running = False

            if start_of_game:
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
    if start_of_game:
        if not pause:
            meathead.update()
            if what_time_i_need == 0:
                which_one()
            what_time_i_need -= 1

            meathead.run()
            pygame.display.flip()
    else:
        scor()
        if not dead:
            start_screen()
        else:
            end_of_game()
        pygame.display.flip()
with open("score.txt", encoding='utf-8') as f:
    read_data = f.read()

if score > int(read_data):
    d = open('score.txt', 'w')
    d.write(str(score))
    d.close()
pygame.quit()
