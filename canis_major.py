# IMPORTS MODULES: PYGAME, SYS, RANDOM, TIME, etc...
import pygame, json, random, time
from pygame.locals import *
from sys import exit
from debug import debug


# INITIALIZES PYGAME MODULE
pygame.mixer.pre_init(44100, 16, 2, 4096)
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

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# MUSIC FILE IMPORTS
villageSound = pygame.mixer.Sound('audio/village.mp3') # CREATES A 'SOUND' OBJECT
villageSound.set_volume(.12) # SETS VOLUME OF SOUNS

villageMusic = pygame.mixer.Sound('audio/CanisMajorForestWandering.mp3')
villageMusic.set_volume(.09)

battleMusic = pygame.mixer.Sound('audio/CanisMajor - BattleJam.mp3')
battleMusic.set_volume(.06)

menuMusic = pygame.mixer.Sound('audio/menu.mp3')
menuMusic.set_volume(.33)


villageSound.set_volume(.12)
villageMusic.set_volume(.09)


sound = pygame.mixer.Channel(1) # CREATES MUSIC CHANNEL

#music.queue() # QUEUES THE NEXT SOUND FILE

music = pygame.mixer.Channel(2)

battle = pygame.mixer.Channel(3)

menuVibe = pygame.mixer.Channel(4)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# DELTA-TIME VARIABLE
previous_time = time.time()

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# LOAD FUNCTION USING JSON
try:
    with open('save_file.txt') as save_file:
        data= json.load(save_file)
        for entry in data.items():
            print(entry)

except:
    print('No Save File Created Yet')

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# BACKGROUND IMAGE CLASS
class BGI:

    def __init__(self, image, xPos, yPos):
        self.image = image
        self.rect = self.image.get_rect(center = (w/2, h/2))
        self.currentBackground = self.image

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
bg = BGI(pygame.transform.scale(pygame.image.load('graphics/test_bgi.jpg'), (800,800)), 0, 0)
bg2 = BGI(pygame.transform.scale(pygame.image.load('graphics/westRoad.png'), (800,800)), 0, 0)
bg3 = BGI(pygame.transform.scale(pygame.image.load('graphics/northManor.png'), (800,800)), 0, 0)
strtScrn = BGI(pygame.transform.scale(pygame.image.load('graphics/startScreen.png'), (800,800)), 0, 0)

currentBackground = ''

menuBGI = pygame.transform.scale(pygame.image.load('graphics/siriusDrawn.jpg'), (420, 720))

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Object(pygame.sprite.Sprite):

    def __init__(self, image, x_pos, y_pos):
        super().__init__()

        self.image = image
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect(bottomleft = (x_pos, y_pos))

        self.hitboxRect = self.rect.inflate(-36, -36)
        self.hitbox = pygame.Surface((self.hitboxRect.width, self.hitboxRect.height))
        self.hitbox.fill((255,255,255))

    def update(self):
        bg.image.blit(self.image, self.rect)
        bg.image.blit(self.hitbox, self.hitboxRect)

tree1 = Object(pygame.image.load('graphics/tree.png').convert(),250, 300)
bush1 = Object(pygame.image.load('graphics/bush1.png').convert(), 123, 321)
bush2 = Object(pygame.image.load('graphics/bush2.png').convert(), 234, 543)
bush1 = Object(pygame.image.load('graphics/bush1.png').convert(), 345, 234)
bush2 = Object(pygame.image.load('graphics/bush2.png').convert(), 132, 643)
bush3 = Object(pygame.image.load('graphics/bush3.png').convert(), 123, 246)
bush3 = Object(pygame.image.load('graphics/bush3.png').convert(), 321, 234)
house1 = Object(pygame.image.load('graphics/house.png').convert(), 432, 213)


class Weapon(pygame.sprite.Sprite):
    def __init__(self, name, description, image, type, attackPower, special):
        super().__init__()

        self.name = name
        self.dscr = description
        self.image = image
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()

        self.stats = {
            'type': type,
            'atk': attackPower,
            'special': special
            }

    def __repr__(self):
        return self.name


    def equip(self):
        if sirius.stats['items'].__contains__(self):
            #sirius.stats['equip']['wpn1'] = self
            print('weapon equipped')
        else:
            print('You dont own that item!')

    def draw(self, xPos, yPos):
        screen.blit(self.image, (xPos, yPos, 66, 66))


