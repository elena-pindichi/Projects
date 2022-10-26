#!/usr/bin/env python3

import random
import pygame, sys
from pygame.locals import *
import argparse

pygame.init()
frame_rate = pygame.time.Clock()

WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)

#globals
# WIDTH = 600
WIDTH = 1500
# HEIGHT = 400
HEIGHT = 800
# BALL_RADIUS = 20
BALL_RADIUS = 40
# PAD_WIDTH = 8
PAD_WIDTH = 16
# PAD_HEIGHT = 80
PAD_HEIGHT = 160
HALF_PAD_WIDTH = PAD_WIDTH // 2
HALF_PAD_HEIGHT = PAD_HEIGHT // 2
PAD_VELOCITY = 9
INITIAL_LEFT_POSITION = [HALF_PAD_WIDTH - 1, HEIGHT // 2]
INITIAL_RIGHT_POSITION = [WIDTH + 1 - HALF_PAD_WIDTH, HEIGHT // 2]


class GameObject:
    def __init__(self, game, position, velocity, dimensions):
        self.position = position
        self.game = game
        self.velocity = velocity
        self.dimensions = dimensions

    def draw(self):
        pass

    def update(self):
        pass

    def collidesWith(self, other):
        return abs(self.position[0] - other.position[0]) < abs(self.dimensions[0] + other.dimensions[0]) and \
               abs(self.position[1] - other.position[1]) < abs(self.dimensions[1] + other.dimensions[1])
        pass


class Paddle(GameObject):
    def __init__(self, game, position, dimensions):
        super().__init__(game, position, [0, 0], dimensions)

    def draw(self):
        color = (75, 0, 130)
        pygame.draw.polygon(self.game.window, color, [[self.position[0] - HALF_PAD_WIDTH, self.position[1] - HALF_PAD_HEIGHT], [self.position[0] - HALF_PAD_WIDTH, self.position[1] + HALF_PAD_HEIGHT], [self.position[0] + HALF_PAD_WIDTH, self.position[1] + HALF_PAD_HEIGHT], [self.position[0] + HALF_PAD_WIDTH, self.position[1] - HALF_PAD_HEIGHT]], 0)

    def update(self):
        self.position[1] += self.velocity[1]
        if self.position[1] + HALF_PAD_HEIGHT > HEIGHT:
            self.position[1] = HEIGHT - + HALF_PAD_HEIGHT
        if self.position[1] - HALF_PAD_HEIGHT < 0:
            self.position[1] = HALF_PAD_HEIGHT

    def moveUp(self):
        self.velocity[1] = -PAD_VELOCITY

    def moveDown(self):
        self.velocity[1] = PAD_VELOCITY

    def stop(self):
        self.velocity[1] = 0

class Ball(GameObject):

    def __init__(self, game, position, dimensions):
        velocity = [0, 0]
        while velocity[0] == 0 or velocity[1] == 0:
            # velocity = [random.randrange(-1, 1), random.randrange(-1, 1)]
            velocity = [random.randrange(-8, 8), random.randrange(-8, 8)]
        super().__init__(game, position, velocity, dimensions)

    def draw(self):

        color = (0, 0, 255)
        pygame.draw.circle(self.game.window, color, self.position, BALL_RADIUS, 0)

    def update(self):

        self.position[0] += int(self.velocity[0])
        self.position[1] += int(self.velocity[1])

        if self.position[1] - self.dimensions[1] < 0:
            self.velocity[1] *= -1
        if self.position[1] + self.dimensions[1] > HEIGHT:
            self.velocity[1] *= -1
            
        if self.position[0] - self.dimensions[0] < -10:
            self.reset()
            self.game.rightPlayerScore += 1
        if self.position[0] + self.dimensions[0] > WIDTH + 10:
            self.reset()
            self.game.leftPlayerScore += 1

    def reset(self):
        self.game.ball = Ball(self.game, [WIDTH // 2, HEIGHT // 2], [BALL_RADIUS, BALL_RADIUS])
        self.game.gameObjects.remove(self)
        self.game.gameObjects.append(self.game.ball)

    def onCollision(self, other):
        self.velocity[0] *= -1.4



class Game:

    def __init__(self):

        self.window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
        pygame.display.set_caption('Pong Multiplayer')

        self.gameObjects = []

        self.paddleLeft = None
        self.paddleRight = None
        self.ball = None

        self.paddleRight = Paddle(self, INITIAL_RIGHT_POSITION, [HALF_PAD_WIDTH, HALF_PAD_HEIGHT])

        self.paddleLeft = Paddle(self, INITIAL_LEFT_POSITION, [HALF_PAD_WIDTH, HALF_PAD_HEIGHT])

        self.ball = Ball(self, [WIDTH // 2, HEIGHT // 2], [BALL_RADIUS, BALL_RADIUS])

        self.gameObjects.append(self.paddleRight)
        self.gameObjects.append(self.paddleLeft)
        self.gameObjects.append(self.ball)

        self.leftPlayerScore = 0
        self.rightPlayerScore = 0

    def run(self):
        while True:
            self.input()
            self.update()
            self.draw()

    def collisionDetection(self):
        for target in self.gameObjects:
            if self.ball != target:
                if self.ball.collidesWith(target):
                    self.ball.onCollision(target)

    def update(self):
        self.collisionDetection()
        for gameObject in self.gameObjects:
            gameObject.update()

    def input(self):

        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key == K_UP:
                    self.paddleRight.stop()
                if event.key == K_DOWN:
                    self.paddleRight.stop()
                if event.key == K_w:
                    self.paddleLeft.stop()
                if event.key == K_s:
                    self.paddleLeft.stop()

            if event.type == KEYDOWN:
                if event.key == K_UP:
                    self.paddleRight.moveUp()
                if event.key == K_DOWN:
                    self.paddleRight.moveDown()
                if event.key == K_w:
                    self.paddleLeft.moveUp()
                if event.key == K_s:
                    self.paddleLeft.moveDown()


    def draw(self):

        color = (200, 162, 200)
        self.window.fill(color)

        pygame.draw.line(self.window, WHITE, [WIDTH // 2, 0],[WIDTH // 2, HEIGHT], 1)
        pygame.draw.line(self.window, WHITE, [PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1)
        pygame.draw.line(self.window, WHITE, [WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1)
        pygame.draw.circle(self.window, WHITE, [WIDTH // 2, HEIGHT//2], 70, 1)

        myfont1 = pygame.font.SysFont("Comic Sans MS", 20)
        label1 = myfont1.render("Score " + str(self.leftPlayerScore), 1, (255,255,0))
        self.window.blit(label1, (50,20))

        myfont2 = pygame.font.SysFont("Comic Sans MS", 20)
        label2 = myfont2.render("Score " + str(self.rightPlayerScore), 1, (255,255,0))
        self.window.blit(label2, (470, 20))
        
        for gameobject in self.gameObjects:
            gameobject.draw()
        
        pygame.display.update()
        
        pygame.time.Clock().tick(60)
        

def main():
    game = Game()
    game.run()

main()
