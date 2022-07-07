
# IMPORTS MODULES: PYGAME, SYS, RANDOM, TIME, etc...
import pygame
import random as r
from pygame.locals import *
from sys import exit


# INITIALIZES PYGAME MODULE
pygame.init()

w = 300
h = 300

# CREATES MAIN DISPLAY SURFACE
screen = pygame.display.set_mode((w,h))

# SETS WINDOW TITLE
pygame.display.set_caption('Canis Major')

# CREATES CLOCK OBJECT TO SET FRAMERATE
clock = pygame.time.Clock()

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
        if self.scrollLeft ==True:
            if self.rect.left <= 0:
               self.rect.left += test1.velocity
            else:
                self.rect.left = 0
                
        if self.scrollRight == True:
            if self.rect.right >= w:
                self.rect.right -= test1.velocity
            else:
                self.rect.right = w

        if self.scrollUp == True:
            if self.rect.top <= 0:
                self.rect.top += test1.velocity
            else:
                self.rect.top = 0

        if self.scrollDown == True:
            if self.rect.bottom >= h:
                self.rect.bottom -= test1.velocity
            else:
                self.rect.bottom = h

# BGI VARIABLE / INSTANCE
bg = BGI(pygame.image.load('graphics/bgi.png'), 0, 0)

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
            screen.blit(self.text, self.rect)


# SETS PLAYER MOVEMENT-TOGGLE-VARIABLES
moveLeft = False
moveRight = False
moveUp = False
moveDown = False

# SPRITES
class Player(pygame.sprite.Sprite):

    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.image = pygame.Surface((30, 30)) # PLAYER SURFACE / SPRITE
        self.image.fill((123,159,147)) # FILLS IMAGE WITH COLOR
        self.rect = self.image.get_rect() # GETS RECT FROM LOADED IMAGE
        self.rect.topleft = [x_pos, y_pos] # SETS RECT COORDS
        self.velocity = 1 # MOVEMENT SPEED
        self.shift = False # FOR SPRINTING: HOLD DOWN WHILE PRESSING ARROW KEYS

    def movement(self):
        if self.shift == True:
            test1.velocity = 3
        else:
            test1.velocity = 1
            
        if moveDown == True:
            self.rect.bottom += self.velocity

        if moveUp == True:
            self.rect.top -= self.velocity

        if moveLeft == True:
            self.rect.left -= self.velocity

        if moveRight == True:
            self.rect.right += self.velocity

    def collision(self):
        if self.rect.left <= 0:
            self.rect.left = 0

        if self.rect.right >= w:
            self.rect.right = w

        if self.rect.top <= 0:
            self.rect.top = 0

        if self.rect.bottom >= h:
            self.rect.bottom = h

            
class NPC(pygame.sprite.Sprite):

    def __init__(self, name, x_pos, y_pos):
        super().__init__()
        self.name = name
        self.image = pygame.Surface([30,30])
        self.image.fill((123,159,147))
        self.rect = self.image.get_rect()
        self.rect.center = [x_pos, y_pos]
        self.velocity = 1

    def __repr__(self):
        return self.name

    def movement(self):
        pass

    def collide(self):
        if pygame.sprite.spritecollide(self, moving_sprites, False):
            banter.show = True
            banter.update()
        else:
            pass


moving_sprites = pygame.sprite.Group() # CREATE SPRITE GROUP
npc_sprites = pygame.sprite.Group()

test1 = Player(100, 100) # CREATE SPRITE
test2 = NPC('Guild Master', 200, 100)
test3 = NPC('Jynx', 420, 200)

moving_sprites.add(test1) # ADD SPRITE
npc_sprites.add(test2, test3)

# TEXT TO SCREEN INSTANCE
banter = text2screen(test2.rect.x-10,test2.rect.y-10,'Guildmaster banter and wisdom...')


menu = False
def Menu():
    global menu

    print('menu entered')

    while menu:

        screen.fill((212,225,155))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    test1.rect.x += 0
                    test1.rect.y += 0
                    print('menu exited')
                    menu = False

        basicFont = pygame.font.SysFont(None, 36, italic = True)
        start = basicFont.render('Menu Screen', False, (0,0,0))
        strtrect = start.get_rect(center = (w/2,h/2))

        screen.blit(start, strtrect)

        pygame.display.update()

        clock.tick(10)


