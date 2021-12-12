import pygame as pg
from pygame.locals import *
import random


class App:

    def __init__(self):
        pg.init()
        self.clock = pg.time.Clock()
        self.WIDTH = 1500
        self.HEIGHT = 1000
        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        self.fruit = None
        self.snake = None

    def run(self):

        if not self.fruit:
            self.fruit = Fruit()
        if not self.snake:
            self.snake = Snake()

        while True:
            if not self.fruit:
                self.fruit = Fruit()

            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                if event.type == KEYDOWN:
                    if event.key == K_s and not self.snake.destination == "UP":
                        self.snake.destination = "DOWN"
                    elif event.key == K_w and not self.snake.destination == "DOWN":
                        self.snake.destination = "UP"
                    elif event.key == K_d and not self.snake.destination == "LEFT":
                        self.snake.destination = "RIGHT"
                    elif event.key == K_a and not self.snake.destination == "RIGHT":
                        self.snake.destination = "LEFT"

            if self.snake.rect.colliderect(self.fruit.rect):
                self.fruit = None

            self.screen.fill((0, 0, 0))
            if self.fruit:
                self.fruit.draw()
            self.snake.draw()
            pg.display.update()
            self.clock.tick(60)


class Fruit:

    def __init__(self):
        self.coord = random.randint(0, app.HEIGHT - 25)
        self.rect = pg.Rect((self.coord, self.coord), (25, 25))
        self.surf = pg.Surface((25, 25))
        self.surf.fill((0, 100, 0))

    def draw(self):
        app.screen.blit(self.surf, self.rect)


class Snake:

    def __init__(self):
        self.speed = 5
        self.coord_x = random.randint(0, app.WIDTH - 25)
        self.coord_y = random.randint(0, app.HEIGHT - 25)
        self.rect = pg.Rect((self.coord_x, self.coord_y), (25, 25))
        self.surf = pg.Surface((25, 25))
        self.surf.fill((0, 200, 200))
        self.destination = "RIGHT"
        self.snake = [(self.rect, self.surf)]

    def draw(self):

        if self.destination == "RIGHT":
            if self.rect[0] <= app.WIDTH + 25:
                self.rect[0] += self.speed
            else:
                self.rect[0] = -25
        elif self.destination == "DOWN":
            if self.rect[1] <= app.HEIGHT + 25:
                self.rect[1] += self.speed
            else:
                self.rect[1] = -25
        elif self.destination == "UP":
            if self.rect[1] >= 0:
                self.rect[1] -= self.speed
            else:
                self.rect[1] = app.HEIGHT
        elif self.destination == "LEFT":
            if self.rect[0] >= 0:
                self.rect[0] -= self.speed
            else:
                self.rect[0] = app.WIDTH
        app.screen.blit(self.surf, self.rect)


app = App()
app.run()