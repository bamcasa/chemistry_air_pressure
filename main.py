import time

import pygame
import sys
import random
import numpy as np
import math


class TextInputBox(pygame.sprite.Sprite):
    def __init__(self, x, y, w, font):
        super().__init__()
        self.color = (255, 255, 255)
        self.backcolor = None
        self.pos = (x, y)
        self.width = w
        self.font = font
        self.active = False
        self.text = ""
        self.render_text()

    def render_text(self):
        t_surf = self.font.render(self.text, True, self.color, self.backcolor)
        self.image = pygame.Surface((max(self.width, t_surf.get_width()+10), t_surf.get_height()+10), pygame.SRCALPHA)
        if self.backcolor:
            self.image.fill(self.backcolor)
        self.image.blit(t_surf, (5, 5))
        pygame.draw.rect(self.image, self.color, self.image.get_rect().inflate(-2, -2), 2)
        self.rect = self.image.get_rect(topleft = self.pos)

    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and not self.active:
                self.active = self.rect.collidepoint(event.pos)
            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.render_text()


pygame.init()

FPS = 30

BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

screen_size = (600, 600)

screen = pygame.display.set_mode((screen_size[0], screen_size[1] + 100))
pygame.font.init()
font = pygame.font.SysFont(None, 30)

n = 100
particles = np.zeros((n, 3))  # y, x, angle
# print(particles[1])
for i in range(len(particles)):
    particles[i][0] = random.randint(50, 550)
    particles[i][1] = random.randint(50, 550)
    particles[i][2] = random.randint(0, 360)

# print(particles)

crashed_times = 0


def draw_screen():
    global particles
    # print(particles)
    screen.fill(WHITE)
    for particle in particles:
        particle_pos = (particle[0], particle[1])
        # print(particle)
        # print(particle_pos)
        pygame.draw.circle(screen, BLACK, particle_pos, 5)


def show_data():
    global crashed_times, start_t
    pygame.draw.rect(screen, (200,200,200), [0, 615, 600, 200])
    text = font.render(f"n : {crashed_times}, P : {round(crashed_times/(time.time() - start_t))}", True, BLACK)
    screen.blit(text, (10, 620))



def move_particles(v):
    for i in range(len(particles)):
        angle_rad = math.radians(particles[i][2])
        particles[i][0] += v * math.sin(angle_rad)
        particles[i][1] += v * math.cos(angle_rad)

        if is_crash(particles[i][0], particles[i][1]):
            particles[i][2] += 90

def is_crash(y, x):
    global crashed_times
    result = False
    if y >= screen_size[0]:  # 아래쪽 부딪힘
        result = True
    if y <= 0:  # 위쪽 부딪힘
        result = True
    if x >= screen_size[1]:  # 오른쪽 부딪힘
        result = True
    if x <= 0:  # 왼쪽 부딪힘
        result = True

    if result:
        crashed_times += 1
    return result

start_t = time.time()

while True:
    clock = pygame.time.Clock()
    clock.tick(FPS)

    move_particles(10)
    draw_screen()
    show_data()
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
