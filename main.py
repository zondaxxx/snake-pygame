import pygame
import time
import random
import json

pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
bright_red = (213, 23, 80)
bright_green = (0, 15, 0)

dis_width = 800
dis_height = 600

dis = pygame.display.set_mode((dis_width, dis_height), pygame.RESIZABLE)
pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()
snake_block = 10
snake_speed = 30

font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)

def load_language(lang):
    with open(f'{lang}.txt', 'r', encoding='utf-8') as f:  # Укажите кодировку здесь
        return json.load(f)


language = load_language('ru')  # Загрузите язык по умолчанию

def draw_button(text, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(dis, ac, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(dis, ic, (x, y, w, h))

    small_text = pygame.font.SysFont(None, 20)
    text_surf, text_rect = text_objects(text, small_text)
    text_rect.center = ((x + (w / 2)), (y + (h / 2)))
    dis.blit(text_surf, text_rect)

def text_objects(text, font):
    text_surface = font.render(text, True, black)
    return text_surface, text_surface.get_rect()

def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        dis.fill(white)
        large_text = pygame.font.SysFont(None, 115)
        TextSurf, TextRect = text_objects(language['game'], large_text)
        TextRect.center = ((dis_width / 2), (dis_height / 2))
        dis.blit(TextSurf, TextRect)

        draw_button(language['go'], 150, 450, 100, 50, green, bright_green, gameLoop)
        draw_button(language['quit'], 550, 450, 100, 50, red, bright_red, quit)

        pygame.display.update()
        clock.tick(15)

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, white, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 2, dis_height / 2])

def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        dis.fill(white)
        large_text = pygame.font.SysFont(None, 115)
        TextSurf, TextRect = text_objects(language['paused'], large_text)
        TextRect.center = ((dis_width / 2), (dis_height / 2))
        dis.blit(TextSurf, TextRect)

        draw_button(language['continue'], 150, 450, 100, 50, green, bright_green, gameLoop)
        draw_button(language['quit'], 550, 450, 100, 50, red, bright_red, quit)

        pygame.display.update()
        clock.tick(15)

def game_over_menu():
    over = True
    while over:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    over = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        dis.fill(white)
        large_text = pygame.font.SysFont(None, 115)
        TextSurf, TextRect = text_objects(language['game_over'], large_text)
        TextRect.center = ((dis_width / 2), (dis_height / 2))
        dis.blit(TextSurf, TextRect)

        draw_button(language['play_again'], 150, 450, 100, 50, green, bright_green, gameLoop)
        draw_button(language['quit'], 550, 450, 100, 50, red, bright_red, quit)

        pygame.display.update()
        clock.tick(15)

def gameLoop():
    global dis_width, dis_height, dis

    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    while not game_over:

        while game_close == True:
            game_over_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                game_close = False
            if event.type == pygame.VIDEORESIZE:
                dis_width = event.w
                dis_height = event.h
                dis = pygame.display.set_mode((dis_width, dis_height), pygame.RESIZABLE)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause()
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

game_intro()
gameLoop()