class Armor(pygame.sprite.Sprite):
    def __init__(self, name, description, image, type, defensePower, special):
        super().__init__()

        self.name = name
        self.dscr = description
        self.image = image
        self.rect = self.image.get_rect()

        self.stats = {
            'type': type,
            'dfn': defensePower,
            'special': special,
            }

    def __repr__(self):
        return self.name


    def equip(self):
        if sirius.stats['items'].__contains__(self):
            sirius.stats['equip']['wpn1'] = self
        else:
            print('You dont own that item!')

    def draw(self, xPos, yPos):
        screen.blit(self.image, self.rect)


dagger = Weapon('Dagger', 'A trusty companion to any cut-throat...',pygame.Surface((66,66)), 'Slash', 3, None)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Player(pygame.sprite.Sprite):

    def __init__(self, x_pos, y_pos):
        super().__init__()

        # SPRITE FRAMES
        idle1, idle2 = pygame.transform.scale(pygame.image.load('graphics/idle1.png').convert_alpha(), (96,96)), pygame.transform.scale(pygame.image.load('graphics/idle2.png').convert_alpha(), (96,96))
        left1, left2 = pygame.transform.scale(pygame.transform.flip(pygame.image.load('graphics/right1.png').convert_alpha(), True, False), (96,96)), pygame.transform.scale(pygame.transform.flip(pygame.image.load('graphics/right2.png').convert_alpha(), True, False), (96,96))
        right1, right2 = pygame.transform.scale(pygame.image.load('graphics/right1.png').convert_alpha(), (96,96)), pygame.transform.scale(pygame.image.load('graphics/right2.png').convert_alpha(), (96,96))
        up1, up2, up3, up4, up5 = pygame.transform.scale(pygame.image.load('graphics/up1.png').convert_alpha(), (96,96)), pygame.transform.scale(pygame.image.load('graphics/up2.png').convert_alpha(), (96,96)), pygame.transform.scale(pygame.image.load('graphics/up3.png').convert_alpha(), (96,96)), pygame.transform.scale(pygame.image.load('graphics/up4.png').convert_alpha(), (96,96)), pygame.transform.scale(pygame.image.load('graphics/up5.png').convert_alpha(), (96,96))
        down1, down2, down3, down4, down5, down6 = pygame.transform.scale(pygame.image.load('graphics/down1.png').convert_alpha(), (96,96)), pygame.transform.scale(pygame.image.load('graphics/down2.png').convert_alpha(), (96,96)), pygame.transform.scale(pygame.image.load('graphics/down3.png').convert_alpha(), (96,96)), pygame.transform.scale(pygame.image.load('graphics/down4.png').convert_alpha(), (96,96)), pygame.transform.scale(pygame.image.load('graphics/down5.png').convert_alpha(), (96,96)), pygame.transform.scale(pygame.image.load('graphics/down6.png').convert_alpha(), (96,96))

        self.velocity = 1 # MOVEMENT SPEED
        self.shift = False # FOR SPRINTING: HOLD LSHFT
        self.moveLeft = False  # ----
        self.moveRight = False # SETS PLAYER MOVEMENT-TOGGLE-VARIABLES
        self.moveUp = False    # ----
        self.moveDown = False  # ----

        self.idle = [idle1, idle2]
        self.idleIndex = 0
        self.idling = False

        self.runRight = [right1, right2]
        self.rightIndex = 0
        self.runningRight = False

        self.runLeft = [left1, left2]
        self.leftIndex = 0
        self.runningLeft = False

        self.runUp = [up1, up2, up3]
        self.upIndex = 0
        self.runningUp = False

        self.runDown = [down1, down2, down3]
        self.downIndex = 0
        self.runningDown = False

        self.moveFrame = 0
        self.moveFrameDown = 0

        self.image = self.idle[self.idleIndex] # PLAYER SURFACE / SPRITE
        #self.image.fill((123,159,147)) # FILLS IMAGE WITH COLOR
        self.rect = self.image.get_rect() # GETS RECT FROM LOADED IMAGE
        self.rect.topleft = [x_pos, y_pos] # SETS RECT COORDS

        try:
            self.stats = {
                'name': 'Sirius',
                'level': data['lvl'],
                'exp': data['xp'],
                'health': data['hp'],
                'items': data['inv'],
                'equip': data['eqp'],
                'magic': data['mgc'],
                '$$$': data['$']
                }
        except:
            self.stats = {
                'name': 'Sirius',
                'level': 3,
                'exp': 0,
                'health': 99,
                'items': [],
                'equip': {
                    'head': None,
                    'body': None,
                    'legs': None,
                    'cowl': None,
                    'wpn1': None,
                    'wpn2': None,
                    },
                'magic': [],
                '$$$': 6
                }
        
        self.walkingPace = 1000 // 7 #Higher == faster. inter-frame delay in milliseconds
        self.runningPace = 1000 // 10
        self.millisec_rate = self.walkingPace
        self.last_frame_at = 0
        self.shouldAnimate = True
        self.isIdling = True
        self.lengthBeforeIdling = 1000

    def movement(self):


        if self.shift:
            self.velocity = 3
            self.millisec_rate = self.runningPace
        else:
            self.velocity = 1
            self.millisec_rate = self.walkingPace


        time_now = pygame.time.get_ticks()
        if (time_now > self.last_frame_at + self.millisec_rate):
            self.moveFrame += 1
            self.shouldAnimate = True
            self.last_frame_at = time_now
        else:
            self.shouldAnimate = False

        if self.moveDown and self.rect.bottom < pygame.display.get_surface().get_height():
            if (self.moveFrame >= len(self.runDown)):
                self.moveFrame = 0
            if self.shouldAnimate:
                self.image = self.runDown[self.moveFrame]
            self.rect.bottom += self.velocity
            self.isIdling = False


        if self.moveUp and self.rect.top > 0:
            if (self.moveFrame >= len(self.runUp)):
                self.moveFrame = 0
            if self.shouldAnimate:
                self.image = self.runUp[self.moveFrame]
            self.rect.top -= self.velocity
            self.isIdling = False


        if self.moveLeft and self.rect.left > 0:
            if (self.moveFrame >= len(self.runLeft)):
                self.moveFrame = 0
            if self.shouldAnimate:
                self.image = self.runLeft[self.moveFrame]
            self.rect.left -= self.velocity
            self.isIdling = False


        if self.moveRight and self.rect.right < pygame.display.get_surface().get_width():
            if (self.moveFrame >= len(self.runRight)):
                self.moveFrame = 0
            if self.shouldAnimate:
                self.image = self.runRight[self.moveFrame]
            self.rect.right += self.velocity
            self.isIdling = False

        if self.isIdling:
            if self.moveFrame >= len(self.idle):
                self.moveFrame = 0
            self.image = self.idle[self.moveFrame]

    def update(self):
        self.movement()
        pygame.display.get_surface().blit(self.image, self.rect)


