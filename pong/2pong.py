'''
This code creates a game of pong for 1 or 2 players
'''
import pygame
import sys
import random


def colwin():
    '''
    checks for colision betwen ball and window borders

    returns 1 if ball colided with left wall
    returns 2 if ball colided with top or bottom
    and 0 in other case
    '''
    global box, win
    if box.right >= win.right:
        return 1
    elif box.top <= win.top or box.bottom >= win.bottom:
        return 2
    else:
        return 0


def colb2():
    '''
    Checks for collisions betwen ball and the other thingy

    returns 1 if distance betwen x coordinates is <= distance betwene y
    returns 2 if distance betewn x coordinates is > distance betwene y
        and ball is higier than box2
    returns 3if distance betewn x coordinates is > distance betwene y
        and ball is lower than box2
    returns 0 if there is no colision
        ands sets inside to 0
    '''
    global box, box2
    if box.colliderect(box2):
        disx = (box.centerx + 15)**2
        disy = (box.centery - box2.centery)**2
        if disx >= disy:
            return 1
        elif box.centery - box2.centery < 0:
            return 2
        elif box.centery - box2.centery >= 0:
            return 3
    else:
        return 0


def colb3():
    '''
    Checks for collisions betwen ball and the third thingy

    returns 1 if distance betwen x coordinates is <= distance betwene y
    returns 2 if distance betewn x coordinates is > distance betwene y
        and ball is higier than box3
    returns 3if distance betewn x coordinates is > distance betwene y
        and ball is lower than box3
    returns 0 if there is no colision
        ands sets inside to 0
    '''
    global box, box3
    if box.colliderect(box3):
        dis2x = (box.centerx + 15)**2
        dis2y = (box.centery - box3.centery)**2
        if dis2x >= dis2y:
            return 1
        elif box.centery - box3.centery < 0:
            return 2
        elif box.centery - box3.centery >= 0:
            return 3
    else:
        return 0


def outs():
    '''
    Checks if ball is outside the window

    Returns 1 if it's highier
    Returns 2 if it's lower
    Returns 3 if it's to the left
    Returns 4 if it's to the right
    Returns 0 if it's not
    '''
    global box, win
    if box.top < win.top:
        return 1
    elif box.bottom > win.bottom:
        return 2
    elif box.right < win.left:
        return 3
    elif box.left > win.right:
        return 4
    else:
        return 0


def b1left():
    '''
    Checks relative x position of ball to the box2

    Returns 1 if it is to the left or in the same line
    Returns 0 if it is not
    '''
    global box, box2
    if box.left <= box2.right:
        return 1
    else:
        return 0


def b1right():
    '''
    Checks relative x position of ball to the box3

    Returns 1 if it is to the left or in the same line
    Returns 0 if it is not
    '''
    global box, box3
    if box.right >= box3.left:
        return 1
    else:
        return 0


def b1hight():
    '''
    Checks if ball if highier or lower then box2

    Returns 1 if it's highier
    Returns 2 if it's lower
    Returns 0 if it's nither
    '''
    global box, box2
    if box.bottom <= box2.top:
        return 1
    elif box.top >= box2.bottom:
        return 2
    else:
        return 0


def b1hight2():
    '''
    Checks if ball if highier or lower then box3

    Returns 1 if it's highier
    Returns 2 if it's lower
    Returns 0 if it's nither
    '''
    global box, box3
    if box.bottom <= box3.top:
        return 1
    elif box.top >= box3.bottom:
        return 2
    else:
        return 0


def move(a):
    '''
    Checks if movement should be allowed

    Accepts 1 and 2, 1 if desired movement direction is up
        and 2 if it's down

    Returns 0 if movement should be free
    Returns 1 if position should be set to top
    Returns 2 if position should be set to bottom
    Returns 3 if position should be set to top with the ball
    Returns 4 if position should be set to bottom with the ball
    '''
    global box, box2, STEP, win
    if b1hight() == 1:
        if a == 1:
            if box2.top - STEP - box.height <= win.top:
                return 3
            else:
                return 0
        elif box2.bottom + STEP >= win.bottom:
            return 2
    elif b1hight() == 2:
        if a == 2:
            if box2.bottom + STEP + box.height >= win.bottom:
                return 4
            else:
                return 0
        elif box2.top - STEP <= win.top:
            return 1
        else:
            return 0
    else:
        if box2.top - STEP <= win.top:
            return 1
        elif box2.bottom + STEP >= win.bottom:
            return 2
        else:
            return 0


