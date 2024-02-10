import pygame
from enum import Enum
import random
import numpy as np

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 10

BLOCK_SIZE = 20
EYE_SIZE = BLOCK_SIZE // 5

SNAKE_COL = (0, 255, 0)
EYE_COL = (255, 0, 0)
FOOD_COL = (255, 0, 0)
FONT_COL = (255, 255, 255)

class Direction(Enum):
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    UP = 4
    STATIONARY = 5

class Food:
    def __init__(self):
        self.shuffle()

    def shuffle(self):
        self.x = random.randrange(0, SCREEN_WIDTH, BLOCK_SIZE)
        self.y = random.randrange(0, SCREEN_HEIGHT, BLOCK_SIZE)

    def draw(self, screen):
        pygame.draw.rect(screen, FOOD_COL, pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE))

    def get_pos(self):
        return (self.x, self.y)

class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def get_pos(self):
            return (self.x, self.y)

class Head(Block):
    def __init__(self, x, y, dir):
        super().__init__(x, y)
        self.dir = dir
        self.old_x = 0
        self.old_y = 0
    
    def get_old_pos(self):
            return (self.old_x, self.old_y)
    
    def set_old_pos(self):
        self.old_x = self.x
        self.old_y = self.y

    def move(self, action):
        dirs = [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]
        idx = dirs.index(self.dir)
        
        if np.array_equal(action, [1, 0, 0]):
            new_dir = dirs[idx]
        elif np.array_equal(action, [0, 1, 0]):
            new_idx = (idx + 1) % 4
            new_dir = dirs[new_idx]
        elif np.array_equal(action, [0, 0, 1]):
            new_idx = (idx - 1) % 4
            new_dir = dirs[new_idx]

        if new_dir == Direction.UP:
            self.move_up()
        elif new_dir == Direction.DOWN:
            self.move_down()
        elif new_dir == Direction.RIGHT:
            self.move_right()
        elif new_dir == Direction.LEFT:
            self.move_left()

    def move_up(self):
        self.y -= BLOCK_SIZE
        self.dir = Direction.UP

    def move_down(self):
        self.y += BLOCK_SIZE
        self.dir = Direction.DOWN
        
    def move_left(self):
        self.x -= BLOCK_SIZE
        self.dir = Direction.LEFT
    
    def move_right(self):
        self.x += BLOCK_SIZE
        self.dir = Direction.RIGHT

class Snake:
    def __init__(self):
        self.head = Head(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, Direction.RIGHT)
        self.body = []

    def move_head(self, dir):
        self.head.set_old_pos()
        self.head.move(dir)

    def move_body(self):
        if len(self.body) > 0: 
            self.body.pop(0)
            self.body.append(Block(*self.head.get_old_pos()))

    def grow(self):
        self.body.append(Block(*self.head.get_old_pos()))

    def isEating(self, food):
        return self.head.get_pos() == food.get_pos()

    def hasHitWall(self, pt=None):
        if pt is None:
            pt = self.head
        x, y = pt.get_pos()
        return x < 0 or x > SCREEN_WIDTH - 1 or y < 0 or y > SCREEN_HEIGHT - 1

    def hasHitSelf(self, pt=None):
        if pt is None:
            pt = self.head
        for block in self.body:
            if pt.get_pos() == block.get_pos():
                return True
        
        return False

    def isColliding(self, pt=None):
        return self.hasHitSelf(pt) or self.hasHitWall(pt)

    def draw(self, screen):
        pygame.draw.rect(screen, SNAKE_COL, pygame.Rect(self.head.x, self.head.y, BLOCK_SIZE, BLOCK_SIZE))

        closerBias = (BLOCK_SIZE // 3) - EYE_SIZE
        furtherBias = ((BLOCK_SIZE * 2) // 3)
        shiftBias = BLOCK_SIZE // 4

        if self.head.dir == Direction.UP:
            pygame.draw.rect(screen, EYE_COL, pygame.Rect(self.head.x + closerBias, self.head.y + shiftBias, EYE_SIZE, EYE_SIZE))
            pygame.draw.rect(screen, EYE_COL, pygame.Rect(self.head.x + furtherBias, self.head.y + shiftBias, EYE_SIZE, EYE_SIZE))
        elif self.head.dir == Direction.RIGHT:
            pygame.draw.rect(screen, EYE_COL, pygame.Rect(self.head.x + BLOCK_SIZE - shiftBias - EYE_SIZE, self.head.y + closerBias, EYE_SIZE, EYE_SIZE))
            pygame.draw.rect(screen, EYE_COL, pygame.Rect(self.head.x + BLOCK_SIZE - shiftBias - EYE_SIZE, self.head.y + furtherBias, EYE_SIZE, EYE_SIZE))
        elif self.head.dir == Direction.DOWN:
            pygame.draw.rect(screen, EYE_COL, pygame.Rect(self.head.x + closerBias, self.head.y + BLOCK_SIZE - shiftBias - EYE_SIZE, EYE_SIZE, EYE_SIZE))
            pygame.draw.rect(screen, EYE_COL, pygame.Rect(self.head.x + furtherBias, self.head.y + BLOCK_SIZE - shiftBias - EYE_SIZE, EYE_SIZE, EYE_SIZE))
        elif self.head.dir == Direction.LEFT:
            pygame.draw.rect(screen, EYE_COL, pygame.Rect(self.head.x + shiftBias, self.head.y + closerBias, EYE_SIZE, EYE_SIZE))
            pygame.draw.rect(screen, EYE_COL, pygame.Rect(self.head.x + shiftBias, self.head.y + furtherBias, EYE_SIZE, EYE_SIZE))

        for block in self.body:
            pygame.draw.rect(screen, SNAKE_COL, pygame.Rect(block.x, block.y, BLOCK_SIZE, BLOCK_SIZE))
    
    def getBodyLength(self):
        return len(self.body)

class SnakeGame:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont("arial", 30)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.snake = Snake()
        self.food = Food()
        self.game_over = False
        self.reward = 0
        self.frame_iter = 0

    def play_step(self, action):
        self.frame_iter += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        self.snake.move_head(action) # move snake in new dir

        if self.snake.isColliding() or self.frame_iter > 100 * self.snake.getBodyLength(): # check is snake is colliding with anything
            self.game_over = True
            self.reward = -10
        else: # if collided, no need to redraw
            if self.snake.isEating(self.food): # check if snake is on food
                self.food.shuffle()
                self.snake.grow()
                self.reward = 10
            else:
                self.snake.move_body()

            self.draw() # draw snake + food

            pygame.display.flip() # apply changes to screen

            self.clock.tick(FPS)  # limits FPS to 60
        score = self.snake.getBodyLength()

        return self.reward, self.game_over, score
    
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.food.draw(self.screen)
        self.snake.draw(self.screen)
        self.draw_score()
    
    def draw_score(self):
        text = self.font.render(f"Score: {self.snake.getBodyLength()}", False, FONT_COL)
        self.screen.blit(text, (BLOCK_SIZE//2, BLOCK_SIZE//2))
