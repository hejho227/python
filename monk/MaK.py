'''
This code creates a game Missionaries and Cannibals
'''
import pygame
import sys
import random
SPEED = 400
WIN = (1200, 800)
CHARA = (50, 150)
RAF = (200, 60)
CEN = (0, 0)
BUTPOS = (400, 200)
BUTSIZE = (400, 200)
DEBUG = 0
BGNUM = 3
DELE = 500
BGCHANCE = 500
RAFTPOS1 = (270, 642)
RAFTPOS2 = (715, 642)
CULPOS1 = (1024, 520)
CULPOS = (400, 100)
PRIPOS = (700, 100)
HEADSIZE = (100, 100)
frames = 0
back = BGNUM
action = "listen"
MAXPASS = 2
LPOSX = [20, 75, 130, 20, 75, 20]
LPOSY = [436, 446, 457, 520, 556, 603]
RPOSX = [1130, 1005, 1100, 1140, 1040, 940]
RPOSY = [404, 585, 585, 685, 685, 685]
RAFTX = [270, 380, 725, 830]
RAFTY = 527
CULVAL = 10
PRIVAL = 1
NOACTORS = 3
step = 1


class charachters:
    '''
    Class for charachters
    '''
    def __init__(self, posx, posy, where, pic):
        '''
        initializacion for charachters

        0 arg is self
        1 arg is position on x axis
        2 arg is position on y axis
        3 arg is where is the character (1 - left, 2 - raft, 3 - right)
        4 arg is the picture
        '''
        self.positionx = posx
        self.positiony = posy
        self.where = where
        self.pic = pic

    def gotox(self, destination):
        '''
        goes to position on x axis
        '''
        while (self.positionx != destination):
            if self.positionx > destination:
                self.positionx -= step
            else:
                self.positionx += step
            show()

    def gotoy(self, destination):
        '''
        goes to position on y axis
        '''
        while (self.positiony != destination):
            if self.positiony > destination:
                self.positiony -= step
            else:
                self.positiony += step
            show()


def start():
    '''
    Starts the game and restarts it
    '''
    global gamestate, action
    gamestate = "0"
    action = "listen"
    star = 0
    cul1.positionx = LPOSX[0]
    cul1.positiony = LPOSY[0]
    cul2.positionx = LPOSX[1]
    cul2.positiony = LPOSY[1]
    cul3.positionx = LPOSX[2]
    cul3.positiony = LPOSY[2]
    pri1.positionx = LPOSX[3]
    pri1.positiony = LPOSY[3]
    pri2.positionx = LPOSX[4]
    pri2.positiony = LPOSY[4]
    pri3.positionx = LPOSX[5]
    pri3.positiony = LPOSY[5]
    cul1.where = 1
    cul2.where = 1
    cul3.where = 1
    pri1.where = 1
    pri2.where = 1
    pri3.where = 1
    raft.positionx = RAFTPOS1[0]
    raft.positiony = RAFTPOS1[1]
    raft.where = 1
    while (star != 1):
        check = 0
        xpos, ypos = pygame.mouse.get_pos()
        if xpos > BUTPOS[0] and xpos < BUTPOS[0] + BUTSIZE[0]:
            if ypos > BUTPOS[1] and ypos < BUTPOS[1] + BUTSIZE[1]:
                check = 1
        scr.blit(bgs, CEN)
        scr.blit(sta, BUTPOS)
        debug()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exi()
            if event.type == pygame.MOUSEBUTTONDOWN and check == 1:
                star = 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exi()
    gam()


def gam():
    '''
    Main game loop
    '''
    global bg, passagers, val, nopas, action, gamegraph, gamestate
    passagers = 0
    val = 0
    nopas = 0
    while True:
        if action == "listen":
            if getkey() == 1:
                if str(val) in gamegraph[gamestate]:
                    gamestate = gamegraph[gamestate][str(val)]
                    charachek()
                if action == "ferry":
                    ferry()
                if gamegraph[gamestate] == "failure":
                    action = "failure"
                elif gamegraph[gamestate] == "success":
                    action = "success"

        show()

        if action == "failure":
            failure()

        if action == "success":
            success()



