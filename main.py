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


def main():
    pygame.init()
    size = width, height = 1000, 600
    screen = pygame.display.set_mode(size)

    all_sprites = pygame.sprite.Group()

    swamp_image = load_image("swamp.png")
    swamp = pygame.sprite.Sprite(all_sprites)
    swamp.image = swamp_image
    swamp.rect = swamp.image.get_rect()

    frog_sheet = pygame.image.load("data/frog_idle.png").convert_alpha()
    frog = Frog(frog_sheet, 8, 1, 100, 100, all_sprites)
    frog.rect.x = 400
    frog.rect.y = 400

    beetle_sheet = pygame.image.load("data/beetle_move_right.png").convert_alpha()
    beetle = insect.Insect(beetle_sheet, 4, 1, 100, 100, all_sprites)

    fps = 8
    clock = pygame.time.Clock()

    running = True
    while running:
        all_sprites.update()
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
