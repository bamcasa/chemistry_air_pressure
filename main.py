import time

import pygame
import sys
import random
import numpy as np
import math

pygame.init()

FPS = 30

BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def init(n1, T1, v1):
    global T
    global n
    global lab_size
    global particles
    T = T1
    n = n1
    lab_size = (v1, v1)

    particles = np.zeros((n, 3))  # y, x, angle
    # print(particles[1])
    for i in range(len(particles)):
        particles[i][0] = random.randint(50, 550)
        particles[i][1] = random.randint(50, 550)
        particles[i][2] = random.randint(0, 360)


lab_size = [600, 600]
n = 100
T = 273
particles = np.array([0])
init(100, 273, 600)

screen_size = [600, 800]
screen = pygame.display.set_mode((screen_size[0], screen_size[1]))
pygame.font.init()
font = pygame.font.Font("ttf\D2coding.ttf",30)





# print(particles)

crashed_times = 0
# ---------------- input box
user_text = str(T)
input_rect = pygame.Rect(400, 660, 140, 32)
color_active = pygame.Color('lightskyblue3')
color_passive = pygame.Color('chartreuse4')
color = color_passive
active = False
#-------------- input box2
user_text2 = str(n)
input_rect2 = pygame.Rect(200, 660, 140, 32)
color_active2 = pygame.Color('lightskyblue3')
color_passive2 = pygame.Color('chartreuse4')
color2 = color_passive2
active2 = False
#----------- input box3
user_text3 = str(lab_size[0])
input_rect3 = pygame.Rect(000, 660, 140, 32)
color_active3 = pygame.Color('lightskyblue3')
color_passive3 = pygame.Color('chartreuse4')
color3 = color_passive3
active3 = False


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
    pygame.draw.rect(screen, (200, 200, 200), [0, 615, 600, 200])
    text3 = font.render(
        f"시간당 부딪힌 횟수: {round(crashed_times / round((time.time() - start_t) + 0.5))}",
        True,
        BLACK)
    screen.blit(text3, (10, 700))

    text2 = font.render(
        f"시간: {round((time.time() - start_t) + 0.5)}초",
        True,
        BLACK)
    screen.blit(text2, (10, 750))


def show_input_box():#T
    if active:
        color = color_active
    else:
        color = color_passive

    text = font.render("온도(K)", True, BLACK)
    screen.blit(text, (400, 620))

    pygame.draw.rect(screen, color, input_rect)

    text_surface = font.render(user_text, True, (255, 255, 255))

    # render at position stated in arguments
    screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

    # set width of textfield so that text cannot get
    # outside of user's text input
    input_rect.w = max(100, text_surface.get_width() + 10)

def show_input_box2(): #n
    if active2:
        color2 = color_active2
    else:
        color2 = color_passive2

    text = font.render("입자수", True, BLACK)
    screen.blit(text, (200, 620))

    pygame.draw.rect(screen, color2, input_rect2)

    text_surface2 = font.render(user_text2, True, (255, 255, 255))

    # render at position stated in arguments
    screen.blit(text_surface2, (input_rect2.x + 5, input_rect2.y + 5))

    # set width of textfield so that text cannot get
    # outside of user's text input
    input_rect2.w = max(100, text_surface2.get_width() + 10)

def show_input_box3(): #V
    if active3:
        color3 = color_active3
    else:
        color3 = color_passive3

    text = font.render("부피", True, BLACK)
    screen.blit(text, (000, 620))

    pygame.draw.rect(screen, color3, input_rect3)

    text_surface3 = font.render(user_text3, True, (255, 255, 255))

    # render at position stated in arguments
    screen.blit(text_surface3, (input_rect3.x + 5, input_rect3.y + 5))

    # set width of textfield so that text cannot get
    # outside of user's text input
    input_rect3.w = max(100, text_surface3.get_width() + 10)


def move_particles(v):
    for i in range(len(particles)):
        angle_rad = math.radians(particles[i][2])
        particles[i][0] += v * math.sin(angle_rad)
        particles[i][1] += v * math.cos(angle_rad)

        if is_crash(particles[i][0], particles[i][1]):
            particles[i][2] += 90
        if is_out(particles[i][0], particles[i][1]):
            particles[i][0] = random.randint(1, lab_size[0] - 1)
            particles[i][1] = random.randint(1, lab_size[1] - 1)


def is_crash(y, x):
    global crashed_times
    result = False
    if y >= lab_size[0]:  # 아래쪽 부딪힘
        result = True
    if y <= 0:  # 위쪽 부딪힘
        result = True
    if x >= lab_size[1]:  # 오른쪽 부딪힘
        result = True
    if x <= 0:  # 왼쪽 부딪힘
        result = True

    if result:
        crashed_times += 1
    return result


def is_out(y, x):
    result = False
    if y >= lab_size[0] + v:  # 아래쪽 부딪힘
        result = True
    if y < 0 - v:  # 위쪽 부딪힘
        result = True
    if x > lab_size[1] + v:  # 오른쪽 부딪힘
        result = True
    if x < 0 - v:  # 왼쪽 부딪힘
        result = True
    return result


start_t = time.time()

while True:
    clock = pygame.time.Clock()
    clock.tick(FPS)

    v = 10 * (T * 1.38 * pow(10, -3) * 2)

    move_particles(v)
    draw_screen()
    show_data()
    show_input_box3()
    show_input_box2()
    show_input_box()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos):
                active = True
                user_text = ""
            else:
                active = False

            if input_rect2.collidepoint(event.pos):
                active2 = True
                user_text2 = ""
            else:
                active2 = False

            if input_rect3.collidepoint(event.pos):
                active3 = True
                user_text3 = ""
            else:
                active3 = False

        if event.type == pygame.KEYDOWN and active:

            # Check for backspace
            if event.key == pygame.K_BACKSPACE:

                # get text input from 0 to -1 i.e. end.
                user_text = user_text[:-1]

            # Unicode standard is used for string
            # formation
            elif event.key == pygame.K_RETURN:
                active = False
                init(n,int(user_text),lab_size[0])
                crashed_times = 0
                start_t = time.time()
            else:
                user_text += event.unicode
        if event.type == pygame.KEYDOWN and active2: #n

            # Check for backspace
            if event.key == pygame.K_BACKSPACE:

                # get text input from 0 to -1 i.e. end.
                user_text2 = user_text2[:-1]

            # Unicode standard is used for string
            # formation
            elif event.key == pygame.K_RETURN:
                active2 = False
                init(int(user_text2),T,lab_size[0])
                crashed_times = 0
                start_t = time.time()
            else:
                user_text2 += event.unicode

        if event.type == pygame.KEYDOWN and active3: #V

            # Check for backspace
            if event.key == pygame.K_BACKSPACE:

                # get text input from 0 to -1 i.e. end.
                user_text3 = user_text3[:-1]

            # Unicode standard is used for string
            # formation
            elif event.key == pygame.K_RETURN:
                active3 = False
                init(n,T,int(user_text3))
                crashed_times = 0
                start_t = time.time()
            else:
                user_text3 += event.unicode


