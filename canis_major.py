# IMPORTS MODULES: PYGAME, SYS, RANDOM, TIME, etc...
import pygame
import random as r
from pygame.locals import *
from sys import exit


# INITIALIZES PYGAME MODULE
pygame.init()

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


# UPLOADED SPRITE FRAMES
idle1, idle2 = pygame.transform.scale(pygame.image.load('graphics/idle1.png').convert_alpha(), (80,80)), pygame.transform.scale(pygame.image.load('graphics/idle2.png').convert_alpha(), (80,80))
left1 = pygame.transform.scale(pygame.transform.flip(pygame.image.load('graphics/right1.png').convert_alpha(), True, False), (80,80))
right1 = pygame.transform.scale(pygame.image.load('graphics/right1.png').convert_alpha(), (80,80))
up1 = pygame.transform.scale(pygame.image.load('graphics/up1.png').convert_alpha(), (80,80))
down1, down2, down3 = pygame.transform.scale(pygame.image.load('graphics/down1.png').convert_alpha(), (80,80)), pygame.transform.scale(pygame.image.load('graphics/down2.png').convert_alpha(), (80,80)), pygame.transform.scale(pygame.image.load('graphics/down3.png').convert_alpha(), (80,80))

# SPRITES
class Player(pygame.sprite.Sprite):

    def __init__(self, x_pos, y_pos):
        super().__init__() 
        self.velocity = 1 # MOVEMENT SPEED
        self.shift = False # FOR SPRINTING: HOLD LSHFT
        self.moveLeft = False  # ----
        self.moveRight = False # SETS PLAYER MOVEMENT-TOGGLE-VARIABLES
        self.moveUp = False    # ----
        self.moveDown = False  # ----

        self.idle = [idle1,idle1,idle1,idle2,idle2,idle2]
        self.idleIndex = 0

        self.runRight = [right1]
        self.rightIndex = 0

        self.runLeft = [left1]
        self.leftIndex = 0

        self.runUp = [up1]
        self.upIndex = 0

        self.runDown = [down1, down2, down3]
        self.downIndex = 0

        self.image = self.idle[self.idleIndex] # PLAYER SURFACE / SPRITE
        #self.image.fill((123,159,147)) # FILLS IMAGE WITH COLOR
        self.rect = self.image.get_rect() # GETS RECT FROM LOADED IMAGE
        self.rect.topleft = [x_pos, y_pos] # SETS RECT COORDS

    def movement(self):
        if self.shift:
            self.velocity = 3
        else:
            self.velocity = 1
            
        if self.moveDown and self.rect.bottom < h:
            self.image = self.runDown[0]
            self.downIndex += 1
            self.rect.bottom += self.velocity

        if self.moveUp and self.rect.top > 0:
            self.image = self.runUp[0]
            self.upIndex += 1
            self.rect.top -= self.velocity

        if self.moveLeft and self.rect.left > 0:
            self.image = self.runLeft[0]
            self.leftIndex += 1
            self.rect.left -= self.velocity

        if self.moveRight and self.rect.right < w:
            self.image = self.runRight[0]
            self.rightIndex += 1
            self.rect.right += self.velocity

    def update(self):
        self.movement()
        screen.blit(self.image, self.rect)

# --------------------------------------------------------

class NPC(pygame.sprite.Sprite):

    def __init__(self, name, x_pos, y_pos):
        super().__init__()
        self.name = name
        self.image = pygame.Surface((32,64))
        self.image.fill((222,54,147))
        self.rect = self.image.get_rect(center = (x_pos, y_pos))
        self.velocity = 1

    def __repr__(self):
        return self.name

    def movement(self):
        pass

    def collide(self):
        if pygame.sprite.spritecollide(self, siriusSprite, False):
            banter.show = True
            banter.update()
        

# SPRITE CLASS INSTANCES
siriusSprite = pygame.sprite.GroupSingle() # CREATE SPRITE GROUP
npc_sprites = pygame.sprite.Group()

