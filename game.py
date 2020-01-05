import random

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

# game control
SNAKE_UP = K_UP
SNAKE_DOWN = K_DOWN
SNAKE_LEFT = K_LEFT
SNAKE_RIGHT = K_RIGHT
ADD_SEGMENT_TO_SNAKE = K_SPACE
ADD_NEW_FOOD = K_c

X_SIZE = WID / SIZE
Y_SIZE = HEI / SIZE

# One snake segment
class Segment:
    def __init__(self, x: int, y: int, dir: int):
        super().__init__()
        self.x = x * SIZE
        self.y = y * SIZE
        self.dir = dir

    def draw(self, color=C_WHITE):
        pygame.draw.rect(window, color, (self.x, self.y, SIZE, SIZE))

    def update(self):
        if self.dir == UP:
            self.y -= SIZE
        elif self.dir == LEFT:
            self.x -= SIZE
        elif self.dir == DOWN:
            self.y += SIZE
        elif self.dir == RIGHT:
            self.x += SIZE
        else:
            None


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

# Food
class Food:
    def __init__(self):
        super().__init__()
        xPosition = random.randint(0,23)
        yPosition = random.randint(0,15)
        self.segments = [Segment(xPosition, yPosition, None)]

    def drawAndUpdate(self):
        for seg in self.segments:
            seg.draw(C_RED)


# Events handling
def input(events):
    global cur_dir
    for event in events:
        if event.type == QUIT:
            sys.exit(0)
        elif event.type == KEYDOWN:
            if event.key == SNAKE_UP:
                if cur_dir != DOWN:
                    cur_dir = UP
            elif event.key == SNAKE_LEFT:
                if cur_dir != RIGHT:
                    cur_dir = LEFT
            elif event.key == SNAKE_DOWN:
                if cur_dir != UP:
                    cur_dir = DOWN
            elif event.key == SNAKE_RIGHT:
                if cur_dir != LEFT:
                    cur_dir = RIGHT
            elif event.key == ADD_SEGMENT_TO_SNAKE:
                snake.addSegment()
            elif event.key == ADD_NEW_FOOD:
                foods.append(Food())




# MAIN
pygame.init()
window = pygame.display.set_mode((WID, HEI))
clock = pygame.time.Clock()
pygame.display.set_caption('Snake')

snake = Snake()
cur_dir = LEFT
foods = []

# Main loop
while True:
    input(pygame.event.get())

    window.fill(C_BLACK)
    snake.drawAndUpdate(cur_dir)
    for food in foods:
        food.drawAndUpdate()
    pygame.display.update()
    clock.tick(GAME_SPEED)

