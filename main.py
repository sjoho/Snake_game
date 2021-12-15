import pygame as pg
from pygame.locals import *
import random


class App:

    def __init__(self):
        pg.init()
        self.clock = pg.time.Clock()
        self.WIDTH = 1200
        self.HEIGHT = 800
        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        self.fruit = None
        self.snake = None
        self.background = pg.image.load("3.jpg")
        self.pickup = pg.mixer.Sound("audio/24f110d27ad0929.ogg")

    def run(self):

        if not self.fruit:
            self.fruit = Fruit()
        if not self.snake:
            self.snake = Snake()

        while True:
            pg.display.set_caption(str(self.clock.get_fps()))
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
                self.pickup.play()
                if self.snake.destination == "RIGHT":
                    self.rect = pg.Rect((self.snake.snake[-1][0][0] - 30, self.snake.snake[-1][0][1]), (25, 25))
                elif self.snake.destination == "LEFT":
                    self.rect = pg.Rect((self.snake.snake[-1][0][0] + 30, self.snake.snake[-1][0][1]), (25, 25))
                elif self.snake.destination == "UP":
                    self.rect = pg.Rect((self.snake.snake[-1][0][0], self.snake.snake[-1][0][1] + 30), (25, 25))
                elif self.snake.destination == "DOWN":
                    self.rect = pg.Rect((self.snake.snake[-1][0][0] - 30, self.snake.snake[-1][0][1]), (25, 25))
                self.surf = pg.Surface((25, 25))
                self.surf.fill((50, 50, 50))
                self.snake.snake.append((self.rect, self.surf))


            self.screen.blit(self.background, (0, 0))
            if self.fruit:
                self.fruit.draw()
            self.snake.draw()
            pg.display.update()
            self.clock.tick(30)


class Fruit:

    def __init__(self):
        self.coord = random.randint(0, app.HEIGHT - 25)
        self.rect = pg.Rect((self.coord, self.coord), (25, 25))
        self.surf = pg.Surface((25, 25))
        self.surf.fill((255, 0, 0))

    def draw(self):
        app.screen.blit(self.surf, self.rect)


class Snake:

    def __init__(self):
        self.speed = 15
        self.coord_x = random.randint(0, app.WIDTH - 25)
        self.coord_y = random.randint(0, app.HEIGHT - 25)
        self.rect = pg.Rect((self.coord_x, self.coord_y), (25, 25))
        self.surf = pg.Surface((25, 25))
        self.surf.fill((0, 0, 0))
        self.destination = "RIGHT"
        self.snake = [(self.rect, self.surf)]
        print(self.rect.center)

    def draw(self):

        self.temp = (self.rect[0], self.rect[1])

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

        if len(self.snake) > 1:
            for i in range(0, len(self.snake) - 1):
                self.temp2 = self.snake[i+1][0][0], self.snake[i+1][0][1]
                self.snake[i+1][0][0] = self.temp[0]
                self.snake[i+1][0][1] = self.temp[1]
                self.temp = self.temp2

        for j in self.snake:
            app.screen.blit(j[1], j[0])


app = App()
app.run()
