'''
This code creates the SHOOTOUT game
'''
import pygame
import sys
import random
import math

from pygame.sprite import Group
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (241, 213, 38)
CHARA = (75, 150)
XGDISPLACEMENT = 10
CORANG = 180
CURSSIZE = (25, 25)
GUNSIZE = (50, 20)
BULLSIZE = (20, 20)
SPREAD = 50
BULLSPEED = 5
DELEY = 100
DEL2 = 20
DEBUG = 0
IDLECHANCE = 100
SPEED = 140
WIN = (1920, 1080)
MAXROLLTIME = 50
RELBOUN = (2, 11)
RELMAIN = (75, 1)
RELMOVE = (2, 11)
MOVECHANGE = 100
STARTINGHP = 6
STARTINGHP2 = 3
RELUP = 10
RECOIL = 10
STEP = 2
SLOW = 1
AMMO1 = 6
AMMO2 = 1
AMMO3 = 15
GDEL = 1
GDEL2 = 2
GDEL3 = 5
DISTEXT = 150
DIS1 = 450
DIS2 = CHARA[1]
ROTANG = 90
BGFRAME = 5
ARROW = (175, 50)
HEROINVINC = 1
HEALSPAWN = 5
HEALRATE = 2
HEROID = 1
SHOTID = 2
MELEID = 3
MACHID = 4
CONVERT = math.pi / 180
CANSTEP = 5
CANIMA0 = 0
CANIMA1 = 1
CANIMA2 = 2
CANIMA3 = 3
CMAINGA = 4
CPAUSE = 5
FONTSIZE = 48
SFONTSIZE = 12
NEROOM1 = 5
NEROOM2 = 10
NEROOM3 = 15
HANI1 = 1
HANI2 = 2
HANI3 = 3
HANI4 = 4
HANI5 = 5
HANI6 = 6
HANI7 = 7
HANI8 = 8
scr = pygame.display.set_mode(WIN)
win = scr.get_rect()


class game():
    '''
    class for storing "global" variables
    '''
    badies = 0
    rooms = 1
    timer = 0
    idletimer = 0
    lastx = 0
    lasty = 0
    done = False
    bullkill = 0
    enekill = 0
    shot = 0
    left = 0
    right = 0
    middle = 0
    createdhealth = 0
    mx = 0
    my = 0
    bg = (pygame.image.load('assets/background/bg.png')).convert()


