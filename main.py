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

screen_size = [600, 600]

screen = pygame.display.set_mode((screen_size[0], screen_size[1] + 100))
pygame.font.init()
font = pygame.font.SysFont(None, 30)

n = 100
T = 273
particles = np.zeros((n, 3))  # y, x, angle
# print(particles[1])
for i in range(len(particles)):
    particles[i][0] = random.randint(50, 550)
    particles[i][1] = random.randint(50, 550)
    particles[i][2] = random.randint(0, 360)

# print(particles)

crashed_times = 0
# ---------------- input box
user_text = '273'
input_rect = pygame.Rect(400, 660, 140, 32)
color_active = pygame.Color('lightskyblue3')
color_passive = pygame.Color('chartreuse4')
color = color_passive
active = False


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
    text = font.render(
        f"n : {crashed_times}, P : {round(crashed_times / round((time.time() - start_t) + 0.5))}, t : {(time.time() - start_t) + 0.5}",
        True,
        BLACK)
    screen.blit(text, (10, 620))


def show_input_box():
    global T
    if active:
        color = color_active
    else:
        color = color_passive

    text = font.render("Temperture", True, BLACK)
    screen.blit(text, (400, 620))

    pygame.draw.rect(screen, color, input_rect)

    text_surface = font.render(user_text, True, (255, 255, 255))

    # render at position stated in arguments
    screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

    # set width of textfield so that text cannot get
    # outside of user's text input
    input_rect.w = max(100, text_surface.get_width() + 10)


def move_particles(v):
    for i in range(len(particles)):
        angle_rad = math.radians(particles[i][2])
        particles[i][0] += v * math.sin(angle_rad)
        particles[i][1] += v * math.cos(angle_rad)

        if is_crash(particles[i][0], particles[i][1]):
            particles[i][2] += 90
        if is_out(particles[i][0], particles[i][1]):
            particles[i][0] = random.randint(50, screen_size[0] - 50)
            particles[i][1] = random.randint(50, screen_size[1] - 50)


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


def is_out(y, x):
    middle_x = screen_size[0] / 2
    middle_y = screen_size[1] / 2
    # print(math.sqrt(2) * screen_size[0])
    # print(round(pow(pow(middle_x - x, 2) + pow(middle_y - y, 2), 1 / 2)))
    if pow(pow(middle_x - x, 2) + pow(middle_y - y, 2), 1 / 2) > math.sqrt(2) * screen_size[0] - 1:
        print("바깥으로 나감")
        return True
    else:
        return False


start_t = time.time()

while True:
    clock = pygame.time.Clock()
    clock.tick(FPS)

    move_particles(10 * (T * 1.38 * pow(10, -3) * 2))
    draw_screen()
    show_data()
    show_input_box()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos):
                active = True
            else:
                active = False
        if event.type == pygame.KEYDOWN and active:

            # Check for backspace
            if event.key == pygame.K_BACKSPACE:

                # get text input from 0 to -1 i.e. end.
                user_text = user_text[:-1]

            # Unicode standard is used for string
            # formation
            elif event.key == pygame.K_RETURN:
                active = False
                T = int(user_text)
                crashed_times = 0
                start_t = time.time()
            else:
                user_text += event.unicode
