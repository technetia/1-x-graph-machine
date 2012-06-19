# utils.py

import os
import pygame

def quit():
    pygame.quit()
    exit()

def cls(surface):
    surface.fill((0, 0, 0))
    
def load_image(name, transparency = False):
    im = pygame.image.load(os.path.join("images", name))
    if transparency:
        corner = im.get_at((0, 0))
        im.set_colorkey(corner, pygame.constants.RLEACCEL)
    return im.convert()

def load_tfile(name, mode):
    return open(os.path.join("text", name), mode)

def get_text(text, size, color):
    font = pygame.font.Font(None, size)
    return font.render(text, True, color)

def blit_text(surface, text, size, color, x, y):
    surface.blit(get_text(text, size, color), (x, y))