class player(pygame.sprite.Sprite):
    '''
    class for charachters
    '''
    def __init__(self, xcord, ycord, type):
        super().__init__()
        self.type = type
        self.gdelay = DEL2
        self.greltime = GDEL
        if self.type == HEROID:
            self.sgammo = AMMO1
            self.gammo = self.sgammo
            self.hp = STARTINGHP
            self.lasthp = STARTINGHP
            self.sprite = pygame.image.load('assets/hero/hero.png')
            self.gsprite = pygame.image.load('assets/weapons/gun.png')
        elif self.type == SHOTID:
            self.sgammo = AMMO2
            self.gammo = self.sgammo
            self.hp = STARTINGHP2
            self.lasthp = STARTINGHP2
            self.sprite = pygame.image.load('assets/enemies/enemy1.png')
            self.gsprite = pygame.image.load('assets/weapons/gun.png')
        elif self.type == MELEID:
            self.sgammo = AMMO2
            self.gammo = self.sgammo
            self.hp = STARTINGHP2
            self.lasthp = STARTINGHP2
            self.sprite = pygame.image.load('assets/enemies/enemy1.png')
            self.gsprite = pygame.image.load('assets/weapons/knife.png')
        elif self.type == MACHID:
            self.sgammo = AMMO3
            self.gammo = self.sgammo
            self.hp = STARTINGHP2
            self.lasthp = STARTINGHP2
            self.sprite = pygame.image.load('assets/enemies/enemy2.png')
            self.gsprite = pygame.image.load('assets/weapons/gun.png')
            self.greltime = GDEL
        self.x = xcord
        self.y = ycord
        self.rect = self.sprite.get_rect()
        self.facing = 1
        self.picfac = 1
        self.gf = self.facing
        self.hitable = 1
        self.isrolling = 0
        self.wasrolling = 0
        self.picstate = 1
        self.gx = xcord
        self.gy = ycord
        self.grect = self.sprite.get_rect()
        self.gtimer = DEL2
        self.grel = 0
        self.rolltimer = 0
        self.gfired = 0
        self.walktimer = 0
        self.newgun = 0
        self.newgunrect = 0
        self.speedx = 0
        self.speedy = 0
        self.ran = 0
        self.rantime = 0

    def update(self):
        '''
        main loop for enemy "ai"
        '''
        if cursor.stage != 5:
            self.supdate(0, self.type)
            if self.isrolling == 0:
                self.behavior()
                self.wupdate(hero.x, hero.y)
        scr.blit(self.newgun, self.newgunrect)
        if self.hitable == 1:
            if pygame.sprite.spritecollide(self, fbulletgroup, True):
                self.hp -= 1
            if self.hp <= 0 or game.enekill == 1:
                self.kill()
                game.badies -= 1
        scr.blit(self.sprite, self.rect)

    def behavior(self):
        '''
        handles behavior of opponents
        '''
        if self.gtimer >= self.gdelay:
            if self.grel == 0:
                if self.gammo > 0:
                    if random.randint(0, 20) == 0:
                        if self.type == SHOTID:
                            ebulletgroup.add(player.hcreatebullet(
                                self, hero.x - SPREAD, hero.y - SPREAD, 2))
                            ebulletgroup.add(player.hcreatebullet(
                                self, hero.x + SPREAD, hero.y + SPREAD, 2))
                            shot3.sfx.play()
                            self.gtimer = 0
                            self.gfired = 1
                        elif self.type == MACHID:
                            ebulletgroup.add(player.hcreatebullet(
                                self, hero.x, hero.y, 2))
                            shot2.sfx.play()
                            self.gtimer = 0
                            self.gfired = 1
                        elif self.type == MELEID:
                            d = math.sqrt(pow((self.x - hero.x), 2) + pow(
                                (self.y - hero.y), 2))
                            if d <= DIS2:
                                herohit2()
                                self.grel = 1
                else:
                    self.grel = 1
        if self.grel != 0:
            if self.grel >= self.greltime * SPEED:
                self.grel = 0
                self.gammo = self.sgammo
            else:
                self.grel += 1
        d = math.sqrt(pow((self.x - hero.x), 2) + pow((self.y - hero.y), 2))
        if d > DIS1 or (self.type == MELEID and d > DIS2):
            if random.randint(1, 2) == 2:
                dx, dy = self.x - hero.x, hero.y - self.y
                tg = math.degrees(math.atan2(dy, dx))
                angle = tg * math.pi / 180
                if game.timer - self.rantime > MOVECHANGE and\
                        self.type == SHOTID:
                    self.ran = random.randint(0, 90)
                    self.rantime = game.timer
                self.speedx = -SLOW * math.cos(angle + self.ran)
                self.speedy = SLOW * math.sin(angle + self.ran)
        else:
            self.speedx = 0
            self.speedy = 0

    def wupdate(self, xpos, ypos):
        '''
        handles weapon update
        '''
        if self.type != MELEID:
            if self.gfired == 1 and self.gtimer <= self.gdelay / 2:
                correction = RECOIL * self.gtimer / self.gdelay
            elif self.gfired == 1 and self.gtimer < self.gdelay:
                correction = (RECOIL * 1/2) - (RECOIL * (
                    self.gtimer % (self.gdelay / 2)) / self.gdelay)
            else:
                correction = 0
            if self.facing == 1:
                if self.gf != self.facing:
                    self.gsprite = pygame.transform.flip(
                        self.gsprite, True, False)
                    self.gf = self.facing
                self.gx = self.x + CHARA[0] + XGDISPLACEMENT
                self.gy = self.y + CHARA[1] / 2
                dx = xpos - self.gx
                dy = self.gy - ypos
                angle = math.degrees(math.atan2(dy, dx)) + correction
            else:
                if self.gf != self.facing:
                    self.gsprite = pygame.transform.flip(
                        self.gsprite, True, False)
                    self.gf = self.facing
                self.gx = self.x - XGDISPLACEMENT
                self.gy = self.y + CHARA[1] / 2
                dx = xpos - self.gx
                dy = self.gy - ypos
                angle = math.degrees(math.atan2(dy, dx)) - CORANG - correction
            self.newgun = pygame.transform.rotate(self.gsprite, angle)
            self.newgunrect = self.newgun.get_rect()
            self.newgunrect.center = (self.gx, self.gy)
            self.gtimer += 1
        else:
            self.newgun = self.gsprite
            self.gx = self.x - XGDISPLACEMENT
            self.gy = self.y + CHARA[1]/2
            self.newgunrect = self.newgun.get_rect()
            self.newgunrect.center = (self.gx, self.gy)

    def supdate(self, pressed, who):
        '''
        Checks mouse position, if it should change the direction charachter
        is looking in changes the position of the charachter
        Is resposible for all movement

        accepts intiger with amount of key pressed and for whom to
        do the calculation
        1 = hero
        2 = enemy
        returns amount of keys pressed and mouse movements
        that changed direction in which the charachter is looking
        '''
        if who == HEROID:
            img = pygame.image.load('assets/hero/hero.png')
        elif who == MACHID:
            img = pygame.image.load('assets/enemies/enemy2.png')
        elif who >= SHOTID:
            img = pygame.image.load('assets/enemies/enemy1.png')
        if self.isrolling == 0:
            if who == HEROID:
                if game.mx > self.x + CHARA[0]/2:
                    self.facing = 1
                elif game.mx < self.x + CHARA[0]/2:
                    self.facing = 2
            else:
                if hero.x > self.x + CHARA[0]/2:
                    self.facing = 1
                elif hero.x < self.x + CHARA[0]/2:
                    self.facing = 2
            if self.facing == 1 and self.picfac != 1:
                self.sprite = img
                pressed += 1
                self.picfac = 1
            elif self.facing == 2 and self.picfac != 2:
                self.sprite = pygame.transform.flip(img, True, False)
                pressed += 1
                self.picfac = 2
        if self.isrolling == 1:
            self.x += self.speedx
            self.y += self.speedy
            if self.hitable == 1:
                self.hitable = 0
                self.wasrolling = 1
            if self.picfac == 1:
                self.sprite = pygame.transform.rotate(img, -ROTANG)
                self.picfac = 10
            else:
                transformat = pygame.transform.rotate(img, ROTANG)
                self.sprite = pygame.transform.flip(
                    transformat, False, True)
                self.picfac = 10

        self.x = max(min(WIN[0] - CHARA[0] - BGFRAME,
                         self.x + self.speedx), BGFRAME)
        self.y = max(min(WIN[1] - CHARA[1] - BGFRAME, self.y + self.speedy), 0)
        self.rect.center = (self.x + CHARA[0] / 2, self.y + CHARA[1] / 2)
        return pressed

    def rollupdate(self):
        '''
        makes sure that the rolls take specified amount of time
        '''
        if self.isrolling == 1:
            self.rolltimer += 1
        if self.rolltimer >= MAXROLLTIME:
            self.rolltimer = 0
            self.isrolling = 0
            self.wasrolling = 0
            self.hitable = 1

    def hcreatebullet(self, xpos, ypos, friend):
        '''
        creates bullets
        '''
        self.gammo -= 1
        return bullets(self.gx, self.gy, xpos, ypos, friend)

    def createhealth(self):
        '''
        creates a health pack
        '''
        return uti()


