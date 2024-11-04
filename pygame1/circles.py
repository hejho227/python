import pygame
import random
import sys

win = (400, 400)
lrad = []
lor1 = []
lor2 = []
fou = 0
white = pygame.Color("white")



def rngcir():
    """
    generates random circle
    returns 1 if found some circle that would be in a same spot
    returns 0 if not
    """
    radius = (random.randint(10, 50))
    orig1 = random.randint(radius, win[0]-radius)
    orig2 = random.randint(radius, win[1]-radius)
    if fou != 0:
        for a in range(fou):
            su = (lor1[a]-orig1)**2 + (lor2[a] - orig2)**2
            dis = (radius + lrad[a])**2
            if su < dis:
                return 1
    lrad.append(radius)
    lor1.append(orig1)
    lor2.append(orig2)
    return 0


pygame.init()
s = pygame.display.set_mode(win)
s.fill(white)
for i in range(100):
    rgb = random.randint(0, 0xFFFFFFFF)
    color = pygame.color.Color(rgb)
    x = 1
    while x == 1:
        x = rngcir()
    fou += 1
    orig = [lor1[i], lor2[i]]
    pygame.draw.circle(s, color, orig, lrad[i])
    pygame.display.flip()


while True:
    for event in pygame.event.get():
        if event.type in (pygame.QUIT, pygame.MOUSEBUTTONDOWN):
            pygame.quit()
            sys.exit()
