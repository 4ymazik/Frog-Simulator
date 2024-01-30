import pygame
import main
import animated_sprite


class Insect(animated_sprite.AnimatedSprite):
    def __init__(self, sheet, columns, rows, x, y, group):
        super().__init__(sheet, columns, rows, x, y, group)
        self.vx = 20
        self.vy = 0

    def move(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if self.rect[0] > 400 and self.rect[1] < 130:
            self.vx = 10
            self.vy = 10
        elif self.rect[0] > 550 and 150 < self.rect[1] < 200:
            self.vx = 0
            self.vy = 10
        elif self.rect[1] > 200:
            self.vx = -10
            self.vy = -8
        print(self.rect)




