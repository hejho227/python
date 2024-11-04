import pygame
import random
import sys

win = (400, 400)
size = (50, 50)
white = pygame.Color("white")
black = pygame.Color("black")
pygame.init()
s = pygame.display.set_mode(win)
s.fill(white)
for x in range(8):
    if x % 2 == 0:
        for y in range(4):
            start = (x * 50, 2 * y * 50)
            rect = [start, size]
            pygame.draw.rect(s, black, rect)
            pygame.display.flip()
    else:
        for y in range(5):
            start = (x * 50, (2 * y - 1) * 50)
            rect = [start, size]
            pygame.draw.rect(s, black, rect)
            pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type in (pygame.QUIT, pygame.MOUSEBUTTONDOWN):
            pygame.quit()
            sys.exit()