def move2(a):
    '''
    Checks if movement should be allowed for p2

    Accepts 1 and 2, 1 if desired movement direction is up
        and 2 if it's down

    Returns 0 if movement should be free
    Returns 1 if position should be set to top
    Returns 2 if position should be set to bottom
    Returns 3 if position should be set to top with the ball
    Returns 4 if position should be set to bottom with the ball
    '''
    global box, box3, STEP, win
    if b1right() == 1:
        if b1hight2() == 1:
            if a == 1:
                if box3.top - STEP - box.height <= win.top:
                    return 3
                else:
                    return 0
            elif box3.bottom + STEP >= win.bottom:
                return 2
        elif b1hight2() == 2:
            if a == 2:
                if box3.bottom + STEP + box.height >= win.bottom:
                    return 4
                else:
                    return 0
            elif box3.top - STEP <= win.top:
                return 1
        else:
            return 0
    else:
        if box3.top - STEP <= win.top:
            return 1
        elif box3.bottom + STEP >= win.bottom:
            return 2
        else:
            return 0


def lose1():
    '''
    Waits for user imput
    quits the game if escape is pressed
    restarts the game if r is pressed
    quits to menu if m is pressed
    '''
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_m:
                    menu()
                if event.key == pygame.K_r:
                    p1()


def lose2():
    '''
    Waits for user imput
    quits the game if escape is pressed
    restarts the game if r is pressed
    quits to menu if m is pressed
    '''
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_m:
                    menu()
                if event.key == pygame.K_r:
                    p2()


def best():
    '''
    checks if player has more points than their best score

    if so sets best score to current amount of points
    '''
    global points, bs
    if points > bs:
        bs = points


def goodbye():
    '''
    prints goodbye and closes the game
    '''
    scr.fill(black)
    msg = myfont.render("Goodbye :)", True, red)
    scr.blit(msg, msg_box3)
    pygame.display.flip()
    pygame.time.wait(1000)
    sys.exit()


def difficulty():
    '''
    allows changing the difficulty

    sets diff to 1 for easy
    sets diff to 2 for hard
    '''
    global diff
    while True:
        scr.fill(black)
        msg = myfont.render("(1)easy or (2)hard", True, red)
        scr.blit(msg, msg_box3)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    diff = 1
                    p1()
                if event.key == pygame.K_2:
                    diff = 2
                    p1()