def show():
    '''
    prints everything on a screen for game loop
    '''
    global bg, passagers, val, nopas
    bgcheck()
    fps = pygame.time.Clock()
    fps.tick(SPEED)
    scr.blit(bg, CEN)
    scr.blit(raft.pic, (raft.positionx, raft.positiony))
    scr.blit(cul1.pic, (cul1.positionx, cul1.positiony))
    scr.blit(cul2.pic, (cul2.positionx, cul2.positiony))
    scr.blit(cul3.pic, (cul3.positionx, cul3.positiony))
    scr.blit(pri1.pic, (pri1.positionx, pri1.positiony))
    scr.blit(pri2.pic, (pri2.positionx, pri2.positiony))
    scr.blit(pri3.pic, (pri3.positionx, pri3.positiony))
    scr.blit(priface, PRIPOS)
    scr.blit(culface, CULPOS)
    scr.blit(but2, BUTPOS)
    myfont = pygame.font.Font('freesansbold.ttf', 48)
    v1 = val % CULVAL
    v2 = int((val - v1) / CULVAL)
    msg1 = myfont.render(f"{v1}", True, (255, 0, 0))
    msg2 = myfont.render(f"{v2}", True, (255, 0, 0))
    msg1_box = msg1.get_rect()
    msg1_box.center = (PRIPOS[0] + HEADSIZE[0] / 2,
                       PRIPOS[1] + (2 * HEADSIZE[1]))
    msg2_box = msg2.get_rect()
    msg2_box.center = (CULPOS[0] + HEADSIZE[0] / 2,
                       CULPOS[1] + (2 * HEADSIZE[1]))
    scr.blit(msg1, msg1_box)
    scr.blit(msg2, msg2_box)
    debug()
    pygame.display.flip()


def debug():
    '''
    debug tool - shows values of position of mouse cursor
    '''
    if DEBUG == 1:
        xpos, ypos = pygame.mouse.get_pos()
        myfont = pygame.font.Font('freesansbold.ttf', 12)
        msg = myfont.render(f"{xpos}, {ypos}", True, (255, 0, 0))
        msg_box = msg.get_rect()
        msg_box.center = (xpos, ypos - 10)
        scr.blit(msg, msg_box)


def getkey():
    '''
    checks for keypresses and mouse presses
    returns 1 if user imput is correct
    '''
    global val, nopas
    done = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exi()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exi()
        check1 = 0
        check2 = 0
        check3 = 0
        xpos, ypos = pygame.mouse.get_pos()
        if xpos > CULPOS[0] and xpos < CULPOS[0] + HEADSIZE[0]:
            if ypos > CULPOS[1] and ypos < CULPOS[1] + HEADSIZE[1]:
                check1 = 1
        if xpos > PRIPOS[0] and xpos < PRIPOS[0] + HEADSIZE[0]:
            if ypos > PRIPOS[1] and ypos < PRIPOS[1] + HEADSIZE[1]:
                check2 = 1
        if xpos > BUTPOS[0] and xpos < BUTPOS[0] + BUTSIZE[0]:
            if ypos > BUTPOS[1] and ypos < BUTPOS[1] + BUTSIZE[1]:
                check3 = 1
        if event.type == pygame.MOUSEBUTTONDOWN and check1 == 1:
            val += 10
            nopas += 1
        elif event.type == pygame.MOUSEBUTTONDOWN and check2 == 1:
            val += 1
            nopas += 1
        elif event.type == pygame.MOUSEBUTTONDOWN and check3 == 1:
            if nopas > 0 and nopas < 3:
                done = 1
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                val += 1
                nopas += 1
            if event.key == pygame.K_c:
                val += 10
                nopas += 1
            if event.key == pygame.K_SPACE:
                if nopas > 0 and nopas < 3:
                    done = 1
        if nopas > 2:
            nopas = 0
            val = 0
    return done


def charachek():
    '''
    checks which type of charachter should be loaded on a boat
    '''
    global val, passagers, action
    while val > 0:
        if val >= CULVAL:
            val -= CULVAL
            if loadcheck(CULVAL) == 1:
                passagers += 1
        else:
            val -= PRIVAL
            if loadcheck(PRIVAL) == 1:
                passagers += 1
    if passagers > 0 and passagers < 3:
        action = "ferry"
    passagers = 0


