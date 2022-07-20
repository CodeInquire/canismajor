# IMPORTS MODULES: PYGAME, SYS, RANDOM, TIME, etc...
import pygame
import random as r
from pygame.locals import *
from sys import exit


# INITIALIZES PYGAME MODULE
pygame.init()
pygame.mixer.init()

w = 800
h = 800

# CREATES MAIN DISPLAY SURFACE
screen = pygame.display.set_mode((w,h))

# SETS WINDOW TITLE
pygame.display.set_caption('Canis Major')

# CREATES CLOCK OBJECT TO SET FRAMERATE
clock = pygame.time.Clock()

system = pygame.cursors.Cursor(pygame.cursors.broken_x)
surf = pygame.Surface((40, 40)) # you could also load an image 
#surf.fill((120, 50, 50))        # and use that as your surface
color = pygame.cursors.Cursor((20, 20), surf)


# AUDIO
villageSound = pygame.mixer.Sound('audio/village.mp3')
villageSound.set_volume(.18)
villageSound.play(-1)


# BACKGROUND IMAGE CLASS
class BGI:

    def __init__(self, image, xPos, yPos):
        self.image = image
        self.rect = self.image.get_rect(center = (w/2, h/2))
        self.scrollLeft = False
        self.scrollRight = False
        self.scrollUp = False
        self.scrollDown = False

    def update(self):
        screen.blit(self.image, self.rect)

    def scroll(self):
        if self.scrollLeft:
            if self.rect.left <= 0:
               self.rect.left += test1.velocity
            else:
                self.rect.left = 0
                
        if self.scrollRight:
            if self.rect.right >= w:
                self.rect.right -= test1.velocity
            else:
                self.rect.right = w

        if self.scrollUp:
            if self.rect.top <= 0:
                self.rect.top += test1.velocity
            else:
                self.rect.top = 0

        if self.scrollDown:
            if self.rect.bottom >= h:
                self.rect.bottom -= test1.velocity
            else:
                self.rect.bottom = h

# BGI VARIABLE / INSTANCE
bg = BGI(pygame.transform.scale(pygame.image.load('graphics/test_bgi2.png'), (800,800)), 0, 0)



# SPRITE CLASS
class Player(pygame.sprite.Sprite):

    def __init__(self, x_pos, y_pos):
        super().__init__()

        # SPRITE FRAMES
        idle1, idle2 = pygame.transform.scale(pygame.image.load('graphics/idle1.png').convert_alpha(), (96,96)), pygame.transform.scale(pygame.image.load('graphics/idle2.png').convert_alpha(), (96,96))
        left1, left2 = pygame.transform.scale(pygame.transform.flip(pygame.image.load('graphics/right1.png').convert_alpha(), True, False), (96,96)), pygame.transform.scale(pygame.transform.flip(pygame.image.load('graphics/right2.png').convert_alpha(), True, False), (96,96))
        right1, right2 = pygame.transform.scale(pygame.image.load('graphics/right1.png').convert_alpha(), (96,96)), pygame.transform.scale(pygame.image.load('graphics/right2.png').convert_alpha(), (96,96))
        up1, up2 = pygame.transform.scale(pygame.image.load('graphics/up1.png').convert_alpha(), (96,96)), pygame.transform.scale(pygame.image.load('graphics/up2.png').convert_alpha(), (96,96))
        down1, down2, down3 = pygame.transform.scale(pygame.image.load('graphics/down1.png').convert_alpha(), (96,96)), pygame.transform.scale(pygame.image.load('graphics/down2.png').convert_alpha(), (96,96)), pygame.transform.scale(pygame.image.load('graphics/down3.png').convert_alpha(), (96,96))

        self.velocity = 1 # MOVEMENT SPEED
        self.shift = False # FOR SPRINTING: HOLD LSHFT
        self.moveLeft = False  # ----
        self.moveRight = False # SETS PLAYER MOVEMENT-TOGGLE-VARIABLES
        self.moveUp = False    # ----
        self.moveDown = False  # ----

        self.idle = [idle1,idle1,idle1,idle1,idle1,idle1,idle1,idle1,idle1,idle1,idle1,idle1,idle1,idle1,idle1,idle2,idle2,idle2,idle2,idle2,idle2,idle2,idle2,idle2,idle2,idle2,idle2,idle2,idle2,idle2]
        self.idleIndex = 0
        self.idling = False

        self.runRight = [right1, right2]
        self.rightIndex = 0
        self.runningRight = False

        self.runLeft = [left1, left2]
        self.leftIndex = 0
        self.runningLeft = False

        self.runUp = [up1, up2]
        self.upIndex = 0
        self.runningUp = False

        self.runDown = [down1, down2, down3]
        self.downIndex = 0
        self.runningDown = False

        self.image = self.idle[self.idleIndex] # PLAYER SURFACE / SPRITE
        #self.image.fill((123,159,147)) # FILLS IMAGE WITH COLOR
        self.rect = self.image.get_rect() # GETS RECT FROM LOADED IMAGE
        self.rect.topleft = [x_pos, y_pos] # SETS RECT COORDS

        self.stats = {
            'name': 'Sirius',
            'level': 1,
            'exp': 0,
            'health': 3,
            'items': [],
            'equip': {
                'head': None,
                'body': None,
                'legs': None,
                'cowl': None,
                'wpn1': None,
                'wpn2': None,
                },
            'magic': []
            }

    def movement(self):
        if self.shift:
            self.velocity = 3
        else:
            self.velocity = 1
            
        if self.moveDown and self.rect.bottom < h:
            self.image = self.runDown[0]
            self.rect.bottom += self.velocity

        if self.moveUp and self.rect.top > 0:
            self.image = self.runUp[0]
            self.rect.top -= self.velocity

        if self.moveLeft and self.rect.left > 0:
            self.image = self.runLeft[0]
            self.rect.left -= self.velocity

        if self.moveRight and self.rect.right < w:
            self.image = self.runRight[0]
            self.rect.right += self.velocity

    def animate(self):
        if self.runningLeft and self.rect.left > 0:
            self.image = self.runLeft[0]
            if self.leftIndex >= len(self.runLeft):
                self.leftIndex = 0
            else:
                self.leftIndex += 1

    def update(self):
        self.movement()
        self.animate()
        screen.blit(self.image, self.rect)

