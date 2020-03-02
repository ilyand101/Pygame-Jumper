import pygame
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLCDNumber, QLabel, QLineEdit, QMainWindow, QInputDialog, QFontDialog
from pygame import *
import random
import os

pygame.init()

window_x = 500
window_y = 550

pygame.mixer.music.load('1.mp3')
pygame.mixer.music.play(-1)

init()
window = display.set_mode((window_x, window_y))
display.set_caption('Jumping')
clock = time.Clock()

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


def load_image(self, image, name, colorkey=None):
    fullname = os.path.join('Proekt', name)
    try:
        image = image.load(fullname)
    except pygame.error as message:
        print('Cannot load image: ', name)
        raise SystemExit
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


class player():
    def __init__(self):
        self.stand1 = image.load('stand1.png')
        self.fall = image.load('fall.png')
        self.jump_right = image.load('jump.png')
        self.jump_left = transform.flip(self.jump_right, True, False)
        self.stand = image.load('stand.png')

        self.reset()
    def reset(self):
        self.speed_x = 0
        self.speed_y = 0
        self.max_speed_x = 5
        self.max_speed_y = 15
        self.x_jumping = 0.5
        self.img = self.jump_right
        self.jump_speed = 15

        player_size = 7
        self.width, self.height = 7 * player_size, 12 * player_size
        self.scale = player_size

        self.x = (window_x - self.width) / 2
        self.y = window_y - self.height

    def update(self, p):
        self.side_control()
        self.physics(p)
        self.move()
        self.show()

        self.x += self.speed_x
        self.y -= self.speed_y

        return (self.img, (self.x, self.y, self.width, self.height))

    def physics(self, p):

        on = False

        for colour, rect in p:
            x, y, w, h = rect

            if self.x + self.width / 2 > x and self.x - self.width / 2 < x + w:

                if self.y + self.height >= y and self.y + self.height <= y + h:

                    if self.speed_y < 0:
                        on = True

        if not on and not self.y >= window_y - self.height:
            self.speed_y -= 0.5
        elif on:
            self.speed_y = self.jump_speed
        else:
            self.y = window_y - self.height
            self.speed_x = 0
            self.speed_y = 0
            if self.x != (window_x - self.width) / 2:
                if self.x > (window_x - self.width) / 2:
                    self.x = max((window_x - self.width) / 2, self.x - 6)
                else:
                    self.x = min((window_x - self.width) / 2, self.x + 6)

            else:
                keys = key.get_pressed()
                if keys[K_SPACE]:
                    self.speed_y = self.jump_speed

    def side_control(self):
        if self.x + self.width < 0:
            self.x = window_x - self.scale
        if self.x > window_x:
            self.x = -self.width

    def show(self):
        if self.speed_y > 0:
            if self.speed_x > 0:
                self.img = self.jump_right
            elif self.speed_x < 0:
                self.img = self.jump_left
        else:
            self.img = self.fall

    def slow_character(self):
        if self.speed_x < 0: self.speed_x = min(0, self.speed_x + self.x_jumping / 6)
        if self.speed_x > 0: self.speed_x = max(0, self.speed_x - self.x_jumping / 6)

    def move(self):
        keys = key.get_pressed()

        if not self.y >= window_y - self.height:

            if keys[K_LEFT] and keys[K_RIGHT]:
                self.slow_character()
            elif keys[K_LEFT]:
                self.speed_x -= self.x_jumping
            elif keys[K_RIGHT]:
                self.speed_x += self.x_jumping
            else:
                self.slow_character()

            self.speed_x = max(-self.max_speed_x, min(self.max_speed_x, self.speed_x))
            self.speed_y = max(-self.max_speed_y, min(self.max_speed_y, self.speed_y))


platform_spacing = 100


class Platform_Manager:
    def __init__(self):
        self.platforms = []
        self.spawns = 0
        self.start_spawn = window_y

        scale = 3
        self.width, self.height = 24 * scale, 6 * scale

    def update(self):
        self.spawner()
        return self.manage()

    def spawner(self):
        if window_y - info['screen_y'] > self.spawns * platform_spacing:
            self.spawn()

    def spawn(self):
        y = self.start_spawn - self.spawns * platform_spacing
        x = random.randint(-self.width, window_x)

        self.platforms.append(Platform(x, y, random.choice([1, -1])))
        self.spawns += 1

    def manage(self):
        u = []
        b = []
        for i in self.platforms:
            i.move()
            i.change_direction()
            b.append(i.show())

            if i.on_screen():
                u.append(i)

        self.platforms = u
        return b


class Platform:
    def __init__(self, x, y, direction):
        self.platform = image.load('sky.png')
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = 2
        #self.colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        size = 3
        self.width, self.height = 25 * size, 6 * size #   Изменение параметров платформ!!!!!!!!!!!!!!!!!!!

    def move(self):
        self.x += self.speed * self.direction
        self.change_direction()

    def change_direction(self):
        if self.x <= 0:
            self.direction = 1
        if self.x + self.width >= window_x:
            self.direction = -1

    def on_screen(self):
        if self.y > info['screen_y'] + window_y:
            return False
        return True

    def show(self):
        return ((255, 255, 255), (self.x, self.y, self.width, self.height))


def blit_images(x):
    for i in x:
        window.blit(transform.scale(i[0], (i[1][2], i[1][3])), (i[1][0], i[1][1] - info['screen_y']))


def event_loop():
    for loop in event.get():
        if loop.type == KEYDOWN:
            if loop.key == K_ESCAPE:
                quit()
        if loop.type == QUIT:
            quit()


f = font.SysFont('', 60)


def show_score(score, pos):
    message = f.render(str(round(score)), True, (255, 0, 0))
    rect = message.get_rect()

    if pos == 0:
        x = window_x - rect.width - 300
    else:
        x = 10
    y = rect.height + 10

    window.blit(message, (x, y))


info = {
    'screen_y': 0,
    'score': 0,
    'high_score': 0
}


BackGround = Background('background.jpg', [0, 0])
stick_man = player()
platform_manager = Platform_Manager()

while True:


    event_loop()

    platform_blit = platform_manager.update()
    stick_blit = stick_man.update(platform_blit)
    info['screen_y'] = min(min(0, stick_blit[1][1] - window_y * 0.4), info['screen_y'])
    info['score'] = (-stick_blit[1][1] + 470) / 50

    # print(stick_blit[1][1], info['screen_y'])
    if stick_blit[1][1] - 470 > info['screen_y']:
        info['score'] = 0
        info['screen_y'] = 0
        stick_man = player()
        platform_manager = Platform_Manager()

    clock.tick(60)

    window.fill((255, 255, 255))
    window.blit(BackGround.image, BackGround.rect)

    blit_images([stick_blit])

    for x in platform_blit:
        i = list(x)
        i[1] = list(i[1])
        i[1][1] -= info['screen_y']
        draw.rect(window, i[0], i[1])

    info['high_score'] = max(info['high_score'], info['score'])


    show_score(info['score'], 1)
    show_score(info['high_score'], 0)

    pygame.display.flip()
    all_sprites.draw(window)

    clock.tick(200)


    display.update()
pygame.quit()