def p1():
    '''
    main loop for 1 player mode
    '''
    global black, white, red, points, SPEED, scr, win
    global box, box2, box3, fps, STEP, myfont, msg, msg1, msg2, msg3
    global msgb, msg_box, msg_box1, msg_box2, msgb_box, diff
    if diff == 1:
        box2 = pygame.Rect(0, 0, 30, 60)
    if diff == 2:
        box2 = pygame.Rect(0, 0, 15, 30)
    box.center = win.center
    box2.center = (0, win.centery)
    scr.fill(black)
    pygame.draw.rect(scr, white, box)
    pygame.draw.rect(scr, white, box2)
    scr.blit(cou3, msg_box3)
    pygame.display.flip()
    pygame.time.wait(1000)
    scr.fill(black)
    pygame.draw.rect(scr, white, box)
    pygame.draw.rect(scr, white, box2)
    scr.blit(cou2, msg_box3)
    pygame.display.flip()
    pygame.time.wait(1000)
    scr.fill(black)
    pygame.draw.rect(scr, white, box)
    pygame.draw.rect(scr, white, box2)
    scr.blit(cou1, msg_box3)
    pygame.display.flip()
    pygame.time.wait(1000)
    points = 0
    vec = [random.randint(1, 2), random.randint(1, 2)]
    if random.randint(0, 1) == 1:
        vec[1] = -vec[1]
    pygame.key.set_repeat(50, 50)
    while True:
        if colwin() == 0:
            pass
        elif colwin() == 1:
            vec[0] = -vec[0]
            hitbord = 1
        elif colwin() == 2:
            vec[1] = -vec[1]
            hitbord = 1
        if colb2() == 0:
            pass
        elif colb2() == 1:
            vec[0] = -vec[0]
            if hitbord == 1:
                points += 1
                hitbord = 0
            best()
            if vec[0] < 0:
                vec[0] -= random.randint(0, 1)
            if vec[0] >= 0:
                vec[0] += random.randint(0, 1)
        elif colb2() == 2:
            vec[1] = -vec[1]
            box.bottom = box2.top
        elif colb2() == 3:
            vec[1] = -vec[1]
            box.top = box2.bottom
        if outs() == 0:
            pass
        elif outs() == 1:
            box.top = win.top
            hitbord = 1
        elif outs() == 2:
            box.bottom = win.bottom
            hitbord = 1
        elif outs() == 3:
            scr.blit(msg1, msg_box1)
            scr.blit(msg2, msg_box2)
            pygame.display.flip()
            lose1()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    if move(1) == 3:
                        box.top = win.top
                        box2.top = box.bottom
                    elif move(1) == 1:
                        box2.top = win.top
                    else:
                        box2 = box2.move(0, -STEP)
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if move(2) == 4:
                        box.bottom = win.bottom
                        box2.bottom = box.top
                    elif move(2) == 2:
                        box2.bottom = win.bottom
                    else:
                        box2 = box2.move(0, STEP)
                if event.key == pygame.K_ESCAPE:
                    goodbye()
        box = box.move(vec)
        fps.tick(SPEED)
        scr.fill(black)
        msg = myfont.render(f"Points: {points}", True, red)
        scr.blit(msg, msg_box)
        msgb = myfont.render(f"best score: {bs}", True, red)
        scr.blit(msgb, msgb_box)
        pygame.draw.rect(scr, white, box)
        pygame.draw.rect(scr, white, box2)
        pygame.display.flip()


def p2():
    '''
    main loop for 2 player mode
    '''
    global black, white, red, points, points2, SPEED, scr, win, box, box2
    global box3, fps, STEP, myfont, msg, msg1, msg2, msg3
    global msg_box, msg_box1, msg_box2, cou1, cou2, cou3
    box2 = pygame.Rect(0, 0, 30, 60)
    box.center = win.center
    box2.center = (0, win.centery)
    box3.center = (win.right, win.centery)
    scr.fill(black)
    pygame.draw.rect(scr, white, box)
    pygame.draw.rect(scr, white, box2)
    pygame.draw.rect(scr, white, box3)
    scr.blit(cou3, msg_box3)
    pygame.display.flip()
    pygame.time.wait(1000)
    scr.fill(black)
    pygame.draw.rect(scr, white, box)
    pygame.draw.rect(scr, white, box2)
    pygame.draw.rect(scr, white, box3)
    scr.blit(cou2, msg_box3)
    pygame.display.flip()
    pygame.time.wait(1000)
    scr.fill(black)
    pygame.draw.rect(scr, white, box)
    pygame.draw.rect(scr, white, box2)
    pygame.draw.rect(scr, white, box3)
    scr.blit(cou1, msg_box3)
    pygame.display.flip()
    pygame.time.wait(1000)
    points = 0
    points2 = 0
    pygame.key.set_repeat(50, 50)
    vec = [random.randint(1, 2), random.randint(1, 2)]
    if random.randint(0, 1) == 1:
        vec[1] = -vec[1]
    while True:
        if colwin() == 0:
            pass
        elif colwin() == 2:
            vec[1] = -vec[1]
        if colb2() == 0:
            pass
        elif colb2() == 1:
            vec[0] = -vec[0]
            points += 1
            if vec[0] < 0:
                vec[0] -= random.randint(0, 1)
            if vec[0] >= 0:
                vec[0] += random.randint(0, 1)
        elif colb2() == 2:
            vec[1] = -vec[1]
            box.bottom = box2.top
        elif colb2() == 3:
            vec[1] = -vec[1]
            box.top = box2.bottom
        if colb3() == 0:
            pass
        elif colb3() == 1:
            vec[0] = -vec[0]
            points2 += 1
            if vec[0] < 0:
                vec[0] -= random.randint(0, 1)
            if vec[0] >= 0:
                vec[0] += random.randint(0, 1)
        elif colb3() == 2:
            vec[1] = -vec[1]
            box.bottom = box3.top
        elif colb3() == 3:
            vec[1] = -vec[1]
            box.top = box3.bottom
        if outs() == 0:
            pass
        elif outs() == 1:
            box.top = win.top
        elif outs() == 2:
            box.bottom = win.bottom
        elif outs() == 3:
            msg1 = myfont.render("p2 wins", True, red)
            scr.blit(msg1, msg_box1)
            scr.blit(msg2, msg_box2)
            pygame.display.flip()
            lose2()
        elif outs() == 4:
            msg1 = myfont.render("p1 wins", True, red)
            scr.blit(msg1, msg_box1)
            scr.blit(msg2, msg_box2)
            pygame.display.flip()
            lose2()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if move(1) == 3:
                        box.top = win.top
                        box2.top = box.bottom
                    elif move(1) == 1:
                        box2.top = win.top
                    else:
                        box2 = box2.move(0, -STEP)
                if event.key == pygame.K_s:
                    if move(2) == 4:
                        box.bottom = win.bottom
                        box2.bottom = box.top
                    elif move(2) == 2:
                        box2.bottom = win.bottom
                    else:
                        box2 = box2.move(0, STEP)
                if event.key == pygame.K_UP:
                    if move2(1) == 3:
                        box.top = win.top
                        box3.top = box.bottom
                    elif move2(1) == 1:
                        box3.top = win.top
                    else:
                        box3 = box3.move(0, -STEP)
                if event.key == pygame.K_DOWN:
                    if move2(2) == 4:
                        box.bottom = win.bottom
                        box3.bottom = box.top
                    elif move2(2) == 2:
                        box3.bottom = win.bottom
                    else:
                        box3 = box3.move(0, STEP)
                if event.key == pygame.K_ESCAPE:
                    goodbye()
        box = box.move(vec)
        fps.tick(SPEED)
        scr.fill(black)
        msg = myfont.render(f"{points} - {points2}", True, red)
        scr.blit(msg, msg_box)
        pygame.draw.rect(scr, white, box)
        pygame.draw.rect(scr, white, box2)
        pygame.draw.rect(scr, white, box3)
        pygame.display.flip()