class sfx():
    '''
    class for souds
    '''
    def __init__(self, path):
        self.sfx = pygame.mixer.Sound(path)
        self.instances = 0


class uti(pygame.sprite.Sprite):
    '''
    class for health packs
    '''
    def __init__(self):
        super().__init__()
        self.sprite = pygame.image.load('assets/other/health.png')
        self.rect = self.sprite.get_rect()
        self.rect.center = win.center

    def update(self):
        '''
        checks if healthpack colides with the player rises hp

        responsible for killing self
        '''
        scr.blit(self.sprite, win.center)
        if game.rooms % 5 != 0:
            self.kill()
        if pygame.sprite.collide_rect(self, hero):
            hero.hp = min(STARTINGHP, hero.hp + HEALRATE)
            self.kill()


class cursors:
    '''
    class for cursor and controling game stage
    '''
    def __init__(self, sprite):
        self.image = sprite
        self.rect = self.image.get_rect()
        self.stage = 0
        self.cooldown = 0

    def update(self):
        '''
        updates position of the cursor and blits its sprite
        '''
        xpos, ypos = pygame.mouse.get_pos()
        scr.blit(self.image, (xpos - CURSSIZE[0] / 2, ypos - CURSSIZE[1] / 2))


class bullets(pygame.sprite.Sprite):
    '''
    class for bullets
    '''
    def __init__(self, posx, posy, xpos, ypos, friend):
        super().__init__()
        self.image = pygame.Surface(BULLSIZE)
        if friend == 1:
            self.image.fill(YELLOW)
        else:
            self.image.fill(RED)
        self.rect = self.image.get_rect(center=(posx, posy))
        dx, dy = xpos - posx, posy - ypos
        tg = math.degrees(math.atan2(dy, dx))
        angle = tg * CONVERT
        self.speedx = BULLSPEED * math.cos(angle)
        self.speedy = -BULLSPEED * math.sin(angle)

    def update(self):
        '''
        updates the position of the bullets
        '''
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.x >= WIN[0] or self.rect.x <= 0:
            self.kill()
        if self.rect.y >= WIN[1] or self.rect.y <= 0:
            self.kill()
        if game.bullkill == 1:
            self.kill()