# --------------------------------------------------------

class NPC(pygame.sprite.Sprite):

    def __init__(self, name, health, image, x_pos, y_pos):
        super().__init__()
        self.name = name
        self.image = image
        #self.image.fill((222,54,147))
        self.rect = self.image.get_rect(center = (x_pos, y_pos))
        #self.velocity = 1
        self.stats = {
            'name': 'Sirius',
            'level': 1,
            'exp': 0,
            'health': health,
            'items': [],
            'equip': {
                'head': None,
                'body': None,
                'legs': None,
                'cowl': None,
                'wpn1': None,
                'wpn2': None,
                },
            'magic': []
            }

    def __repr__(self):
        return self.name

    def movement(self):
        pass

    def collide(self):
        if pygame.sprite.spritecollide(self, siriusSprite, False):
            pass

    def update(self):
        screen.blit(self.image, self.rect)
        

# SPRITE CLASS INSTANCES
siriusSprite = pygame.sprite.GroupSingle() # CREATE SPRITE GROUP
npc_sprites = pygame.sprite.Group()
allSprites = pygame.sprite.Group()

sirius = Player(400, 600) # CREATE SPRITE
aldhara = NPC('Aldhara', 300, pygame.Surface((32,64)), 333, 666)
jynx = NPC('Jynx', 50, pygame.transform.flip(pygame.transform.scale(pygame.image.load('graphics/Juggler_Attack_Blue.gif').convert_alpha(), (96,96)), True, False), 500, 300)
shopKeep = NPC('Item Shop Owner', 30, pygame.Surface((32,64)), 600, 600)

siriusSprite.add(sirius) # ADD SPRITE
npc_sprites.add(aldhara, jynx, shopKeep)
allSprites.add(sirius, aldhara, jynx, shopKeep)


class Button:
    def __init__(self, text, w, h, pos, textColor, rectColor):

        basicFont = pygame.font.SysFont(None, 36, italic = True)

        
        # TOP RECT
        self.topRect = pygame.Rect(pos,(w,h))
        self.topColor = rectColor

        # TEXT
        self.textSurf = basicFont.render(text, False, textColor)
        self.textRect = self.textSurf.get_rect(center = self.topRect.center)

    def draw(self):
        pygame.draw.rect(screen, self.topColor, self.topRect, border_radius = 12)
        screen.blit(self.textSurf, self.textRect)

    def checkClick(self):
        mousePos = pygame.mouse.get_pos()
        if self.topRect.collidepoint(mousePos):
            print('collide point')
            self.topColor = (255,50,50)
        else:
            self.topColor = (33,255,33)


saveExit = Button('Save & Exit', 200, 50, (500, 700), (0,0,0), (33,255,33))

mapScrn = Button('Map', 200, 50, (150, 700), (0,0,0), (33,255,33))


