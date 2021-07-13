import pygame
import random
from enum import Enum
from collections import namedtuple
#### NN part
import tensorflow as tf
import numpy as np
from tensorflow import keras
model=keras.models.load_model('snake_neural.h5')
model.compile(loss='mean_squared_error', optimizer=tf.keras.optimizers.Adam(0.01))
####
pygame.init()
font = pygame.font.Font('arial.ttf', 25)
#font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
class Reward(Enum):
    NEUTRAL = 0
    GOOD = 1
    BAD = -1
Point = namedtuple('Point', 'x, y')
# Width here is the number of block per edge of the play ground
WIDTH=8 #you can edit the width by yourself
# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)

BLOCK_SIZE = 20
SPEED = 10
class SnakeGame:
    #160,160 or 120,120 for training
    #240,240 for see
    def __init__(self, w=WIDTH*BLOCK_SIZE, h=WIDTH*BLOCK_SIZE):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        
        # init game state
        self.direction = Direction.RIGHT
        
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head]
        
        self.score = 0
        self.food = None
        self.reward=Reward.NEUTRAL #neutral in the beginning
        self.state=None
        self._place_food()
        
    def get_state(self):
        arr_dir=[0,0,0,0]
        if self.direction==Direction.LEFT:
            arr_dir[0]=1
        elif self.direction==Direction.RIGHT:
            arr_dir[1]=1
        elif self.direction==Direction.UP:
            arr_dir[2]=1
        elif self.direction==Direction.DOWN:
            arr_dir[3]=1
        food_dir=[0,0,0,0]
        if self.food.x< self.head.x:
            food_dir[0]=1
        if self.food.x> self.head.x:
            food_dir[1]=1
        if self.food.y< self.head.y:
            food_dir[2]=1
        if self.food.y> self.head.y:
            food_dir[3]=1
        danger_dir=[0,0,0] #straight, left, right
        if self.head.x==self.w-BLOCK_SIZE:
            if self.direction==Direction.RIGHT:
                danger_dir[0]=1
            elif self.direction==Direction.DOWN:
                danger_dir[1]=1
            elif self.direction==Direction.UP:
                danger_dir[2]=1
        if self.head.x==0:
            if self.direction==Direction.LEFT:
                danger_dir[0]=1
            elif self.direction==Direction.UP:
                danger_dir[1]=1
            elif self.direction==Direction.DOWN:
                danger_dir[2]=1
        if self.head.y==self.h-BLOCK_SIZE:
            if self.direction==Direction.DOWN:
                danger_dir[0]=1
            elif self.direction==Direction.LEFT:
                danger_dir[1]=1
            elif self.direction==Direction.RIGHT:
                danger_dir[2]=1
        if self.head.y==0:
            if self.direction==Direction.UP:
                danger_dir[0]=1
            elif self.direction==Direction.RIGHT:
                danger_dir[1]=1
            elif self.direction==Direction.LEFT:
                danger_dir[2]=1
        # body collision
        if Point(self.head.x+BLOCK_SIZE, self.head.y) in self.snake:
            if self.direction==Direction.RIGHT:
                danger_dir[0]=1
            elif self.direction==Direction.DOWN:
                danger_dir[1]=1
            elif self.direction==Direction.UP:
                danger_dir[2]=1
        if Point(self.head.x-BLOCK_SIZE, self.head.y) in self.snake:
            if self.direction==Direction.LEFT:
                danger_dir[0]=1
            elif self.direction==Direction.UP:
                danger_dir[1]=1
            elif self.direction==Direction.DOWN:
                danger_dir[2]=1
        if Point(self.head.x, self.head.y+BLOCK_SIZE) in self.snake:
            if self.direction==Direction.DOWN:
                danger_dir[0]=1
            elif self.direction==Direction.LEFT:
                danger_dir[1]=1
            elif self.direction==Direction.RIGHT:
                danger_dir[2]=1
        if Point(self.head.x, self.head.y-BLOCK_SIZE) in self.snake:
            if self.direction==Direction.UP:
                danger_dir[0]=1
            elif self.direction==Direction.RIGHT:
                danger_dir[1]=1
            elif self.direction==Direction.LEFT:
                danger_dir[2]=1

        return np.array([danger_dir+arr_dir+food_dir]) 
        
    def _place_food(self):
        x = random.randint(1, (self.w-2*BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(1, (self.h-2*BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()
    

    def play_step(self):
        # 0. store the pos of prev state
        old_dis=abs(self.head.x-self.food.x)**2+abs(self.head.y-self.food.y)**2
        # 1. collect user input
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) :
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN
                elif event.key == pygame.K_1:
                    self.receive_decision(1)
                elif event.key == pygame.K_2:
                    self.receive_decision(2)
                elif event.key == pygame.K_0:
                    self.receive_decision(0)
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
        
        # 2. move
        self._move(self.direction) # update the head
        self.snake.insert(0, self.head)
        
        # 3. check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            self.reward=Reward.BAD # bad reward for game over
            return game_over, self.score
            
        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            self.reward=Reward.GOOD # good if eat food
            self._place_food()
        else:
            self.snake.pop()
            self.reward=Reward.NEUTRAL # neutral if nothing hapen
        # check for the good reward
        if self.state[0,:3].sum()>0 : # escape from collision
            self.reward=Reward.GOOD
        new_dis=abs(self.head.x-self.food.x)**2+abs(self.head.y-self.food.y)**2
        # if new_dis<old_dis: #get closer to food
        #     self.reward=Reward.GOOD
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        
        # 6. return game over and score
        return game_over, self.score
    
    def _is_collision(self):
        # hits boundary
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        # hits itself
        if self.head in self.snake[1:]:
            return True
        
        return False
        
    def _update_ui(self):
        self.display.fill(BLACK)
        
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))
            
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
        
    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
            
        self.head = Point(x, y)

    def receive_decision(self,dec):
        if dec==0:
            pass
        elif dec==1:
            if self.direction==Direction.UP:
                self.direction=Direction.LEFT
            elif self.direction==Direction.LEFT:
                self.direction=Direction.DOWN
            elif self.direction==Direction.DOWN:
                self.direction=Direction.RIGHT
            elif self.direction==Direction.RIGHT:
                self.direction=Direction.UP
        elif dec==2:
            if self.direction==Direction.UP:
                self.direction=Direction.RIGHT
            elif self.direction==Direction.RIGHT:
                self.direction=Direction.DOWN
            elif self.direction==Direction.DOWN:
                self.direction=Direction.LEFT
            elif self.direction==Direction.LEFT:
                self.direction=Direction.UP  

if __name__ == '__main__':
    game = SnakeGame()
    
    # game loop
    i=0
    num_game=0
    while True:
        i=i+1
        #get infomation from the enviroment and predict for the next move
        game.state=input_state=game.get_state()
        decision=model.predict(input_state)
        #print(str(input_state)+"\npre: "+str(decision))
        decision=decision[0].argmax()
        #move the snack in the environment
        game.receive_decision(decision)
        game_over, score = game.play_step()
        #retrain the model
        if game.reward==Reward.NEUTRAL:
            y=np.array([[0.333,0.333,0.333]])
            y[0][decision]=0.3
            model.fit(input_state,y)
        elif game.reward==Reward.GOOD:
            y=np.array([[0,0,0]])
            y[0][decision]=2 #value 1 at the right decision
            model.fit(input_state,y)
        elif game.reward==Reward.BAD:
            y=np.array([[1,1,1]])
            y[0][decision]=0 #value 0 at the bad decision
            model.fit(input_state,y)
        #save model
        #print(str(game.reward) +" at "+ str(decision))
        decision=model.predict(input_state)
        #print(str(game.head)+" "+str(game.food))
        #print("aft: "+str(decision)+"\n")
        model.save('snake_neural.h5')
        
        if game_over == True or i%500==0:
            num_game=num_game+1
            game = SnakeGame()
        
    #print('Final Score', score)
        
        
    pygame.quit()