class text:
    '''
    class for text in form of premade graphics
    '''
    def __init__(self, pic, y):
        self.image = pygame.transform.scale2x(pygame.image.load(pic))
        self.rect = self.image.get_rect()
        self.rect.center = (0, y)
        self.rect.right = 0
        self.hover = 0


def main():
    '''
    main game loop
    '''
    game.badies = 0
    game.rooms = 0
    game.timer = 0
    game.idletimer = 0
    game.lastx = 0
    game.lasty = 0
    game.done = False
    game.bullkill = 0
    game.shot = 0
    game.createdhealth = 0
    game.bg = (pygame.image.load('assets/background/bg.png')).convert()
    hero.x = starx
    hero.y = stary
    cursor.stage = CANIMA0
    hero.hp = STARTINGHP
    name.rect.right = win.left
    play.rect.right = win.left
    quit.rect.right = win.left
    hero.isrolling = 0
    while not game.done:
        game.left, game.middle, game.right = pygame.mouse.get_pressed()
        game.mx, game.my = pygame.mouse.get_pos()
        if cursor.stage < CMAINGA:
            mainmenu()
        elif hero.hp <= 0:
            cursor.stage = CPAUSE
        if cursor.stage == CMAINGA:
            game.timer += 1
            if game.shot == 0 and game.left == 0:
                hero.gammo = hero.sgammo
                game.bullkill = 1
                fbulletgroup.update()
                ebulletgroup.update()
                game.bullkill = 0
                game.shot = 1
            if hero.isrolling == 0:
                hero.speedx = 0
                hero.speedy = 0
                pressed = getkeys()
            pressed = hero.supdate(pressed, 1)
            hero.rollupdate()
            game.lastx = game.mx
            game.lasty = game.my
            if pressed > 0:
                game.idletimer = 0
            else:
                game.idletimer += 1
            if idlehero() == 1:
                game.idletimer = 0
            show()
            herohit()
            nextcheck()
        elif cursor.stage == CPAUSE:
            pause()
        quitcheck()


def spawn(mele, shotgun, machin, all):
    '''
    handles spawning enemies

    accepts 4x int one for each type of enemies and 1 for combined
    '''
    for i in range(mele):
        x = random.randint(int(WIN[0] / 2), WIN[0])
        y = random.randint(0, WIN[1])
        enemiesgroup.add(player(x, y, MELEID))
        game.badies += 1
    for i in range(shotgun):
        x = random.randint(int(WIN[0] / 2), WIN[0])
        y = random.randint(0, WIN[1])
        enemiesgroup.add(player(x, y, SHOTID))
        game.badies += 1
    for i in range(machin):
        x = random.randint(int(WIN[0] / 2), WIN[0])
        y = random.randint(0, WIN[1])
        enemiesgroup.add(player(x, y, MACHID))
        game.badies += 1
    for i in range(all):
        rand = random.randint(2, 4)
        x = random.randint(int(WIN[0] / 2), WIN[0])
        y = random.randint(0, WIN[1])
        enemiesgroup.add(player(x, y, rand))
        game.badies += 1


def mainmenu():
    '''
    main loop for main menu
    '''
    scr.blit(bg1, win.topleft)
    scr.blit(name.image, name.rect)
    scr.blit(play.image, play.rect)
    scr.blit(quit.image, quit.rect)
    animat()
    mousecheck()
    cursors.update(cursor)
    flip()