def Menu():
    
    menu = True
    villageSound.stop()

    print('menu entered')

    basicFont = pygame.font.SysFont(None, 36, italic = True)
    start = basicFont.render('Menu Screen', False, (0,0,0))
    strtrect = start.get_rect(center = (w/2,h/2))

    menuPlyr = pygame.transform.scale(pygame.image.load('graphics/down6.png').convert_alpha(), (160,160))
    menuPlayer = menuPlyr
    menuPlayerRect = menuPlyr.get_rect(center = (130, 230))
    plrBorder = pygame.Rect(menuPlayerRect.x, menuPlayerRect.y, menuPlayerRect.width, menuPlayerRect.height)
    playerText = basicFont.render('Sirius', False, (0,0,0))
    playerTextRect = playerText.get_rect(bottomleft = plrBorder.topleft)

    itemBorder = pygame.Rect(menuPlayerRect.x*6, menuPlayerRect.y, 444, menuPlayerRect.height)
    itemText = basicFont.render('INVENTORY', False, (213,123,213))
    itemTextRect = itemText.get_rect(bottomleft = itemBorder.topleft)

    while menu:

        screen.fill((123,123,231))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print('menu exited')
                    villageSound.play(-1)
                    menu = False
                    
            # MOUSE EVENT DETECTION

            #pygame.mouse.set_cursor(system)
            mx, my = pygame.mouse.get_pos()

            left, middle, right = pygame.mouse.get_pressed()

            rightClicking = False
            leftCLicking = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:

                if left:
                    leftClicking = True

                if middle:
                    print('middle button clicked')

                if right:
                    rightClicking = True
                    if aldhara.rect.collidepoint(mx,my) or jynx.rect.collidepoint(mx,my):
                        if left:
                            print('SPECIAL')
                        else:
                            print('open NPC interact options')

            if event.type == pygame.MOUSEBUTTONUP:

                if left:
                    leftClicking = False

                if right:
                    rightClicking = False
            

        screen.blit(start, strtrect)
        screen.blit(menuPlayer, menuPlayerRect)
        screen.blit(itemText, itemTextRect)
        screen.blit(playerText, playerTextRect)

        saveExit.draw()
        mapScrn.draw()

        pygame.draw.rect(screen, (255,255,255), plrBorder, 5)
        pygame.draw.rect(screen, (255,255,255), itemBorder, 5)

        saveExit.checkClick()
        mapScrn.checkClick()

        pygame.display.update()

        clock.tick(60)


message = False
def messageToScreen():

    basicFont = pygame.font.SysFont(None, 36, italic = True)

    msg = basicFont.render('This text will be some sort of dialogue...', False, (0,0,0))

    msgRect = msg.get_rect(center = (w/2,int(h/3)))

    msgBox = pygame.Rect(((msgRect.x - 3),
                          (msgRect.y - 3),
                          (msgRect.width + 3),
                          (msgRect.height + 3)))
    
    msgBoxFill = pygame.Rect(((msgRect.x - 3),
                              (msgRect.y - 3),
                              (msgRect.width + 3),
                              (msgRect.height + 3)))

    pygame.draw.rect(screen, (123,23,123), msgBox, 5)
    pygame.draw.rect(screen, (234,234,234), msgBoxFill)

    screen.blit(msg,msgRect)


def battle(atkr, dfndr):

    basicFont = pygame.font.SysFont(None, 66, italic = True)
    

    atkrCopy = pygame.transform.scale(atkr.image, (320, 320))
    aHealthBar = []
    for i in range(0, atkr.stats['health']):
        aHealthBar.append(pygame.draw.rect(screen, (50,220,50), (i + 630, 500, 5, 20)))


    dfndrCopy = pygame.transform.scale(dfndr.image, (320, 320))
    dHealthBar = []
    for i in range(0, dfndr.stats['health']):
        dHealthBar.append(pygame.draw.rect(screen, (50,220,50), (i + 100, 500, 5, 20)))


    


    fight = True
    while fight:

        villageSound.stop()
        
        screen.fill((0,0,0))

        for event in pygame.event.get():

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    villageSound.play(-1)
                    fight = False

            # MOUSE EVENT DETECTION

            #pygame.mouse.set_cursor(system)
            mx, my = pygame.mouse.get_pos()

            left, middle, right = pygame.mouse.get_pressed()

            rightClicking = False
            leftCLicking = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:

                if left:
                    leftClicking = True
                    print('left button clicked')
                    if len(dHealthBar) > 0:
                        print('1 damage')
                        dHealthBar.pop()
                    else:
                        print('battle over')
                        fight = False

                if middle:
                    print('middle button clicked')

                if right:
                    rightClicking = True
                    print('right button clicked')

            if event.type == pygame.MOUSEBUTTONUP:

                if left:
                    leftClicking = False

                if right:
                    rightClicking = False

        aHealthDisplay = basicFont.render(str(len(aHealthBar)), False, (255,255,255))
        aHealthDisplayRect = aHealthDisplay.get_rect(center = (w/2,h/6))
        for hp in range(len(aHealthBar)):
            pygame.draw.rect(screen, (50,220,50), aHealthBar[hp])
        screen.blit(aHealthDisplay, aHealthDisplayRect)

        dHealthDisplay = basicFont.render(str(len(dHealthBar)), False, (255,255,255))
        dHealthDisplayRect = dHealthDisplay.get_rect(center = (w/2,h/6))
        for hp in range(len(dHealthBar)):
            pygame.draw.rect(screen, (50,220,50), dHealthBar[hp])
        screen.blit(dHealthDisplay, dHealthDisplayRect)


        screen.blit(dfndrCopy,(w-800,h/4,10,10))
        screen.blit(atkrCopy, (w-300,h/4-30,10,10))

        
        pygame.display.update()


        clock.tick(120)


