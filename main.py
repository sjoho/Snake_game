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
        self.game = True
        self.round = False
        self.font = pg.font.Font(None, 64)
        self.walls = None
        pg.display.set_caption("SUPER SNAKE")
        pg.mixer.music.load("audio/48bb90af8e1e401.mp3")


    def run(self):

        if not self.fruit:
            self.fruit = Fruit()
        if not self.snake:
            self.snake = Snake()

        while self.game:

            self.screen.blit(self.background, (0, 0))

            self.surf = pg.Surface((350, 100))
            self.surf.fill((0, 191, 240))
            self.text = self.font.render("ИГРАТЬ", True, (155, 0, 0))
            self.surf.blit(self.text, ((350 - self.font.size("ИГРАТЬ")[0]) / 2, 20))
            self.rect = pg.Rect(((self.WIDTH - 350) / 2, 100), (350, 100))
            self.screen.blit(self.surf, self.rect)

            self.surf2 = pg.Surface((176, 100))
            self.surf2.fill((0, 191, 240))
            self.text2 = self.font.render("ВЫХОД", True, (155, 0, 0))
            self.surf2.blit(self.text2, ((176 - self.font.size("ВЫХОД")[0]) / 2, 20))
            self.rect2 = pg.Rect(((self.WIDTH - 176) / 2, 300), (176, 100))
            self.screen.blit(self.surf2, self.rect2)

            if not self.walls:
                self.walls = [Walls() for i in range(5)]

            for event in pg.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    if self.rect.collidepoint(pg.mouse.get_pos()):
                        self.round = True
                       # pg.mixer.music.play(-1)
                    if self.rect2.collidepoint(pg.mouse.get_pos()):
                        pg.quit()
                elif event.type == QUIT:
                    pg.quit()

            pg.display.update()
            while self.round:

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

                for i in self.walls:
                    if i.rect.colliderect(self.snake.rect):
                        self.round = False
                        self.snake.__init__()
                        self.walls = []
                    elif self.fruit and i.rect.colliderect(self.fruit.rect):
                        self.fruit = None

                self.screen.blit(self.background, (0, 0))

                if self.fruit:
                    self.fruit.draw()
                for i in self.walls:
                    i.draw()
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
        self.get_touched = False


    def draw(self):

        self.temp = (self.rect[0], self.rect[1])

        if self.destination == "RIGHT":
            if self.rect[0] <= app.WIDTH + 25:
                self.rect[0] += self.speed
            else:
                self.get_touched = True
        elif self.destination == "DOWN":
            if self.rect[1] <= app.HEIGHT + 25:
                self.rect[1] += self.speed
            else:
                self.get_touched = True
        elif self.destination == "UP":
            if self.rect[1] >= 0:
                self.rect[1] -= self.speed
            else:
                self.get_touched = True
        elif self.destination == "LEFT":
            if self.rect[0] >= 0:
                self.rect[0] -= self.speed
            else:
                self.get_touched = True

        if self.get_touched:
            app.round = False
            pg.mixer.music.stop()
            self.__init__()
            app.walls = []

        if len(self.snake) > 1:
            for i in range(0, len(self.snake) - 1):
                self.temp2 = self.snake[i+1][0][0], self.snake[i+1][0][1]
                self.snake[i+1][0][0] = self.temp[0]
                self.snake[i+1][0][1] = self.temp[1]
                self.temp = self.temp2

        for j in self.snake:
            app.screen.blit(j[1], j[0])


class Walls:

    def __init__(self):
        self.size = random.randint(0, 1)
        if self.size == 0:
            self.coord_x = random.randint(0, app.WIDTH - 100)
            self.coord_y = random.randint(0, app.HEIGHT - 80)
            self.rect = pg.Rect((self.coord_x, self.coord_y), (app.HEIGHT / 40, app.WIDTH / 6))
            self.surf = pg.Surface((app.HEIGHT / 40, app.WIDTH / 6))
            self.surf.fill((0, 120, 0))
        elif self.size == 1:
            self.coord_x = random.randint(0, app.WIDTH - 100)
            self.coord_y = random.randint(0, app.HEIGHT - 80)
            self.rect = pg.Rect((self.coord_x, self.coord_y), (app.HEIGHT / 4, app.WIDTH / 60))
            self.surf = pg.Surface((app.HEIGHT / 4, app.WIDTH / 60))
            self.surf.fill((0, 120, 0))

    def draw(self):
        app.screen.blit(self.surf, self.rect)


app = App()
app.run()
