import pygame, sys, os, time
from pygame.locals import *

WID, HEI, SIZE = 800, 600, 25 # window params
C_BLACK, C_WHITE = (0, 0, 0), (255, 255, 255) # colors
UP, LEFT, DOWN, RIGHT = 0, 1, 2, 3 # directions

X_SIZE, Y_SIZE  = WID/SIZE, HEI/SIZE

# One snake segment
class Segment:
    def __init__(self, x: int, y: int, dir: int):
        super().__init__()
        self.x = x*SIZE
        self.y = y*SIZE
        self.dir = dir

    def draw(self):
        pygame.draw.rect(window, C_WHITE, (self.x, self.y, SIZE, SIZE))

    def update(self):
        if self.dir == UP:
            self.y -= SIZE
        elif self.dir == LEFT:
            self.x -= SIZE
        elif self.dir == DOWN:
            self.y += SIZE
        else:
            self.x += SIZE

# Whole snake
class Snake:
    def __init__(self):
        super().__init__()
        self.segments = [Segment(X_SIZE//2-1, Y_SIZE//2, LEFT),
                         Segment(X_SIZE//2, Y_SIZE//2, LEFT),
                         Segment(X_SIZE//2+1, Y_SIZE//2, LEFT)]

    def drawAndUpdate(self, dir: int):
        for seg in self.segments:
            seg.draw()
            seg.update()
            seg.dir, dir = dir, seg.dir

# Events handling
def input(events):
    global cur_dir
    for event in events:
        if event.type == QUIT:
            sys.exit(0)
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                if cur_dir != DOWN:
                    cur_dir = UP
            elif event.key == K_LEFT:
                if cur_dir != RIGHT:
                    cur_dir = LEFT
            elif event.key == K_DOWN:
                if cur_dir != UP:
                    cur_dir = DOWN
            elif event.key == K_RIGHT:
                if cur_dir != LEFT:
                    cur_dir = RIGHT

# MAIN
pygame.init()
window = pygame.display.set_mode((WID, HEI))
clock = pygame.time.Clock()
pygame.display.set_caption('Snake')

snake = Snake()
cur_dir = LEFT

# Main loop
while True:
    input(pygame.event.get())

    window.fill(C_BLACK)
    snake.drawAndUpdate(cur_dir)
    pygame.display.update()
    clock.tick(30)

    