def loadcheck(x):
    '''
    checks which instance of character type should get loaded

    accepts intigers for diferent characters that should get loaded
    returns 1 if successful
    '''
    if x == CULVAL:
        if cul1.where == raft.where:
            cul1.where = 2
            if passagers == 0:
                charachters.gotoy(cul1, RAFTY)
                if raft.where == 1:
                    charachters.gotox(cul1, RAFTX[0])
                else:
                    charachters.gotox(cul1, RAFTX[2])
            else:
                charachters.gotoy(cul1, RAFTY)
                if raft.where == 1:
                    charachters.gotox(cul1, RAFTX[1])
                else:
                    charachters.gotox(cul1, RAFTX[3])
            return 1
        elif cul2.where == raft.where:
            cul2.where = 2
            if passagers == 0:
                charachters.gotoy(cul2, RAFTY)
                if raft.where == 1:
                    charachters.gotox(cul2, RAFTX[0])
                else:
                    charachters.gotox(cul2, RAFTX[2])
            else:
                charachters.gotoy(cul2, RAFTY)
                if raft.where == 1:
                    charachters.gotox(cul2, RAFTX[1])
                else:
                    charachters.gotox(cul2, RAFTX[3])
            return 1
        elif cul3.where == raft.where:
            cul3.where = 2
            if passagers == 0:
                charachters.gotoy(cul3, RAFTY)
                if raft.where == 1:
                    charachters.gotox(cul3, RAFTX[0])
                else:
                    charachters.gotox(cul3, RAFTX[2])
            else:
                charachters.gotoy(cul3, RAFTY)
                if raft.where == 1:
                    charachters.gotox(cul3, RAFTX[1])
                else:
                    charachters.gotoy(cul3, RAFTX[3])
            return 1
    else:
        if pri1.where == raft.where:
            pri1.where = 2
            if passagers == 0:
                charachters.gotoy(pri1, RAFTY)
                if raft.where == 1:
                    charachters.gotox(pri1, RAFTX[0])
                else:
                    charachters.gotox(pri1, RAFTX[2])
            else:
                charachters.gotoy(pri1, RAFTY)
                if raft.where == 1:
                    charachters.gotox(pri1, RAFTX[1])
                else:
                    charachters.gotox(pri1, RAFTX[3])
            return 1
        elif pri2.where == raft.where:
            pri2.where = 2
            if passagers == 0:
                charachters.gotoy(pri2, RAFTY)
                if raft.where == 1:
                    charachters.gotox(pri2, RAFTX[0])
                else:
                    charachters.gotox(pri2, RAFTX[2])
            else:
                charachters.gotoy(pri2, RAFTY)
                if raft.where == 1:
                    charachters.gotox(pri2, RAFTX[1])
                else:
                    charachters.gotox(pri2, RAFTX[3])
            return 1
        elif pri3.where == raft.where:
            pri3.where = 2
            if passagers == 0:
                charachters.gotoy(pri3, RAFTY)
                if raft.where == 1:
                    charachters.gotox(pri3, RAFTX[0])
                else:
                    charachters.gotox(pri3, RAFTX[2])
            else:
                charachters.gotoy(pri3, RAFTY)
                if raft.where == 1:
                    charachters.gotox(pri3, RAFTX[1])
                else:
                    charachters.gotox(pri3, RAFTX[3])
            return 1


