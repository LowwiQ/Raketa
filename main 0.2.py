import pygame
from copy import deepcopy
import os
from random import choice, randrange

# Game Initialization
pygame.init()

# Center the Game Application
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Game Resolution
screen_width = 520
screen_height = 700
screen=pygame.display.set_mode((screen_width, screen_height))

#Вывод текста в меню
def text_format(message, textFont, textSize, textColor):
    newFont=pygame.font.Font(textFont, textSize)
    newText=newFont.render(message, 0, textColor)
    return newText
###

#Цвета меню
white = (255, 255, 255)
black = (0, 0, 0)
gray = (50, 50, 50)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (180, 180, 0)
yellow = (255, 255, 0)
###

#Шрифт
font = "Retro.ttf"
###

# Game Framerate
clock = pygame.time.Clock()
fps = 60
###

# Main Menu
def main_menu():

    menu=True
    selected="start"

    while menu:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    selected="start"
                elif event.key==pygame.K_DOWN:
                    selected="quit"
                if event.key==pygame.K_RETURN:
                    if selected=="start":
                        menu = False
                    if selected=="quit":
                        pygame.quit()
                        quit()

        # Main Menu UI
        screen.fill(blue)
        title=text_format("TETRIS", font, 70, yellow)
        if selected=="start":
            text_start=text_format("GO", font, 75, white)
        else:
            text_start = text_format("START", font, 75, black)
        if selected=="quit":
            text_quit=text_format("QUIT", font, 75, white)
        else:
            text_quit = text_format("QUIT", font, 75, black)

        title_rect=title.get_rect()
        start_rect=text_start.get_rect()
        quit_rect=text_quit.get_rect()

        # Main Menu Text
        screen.blit(title, (screen_width/2 - (title_rect[2]/2), 80))
        screen.blit(text_start, (screen_width/2 - (start_rect[2]/2), 300))
        screen.blit(text_quit, (screen_width/2 - (quit_rect[2]/2), 360))
        pygame.display.update()
        clock.tick(fps)
        pygame.display.set_caption("Python - Pygame Simple Main Menu Selection")
###

#Вывод меню
main_menu()
###

#задаем параметры игры
wight, hight = 10, 20
title_size = 35
screen_size = 520, 700
score = 0
pygame.init()
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
###

#для рисоввания сетки
grid = [pygame.Rect(x * title_size, y * title_size, title_size, title_size)
        for x in range(wight) for y in range(hight)]
###

#координаты для рисования фигур
figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]
###

#само рисование
figures = [[pygame.Rect(x + wight // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
figure_rect = pygame.Rect(0, 0, title_size - 2, title_size - 2)
map = [[0 for i in range(wight)] for j in range(hight)]
###

#параметры падения
anim_count, anim_speed, anim_limit = 0, 60, 2000
###

#генерация цвета для следующих фигур
get_color = lambda : (randrange(30, 256), randrange(30, 256), randrange(30, 256))
###

#копии фигур для выявления следующей фигуры и корректировки выхода за границу
figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
color, next_color = get_color(), get_color()
###

#ограничение перемещения фигуры по карте
def check_positions():
    if figure[i].x < 0 or figure[i].x > wight - 1:
        return False
    elif figure[i].y > hight - 1 or map[figure[i].y][figure[i].x]:
        return False
    return True
###

#вывод счета
def draw(screen):
    font = pygame.font.Font(None, 50)
    text = font.render("score:" + str(score), True, (100, 255, 100))
    text_x = 365
    text_y = 20
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10, text_w + 20, text_h + 20), 1)
###

#аудио
pygame.mixer.music.load("muz.mp3")
move_muz =  pygame.mixer.Sound('muzd.mp3')
down_muz =  pygame.mixer.Sound('muzdown.mp3')
rotate_muz =  pygame.mixer.Sound('muzrotate.mp3')
line_muz =  pygame.mixer.Sound('muzline.mp3')
upal_muz =  pygame.mixer.Sound('muzupal.mp3')
over_muz =  pygame.mixer.Sound('gameover.mp3')
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)
###

#основной игровой цикл
while True:
    screen.fill((0, 0, 0))
    dx, dy, rotate = 0, 0, False

#управление
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_muz.play()
                dx = -1
            elif event.key == pygame.K_RIGHT:
                move_muz.play()

                dx = 1
            elif event.key == pygame.K_DOWN:
                move_muz.play()
                dy = 1
            elif event.key == pygame.K_SPACE:
                down_muz.play()
                anim_limit = 100

            elif event.key == pygame.K_UP:
                rotate_muz.play()
                rotate = True
###

    #движение по x
    figure_old = deepcopy(figure)
    for i in range(4):
        figure[i].x += dx
        figure[i].y += dy
        if not check_positions():
            figure = deepcopy(figure_old)
            break
    ###

    #движение по y
    anim_count += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if not check_positions():
                for i in range(4):
                    map[figure_old[i].y][figure_old[i].x] = color
                figure, color = next_figure, next_color
                next_figure, next_color = deepcopy(choice(figures)), get_color()
                anim_limit = 2000
                break
    ###

    #поворот
    center = figure[0]
    figure_old = deepcopy(figure)
    if rotate:
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not check_positions():
                figure = deepcopy(figure_old)
                break
    ###

    #удаление сложившейся линии
    line = hight - 1
    for row in range(hight - 1, -1, -1):
        count = 0
        for i in range(wight):
            if map[row][i]:
                count += 1
            map[line][i] = map[row][i]
        if count < wight:
            line -= 1
        else:
            anim_speed += 3

            line_muz.play()
            score +=1
    ###

    #рисование сетки
    for i_rect in grid:
        pygame.draw.rect(screen, (40, 40, 0), i_rect, 1)
    ###

    #рисование падающей фигуры
    for i in range(4):
        figure_rect.x = figure[i].x * title_size
        figure_rect.y = figure[i].y * title_size
        pygame.draw.rect(screen, color, figure_rect)
    ###

    #рисование упавших фигур
    for y, raw in enumerate(map):
        for x, col in enumerate(raw):
            if col:
                figure_rect.x, figure_rect.y = x * title_size, y * title_size
                pygame.draw.rect(screen, col, figure_rect)
    ####

    #рисование следующей фигуры
    pygame.draw.rect(screen, (180, 180, 0), (350, 0, 250, 700))
    for i in range(4):
        figure_rect.x = next_figure[i].x * title_size + 255
        figure_rect.y = next_figure[i].y * title_size + 185
        pygame.draw.rect(screen, next_color, figure_rect)
    ###

    ###вывод счета
    draw(screen)
    ###

    #поражение
    for i in range(wight):
        if map[0][i]:
            map = [[0 for i in range(wight)] for i in range(hight)]
            anim_count, anim_speed, anim_limit = 0, 60, 2000
            score = 0
            for i_rect in grid:
                pygame.draw.rect(screen, get_color(), i_rect)
                pygame.display.flip()
            over_muz.play()

            main_menu()
    ###

    pygame.display.flip()
    clock.tick(fps)
###