import sys
import math
import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
pygame.init()
scr = pygame.display.set_mode((800, 550))
scr.fill(WHITE)
win = scr.get_rect()


def drawtree(x1,y1,x2,y2,n, isbra):
    drawline(x1,y1,x2,y2)
    dx = (x2-x1)* SCALE
    dy = (y2-y1)* SCALE
    x3 = x2 + dx*cos1*SCALE2 - dy*sin1*SCALE2
    y3 = y2 + dx*sin1*SCALE2 + dy*cos1*SCALE2
    x4 = x2 + dx*cos2*SCALE2 - dy*sin2*SCALE2
    y4 = y2 + dx*sin2*SCALE2 + dy*cos2*SCALE2
    x5 = x2 + dx*cos3 - dy*sin3
    y5 = y2 + dx*sin3 + dy*cos3
    if n > 1:
        drawtree(x2,y2,x3,y3, n-1, 1)
        drawtree(x2,y2,x4,y4, n-1, 1)
        drawtree(x2,y2,x5,y5, n-1, 0)


def drawline(xa, ya, xb, yb):
    s1, s2 = (win.centerx+xa, win.height-ya), (win.centerx+xb, win.height-yb)
    pygame.draw.line(scr, BLACK, s1, s2, 1)


PHI1 = math.radians( 60)
PHI2 = math.radians(-80)
PHI3 = math.radians(4)
sin1 = math.sin(PHI1)
cos1 = math.cos(PHI1)
sin2 = math.sin(PHI2)
cos2 = math.cos(PHI2)
sin3 = math.sin(PHI3)
cos3 = math.cos(PHI3)
SCALE = 0.8
SCALE2 = 0.4
drawtree(0,0,0,85, 15, 0)
pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.key == pygame.K_RETURN:
                sys.exit()