sirius = Player(100, 100) # CREATE SPRITE
aldhara = NPC('Aldhara', 110, 100)
jynx = NPC('Jynx', bg.rect.w/4, bg.rect.height/4)

siriusSprite.add(sirius) # ADD SPRITE
npc_sprites.add(aldhara, jynx)


# TEXT TO SCREEN CLASS
class text2screen:
    def __init__(self, xPos, yPos, text):
        basicFont = pygame.font.SysFont(None, 21, italic = True)
        self.text = basicFont.render(text, False, (0,0,0))
        self.rect = (self.text.get_rect(topleft = (xPos,yPos)))
        border = pygame.draw.rect(screen, (255,255,255), ((self.rect.x + 3), (self.rect.y + 3),(self.rect.width + 3), (self.rect.height + 3)))
        self.show = False

    def __repr__(self):
        return self.text

    def update(self):
        if self.show:
            bg.image.blit(self.text, self.rect)

# TEXT TO SCREEN INSTANCE
banter = text2screen(aldhara.rect.x-10,aldhara.rect.y-10,'Guildmaster banter and wisdom...')


menu = False
def Menu():
    global menu

    print('menu entered')

    while menu:

        screen.fill((212,225,155))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print('menu exited')
                    menu = False

        basicFont = pygame.font.SysFont(None, 36, italic = True)
        start = basicFont.render('Menu Screen', False, (0,0,0))
        strtrect = start.get_rect(center = (w/2,h/2))

        screen.blit(start, strtrect)

        pygame.display.update()

        clock.tick(60)


fight = False
def battle():
    global fight, test3
    
    while fight:

        screen.fill((155,155,155))

        for event in pygame.event.get():

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    fight = False

        basicFont = pygame.font.SysFont(None, 36, italic = True)
        start = basicFont.render('Battle Screen', False, (0,0,0))
        strtrect = start.get_rect(center = (w/2,h/2))

        screen.blit(start, strtrect)

        pygame.display.update()

        clock.tick(120)


message = False
def messageToScreen():
    basicFont = pygame.font.SysFont(None, 36, italic = True)
    msg = basicFont.render('This text will be some sort of dialogue...', False, (0,0,0))
    msgrect = msg.get_rect(center = (w/2,int(h/3)))
    msgBox = pygame.Rect(((msgrect.x - 3), (msgrect.y - 3),(msgrect.width + 3), (msgrect.height + 3)))
    msgBoxFill = pygame.Rect(((msgrect.x - 3), (msgrect.y - 3),(msgrect.width + 3), (msgrect.height + 3)))
    pygame.draw.rect(screen, (123,23,123), msgBox, 5)
    pygame.draw.rect(screen, (234,234,234), msgBoxFill)
    screen.blit(msg, msgrect)


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
        #print('sprite colliding')
        message = True
        messageToScreen()


    # EVENT DETECTION LOOP
    for event in pygame.event.get():

        # QUIT GAME EVENT DETECTION
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

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
                menu = True
                Menu()

            if event.key == pygame.K_LSHIFT:# IF LSHFT HELD: 'SPRINT MOVEMENT'
                print('shift Pressed')
                sirius.shift = True


        # KEY UP
        if event.type == pygame.KEYUP:

            if event.key == pygame.K_LEFT:
                print('left arrow released')
                sirius.moveLeft = False
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

        pygame.mouse.set_cursor(system)
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


    # DRAW SPRITE
    npc_sprites.draw(bg.image)
    siriusSprite.draw(screen)
    sirius.update()
    #bg.image.blits((test2.image, test2.rect) for spr in npc_sprites)

    sirius.idleIndex += 1
    if sirius.idleIndex > len(sirius.idle):
        sirius.idleIndex = 0
    
    # SPRITE COLLISION FUNCTION
    aldhara.collide()
    jynx.collide()

    bg.scroll()
    
# --------------------------------------------------------

    # UPDATES DISPLAY EACH FRAME
    pygame.display.update()


    # RESETS FRAMERATE EACH FRAME 
    clock.tick(60)
