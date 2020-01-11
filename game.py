import random
import pygame, sys, os, time
import tkinter as tk
from tkinter import messagebox
from pygame.locals import *

# window params
WID = 480
HEI = 320
SIZE = 20
GAME_SPEED = 10

# colors
C_BLACK = (0, 0, 0)
C_GRAY = (180, 180, 180)
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

maxX = 23
maxY = 15

# One snake segment
class Segment:
    def __init__(self, x: int, y: int, dir: int):
        super().__init__()
        self.Xpos = x
        self.Ypos = y

        self.x = self.Xpos * SIZE
        self.y = self.Ypos * SIZE
        self.dir = dir

    def draw(self, color=C_WHITE):
        pygame.draw.rect(window, color, (self.x, self.y, SIZE, SIZE))

    def update(self):
        self.Xpos = self.x//SIZE
        self.Ypos = self.y//SIZE
        if self.dir == UP:
            if self.Ypos>0:
                self.y -= SIZE
            else:
                self.y = maxY*SIZE
        elif self.dir == DOWN:
            if self.Ypos<maxY:
                self.y += SIZE
            else:
                self.y = 0
        elif self.dir == LEFT:
            if self.Xpos>0:
                self.x -= SIZE
            else:
                self.x = maxX*SIZE
        elif self.dir == RIGHT:
            if self.Xpos<maxX:
                self.x += SIZE
            else:
                self.x = 0
        else:
            None

# Whole snake
class Snake:

    def __init__(self):
        super().__init__()
        self.segments = [Segment(X_SIZE // 2 - 1, Y_SIZE // 2, LEFT),
                         Segment(X_SIZE // 2, Y_SIZE // 2, LEFT)]
        self.head = self.segments[0]
        self.tail = self.segments[-1]
        self.readyToAddSegment = True
        self.lockedHeadX = None #dopóki się nie zmieni nie można dodawać nowych segmentów
        self.lockedHeadY = None #dopóki się nie zmieni nie można dodawać nowych segmentów


    def addSegment(self):
        last = self.segments[-1]
        direction = last.dir
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

    def detectCollision(self):
        for seg in self.segments:
            if self.head.Xpos==seg.Xpos and self.head.Ypos==seg.Ypos and seg!=self.segments[0]:
                displayMessageBox("Game Over", "You hit in your own tail :( Mission Failed Bro!")
                global continueGame
                continueGame=False

    def detectFood(self):
        for food in foods:
            if self.head.Xpos == food.xPosition and self.head.Ypos == food.yPosition:
                self.addSegment()
                foods.remove(food)
                self.lockedHeadX = self.head.Xpos #Dopiero gdy to przestanie być prawdziwe będzie mogła zostać zdjęta blokada
                self.lockedHeadY = self.head.Ypos #czyli gdy snake przemieści się o 1 pole
                self.readyToAddSegment = False #Założenie blokady

    def deleteLockInFlag(self):
        if self.head.Xpos != self.lockedHeadX:
            if self.head.Ypos != self.lockedHeadY:
                self.readyToAddSegment = True

    def drawAndUpdate(self, dir: int):
        for seg in self.segments:
            if seg==self.head:
                seg.draw(C_WHITE)
            else:
                seg.draw(C_GRAY)
            seg.update()
            seg.dir, dir = dir, seg.dir
            self.tail = self.segments[-1]
            self.head = self.segments[0]
        self.deleteLockInFlag()
        self.detectCollision()
        if self.readyToAddSegment:
            self.detectFood()

# Food
class Food:
    def __init__(self):
        super().__init__()
        self.xPosition = random.randint(0,maxX)
        self.yPosition = random.randint(0,maxY)
        self.segments = [Segment(self.xPosition, self.yPosition, None)]


    def drawAndUpdate(self):
        for seg in self.segments:
            seg.draw(C_RED)

def addFoodInRandomPositionAndTime():
    maxFoodsInGameBoard = 6
    actualFoodsInGameBoard = len(foods)
    randomParameter = 30

    if actualFoodsInGameBoard < maxFoodsInGameBoard:
        print(actualFoodsInGameBoard)
        #Add one food if board is empty
        if actualFoodsInGameBoard == 0:
            foods.append(Food())
        #Add next food to board sometimes
        if random.randint(0, randomParameter) == 1:
            foods.append(Food())



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

def drawGameWindow():
    window.fill(C_BLACK)
    for food in foods:
        food.drawAndUpdate()
    snake.drawAndUpdate(cur_dir)
    pygame.display.update()

def displayMessageBox(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

# MAIN
pygame.init()
window = pygame.display.set_mode((WID, HEI))
clock = pygame.time.Clock()
pygame.display.set_caption('Snake')

snake = Snake()
cur_dir = LEFT
foods = []

continueGame = True

# Main loop
while continueGame:
    input(pygame.event.get())
    addFoodInRandomPositionAndTime()
    drawGameWindow()
    clock.tick(GAME_SPEED)

