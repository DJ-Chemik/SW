import pygame, sys, os, time
from pygame.locals import *

# window params
WID = 480
HEI = 320
SIZE = 20
GAME_SPEED = 8

# colors
C_BLACK = (0, 0, 0)
C_RED = (255, 0, 0)
C_GREEN = (0, 255, 0)
C_BLUE = (0, 0, 255)
C_WHITE = (255, 255, 255)

# directions
UP, LEFT, DOWN, RIGHT = 0, 1, 2, 3

X_SIZE = WID / SIZE
Y_SIZE = HEI / SIZE

# One snake segment
class Segment:
    def __init__(self, x: int, y: int, dir: int):
        super().__init__()
        self.x = x * SIZE
        self.y = y * SIZE
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
        self.segments = [Segment(X_SIZE // 2 - 1, Y_SIZE // 2, LEFT),
                         Segment(X_SIZE // 2, Y_SIZE // 2, LEFT)]


    def addSegment(self):
        last = self.segments[-1]
        direction = last.dir
        # maxX = 23, maxY=15
        x : int = last.x//SIZE
        y : int = last.y//SIZE
        print("X: ", x, " Y: ", y, " || DIR= ", direction)

        if direction == LEFT:
            self.segments.append(Segment(x+1, y, direction))
        elif direction == RIGHT:
            self.segments.append(Segment(x-1, y, direction))
        elif direction == UP:
            self.segments.append(Segment(x, y+1, direction))
        elif direction == DOWN:
            self.segments.append(Segment(x, y-1, direction))


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
            elif event.key == K_SPACE:
                snake.addSegment()



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
    clock.tick(GAME_SPEED)