# MAIN GAME LOOP
run = True
while run:
    #print(pygame.time.get_ticks())


    


    # FILLS SCREEN WITH A BACKGROUND COLOR
    screen.fill((255,255,255))


    bg.update()
    

    # CHECKS FOR COLLISION BETWEEN SPRITES / GROUPS
    if pygame.sprite.spritecollide(sirius, npc_sprites, False):
        pass


    # EVENT DETECTION LOOP
    for event in pygame.event.get():

        # QUIT GAME EVENT DETECTION
        if event.type == pygame.QUIT:
            not run

        # KEYBOARD EVENT DETECTION
        # KEY DOWN

        held_keys = pygame.key.get_pressed() # RETURNS ALL BUTTONS PRESSED

        if held_keys[pygame.K_LEFT]: # LEFT
            #test1.moveLeft = True
            pass
        
        if held_keys[pygame.K_RIGHT]: # RIGHT
            #test1.moveRight = True
            pass
                  
        if held_keys[pygame.K_UP]: # UP
            #test1.moveUp = True
            pass
       
        if held_keys[pygame.K_DOWN]: # DOWN
            #test1.moveDown = True
            pass

# --------------------------------------------------------
        
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

            if event.key == pygame.K_LEFT:
                print('Left Arrow Pressed')
                sirius.moveLeft = True
                sirius.runningLeft = True
                #bg.scrollLeft = True

            if event.key == pygame.K_RIGHT:
                print('Right Arrow Pressed')
                sirius.moveRight = True
                #bg.scrollRight = True

            if event.key == pygame.K_UP:
                print('Up Arrow Pressed')
                sirius.moveUp = True
                #bg.scrollUp = True

            if event.key == pygame.K_DOWN:
                print('Down Arrow Pressed')
                sirius.moveDown = True
                #bg.scrollDown = True

            if event.key == pygame.K_SPACE:
                print('Space Bar Pressed')
                Menu()

            if event.key == pygame.K_LSHIFT:# IF LSHFT HELD: 'SPRINT MOVEMENT'
                print('shift Pressed')
                sirius.shift = True


        # KEY UP
        if event.type == pygame.KEYUP:

            if event.key == pygame.K_LEFT:
                print('left arrow released')
                sirius.moveLeft = False
                sirius.runningLeft = False
                bg.scrollLeft = False

            if event.key == pygame.K_RIGHT:
                print('Right arrow released')
                sirius.moveRight= False
                bg.scrollRight = False

            if event.key == pygame.K_UP:
                print('Up arrow released')
                sirius.moveUp = False
                bg.scrollUp = False

            if event.key == pygame.K_DOWN:
                print('Down arrow released')
                sirius.moveDown = False
                bg.scrollDown = False

            if event.key == pygame.K_SPACE:
                print('Space Bar Released')
                Menu = False

            if event.key == pygame.K_LSHIFT:
                print('shift released')
                sirius.shift = False


        # MOUSE EVENT DETECTION

        #pygame.mouse.set_cursor(system)
        mx, my = pygame.mouse.get_pos()

        left, middle, right = pygame.mouse.get_pressed()

        rightClicking = False
        leftCLicking = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:

            if left:
                leftClicking = True
                print('left button clicked')
                battle(jynx, sirius)

            if middle:
                print('middle button clicked')

            if right:
                rightClicking = True
                print('right button clicked')
                if aldhara.rect.collidepoint(mx,my) or jynx.rect.collidepoint(mx,my):
                    if left:
                        print('SPECIAL')
                    else:
                        print('open NPC interact options')

        if event.type == pygame.MOUSEBUTTONUP:

            if left:
                leftClicking = False

            if right:
                rightClicking = False


    # DRAW SPRITE   
    siriusSprite.update()


    # RENDERS SPRITES IN ORDER ACCORDING TO Y-AXIS
    for sprite in sorted(allSprites, key = lambda sprite: sprite.rect.centery):
        screen.blit(sprite.image, sprite.rect)

    
    #bg.image.blits((test2.image, test2.rect) for spr in npc_sprites)


    #bg.scroll()
    
# --------------------------------------------------------

    # UPDATES DISPLAY EACH FRAME
    pygame.display.update()


    # RESETS FRAMERATE EACH FRAME 
    clock.tick(120)

pygame.quit()
exit()
