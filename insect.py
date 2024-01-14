import pygame
import main


class Insect(main.AnimatedSprite):
    def __init__(self, sheet, columns, rows, x, y, group):
        super().__init__(sheet, columns, rows, x, y, group)
        self.vx = 20
        self.vy = 0

    def move(self):
        self.rect = self.rect.move(self.vx, self.vy)