def animat():
    '''
    handles text slide animation when entering the game for the first time
    '''
    if cursor.stage == CANIMA0:
        if name.rect.center[0] != WIN[0] / 2:
            name.rect.right += CANSTEP
        else:
            cursor.stage = CANIMA1
    elif cursor.stage == CANIMA1:
        if play.rect.center[0] != WIN[0] / 2:
            play.rect.right += CANSTEP
        else:
            cursor.stage = CANIMA2
    elif cursor.stage == CANIMA2:
        if quit.rect.center[0] != WIN[0] / 2:
            quit.rect.right += CANSTEP
        else:
            cursor.stage = CANIMA3
    if game.left:
        name.rect.center = (WIN[0] / 2, name.rect.center[1])
        play.rect.center = (WIN[0] / 2, play.rect.center[1])
        quit.rect.center = (WIN[0] / 2, quit.rect.center[1])
        cursor.stage = CANIMA3


def mousecheck():
    '''
    checks positon of the mouse, changes sprites of the text

    handles quiting from main menu and starting actual game
    '''
    if play.rect.collidepoint(game.mx, game.my):
        if play.hover == 0:
            pic = pygame.image.load('assets/other/play2.png')
            play.image = pygame.transform.scale2x(pic)
            play.hover = 1
        if game.left:
            cursor.stage = CMAINGA
            game.bullkill = 1
    elif play.hover == 1:
        pic = pygame.image.load('assets/other/play1.png')
        play.image = pygame.transform.scale2x(pic)
        play.hover = 0
    if quit.rect.collidepoint(game.mx, game.my):
        if quit.hover == 0:
            pic = pygame.image.load('assets/other/quit2.png')
            quit.image = pygame.transform.scale2x(pic)
            quit.hover = 1
        if game.left:
            sys.exit()
    elif quit.hover == 1:
        pic = pygame.image.load('assets/other/quit1.png')
        quit.image = pygame.transform.scale2x(pic)
        quit.hover = 0


def pause():
    '''
    main loop for pause
    '''
    show()
    scr.blit(menu, menu_rect)
    if hero.hp > 0:
        scr.blit(resu.image, resu.rect)
    scr.blit(retu.image, retu.rect)
    scr.blit(quit.image, quit.rect)
    mousecheck2()
    cursors.update(cursor)
    flip()
    quitcheck()


def mousecheck2():
    '''
    checks positon of the mouse, changes sprites of the text

    handles quiting from pause menu and restarting the game
    '''
    if resu.rect.collidepoint(game.mx, game.my):
        if resu.hover == 0:
            pic = pygame.image.load('assets/other/resume2.png')
            resu.image = pygame.transform.scale2x(pic)
            resu.hover = 1
        if game.left:
            cursor.stage = CMAINGA
    elif resu.hover == 1:
        pic = pygame.image.load('assets/other/resume1.png')
        resu.image = pygame.transform.scale2x(pic)
        resu.hover = 0
    if retu.rect.collidepoint(game.mx, game.my):
        if retu.hover == 0:
            pic = pygame.image.load('assets/other/return2.png')
            retu.image = pygame.transform.scale2x(pic)
            retu.hover = 1
        if game.left:
            game.enekill = 1
            enemiesgroup.update()
            game.enekill = 0
            main()
    elif retu.hover == 1:
        pic = pygame.image.load('assets/other/return1.png')
        retu.image = pygame.transform.scale2x(pic)
        retu.hover = 0
    if quit.rect.collidepoint(game.mx, game.my):
        if quit.hover == 0:
            pic = pygame.image.load('assets/other/quit2.png')
            quit.image = pygame.transform.scale2x(pic)
            quit.hover = 1
        if game.left:
            sys.exit()
    elif quit.hover == 1:
        pic = pygame.image.load('assets/other/quit1.png')
        quit.image = pygame.transform.scale2x(pic)
        quit.hover = 0


def flip():
    '''
    displays the queued things
    '''
    pygame.display.flip()


