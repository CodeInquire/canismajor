import pygame

pygame.mixer.init()

villageSound = pygame.mixer.Sound('audio/village.mp3') # CREATES A 'SOUND' OBJECT
villageSound.set_volume(.18) # SETS VOLUME OF SOUNS
villageMusic = pygame.mixer.Sound('audio/CanisMajorForestWandering.mp3')
villageMusic.set_volume(.10)

sound = pygame.mixer.Channel(1) # CREATES MUSIC CHANNEL
sound.play(villageSound, -1) # PLAYS MUSIC CHANNEL INDEFINITELY 
#music.queue() # QUEUES THE NEXT SOUND FILE
music = pygame.mixer.Channel(2)
music.play(villageMusic, -1)

def messageToScreen(text, xPos, yPos):

    basicFont = pygame.font.SysFont(None, 36, italic = True)

    msg = basicFont.render(text, True, (0,0,0))
    msgRect = msg.get_rect(center = (xPos, yPos))
    msgBox = pygame.Rect(((msgRect.x - 3),
                          (msgRect.y - 3),
                          (msgRect.width + 3),
                          (msgRect.height + 3)))
    
    msgBoxFill = pygame.Rect(((msgRect.x - 3),
                              (msgRect.y - 3),
                              (msgRect.width + 3),
                              (msgRect.height + 3)))

    pygame.draw.rect(pygame.display.get_surface(), (123,23,123), msgBox, 5)
    pygame.draw.rect(pygame.display.get_surface(), (234,234,234), msgBoxFill)

    pygame.display.get_surface().blit(msg,msgRect)

def displayStats():
    messageToScreen(f'LEVEL: {sirius.stats["level"]}', 130, 345)
    messageToScreen(f'EXPERIENCE: {sirius.stats["exp"]}', 130, 385)
    messageToScreen(f'HP PTS: {sirius.stats["health"]}', 130, 425)

def Menu():
    global saveExit, mapScreen
    
    menu = True
    
    sound.pause()
    music.pause()

    print('menu entered')

    basicFont = pygame.font.SysFont(None, 36, italic = True)

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

        pygame.display.get_surface().fill((123,123,231))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print('menu exited')
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
                            'hp': sirius.stats['health'],
                            'mgc': sirius.stats['magic'],
                            'inv': sirius.stats['items'],
                            'eqp': sirius.stats['equip'],
                            }

                        with open('save_file.txt', 'w') as test_file:
                            json.dump(data, test_file)

                        pygame.quit()
                        exit()

                    else:
                        print(sirius.stats['equip']['wpn1'])

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
            
        pygame.display.get_surface().blit(menuPlayer, menuPlayerRect)
        pygame.display.get_surface().blit(itemText, itemTextRect)
        pygame.display.get_surface().blit(playerText, playerTextRect)

        saveExit.draw()
        mapScrn.draw()

        pygame.draw.rect(pygame.display.get_surface(), (255,255,255), plrBorder, 5)
        pygame.draw.rect(pygame.display.get_surface(), (255,255,255), itemBorder, 5)

        displayStats()

        saveExit.checkClick()
        mapScrn.checkClick()

        pygame.display.update()

        clock.tick(60)

def battle(atkr, dfndr):

    basicFont = pygame.font.SysFont(None, 66, italic = True)
    

    atkrCopy = pygame.transform.scale(atkr.image, (320, 320))
    aHealthBar = []
    for i in range(0, atkr.stats['health']):
        aHealthBar.append(pygame.draw.rect(pygame.display.get_surface(), (50,220,50), (i + 630, 500, 5, 20)))


    dfndrCopy = pygame.transform.scale(dfndr.image, (320, 320))
    dHealthBar = []
    for i in range(0, dfndr.stats['health']):
        dHealthBar.append(pygame.draw.rect(pygame.display.get_surface(), (50,220,50), (i + 100, 500, 5, 20)))


    fight = True
    while fight:

        villageSound.stop()
        
        pygame.display.get_surface().fill((0,0,0))

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
        aHealthDisplayRect = aHealthDisplay.get_rect(center = (800/2,800/6))
        for hp in range(len(aHealthBar)):
            pygame.draw.rect(pygame.display.get_surface(), (50,220,50), aHealthBar[hp])
        pygame.display.get_surface().blit(aHealthDisplay, aHealthDisplayRect)

        dHealthDisplay = basicFont.render(str(len(dHealthBar)), False, (255,255,255))
        dHealthDisplayRect = dHealthDisplay.get_rect(center = (800/2,800/6))
        for hp in range(len(dHealthBar)):
            pygame.draw.rect(pygame.display.get_surface(), (50,220,50), dHealthBar[hp])
        pygame.display.get_surface().blit(dHealthDisplay, dHealthDisplayRect)


        pygame.display.get_surface().blit(dfndrCopy,(800-800,800/4,10,10))
        pygame.display.get_surface().blit(atkrCopy, (800-300,800/4-30,10,10))


        btlAtk.draw()
        btlAtk.checkClick()

        btlDfn.draw()
        btlDfn.checkClick()

        btlInv.draw()
        btlInv.checkClick()

        
        pygame.display.update()


        clock.tick(60)
