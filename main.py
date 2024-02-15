import pygame
import sys
import os
import insect
import animated_sprite
import starter_screen
import final_screen
import random


def load_image(name, color_key=None):   # функция для загрузки картинки
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Frog(animated_sprite.AnimatedSprite):   # класс лягушки
    def __init__(self, sheet, columns, rows, x, y, group):
        super().__init__(sheet, columns, rows, x, y, group)


class Border(pygame.sprite.Sprite):     # барьер для игры
    def __init__(self, x1, y1, x2, y2, all_sprites, group):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(group)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(group)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class HealthBar:       # шкала здоровья
    def __init__(self, x, y, w, h, max_hp):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp

    def draw(self, surface):
        ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, "red", (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surface, "green", (self.x, self.y, self.w * ratio, self.h))


class KillCount:    # счетчик убийств букашек и его отображение
    def __init__(self, kills_left, level, background, image):
        self.text = [f"Уровень {level}", f"Осталось букашек: {kills_left}"]
        self.font = pygame.font.Font(None, 30)
        self.text_coord = 475
        self.kills_left = kills_left
        self.image = image
        self.background = background
        self.level = level

        for line in self.text:
            self.string_rendered = self.font.render(line, 1, pygame.Color('white'))
            self.intro_rect = self.string_rendered.get_rect()
            self.text_coord += 10
            self.intro_rect.top = self.text_coord
            self.intro_rect.x = 650
            self.text_coord += self.intro_rect.height
            self.background.blit(self.string_rendered, self.intro_rect)

    def killed(self):   # обновление текста после убийства
        self.kills_left -= 1
        self.background.blit(self.image, (0, 0))
        self.text = [f"Уровень {self.level}", f"Осталось букашек: {self.kills_left}"]
        self.text_coord = 475
        for line in self.text:
            self.string_rendered = self.font.render(line, 1, pygame.Color('white'))
            self.intro_rect = self.string_rendered.get_rect()
            self.text_coord += 10
            self.intro_rect.top = self.text_coord
            self.intro_rect.x = 650
            self.text_coord += self.intro_rect.height
            self.background.blit(self.string_rendered, self.intro_rect)
        print(self.kills_left)
        print(self.text)


def main(level):    # основная функция игры
    pygame.init()
    size = width, height = 1000, 600
    screen = pygame.display.set_mode(size)
    kills_left = 0

    all_sprites = pygame.sprite.Group()
    all_insects = pygame.sprite.Group()
    horizontal_borders = pygame.sprite.Group()
    vertical_borders = pygame.sprite.Group()

    swamp_image = load_image("swamp.png")   # задний фон
    swamp_image2 = load_image("swamp.png")  # чтобы перекрыть надпись
    swamp = pygame.sprite.Sprite(all_sprites)
    swamp.image = swamp_image
    swamp.rect = swamp.image.get_rect()

    Border(5, 5, width - 5, 5, all_sprites, vertical_borders)   # все границы экрана
    Border(5, height - 5, width - 5, height - 5, all_sprites, vertical_borders)
    Border(5, 5, 5, height - 5, all_sprites, horizontal_borders)
    Border(width - 5, 5, width - 5, height - 5, all_sprites, horizontal_borders)

    frog_sheet = pygame.image.load("data/frog_idle.png").convert_alpha()
    frog = Frog(frog_sheet, 8, 1, 100, 100, all_sprites)
    frog.rect.x = 400
    frog.rect.y = 400

    beetle_sheet = pygame.image.load("data/beetle_move_right.png").convert_alpha()
    beetle = insect.Insect(beetle_sheet, 4, 1, 100, 100, all_insects)

    if level == 1:
        kills_left = 10
    elif level == 2:
        kills_left = 15
    elif level == 3:
        kills_left = 20

    health_bar = HealthBar(1, 550, 300, 40, 100)
    health_bar.hp = 100
    kills_count = KillCount(kills_left, level, swamp_image, swamp_image2)
    fps = 8
    clock = pygame.time.Clock()
    spawn_count = 0
    running = True
    while running:
        all_sprites.update()
        all_insects.update()
        spawn_count += 1
        if level == 1:
            health_bar.hp -= 1
        elif level == 2:
            health_bar.hp -= 1
            for beetle in all_insects:
                beetle.vx = 30
        elif level == 3:
            health_bar.hp -= 2
            for beetle in all_insects:
                beetle.vx = 40
        if spawn_count == 12:
            beetle = insect.Insect(beetle_sheet, 4, 1, random.randint(10, 990), 100, all_insects)
            spawn_count = 0

        for beetle in all_insects:
            beetle.move()
            if pygame.sprite.spritecollideany(beetle, horizontal_borders):  # букашка меняет направление движения при
                beetle.vx = -beetle.vx                                      # касании границ экрана
            elif pygame.sprite.spritecollideany(beetle, vertical_borders):
                beetle.vy = -beetle.vy
        if health_bar.hp <= 0:  # закончилось хп? проиграл
            running = False
            final_screen.final_screen(win=False)
        if kills_count.kills_left <= 0:
            running = False
            if level != 3:  # запуск следующего уровня при победе
                main(level + 1)
            elif level == 3:
                final_screen.final_screen(win=True)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:  # убийство букашки при нажатии
                pos = pygame.mouse.get_pos()
                clicked_sprites = [s for s in all_insects if s.rect.collidepoint(pos)]
                for beetle in all_insects:
                    if beetle in clicked_sprites:
                        beetle.kill()
                        if health_bar.hp <= 85:
                            health_bar.hp += 15
                        else:
                            health_bar.hp = 100
                        kills_count.killed()

            if event.type == pygame.QUIT:
                running = False
                sys.exit()

        all_sprites.draw(screen)
        all_insects.draw(screen)
        health_bar.draw(screen)
        clock.tick(fps)
        pygame.display.flip()

    while pygame.event.wait().type != pygame.QUIT:
        pass


pygame.quit()

if __name__ == '__main__':
    starter_screen.start_screen()
