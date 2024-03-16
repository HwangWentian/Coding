import pygame as pg
from time import sleep

pg.init()
screen = pg.display.set_mode((1000, 600))
pg.display.set_caption("Badminton")
clock = pg.time.Clock()


def field():
    screen.fill((81,92,107))
    pg.draw.rect(screen, (200,200,200), (0,530,1000,20))
    pg.draw.rect(screen, (1,133,116), (485,350,30,180))


class Ball:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.direction = 0
        self.v = 0
    
    def strike(self):
        pass

    def show(self):
        pg.draw.circle(screen, (240, 240, 240), (self.x,self.y), 10)
    


ball = Ball()
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT: pg.quit()
    
    field()
    pg.draw.rect(screen, (50,30,40), (10,450,48,80))
    ball.show()

    clock.tick(30)
    pg.display.flip()
