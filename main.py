import pygame as pg
import numpy as np
import random
import math
import time
import sys


WIDTH = 1600
HEIGHT = 900
FPS = 60
TITLE = "Starfield"


class Star:
    def __init__(self, app):
        self.app = app
        self.position = np.array([0, 0], dtype="float64")
        self.size = 3
        self.color = [255, 255, 255]
        self.velocity = np.array([0, 0], dtype="float64")
        self.acceleration = np.array([0, 0], dtype="float64")
        self.speed = 0.5
        self.opacity = 0
        self.on_init()
        self.getTicksLastFrame = time.time()


    def on_init(self):
        centerX = self.app.width/2
        centerY = self.app.height/2
        self.position[0] = centerX
        self.position[1] = centerY

        xAcc = random.uniform(-self.speed, self.speed)
        while xAcc == 0:
            xAcc = random.uniform(-self.speed, self.speed)
        yAcc = random.uniform(-self.speed, self.speed)
        while xAcc == 0:
            yAcc = random.uniform(-self.speed, self.speed)
        self.acceleration = np.array([xAcc, yAcc], dtype="float64")


    def update(self):
        self.transparent()
        self.position += self.velocity
        self.velocity += self.acceleration


    def transparent(self):
        self.opacity += self.get_dist()*0.001
        self.opacity = min(1, self.opacity)
        self.color[0] = 255 * self.opacity
        self.color[1] = 255 * self.opacity
        self.color[2] = 255 * self.opacity


    def isOutOfScreen(self):
        if self.position[0] + self.size > self.app.width or self.position[0] - self.size < 0:
            return True
        if self.position[0] + self.size > self.app.width or self.position[0] - self.size < 0:
            return True


    def draw(self, screen):
        if not self.isOutOfScreen():
            pg.draw.circle(screen, self.color, (self.position[0], self.position[1]), self.size)



    def get_dist(self):
        return math.sqrt((self.position[0]-self.app.width/2)**2 + (self.position[1]-self.app.height/2)**2)



class App:
    def __init__(self, width, height, fps, title):
        pg.init()
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.screen = pg.display.set_mode((self.width, self.height))
        pg.display.set_caption(self.title)
        self.clock = pg.time.Clock()
        self.time = pg.time.get_ticks()
        self.stars = []
        STAR_COUNT = 300

        for i in range(STAR_COUNT):
            self.stars.append(Star(self))




    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse = pg.mouse.get_pos()
                self.stars.append(Star(mouse[0], mouse[1]))
                print("working")

        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            pass
        if keys[pg.K_d]:
            pass
        if keys[pg.K_w]:
            pass
        if keys[pg.K_s]:
            pass


    def update_screen(self):
        self.screen.fill(0)
        for star in self.stars:
            if star.isOutOfScreen():
                self.stars.remove(star)
                self.stars.append(Star(self))
            star.update()
            star.draw(self.screen)
        pg.display.update()


    def run(self):
        while True:
            self.clock.tick(self.fps)
            self.check_events()
            self.update_screen()


if __name__ == "__main__":
    app = App(WIDTH, HEIGHT, FPS, TITLE)
    app.run()