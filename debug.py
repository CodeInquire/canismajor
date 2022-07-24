import pygame

pygame.init()

font = pygame.font.Font(None, 33)

def debug(info, x = 100, y = 100):

    displaySurf = pygame.display.get_surface()

    debugSurf = font.render(str(info), True, 'Black')

    debugRect = debugSurf.get_rect(topleft = (x, y))

    displaySurf.blit(debugSurf, debugRect)
