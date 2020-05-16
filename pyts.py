import pygame
import sys
import math
from pygame.locals import *

def getSpriteArea(direction, frame):
    dir_num = {'N':12, 'NE':140, 'E':400, 'SE':784, 'S':1040, 'SW':784, 'W':400, 'NW':140}
    # SW, W and NW need to be mirror image

    sprite_x = dir_num[direction]
    sprite_y = 270 + frame * 64

    return pygame.Rect(sprite_x, sprite_y, 40, 40)

def startWalking(marine, mouse_x, mouse_y):
    marine['dest_x'] = mouse_x
    marine['dest_y'] = mouse_y

    dx = marine['dest_x'] - marine['x']
    dy = marine['dest_y'] - marine['y']

    #atan2 returns +/- 180
    rad = math.atan2(-dy, dx)
    marine['speed_x'] = marine['speed_walk'] * math.cos(rad)
    marine['speed_y'] = marine['speed_walk'] * math.sin(rad) * -1.0
    marine['mirrored'] = False
    deg = 180.0 / math.pi * rad

    if deg > 112.5 and deg <= 157.5:
        result = 'NW'
        marine['mirrored'] = True
    elif deg > 67.5 and deg <= 112.5:
        result = 'N'
    elif deg > 22.5 and deg <= 67.5:
        result = 'NE'
    elif deg > -22.5 and deg <= 22.5:
        result = 'E'
    elif deg > -67.5 and deg <= -22.5:
        result = 'SE'
    elif deg > -112.5 and deg <= -67.5:
        result = 'S'
    elif deg > -157.5 and deg <= -112.5:
        result = 'SW'
        marine['mirrored'] = True
    else:
        result = 'W'
        marine['mirrored'] = True

    #print('dx: ' + str(dx) + ', dy: ' + str(dy) + ', deg: ' + str(deg) + 'dir: ' + result)
    marine['direction'] = result
    marine['animation'] = 'walking'

def updateAnimation(marine):
    tol = 10
    at_x = abs(marine['x'] - marine['dest_x']) < tol
    at_y = abs(marine['y'] - marine['dest_y']) < tol
    if at_x and at_y:
        marine['animation'] = 'idle'
        marine['speed_x'] = 0
        marine['speed_y'] = 0

SCREEN_W = 400
SCREEN_H = 300
BGCOLOR = (128, 128, 128)
FPS = 15

fpsClock = pygame.time.Clock()

pygame.init()
DISPLAYSURF = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Marine Demo')

marineSprite = pygame.image.load('sprite_marine.png')
marine = {
    'x': SCREEN_W // 2,
    'y': SCREEN_H // 2,
    'direction': 'SE',
    'frame': 0,
    'speed_x': 0,
    'speed_y': 0,
    'speed_walk' : 40 / FPS,
    'dest_x': 0,
    'dest_y': 0,
    'max_frames': 9,
    'animation': 'idle',
    'mirrored': False
}

while True: # main game loop
    DISPLAYSURF.fill(BGCOLOR)

    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            startWalking(marine, mouse_x, mouse_y)
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()

    marine['x'] += marine['speed_x']
    marine['y'] += marine['speed_y']

    spriteArea = getSpriteArea(marine['direction'], marine['frame'])
    
    toDraw = marineSprite

    #TODO need to mirror image, will need a buffer otherwise entire image is mirrored
    DISPLAYSURF.blit(toDraw, (int(marine['x']), int(marine['y'])), area=spriteArea)

    if marine['animation'] != 'idle':
        marine['frame'] += 1
        if marine['frame'] == marine['max_frames']:
            marine['frame'] = 0
        
        updateAnimation(marine)

    pygame.display.update()
    fpsClock.tick(FPS)
