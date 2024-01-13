import pygame
import main


class Insect(main.AnimatedSprite):
    def __init__(self, sheet, columns, rows, x, y, group):
        super().__init__(sheet, columns, rows, x, y, group)