def getkeys():
    '''
    Checks for button presses

    accetpst int with no. of frames walked
    returns the amount of them
    '''
    global walktimer
    keys = pygame.key.get_pressed()
    inputpressed = 0
    if keys[pygame.K_d]:
        hero.speedx += STEP
        inputpressed += 1
    if keys[pygame.K_a]:
        hero.speedx -= STEP
        inputpressed += 1
    if keys[pygame.K_w]:
        hero.speedy -= STEP
        inputpressed += 1
    if keys[pygame.K_s]:
        hero.speedy += STEP
        inputpressed += 1
    if keys[pygame.K_r] and hero.gammo < AMMO1 and hero.grel == 0:
        hero.grel = 1
        inputpressed += 1
    if inputpressed > 0:
        walktimer += 1
    else:
        walktimer = 0
    if inputpressed >= 1 and walktimer > DEL2:
        walkhero()
    if game.left:
        if hero.gtimer >= hero.gdelay and hero.grel == 0:
            if hero.gammo > 0:
                fbulletgroup.add(
                    player.hcreatebullet(hero, game.mx, game.my, 1))
                shot.sfx.play()
                hero.gfired = 1
                hero.gtimer = 0
            else:
                hero.grel = 1
        inputpressed += 1
    testspeed = STEP * hero.speedx + hero.speedy
    if game.right and testspeed != 0:
        hero.isrolling = 1
        inputpressed += 1
    if game.mx != game.lastx or game.my != game.lasty:
        inputpressed += 1
    return inputpressed


def walkhero():
    '''
    handles walking animation for the hero
    '''
    walktimer = 0
    if hero.picfac == 1:
        if hero.picstate == 1:
            hero.picstate = -1
            hero.sprite = pygame.image.load('assets/hero/herowalk1.png')
        elif hero.picstate == -1:
            hero.picstate = -2
            hero.sprite = pygame.image.load('assets/hero/herowalk2.png')
        else:
            hero.picstate = 1
            hero.sprite = pygame.image.load('assets/hero/hero.png')
    else:
        if hero.picstate == 1:
            hero.picstate = -1
            hero.sprite = pygame.transform.flip(
                pygame.image.load('assets/hero/herowalk1.png'), True, False)
        elif hero.picstate == -1:
            hero.picstate = -2
            hero.sprite = pygame.transform.flip(
                pygame.image.load('assets/hero/herowalk2.png'), True, False)
        else:
            hero.picstate = 1
            hero.sprite = pygame.transform.flip(
                pygame.image.load('assets/hero/hero.png'), True, False)


def idlehero():
    '''
    Code for idle animation
    '''
    if (hero.picstate == HANI8 and game.idletimer >= DELEY) \
            or (hero.picstate < 0 and game.idletimer > 0):
        if hero.picfac == 1:
            hero.sprite = pygame.image.load('assets/hero/hero.png')
            hero.picstate = HANI1
        if hero.picfac == 2:
            hero.sprite = pygame.transform.flip(
                pygame.image.load('assets/hero/hero.png'), True, False)
            hero.picstate = HANI1
        return 1
    if hero.picstate == HANI1:
        if game.idletimer >= DELEY and random.randint(1, IDLECHANCE) == 1:
            hero.picstate = HANI2
            if hero.picfac == 1:
                hero.sprite = pygame.image.load('assets/hero/heroidle2.png')
            elif hero.picfac == 2:
                hero.sprite = pygame.transform.flip(
                    pygame.image.load('assets/hero/heroidle2.png'), True, False)
            return 1
    if hero.picstate == HANI2 and game.idletimer >= DELEY:
        hero.picstate = HANI3
        if hero.picfac == 1:
            hero.sprite = pygame.image.load('assets/hero/heroidle3.png')
        elif hero.picfac == 2:
            hero.sprite = pygame.transform.flip(
                pygame.image.load('assets/hero/heroidle3.png'), True, False)
        return 1
    if hero.picstate == HANI3 and game.idletimer >= DELEY:
        hero.picstate = HANI4
        if hero.picfac == 1:
            hero.sprite = pygame.image.load('assets/hero/heroidle4.png')
        elif hero.picfac == 2:
            hero.sprite = pygame.transform.flip(
                pygame.image.load('assets/hero/heroidle4.png'), True, False)
        return 1
    if hero.picstate == HANI4 and game.idletimer >= DELEY:
        hero.picstate = HANI5
        if hero.picfac == 1:
            hero.sprite = pygame.image.load('assets/hero/heroidle5.png')
        elif hero.picfac == 2:
            hero.sprite = pygame.transform.flip(
                pygame.image.load('assets/hero/heroidle5.png'), True, False)
        return 1
    if hero.picstate == HANI5 and game.idletimer >= DELEY:
        hero.picstate = HANI6
        if hero.picfac == 1:
            hero.sprite = pygame.image.load('assets/hero/heroidle6.png')
        elif hero.picfac == 2:
            hero.sprite = pygame.transform.flip(
                pygame.image.load('assets/hero/heroidle6.png'), True, False)
        return 1
    if hero.picstate == HANI6 and game.idletimer >= DELEY:
        hero.picstate = HANI7
        if hero.picfac == 1:
            hero.sprite = pygame.image.load('assets/hero/heroidle7.png')
        elif hero.picfac == 2:
            hero.sprite = pygame.transform.flip(
                pygame.image.load('assets/hero/heroidle7.png'), True, False)
        return 1
    if hero.picstate == HANI7 and game.idletimer >= DELEY:
        hero.picstate = HANI8
        if hero.picfac == 1:
            hero.sprite = pygame.image.load('assets/hero/heroidle8.png')
        elif hero.picfac == 2:
            hero.sprite = pygame.transform.flip(
                pygame.image.load('assets/hero/heroidle8.png'), True, False)
        return 1