def ferry():
    '''
    Transports charachters on a raft and the raft itself to the other side
    '''
    fps = pygame.time.Clock()
    if raft.where == 1:
        while raft.positionx != RAFTPOS2[0]:
            raft.positionx += step
            if cul1.where == 2:
                cul1.positionx += step
            if cul2.where == 2:
                cul2.positionx += step
            if cul3.where == 2:
                cul3.positionx += step
            if pri1.where == 2:
                pri1.positionx += step
            if pri2.where == 2:
                pri2.positionx += step
            if pri3.where == 2:
                pri3.positionx += step
            show()
        unload(3)
        if cul1.where == 2:
            cul1.where = 3
        if cul2.where == 2:
            cul2.where = 3
        if cul3.where == 2:
            cul3.where = 3
        if pri1.where == 2:
            pri1.where = 3
        if pri2.where == 2:
            pri2.where = 3
        if pri3.where == 2:
            pri3.where = 3
        raft.where = 3
        return 0
    if raft.where == 3:
        while raft.positionx != RAFTPOS1[0]:
            raft.positionx -= step
            if cul1.where == 2:
                cul1.positionx -= step
            if cul2.where == 2:
                cul2.positionx -= step
            if cul3.where == 2:
                cul3.positionx -= step
            if pri1.where == 2:
                pri1.positionx -= step
            if pri2.where == 2:
                pri2.positionx -= step
            if pri3.where == 2:
                pri3.positionx -= step
            show()
        unload(1)
        if cul1.where == 2:
            cul1.where = 1
        if cul2.where == 2:
            cul2.where = 1
        if cul3.where == 2:
            cul3.where = 1
        if pri1.where == 2:
            pri1.where = 1
        if pri2.where == 2:
            pri2.where = 1
        if pri3.where == 2:
            pri3.where = 1
        raft.where = 1
        return 0


def unload(x):
    '''
    unloads charachters from a raft
    '''
    global action
    if x == 3:
        if cul1.where == 2:
            charachters.gotox(cul1, RPOSX[0])
            charachters.gotoy(cul1, RPOSY[0])
        if cul2.where == 2:
            charachters.gotox(cul2, RPOSX[1])
            charachters.gotoy(cul2, RPOSY[1])
        if cul3.where == 2:
            charachters.gotox(cul3, RPOSX[2])
            charachters.gotoy(cul3, RPOSY[2])
        if pri1.where == 2:
            charachters.gotox(pri1, RPOSX[3])
            charachters.gotoy(pri1, RPOSY[3])
        if pri2.where == 2:
            charachters.gotox(pri2, RPOSX[4])
            charachters.gotoy(pri2, RPOSY[4])
        if pri3.where == 2:
            charachters.gotox(pri3, RPOSX[5])
            charachters.gotoy(pri3, RPOSY[5])
    if x == 1:
        if cul1.where == 2:
            charachters.gotox(cul1, LPOSX[0])
            charachters.gotoy(cul1, LPOSY[0])
        if cul2.where == 2:
            charachters.gotox(cul2, LPOSX[1])
            charachters.gotoy(cul2, LPOSY[1])
        if cul3.where == 2:
            charachters.gotox(cul3, LPOSX[2])
            charachters.gotoy(cul3, LPOSY[2])
        if pri1.where == 2:
            charachters.gotox(pri1, LPOSX[3])
            charachters.gotoy(pri1, LPOSY[3])
        if pri2.where == 2:
            charachters.gotox(pri2, LPOSX[4])
            charachters.gotoy(pri2, LPOSY[4])
        if pri3.where == 2:
            charachters.gotox(pri3, LPOSX[5])
            charachters.gotoy(pri3, LPOSY[5])
    action = "listen"


def bgcheck():
    '''
    checks if there should be a change of background animation
    '''
    global back, frames
    if back == BGNUM and random.randint(1, BGCHANCE) == 1 and frames > DELE:
        back = 1
        frames = 0
        background(back)
    elif back < BGNUM and frames > DELE:
        back += 1
        background(back)
        frames = 0
    else:
        frames += 1


def background(x):
    '''
    checks which bg pic should be next

    accepts difrent intigers for difrent bg pics
    '''
    global bg
    if x == 1:
        bg = pygame.transform.scale(pygame.image.load('pics/bg2.png'), WIN)
    elif x == 2:
        bg = pygame.transform.scale(pygame.image.load('pics/bg3.png'), WIN)
    else:
        bg = pygame.transform.scale(pygame.image.load('pics/bg1.png'), WIN)


def failure():
    '''
    takes care of failed attempts
    '''
    myfont = pygame.font.Font('freesansbold.ttf', 48)
    msg = myfont.render("Failure", True, (255, 0, 0))
    msg_box = msg.get_rect()
    msg_box.center = win.center
    scr.blit(bg, CEN)
    scr.blit(gover, CEN)
    pygame.display.flip()
    scr.blit(msg, msg_box)
    pygame.display.flip()
    pygame.time.wait(5000)
    start()