fight = False
def battle():
    global fight
    
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
    screen.blit(msg, msgrect)
    pygame.draw.rect(screen, (0,0,0), msgBox, 2)


# MAIN GAME LOOP
run = True
while run:
    print(pygame.time.get_ticks())

    

    # FILLS SCREEN WITH A BACKGROUND COLOR
    screen.fill((255,0,0))

    bg.update()
    bg.scroll()

    held_keys = pygame.key.get_pressed()

    if held_keys[pygame.K_LEFT]: # LEFT
       pass
        
    if held_keys[pygame.K_RIGHT]: # RIGHT
        pass
                  
    if held_keys[pygame.K_UP]: # UP
        pass
       
    if held_keys[pygame.K_DOWN]: # DOWN
        pass
    

    # CHECKS FOR COLLISION BETWEEN SPRITES / GROUPS
    if pygame.sprite.spritecollide(test1, npc_sprites, False):
        pass
        #print('sprite colliding')
        #message = True
        #messageToScreen()


    # EVENT DETECTION LOOP
    for event in pygame.event.get():

        # QUIT GAME EVENT DETECTION
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # KEYBOARD EVENT DETECTION
        # KEY DOWN
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

            if event.key == pygame.K_LEFT:
                print('Left Arrow Pressed')
                moveLeft = True
                bg.scrollLeft = True

            if event.key == pygame.K_RIGHT:
                print('Right Arrow Pressed')
                moveRight = True
                bg.scrollRight = True

            if event.key == pygame.K_UP:
                print('Up Arrow Pressed')
                moveUp = True
                bg.scrollUp = True

            if event.key == pygame.K_DOWN:
                print('Down Arrow Pressed')
                moveDown = True
                bg.scrollDown = True

            if event.key == pygame.K_SPACE:
                print('Space Bar Pressed')
                menu = True
                Menu()

            if event.key == pygame.K_LSHIFT:# IF LSHFT HELD: 'SPRINT MOVEMENT'
                print('shift Pressed')
                test1.shift = True

            if event.key == pygame.K_n:
                if test2.rect.center == (200,100):
                    for i in range(100):
                        test2.rect.x += 1

        # KEY UP
        if event.type == pygame.KEYUP:

            if event.key == pygame.K_LEFT:
                print('left arrow released')
                moveLeft = False
                bg.scrollLeft = False

            if event.key == pygame.K_RIGHT:
                print('Right arrow released')
                moveRight= False
                bg.scrollRight = False

            if event.key == pygame.K_UP:
                print('Up arrow released')
                moveUp = False
                bg.scrollUp = False

            if event.key == pygame.K_DOWN:
                print('Down arrow released')
                moveDown = False
                bg.scrollDown = False

            if event.key == pygame.K_SPACE:
                print('Space Bar Released')
                Menu = False

            if event.key == pygame.K_LSHIFT:
                print('shift released')
                test1.shift = False


        # MOUSE EVENT DETECTION
        mx, my = pygame.mouse.get_pos()
        
        if event.type == pygame.MOUSEBUTTONDOWN:

            left, middle, right = pygame.mouse.get_pressed()

            if left:
                if test2.rect.collidepoint(mx,my):
                    print('sprite clicked')

                else:
                    print('left button clicked')

            if middle:
                print('middle button clicked')

            if right:
                print('right button clicked')
                if test2.rect.collidepoint(mx,my):
                    if left:
                        print('sprite clicked')


    # DRAW SPRITE
    moving_sprites.draw(screen)
    
    # SPRITE MOVEMENT FUNCTION
    test1.movement()
    
    # SPRITE COLLISION FUNCTION
    test1.collision()

    npc_sprites.draw(screen)
    test2.collide()
    test3.collide()
# --------------------------------------------------------
    # UPDATES DISPLAY EACH FRAME
    pygame.display.update()


    # RESETS FRAMERATE EACH FRAME 
    clock.tick(60)
