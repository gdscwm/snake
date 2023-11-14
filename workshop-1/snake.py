import random
import pygame
import tkinter as tk
from tkinter import messagebox

WIDTH = 500
ROWS = 20

SURFACE_COL = (0, 0, 0)
GRID_COL = (255, 255, 255)
SNAKE_COL = (255, 0, 255)
SNACK_COL = (0, 255, 0)


class Cube():
    def __init__(self, start, dirx=1, diry=0, color=SNAKE_COL):
        self.pos = start
        self.dirx = dirx
        self.diry = diry
        self.color = color

    def move(self, dirx, diry):
        self.dirx = dirx
        self.diry = diry
        self.pos = (self.pos[0] + self.dirx, self.pos[1] + self.diry)

    def draw(self, surface, head=False):
        dis = WIDTH // ROWS
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 1, dis - 2))


class Snake():

    def __init__(self):
        pass

    def move(self):
        pass

    def reset(self):
        pass

    def add_cube(self):
        pass

    def draw(self):
        pass


def random_snack():
    pass


def message_box():
    pass


def redraw_surface(surface):
    surface.fill(SURFACE_COL)
    draw_grid(surface)
    pygame.display.update()


def draw_grid(surface):
    square_size = WIDTH // ROWS

    x = 0
    y = 0
    for _ in range(ROWS):
        x = x + square_size
        y = y + square_size

        pygame.draw.line(surface, GRID_COL, (x, 0), (x, WIDTH))  # vertical lines
        pygame.draw.line(surface, GRID_COL, (0, y), (WIDTH, y))  # horizontal lines


def main():
    surface = pygame.display.set_mode(size=(WIDTH, WIDTH))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        redraw_surface(surface)


main()
