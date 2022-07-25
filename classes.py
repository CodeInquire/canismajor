import pygame

class Object(pygame.sprite.Sprite):

    def __init__(self, image, x_pos, y_pos):
        super().__init__()

        self.image = image
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect(bottomleft = (x_pos, y_pos))

        self.hitbox = self.rect.inflate(0, -30)

    def update(self):
        pygame.display.get_surface().blit(self.image, self.rect)

class BGI:

    def __init__(self, image, xPos, yPos):
        self.image = image
        self.rect = self.image.get_rect(center = (800/2, 800/2))
        self.scrollLeft = False
        self.scrollRight = False
        self.scrollUp = False
        self.scrollDown = False

    def update(self):
        pygame.display.get_surface().blit(self.image, self.rect)

    def scroll(self):
        if self.scrollLeft:
            if self.rect.left <= 0:
               self.rect.left += test1.velocity
            else:
                self.rect.left = 0
                
        if self.scrollRight:
            if self.rect.right >= 800:
                self.rect.right -= test1.velocity
            else:
                self.rect.right = 800

        if self.scrollUp:
            if self.rect.top <= 0:
                self.rect.top += test1.velocity
            else:
                self.rect.top = 0

        if self.scrollDown:
            if self.rect.bottom >= 800:
                self.rect.bottom -= test1.velocity
            else:
                self.rect.bottom = 800

class Weapon(pygame.sprite.Sprite):
    def __init__(self, name, description, image, type, attackPower, special):
        super().__init__()

        self.name = name
        self.dscr = description
        self.image = image
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
            sirius.stats['equip']['wpn1'] = self
        else:
            print('You dont own that item!')


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

        self.idle = [idle1, idle2]
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

        self.moveFrame = 0
        self.moveFrameDown = 0

        self.image = self.idle[self.idleIndex] # PLAYER SURFACE / SPRITE
        #self.image.fill((123,159,147)) # FILLS IMAGE WITH COLOR
        self.rect = self.image.get_rect() # GETS RECT FROM LOADED IMAGE
        self.rect.topleft = [x_pos, y_pos] # SETS RECT COORDS

        self.stats = {
            'name': 'Sirius',
            'level': data['lvl'],
            'exp': data['xp'],
            'health': data['hp'],
            'items': data['inv'],
            'equip': data['eqp'],
            'magic': data['mgc']
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
        # self.animate()
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
        pygame.draw.rect(pygame.display.get_surface(), self.topColor, self.topRect, border_radius = 12)
        screen.blit(self.textSurf, self.textRect)

    def checkClick(self):
        mousePos = pygame.mouse.get_pos()
        if self.topRect.collidepoint(mousePos):
            
            self.topColor = (255,50,50)
            self.clicked = True
            
        else:
            self.topColor = (33,255,33)
            self.clicked = False