def menu():
    '''
    main menu
    '''
    while True:
        global msg3, msg_box3, red
        scr.fill(black)
        scr.blit(msg3, msg_box3)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    difficulty()
                if event.key == pygame.K_2:
                    p2()


if __name__ == "__main__":
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    pygame.init()
    points = 0
    points2 = 0
    SPEED = 100
    hitbord = 1
    scr = pygame.display.set_mode((600, 400))
    win = scr.get_rect()
    box = pygame.Rect(0, 0, 15, 15)
    box.center = win.center
    box2 = pygame.Rect(0, 0, 30, 60)
    box2.center = (0, win.centery)
    box3 = pygame.Rect(0, 0, 30, 60)
    box3.center = (win.right, win.centery)
    fps = pygame.time.Clock()
    STEP = 10
    myfont = pygame.font.Font('freesansbold.ttf', 20)
    myfontbig = pygame.font.Font('freesansbold.ttf', 40)
    msg = myfont.render(f"Points: {points}", True, red)
    msg_box = msg.get_rect()
    msg_box.center = [win.right - 60, win.top + 20]
    msg1 = myfont.render("Game Over", True, red)
    msg_box1 = msg1.get_rect()
    msg_box1.center = win.center
    msg2 = myfont.render("Quit(esc)? (r)estart? (m)enu?", True, red)
    msg_box2 = msg2.get_rect()
    msg_box2.center = [win.centerx, win.centery + 30]
    msg3 = myfont.render("(1)p or (2)p", True, red)
    msg_box3 = msg3.get_rect()
    msg_box3.center = win.center
    cou3 = myfontbig.render("3", True, red)
    cou2 = myfontbig.render("2", True, red)
    cou1 = myfontbig.render("1", True, red)
    bs = 0
    diff = 0
    msgb = myfont.render(f"best score: 0", True, red)
    msgb_box = msg.get_rect()
    msgb_box.center = [win.centerx, win.bottom - 30]
    menu()