def show():
    '''
    queues all the sprites in the actual game
    '''
    fps = pygame.time.Clock()
    fps.tick(SPEED)
    scr.blit(game.bg, win.topleft)
    if cursor.stage != CPAUSE:
        fbulletgroup.update()
        ebulletgroup.update()
        healgroup.update()
        if hero.grel != 0:
            reload()
    fbulletgroup.draw(scr)
    ebulletgroup.draw(scr)
    scr.blit(hero.sprite, hero.rect)
    if game.badies == 0:
        scr.blit(arrow, (WIN[0] - ARROW[0], (WIN[1] - ARROW[1]) / 2))
        if game.rooms % 5 == 0 and game.createdhealth == 0:
            healgroup.add(hero.createhealth())
            game.createdhealth = 1
        if game.rooms % 5 != 0 and game.createdhealth != 1:
            game.createdhealth = 0
    ammo()
    if hero.isrolling == 0:
        if cursor.stage != CPAUSE:
            hero.wupdate(game.mx, game.my)
        scr.blit(hero.newgun, hero.newgunrect)
    enemiesgroup.update()
    debug()
    if cursor.stage != CPAUSE:
        cursors.update(cursor)
        flip()


def ammo():
    '''
    queues main information about the no. of room/ ammunition/ hp
    '''
    myfont = pygame.font.Font('freesansbold.ttf', FONTSIZE)
    msg = myfont.render(f"{hero.gammo} / {hero.sgammo}", True, RED)
    msg_box = msg.get_rect()
    msg_box.bottomleft = win.bottomleft
    scr.blit(msg, msg_box)
    myfont = pygame.font.Font('freesansbold.ttf', FONTSIZE)
    msg = myfont.render(f"{hero.hp} / 6", True, RED)
    msg_box = msg.get_rect()
    msg_box.bottomright = win.bottomright
    scr.blit(msg, msg_box)
    myfont = pygame.font.Font('freesansbold.ttf', FONTSIZE)
    msg = myfont.render(f"room {game.rooms}", True, RED)
    msg_box = msg.get_rect()
    msg_box.topleft = win.topleft
    scr.blit(msg, msg_box)


def debug():
    '''
    debug tool - shows values of position of mouse cursor
    '''
    if DEBUG == 1:
        xpos, ypos = pygame.mouse.get_pos()
        myfont = pygame.font.Font('freesansbold.ttf', SFONTSIZE)
        msg = myfont.render(f"{xpos}, {ypos}", True, RED)
        msg_box = msg.get_rect()
        msg_box.center = (xpos, ypos - 2 * BGFRAME)
        scr.blit(msg, msg_box)


def herohit():
    '''
    checks if hero should be hit
    '''
    if hero.hitable == 1:
        if pygame.sprite.spritecollide(hero, ebulletgroup, True):
            herohit2()
        if hero.hp <= 0:
            pass
    if hero.hitable == 0:
        if game.timer - hero.rantime >= SPEED * HEROINVINC:
            hero.hitable = 1