class NPC(pygame.sprite.Sprite):

    def __init__(self, name, health, image, x_pos, y_pos):
        super().__init__()

        self.name = name
        self.image = image
        #self.image.fill((222,54,147))
        self.rect = self.image.get_rect(center = (x_pos, y_pos))
        #self.velocity = 1
        self.stats = {
            'name': name,
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
            sirius.stats['health'] += 1

    def update(self):
        screen.blit(self.image, self.rect)
        

# SPRITE CLASS INSTANCES
siriusSprite = pygame.sprite.GroupSingle() # CREATE SPRITE GROUP
npc_sprites = pygame.sprite.Group()
allSprites = pygame.sprite.Group()
objectSprites = pygame.sprite.Group()

sirius = Player(400, 600) # CREATE SPRITE
aldhara = NPC('Aldhara', 300, pygame.Surface((32,64)), 333, 666)
jynx = NPC('Jynx', 50, pygame.transform.flip(pygame.transform.scale(pygame.image.load('graphics/Juggler_Attack_Blue.gif').convert_alpha(), (96,96)), True, False), 600, 200)
shopKeep = NPC('Item Shop Owner', 30, pygame.Surface((32,64)), 600, 600)

siriusSprite.add(sirius) # ADD SPRITE
npc_sprites.add(aldhara, jynx, shopKeep)
#objectSprites.add(tree1, bush1, bush1, bush2, bush2, bush3, bush3)
allSprites.add(sirius, aldhara, jynx, shopKeep, house1, tree1,
               bush1, bush1, bush2, bush2, bush3, bush3)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def messageToScreen(text, xPos, yPos):

    basicFont = pygame.font.SysFont(None, 36, italic = True)

    msg = basicFont.render(text, True, (33,33,33))
    msgRect = msg.get_rect(center = (xPos, yPos))
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

# FUNCTION TO DISPLAY STATS IN MENU SCREEN
def displayStats():
    messageToScreen(f'LEVEL: {sirius.stats["level"]}', 130, 369)
    messageToScreen(f'EXPERIENCE: {sirius.stats["exp"]}', 130, 408)
    messageToScreen(f'HP: {sirius.stats["health"]}', 130, 450)
    messageToScreen(f'Currency: {sirius.stats["$$$"]} pcs', 130, 490)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Button:
    def __init__(self, text, w, h, pos, textColor, rectColor):

        basicFont = pygame.font.SysFont(None, 36, italic = True)

        
        # TOP RECT
        self.topRect = pygame.Rect(pos,(w,h))
        self.topColor = rectColor

        # TEXT
        self.textSurf = basicFont.render(text, False, textColor)
        self.textRect = self.textSurf.get_rect(center = self.topRect.center)


        self.clicked = False

    def draw(self):
        pygame.draw.rect(screen, self.topColor, self.topRect, border_radius = 12)
        screen.blit(self.textSurf, self.textRect)

    def checkClick(self):
        mousePos = pygame.mouse.get_pos()
        if self.topRect.collidepoint(mousePos):
            self.clicked = True
            self.topColor = (255,50,50)
            
        else:
            self.topColor = (33,255,33)
            self.clicked = False


saveExit = Button('Save & Exit', 200, 50, (525, 720), (0,0,0), (33,255,33))

mapScrn = Button('Map', 200, 50, (525, 666), (0,0,0), (33,255,33))

btlAtk = Button('Attack!', 150, 50, (100, 600), (0,0,0), (33,255,33))

btlDfn = Button('Defend', 150, 50, (100, 650), (0,0,0), (22,255,33))

btlInv = Button('Items', 150, 50, (100, 700), (0,0,0), (22,255,33))

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def Menu():
    global dagger
    
    menu = True
    
    sound.pause()
    music.pause()
    menuVibe.unpause()

    print('menu entered')

    basicFont = pygame.font.SysFont(None, 36, italic = True)

    menuPlyr = pygame.transform.scale(pygame.image.load('graphics/down6.png').convert_alpha(), (160,160))
    menuPlayer = menuPlyr
    menuPlayerRect = menuPlyr.get_rect(center = (130, 230))

    plrBorder = pygame.Rect(menuPlayerRect.x, menuPlayerRect.y, menuPlayerRect.width, menuPlayerRect.height)
    playerText = basicFont.render('Sirius', True, (213,123,213))
    playerTextRect = playerText.get_rect(bottomleft = plrBorder.topleft)

    itemBorder = pygame.Rect(30, 630, 444, 150)
    itemText = basicFont.render('INVENTORY', True, (213,123,213))
    itemTextRect = itemText.get_rect(bottomleft = itemBorder.topleft)

    while menu:

        screen.fill((245,245,245))

        screen.blit(menuBGI, (400, 0, 420, 720))
        menuBGI.set_alpha(81)
        pygame.draw.line(screen, (0,0,0), (530,81), (369,81), 2)
        pygame.draw.line(screen, (0,0,0), (500,150), (369,150), 2)
        pygame.draw.line(screen, (0,0,0), (480,300), (369,300), 2)
        pygame.draw.line(screen, (0,0,0), (540,600), (369,600), 2)
        pygame.draw.rect(screen, (0,0,0), (270, 15, 72, 72), 2)
        pygame.draw.rect(screen, (0,0,0), (270, 144, 72, 72), 2)
        pygame.draw.rect(screen, (0,0,0), (270, 291, 72, 72), 2)
        pygame.draw.rect(screen, (0,0,0), (270, 531, 72, 72), 2)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print('menu exited')
                    menuVibe.pause()
                    sound.unpause()
                    music.unpause()
                    menu = False
                    
            # MOUSE EVENT DETECTION

            pygame.mouse.set_cursor(system)
            mx, my = pygame.mouse.get_pos()

            left, middle, right = pygame.mouse.get_pressed()

            rightClicking = False
            leftCLicking = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:

                if left:
                    leftClicking = True
                    if saveExit.clicked == True:
                        data = {
                            'lvl': sirius.stats['level'],
                            'xp': sirius.stats['exp'],
                            '$': sirius.stats['$$$'],
                            'hp': sirius.stats['health'],
                            'mgc': sirius.stats['magic'],
                            'inv': sirius.stats['items'],
                            'eqp': sirius.stats['equip'],
                            }

                        with open('save_file.txt', 'w') as test_file:
                            json.dump(data, test_file)

                        pygame.quit()
                        exit()

                    elif mapScrn.clicked == True:
                        #messageToScreen('Navigate to MAP screen', 400, 400)
                        dagger.equip()

                    else:
                        print('nothing to interact with')

                if middle:
                    print('middle button clicked')

                if right:
                    print('right button clicked')
                    rightClicking = True
                    if aldhara.rect.collidepoint(mx,my) or jynx.rect.collidepoint(mx,my):
                        if leftClicking:
                            print('SPECIAL')
                        else:
                            print('open NPC interact options')

            if event.type == pygame.MOUSEBUTTONUP:

                if left:
                    leftClicking = False

                if right:
                    rightClicking = False
            
        screen.blit(menuPlayer, menuPlayerRect)
        screen.blit(itemText, itemTextRect)
        screen.blit(playerText, playerTextRect)

        saveExit.draw()
        mapScrn.draw()

        pygame.draw.rect(screen, (123,23,123), plrBorder, 2)
        pygame.draw.rect(screen, (0,0,0), itemBorder, 2)

        dagger.draw(273, 18)

        displayStats()

        saveExit.checkClick()
        mapScrn.checkClick()

        pygame.display.update()

        clock.tick(60)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def Battle(atkr, dfndr):

    music.pause()
    sound.pause()
    battle.play(battleMusic, -1)

    basicFont = pygame.font.SysFont(None, 66, italic = True)

    atkTimer = 333

    enemyAtkTimer = 333
    

    atkrCopy = pygame.transform.scale(atkr.image, (320, 320))
    aHealthBar = []
    for i in range(0, atkr.stats['health']):
        aHealthBar.append(pygame.draw.rect(screen, (255,25,25), (i + 630, 500, 5, 20)))


    dfndrCopy = pygame.transform.scale(pygame.image.load('graphics/right2.png').convert_alpha(), (320, 320))
    dHealthBar = []
    for i in range(0, dfndr.stats['health']):
        dHealthBar.append(pygame.draw.rect(screen, (255,25,25), (i + 100, 500, 5, 20)))


    fight = True
    while fight:

        villageSound.stop()
        
        screen.fill((255,255,255))

        for event in pygame.event.get():

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    battle.stop()
                    music.unpause()
                    sound.unpause()
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

                    if btlAtk.clicked == True:

                        if atkTimer <= 1:

                            hitChance = random.randint(1,100)

                            if hitChance >= 66:
                                print('attack successful')

                            else:
                                print('Attack MISSED!')

                            atkTimer = 450

                        else:
                            print('wait for atk cooldown')

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
            pygame.draw.rect(screen, (255,25,25), aHealthBar[hp])
        screen.blit(aHealthDisplay, aHealthDisplayRect)

        dHealthDisplay = basicFont.render(str(len(dHealthBar)), False, (255,255,255))
        dHealthDisplayRect = dHealthDisplay.get_rect(center = (w/2,h/6))
        for hp in range(len(dHealthBar)):
            pygame.draw.rect(screen, (255,25,25), dHealthBar[hp])
        screen.blit(dHealthDisplay, dHealthDisplayRect)


        screen.blit(dfndrCopy,(w-800,h/4,10,10))
        screen.blit(atkrCopy, (w-300,h/4-30,10,10))


        btlAtk.draw()
        btlAtk.checkClick()

        btlDfn.draw()
        btlDfn.checkClick()

        btlInv.draw()
        btlInv.checkClick()

        # ATTACK TIMER TO LIMIT ATK INPUT
        atkTimer -= 1

        debug(atkTimer)

        if atkTimer <= 0:
            atkTimer = 0


        enemyAtkTimer -= 1

        messageToScreen(str(enemyAtkTimer), atkr.rect.x, atkr.rect.y-30)

        if enemyAtkTimer <= 0:

            choices = ['atk', 'heal', 'escape']

            choice = random.choice(choices)

            if choice == 'atk':

                hitChance = random.randint(1, 100)

                if hitChance > 66 and hitChance < 99:
                    print(choice)

                else:
                    print(choice, 'misses')

            elif choice == 'heal':
                print(choice)

            elif choice == 'escape':
                print(choice)

            enemyAtkTimer = 333

        
        pygame.display.update()


        clock.tick(60)

def Start():
    global siriusSprite

    up1 = pygame.transform.scale(pygame.image.load('graphics/up1.png').convert_alpha(), (96,96))

    menuVibe.play(menuMusic, -1)

    STRT = Button('Click To Begin', 200, 50, (300, 400), (255,255,255),(123,123,255))
    SET = Button('Settings', 200, 50, (300, 500), (255,255,255),(123,123,255))
    
    start = True
    while start:
        # EVENT DETECTION LOOP
        for event in pygame.event.get():

        # QUIT GAME EVENT DETECTION
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        left, middle, right = pygame.mouse.get_pressed()

        rightClicking = False
        leftCLicking = False

        if left:
            leftClicking = True
            if STRT.clicked == True:
                menuVibe.pause()
                music.play(villageMusic, -1)
                sound.play(villageSound, -1)
                break

            elif SET.clicked == True:
                SETTINGS()

            else:
                print('Left Button Clicked')

        strtScrn.update()

        STRT.draw()
        STRT.checkClick()

        SET.draw()
        SET.checkClick()

        sirius.image = up1
        siriusSprite.draw(screen)
        sirius.rect.center = (230, 580)

        pygame.display.update()
        clock.tick(60)

def SETTINGS():

    bgi = pygame.Surface((800, 800))
    bgi.fill((133,133,133))
    bgi.set_alpha(6)

    volUp = Button('Louder', 100, 50, (300, 400), (123,123,123),(231,123,255))
    volDown = Button('Softer', 100, 50, (300, 500), (123,123,123),(231,123,255))
    
    settings = True
    while settings:

        messageToScreen('Volume', 333, 475)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    settings = False

        left, middle, right = pygame.mouse.get_pressed()

        rightClicking = False
        leftCLicking = False

        if left:
            leftClicking = True
            if volUp.clicked == True:
                menuMusic.set_volume(menuMusic.get_volume()+.01)
            elif volDown.clicked == True:
                menuMusic.set_volume(menuMusic.get_volume()-.01)

            #else:
                #print('Left Button Clicked')

        volUp.draw()
        volUp.checkClick()

        volDown.draw()
        volDown.checkClick()

        screen.blit(bgi, (0,0,800,800))

        pygame.display.update()
        clock.tick(60)


# THIS VARIABLE WILL CONTROL WHEN THE BOSS BATTLE OPENS UP (ONCE 3 SLAIN, BOSS BATTLE, ETC)
enemiesKilled = 0

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# MAIN GAME LOOP
run = True

Start()

while run:

    #print(pygame.time.get_ticks())


    # DELTA-TIME VARIABLES
    dt = time.time() - previous_time
    previous_time = time.time()


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
            run = False

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

      
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                pass

            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                print('Left Arrow Pressed')
                sirius.moveLeft = True

            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                print('Right Arrow Pressed')
                sirius.moveRight = True

            if event.key == pygame.K_w or event.key == pygame.K_UP:
                print('Up Arrow Pressed')
                sirius.moveUp = True

            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                print('Down Arrow Pressed')
                sirius.moveDown = True

            if event.key == pygame.K_SPACE:
                print('Space Bar Pressed')
                Menu()

            if event.key == pygame.K_LSHIFT:# IF LSHFT HELD: 'SPRINT MOVEMENT'
                print('shift Pressed')
                sirius.shift = True


        # KEY UP
        if event.type == pygame.KEYUP:

            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                print('left arrow released')
                sirius.moveLeft = False
                bg.scrollLeft = False

            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                print('Right arrow released')
                sirius.moveRight= False
                bg.scrollRight = False

            if event.key == pygame.K_w or event.key == pygame.K_UP:
                print('Up arrow released')
                sirius.moveUp = False
                bg.scrollUp = False

            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
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
                print(dagger)
                print(type(dagger))
                dagger.equip()

            if middle:
                print('middle button clicked')

            if right:
                rightClicking = True
                print('right button clicked')
                if aldhara.rect.collidepoint(mx,my):
                    if left:
                        print('SPECIAL')
                    else:
                        print('open NPC interact options')
                elif jynx.rect.collidepoint(mx,my):
                    Battle(jynx, sirius)

        if event.type == pygame.MOUSEBUTTONUP:

            if left:
                leftClicking = False

            if right:
                rightClicking = False


    # DRAW SPRITE
    siriusSprite.update()
    sirius.movement()

    jynx.collide()


    # RENDERS SPRITES IN ORDER ACCORDING TO Y-AXIS
    allSprites.update()

    for sprite in sorted(allSprites, key = lambda sprite: sprite.rect.bottom):
        pygame.display.get_surface().blit(sprite.image, sprite.rect)

    
    #bg.scroll()


    debug('DEMO VERSION')


    # UPDATES DISPLAY EACH FRAME
    pygame.display.update()


    # RESETS FRAMERATE EACH FRAME 
    clock.tick(60)

pygame.quit()
exit()
