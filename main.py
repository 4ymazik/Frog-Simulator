import pygame
import os
import insect
import animated_sprite


def load_image(name, color_key=None):
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


def start_screen():
    pygame.init()
    size = width, height = 1000, 600
    screen = pygame.display.set_mode(size)
    intro_text = ["ЗАСТАВКА"]

    color = (0, 30, 0)
    screen.fill(color)
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    running = True
    fps = 8
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                main()
        pygame.display.flip()
        clock.tick(fps)

class Frog(animated_sprite.AnimatedSprite):
    def __init__(self, sheet, columns, rows, x, y, group):
        super().__init__(sheet, columns, rows, x, y, group)


class Border(pygame.sprite.Sprite):
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


class HealthBar:
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


def main():
    pygame.init()
    size = width, height = 1000, 600
    screen = pygame.display.set_mode(size)

    all_sprites = pygame.sprite.Group()
    horizontal_borders = pygame.sprite.Group()
    vertical_borders = pygame.sprite.Group()

    swamp_image = load_image("swamp.png")
    swamp = pygame.sprite.Sprite(all_sprites)
    swamp.image = swamp_image
    swamp.rect = swamp.image.get_rect()

    Border(5, 5, width - 5, 5, all_sprites,vertical_borders)
    Border(5, height - 5, width - 5, height - 5, all_sprites, vertical_borders)
    Border(5, 5, 5, height - 5, all_sprites, horizontal_borders)
    Border(width - 5, 5, width - 5, height - 5, all_sprites, horizontal_borders)

    frog_sheet = pygame.image.load("data/frog_idle.png").convert_alpha()
    frog_sheet2 = pygame.image.load("data/frog_idle2.png").convert_alpha()
    frog = Frog(frog_sheet,8, 1, 100, 100, all_sprites)
    frog.rect.x = 400
    frog.rect.y = 400

    beetle_sheet = pygame.image.load("data/beetle_move_right.png").convert_alpha()
    beetle_sheet2 = pygame.image.load("data/beetle_move_left.png").convert_alpha()
    beetle = insect.Insect(beetle_sheet, 4, 1, 100, 100, all_sprites)

    health_bar = HealthBar(250, 200, 300, 40, 100)
    health_bar.hp = 100
    fps = 8
    clock = pygame.time.Clock()

    running = True
    while running:
        all_sprites.update()
        health_bar.draw(screen)
        health_bar.hp -= 1

        if pygame.sprite.spritecollideany(beetle, horizontal_borders):
            beetle.vx = -beetle.vx
        elif pygame.sprite.spritecollideany(beetle, vertical_borders):
            beetle.vy = -beetle.vy
        beetle.move()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                clicked_sprites = [s for s in all_sprites if s.rect.collidepoint(pos)]
                if beetle in clicked_sprites:
                    beetle.kill()
                    if health_bar.hp <= 75:
                        health_bar.hp += 15
                    else:
                        health_bar.hp = 100
            if event.type == pygame.QUIT:
                running = False

        all_sprites.draw(screen)
        clock.tick(fps)
        pygame.display.flip()

    while pygame.event.wait().type != pygame.QUIT:
        pass

    pygame.quit()


if __name__ == '__main__':
    start_screen()
