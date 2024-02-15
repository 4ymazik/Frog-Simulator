import pygame
import main
import sys


def start_screen():     # стартовое окно
    pygame.init()
    size = 1000, 600
    screen = pygame.display.set_mode(size)
    intro_text = ["Симулятор Лягушки", "Чтобы начать игру нажмите любую клавишу"]

    color = (0, 30, 0)
    screen.fill(color)
    font = pygame.font.Font(None, 30)
    text_coord = 200
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 300
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    running = True
    fps = 8
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                main.main(1)
        pygame.display.flip()
        clock.tick(fps)