def success():
    '''
    takes care of succesful attempts
    '''
    scr.blit(bgs, WIN)
    myfont = pygame.font.Font('freesansbold.ttf', 48)
    msg = myfont.render("SUCCESS!", True, (255, 0, 0))
    msg_box = msg.get_rect()
    msg_box.center = win.center
    scr.blit(msg, msg_box)
    pygame.display.flip()
    pygame.time.wait(1000)
    start()


def exi():
    '''
    exits the game
    '''
    pygame.image.save(scr, "game-over.bmp")
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    pygame.font.init()
    passagers = 0
    val = 0
    nopas = 0
    cul1 = charachters(LPOSX[0], LPOSY[0], 1,
                       pygame.transform.scale
                       (pygame.image.load('pics/cultist.png'), CHARA))
    cul2 = charachters(LPOSX[1], LPOSY[1], 1,
                       pygame.transform.scale
                       (pygame.image.load('pics/cultist.png'), CHARA))
    cul3 = charachters(LPOSX[2], LPOSY[2], 1,
                       pygame.transform.scale
                       (pygame.image.load('pics/cultist.png'), CHARA))
    pri1 = charachters(LPOSX[3], LPOSY[3], 1,
                       pygame.transform.scale
                       (pygame.image.load('pics/prist.png'), CHARA))
    pri2 = charachters(LPOSX[4], LPOSY[4], 1,
                       pygame.transform.scale
                       (pygame.image.load('pics/prist.png'), CHARA))
    pri3 = charachters(LPOSX[5], LPOSY[5], 1,
                       pygame.transform.scale
                       (pygame.image.load('pics/prist.png'), CHARA))
    raft = charachters(RAFTPOS1[0], RAFTPOS1[1], 1, pygame.transform.scale(
                                     pygame.image.load('pics/raft.png'), RAF))
    culface = pygame.transform.scale(pygame.image.load
                                     ('pics/culhead.png'), HEADSIZE)
    priface = pygame.transform.scale(pygame.image.load
                                     ('pics/prihead.png'), HEADSIZE)
    but2 = pygame.transform.scale(pygame.image.load('pics/go.png'), BUTSIZE)
    bg = pygame.transform.scale(pygame.image.load('pics/bg1.png'), WIN)
    gover = pygame.transform.scale(pygame.image.load('pics/gover.png'), WIN)
    bgs = pygame.transform.scale(pygame.image.load('pics/start.png'), WIN)
    sta = pygame.transform.scale(pygame.image.load('pics/play.png'), BUTSIZE)
    scr = pygame.display.set_mode(WIN)
    win = scr.get_rect()

    gamegraph = {
        "0": {"1": "1", "2": "2", "11": "11r", "10": "10r", "20": "20r"},
        "10r": {"10": "0"},
        "11r": {"1": "10l", "10": "1", "11": "0"},
        "10l": {"1": "11r", "2": "12", "10": "20r", "20": "30r", "11": "21"},
        "20r": {"10": "10l", "20": "0"},
        "30r": {"10": "20l", "20": "10l"},
        "20l": {"1": "21", "2": "22r", "10": "30r", "11": "31"},
        "22r": {"1": "21", "2": "20l", "10": "12", "20": "2", "11": "11l"},
        "11l": {"1": "12", "2": "13r", "10": "21", "20": "31", "11": "22r"},
        "13r": {"1": "12", "2": "11l", "10": "3l", "11": "2"},
        "3l": {"10": "13r", "20": "23r"},
        "23r": {"1": "22l", "2": "21", "10": "13l", "20": "3l", "11": "12"},
        "13l": {"10": "23r", "20": "33"},
        "22l": {"1": "23r", "10": "32", "11": "33"},
        "1": "failure",
        "2": "failure",
        "12": "failure",
        "21": "failure",
        "31": "failure",
        "32": "failure",
        "33": "success",
    }
    gamestate = "0"
    start()