def herohit2():
    '''
    deals dmg to the player
    '''
    hit.sfx.play()
    hero.hp -= 1
    if hero.hp == 0:
        dead.sfx.play()
    hero.hitable = 0
    hero.rantime = game.timer


def reload():
    '''
    handles reloading

    queues for display reload indicator above the hero
    '''
    lstar = (hero.x, hero.y - RELUP)
    lbound = [lstar, RELBOUN]
    rstar = (hero.x + CHARA[0], hero.y - RELUP)
    rbound = [rstar, RELBOUN]
    mstar = (hero.x, hero.y - ((RELUP - RELMOVE[0]) / 2))
    main = [mstar, RELMAIN]
    mostar = (hero.x + (hero.grel * RELMAIN[0] / SPEED),
              mstar[1] - RELMOVE[1] / 2)
    move = [mostar, RELMOVE]
    pygame.draw.rect(scr, WHITE, lbound)
    pygame.draw.rect(scr, WHITE, rbound)
    pygame.draw.rect(scr, WHITE, main)
    pygame.draw.rect(scr, BLACK, move)
    if hero.grel >= hero.greltime * SPEED:
        hero.grel = 0
        hero.gammo = hero.sgammo
    else:
        hero.grel += 1


def nextcheck():
    '''
    handles changing rooms

    sets wich enemies to spawn
    '''
    if game.badies <= 0 and hero.x == WIN[0] - CHARA[0] - BGFRAME:
        if hero.speedx > 0:
            game.bullkill = 1
            mel = 0
            sho = 0
            mac = 0
            all = 0
            if game.rooms == NEROOM2:
                game.bg = (pygame.image.load
                           ('assets/background/bg1.png')).convert()
            game.rooms += 1
            hero.x = 0
            if game.rooms <= NEROOM1:
                mel = random.randint(3, 5)
            elif game.rooms <= NEROOM2:
                mel = random.randint(1, 3)
                sho = random.randint(3, 5)
            elif game.rooms <= NEROOM3:
                mel = random.randint(0, 2)
                sho = random.randint(1, 3)
                mac = random.randint(1, 5)
            else:
                all = random.randint(7, 15)
            spawn(mel, sho, mac, all)
            show()
    else:
        game.bullkill = 0


def quitcheck():
    '''
    checks if the game should be quited or pause should be activated
    '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if cursor.stage == CMAINGA and cursor.cooldown == 0:
                    cursor.stage = CPAUSE
                    cursor.cooldown = 1
                if cursor.stage == CPAUSE and cursor.cooldown == 0:
                    cursor.stage = CMAINGA
                    cursor.cooldown = 1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                cursor.cooldown = 0


if __name__ == "__main__":
    starx = 0
    stary = (WIN[1] - CHARA[1]) / 2
    pygame.mixer.init()
    hero = player(starx, stary, 1)
    cursor = cursors(pygame.image.load('assets/other/cursor.png'))
    bg1 = (pygame.transform.scale((pygame.image.load('assets/other/ener.png')),
                                  WIN)).convert()
    shot = sfx('assets/sound/gunshot.wav')
    shot2 = sfx('assets/sound/gunshot2.wav')
    shot3 = sfx('assets/sound/1gunshot.wav')
    hit = sfx('assets/sound/hit.wav')
    dead = sfx('assets/sound/dead.wav')
    menu = pygame.image.load('assets/other/pause.png')
    menu_rect = menu.get_rect()
    menu_rect.center = win.center
    arrow = pygame.image.load('assets/other/arrow.png')
    name = text('assets/other/name.png', (WIN[1] / 5))
    play = text('assets/other/play1.png', (WIN[1] / 2))
    quit = text('assets/other/quit1.png', ((WIN[1] / 2) + 2 * DISTEXT))
    name = text('assets/other/name.png', (WIN[1] / 5))
    retu = text('assets/other/return1.png', ((WIN[1] / 2 + DISTEXT)))
    resu = text('assets/other/resume1.png', (WIN[1] / 2))
    retu.rect.center = (WIN[0] / 2, retu.rect.center[1])
    resu.rect.center = (WIN[0] / 2, resu.rect.center[1])
    pygame.mouse.set_visible(False)
    fbulletgroup = pygame.sprite.Group()
    enemiesgroup = pygame.sprite.Group()
    ebulletgroup = pygame.sprite.Group()
    healgroup = pygame.sprite.Group()
    pygame.font.init()
    main()
