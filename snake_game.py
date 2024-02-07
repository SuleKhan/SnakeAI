import pygame
from enum import Enum
import random

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 10

BLOCK_SIZE = 20

SNAKE_COL = (0, 255, 0)
FOOD_COL = (255, 0, 0)

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

    def move(self, dir):
        if dir == Direction.UP and self.dir != Direction.DOWN:
            self.move_up()
        elif dir == Direction.DOWN and self.dir != Direction.UP:
            self.move_down()
        elif dir == Direction.RIGHT and self.dir != Direction.LEFT:
            self.move_right()
        elif dir == Direction.LEFT and self.dir != Direction.RIGHT:
            self.move_left()
        elif dir == Direction.STATIONARY:
            pass
        else:
            self.move(self.dir)

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

    def move(self, dir):
        if len(self.body) > 0: 
            self.body.pop(0)
            self.body.append(Block(*self.head.get_pos()))
        self.head.move(dir)

    def grow(self):
        self.body.append(Block(*self.head.get_pos()))

    def isEating(self, food):
        return self.head.get_pos() == food.get_pos()

    def hasHitWall(self):
        x, y = self.head.get_pos()
        return x < 0 or x > SCREEN_WIDTH - 1 or y < 0 or y > SCREEN_HEIGHT - 1

    def hasHitSelf(self):
        for block in self.body:
            if self.head.get_pos() == block.get_pos():
                return True
        
        return False

    def isColliding(self):
        return self.hasHitSelf() or self.hasHitWall()

    def draw(self, screen):
        pygame.draw.rect(screen, SNAKE_COL, pygame.Rect(self.head.x, self.head.y, BLOCK_SIZE, BLOCK_SIZE))

        for block in self.body:
            pygame.draw.rect(screen, SNAKE_COL, pygame.Rect(block.x, block.y, BLOCK_SIZE, BLOCK_SIZE))

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.food = Food()
        self.game_over = False

    def play_step(self):
        new_dir = self.get_action() # get new dir
        self.snake.move(new_dir) # move snake in new dir

        if self.snake.isColliding(): # check is snake is colliding with anything
            self.game_over = True
        else: # if collided, no need to redraw
            if self.snake.isEating(self.food): # check if snake is on food
                self.food.shuffle()
                self.snake.grow()

            self.draw() # draw snake + food

            pygame.display.flip() # apply changes to screen

            self.clock.tick(FPS)  # limits FPS to 60

        return self.game_over
    
    def draw(self):
        self.screen.fill((0, 0, 0))
        self.food.draw(self.screen)
        self.snake.draw(self.screen)

    def get_action(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    return Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    return Direction.RIGHT
                elif event.key == pygame.K_UP:
                    return Direction.UP
                elif event.key == pygame.K_DOWN:
                    return Direction.DOWN
                
def main():
    game = SnakeGame()
    game_over = False
    while not game_over:
        game_over = game.play_step()
        
    pygame.quit()


main()
