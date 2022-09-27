#!/usr/bin/env python3

import random
import pygame, sys
from pygame.locals import *
import argparse

pygame.init()
frame_rate = pygame.time.Clock()

# date globale
SNAKE_VELOCITY = 5
SNAKE_WIDTH = 35
FRUIT_WIDTH = 10
WIDTH = 720
HEIGHT = 480
SNAKE_INITIAL_POSITION = [400, 100]
# FRUIT_INITIAL_POSITION = [random.randrange(1, (WIDTH//10)) * 10, random.randrange(1, (HEIGHT//10)) * 10]
FRUIT_INITIAL_POSITION = [200, 200]

# define game object
class GameObject:
    def __init__(self, game, position, velocity, dimension, direction):
        self.game = game
        self.position = position
        self.velocity = velocity
        self.dimension = dimension
        self.direction = direction
    
    def draw(self):
        pass

    def update(self):
        pass

    def collidesWith(self, other):
        return abs(self.position[0] - other.position[0]) < abs(self.dimension[0] - other.dimension[0]) and \
               abs(self.position[1] - other.position[1]) < abs(self.dimension[1] - other.dimension[1])
        # return self.position[0] == other.position[0] and self.position[1] == other.position[1]
    

# define snake
class Snake(GameObject):
    def __init__(self, game, position, dimension, direction):
        super().__init__(game, position, [0, 0], dimension, direction)

    def draw(self):
        color = (0, 107, 60)
        pygame.draw.rect(self.game.window, color, [self.position[0], self.position[1], 25, 25])

    def update(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        
    
    def moveUp(self):
        self.velocity[1] = -SNAKE_VELOCITY // 3
    
    def moveDown(self):
        self.velocity[1] = SNAKE_VELOCITY // 3
    
    def moveLeft(self):
        self.velocity[0] = -SNAKE_VELOCITY // 3
    
    def moveRight(self):
        self.velocity[0] = SNAKE_VELOCITY // 3
    
    def stop(self):
        self.velocity[1] = 0
        self.velocity[0] = 0
    
# define fruit
class Fruit(GameObject):
    def __init__(self, game, position, dimension):
        super().__init__(game, position, [0, 0], dimension, 'NONE')
    
    def draw(self):
        color = (170, 51, 106)
        pygame.draw.circle(self.game.window, color, self.position, FRUIT_WIDTH, 0)

    def update(self):
        pass
    
    def onCollision(self, other):
        self.game.Score += 10
        self.reset()

    def reset(self):
        self.position = [random.randrange(10, (WIDTH  // 10)) * 10, random.randrange(10, (HEIGHT //10)) * 10]

    
# define game
class Game:
    def __init__(self):
        
        self.window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
        pygame.display.set_caption('Snake')
        
        self.gameObjects = []
        self.snake = Snake(self, SNAKE_INITIAL_POSITION, [SNAKE_WIDTH, SNAKE_WIDTH], 'RIGHT')
        self.fruit = Fruit(self, FRUIT_INITIAL_POSITION, [FRUIT_WIDTH, FRUIT_WIDTH])

        self.gameObjects.append(self.snake)
        self.gameObjects.append(self.fruit)
        
        self.Score = 0
    
    def update(self):
        self.collisionDetection()
        for gameObject in self.gameObjects:
            gameObject.update()
    
    def input(self):
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key == K_UP:
                    self.snake.stop()
                if event.key == K_DOWN:
                    self.snake.stop()
                if event.key == K_LEFT:
                    self.snake.stop()
                if event.key == K_RIGHT:
                    self.snake.stop()
                    
            if event.type == KEYDOWN:
                if event.key == K_UP and self.snake.direction != 'DOWN':
                    self.snake.moveUp()
                    self.snake.direction = 'UP'
                if event.key == K_DOWN and self.snake.direction != 'UP':
                    self.snake.moveDown()
                    self.snake.direction = 'DOWN'
                if event.key == K_LEFT and self.snake.direction != 'RIGHT':
                    self.snake.moveLeft()
                    self.snake.direction = 'LEFT'
                if event.key == K_RIGHT and self.snake.direction != 'LEFT':
                    self.snake.moveRight()
                    self.snake.direction = 'RIGHT'
            
        if self.snake.direction == 'RIGHT':
            self.snake.position[0] += 5
        if self.snake.direction == 'LEFT':
            self.snake.position[0] -= 5
        if self.snake.direction == 'UP':
            self.snake.position[1] -= 5
        if self.snake.direction == 'DOWN':
            self.snake.position[1] += 5
    
    def collisionDetection(self):
        for target in self.gameObjects:
            if self.snake != target:
                if self.snake.collidesWith(target):
                    self.fruit.onCollision(target)
    
    def draw(self):

        color_background = (123, 182, 97)
        self.window.fill(color_background)
        
        score_font = pygame.font.SysFont("Arial", 20)
        label = score_font.render("Score " + str(self.Score), 1, (255,255,0))
        self.window.blit(label, (50,20))
        
        for gameObject in self.gameObjects:
            gameObject.draw()
        
        pygame.display.update()
        pygame.time.Clock().tick(60)
    
    def run(self):
        while True:
            self.input()
            self.update()
            self.draw()

def main():
    game = Game()
    game.run()

main()