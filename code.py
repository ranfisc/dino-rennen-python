import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "600,200"
import pgzrun
import pgzero.screen
screen: pgzero.screen.Screen
from pgzero.builtins import *

import random

ground_width = images.ground.get_width() # ground_width is 642

WIDTH = ground_width
HEIGHT = 212
TITLE = "Chrome Dino Game!"

ground_x = 0
ground_y = 200
ground_v = 6

ground2_x = ground_x + ground_width
ground2_y = 200
ground_level = 165

player_x = 30
player_y = ground_level
player_v = 10 # player_v for jumping speed
player_width = 43
player_height = -50 

counter = 0 # counter for dino walk cycle

dino_jump = False
dino_duck = False
game_over = False

class Cacti:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
    def draw(self):
        screen.blit("cactus1", (self.x, self.y)) # change between cacti, cactus4.png - cactus6.png have different ground level

cactus = Cacti(ground_width, ground_level)
cactus2 = Cacti(ground_width + 300, ground_level)

cacti = [cactus, cactus2]

ptero_x = ground_width + 1000
ptero_y = ground_level - 12 # dino standing height: - 40 // dino ducking height: - 15

def on_key_down(key):
    global dino_jump
    if key == keys.UP and game_over == False:
        dino_jump = True # --> so dino can't jump when dead

bg_color = (255, 222, 156) # for background color

def update():
    global ground_x, ground_v, ground2_x, counter, player_x, player_y, player_v, dino_jump, dino_duck, game_over, ptero_x
    
    ground_x -= ground_v
    ground2_x -= ground_v

    for i in range(len(cacti)):
        cactus_item = cacti[i]
        cactus_item.x -= ground_v

    ptero_x -= ground_v

    if ground_x <= -ground_width:
        ground_x = ground2_x + ground_width
    if ground2_x <= -ground_width:
        ground2_x = ground_x + ground_width

    for i in range(len(cacti)):
        cactus_item = cacti[i]
        if cactus_item.x < 0:
            cactus_item.x =+ ground_width + random.randint(0, 600)

    counter += 1

    if counter > 10:
        counter = 1

    if dino_jump == True:
        player_y -= player_v
        if player_y <= 40:
            player_v = -player_v
        if player_y >= ground_level:
            player_y = ground_level
            player_v = -player_v
            dino_jump = False

    if keyboard.down:
        dino_duck = True
    else:
        dino_duck = False

    if game_over == True: # ground stops moving
        ground_v = 0

    for i in range(len(cacti)):
        cactus_item = cacti[i]
        if player_x == cactus_item.x and player_y >= cactus_item.y:
            game_over = True

    if player_x + player_width - ptero_x >= 0 and dino_duck == False:
        game_over = True

def draw():
    # background
    screen.fill(bg_color)
    screen.blit("ground", (ground_x, ground_y))
    screen.blit("ground", (ground2_x, ground2_y))
    
    #cacti
    for i in range(len(cacti)):
        cactus_item = cacti[i]
        cactus_item.draw()

    # ptero
    if counter >= 5:
        screen.blit("ptero1", (ptero_x, ptero_y))
    else:
        screen.blit("ptero2", (ptero_x, ptero_y))
    
    # dino
    if game_over == True:
        screen.blit("dinogameover", (player_x, player_y))
        screen.blit("gameover", (ground_width/2 - 50, 80)) # 100 = width game over text, 50 half of that
        
    elif dino_jump == True:
        screen.blit("dinojumping", (player_x, player_y))

    elif dino_duck == True:
        if counter >= 5:
            screen.blit("dinoducking1", (player_x, player_y+18))
        else:
            screen.blit("dinoducking2", (player_x, player_y+18))

    else:
        if counter >= 5:
            screen.blit("dino1", (player_x, player_y))
        else:
            screen.blit("dino2", (player_x, player_y))

pgzrun.go()

