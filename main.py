import pygame
import os
import insect


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


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, group):
        super().__init__(group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.image = self.image.convert_alpha()


class Frog(AnimatedSprite):
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


def main():
    pygame.init()
    size = width, height = 1000, 600
    screen = pygame.display.set_mode(size)

    all_sprites = pygame.sprite.Group()
    horizontal_borders = pygame.sprite.Group()
    vertical_borders = pygame.sprite.Group()

    Border(5, 5, width - 5, 5, all_sprites,vertical_borders)
    Border(5, height - 5, width - 5, height - 5, all_sprites, vertical_borders)
    Border(5, 5, 5, height - 5, all_sprites, horizontal_borders)
    Border(width - 5, 5, width - 5, height - 5, all_sprites, horizontal_borders)

    swamp_image = load_image("swamp.png")
    swamp = pygame.sprite.Sprite(all_sprites)
    swamp.image = swamp_image
    swamp.rect = swamp.image.get_rect()

    frog_sheet = pygame.image.load("data/frog_idle.png").convert_alpha()
    frog = Frog(frog_sheet, 8, 1, 100, 100, all_sprites)
    frog.rect.x = 400
    frog.rect.y = 400

    beetle_sheet = pygame.image.load("data/beetle_move_right.png").convert_alpha()
    beetle_sheet2 = pygame.image.load("data/beetle_move_right.png").convert_alpha()
    beetle = insect.Insect(beetle_sheet, 4, 1, 100, 100, all_sprites)

    fps = 8
    clock = pygame.time.Clock()

    running = True
    while running:
        all_sprites.update()
        if pygame.sprite.spritecollideany(beetle, horizontal_borders):
            beetle.vx = -beetle.vx
        elif pygame.sprite.spritecollideany(beetle, vertical_borders):
            beetle.vy = -beetle.vy
        beetle.move()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        all_sprites.draw(screen)
        clock.tick(fps)
        pygame.display.flip()

    while pygame.event.wait().type != pygame.QUIT:
        pass

    pygame.quit()


if __name__ == '__main__':
    main()
