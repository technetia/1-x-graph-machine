# gui.py
#
# GUI elements.

import pygame
from pygame.locals import *
pygame.init()

class Container(pygame.sprite.Group):
    """
    A container of widgets.

    Currently nothing over a normal Group.
    """
    pass

class Widget(pygame.sprite.Sprite):
    """
    Abstract base class for widgets.
    """

    def __init__(self):
        super(Widget, self).__init__()
        
    def get_rect(self):
        return pygame.Rect(
            self.x, self.y, self.image.get_width(), self.image.get_height())

    def update(self, *events):
        self.check_events(*events)

    def check_events(self, *events):
        pass

class Label(Widget):
    """
    Plain text.
    """

    def __init__(self, x, y, text, size = 25, color = (255, 255, 255)):
        """
        x, y - coordinates of the Label
        text - self-explanatory
        size - text size
        color - text color
        """
        super(Label, self).__init__()
        self.x = x
        self.y = y
        self.text = text
        self.size = size
        self.color = color
        self.__f = pygame.font.Font(None, size)
        self.image = self.__f.render(text, True, color)
        self.rect = self.get_rect()

    def update(self, *events):
        super(Label, self).update(*events)
        self.image = self.__f.render(self.text, True, self.color)
        self.rect = self.get_rect()
        
class Button(Widget):
    """
    A basic button that uses an image.

    It displays the given text whenever the mouse cursor hovers on it,
    unless the text is a null string, in which case the parameters
    size and color are irrelevant.
    """
    
    def __init__(self, x, y, image, text, size = 25, color = (255, 255, 255),
                 function = None):
        """
        x, y - coordinates of the Button
        image - image of the Button
        text - text the Button will display when cursor hovers over it
        size - text size
        color - text color
        function - if not None, it calls the given function when clicked
        (can only be a function without arguments)
        """
        super(Button, self).__init__()
        self.x = x
        self.y = y
        self.image = image
        self.__original_image_copy = image
        self.text = text
        self.size = size
        self.color = color
        self.__f = pygame.font.Font(None, self.size)
        
        self.clicked = False
        # this status variable tests if the mouse button was pressed
        # down on this particular Button - the purpose is so that when
        # the mouse button is released, we can see if it's still overlapping
        # the same Button
        self.__button_down = False
        
        self.__text_on = False
        self.rect = self.get_rect()
        self.function = function

    def set_new_image(self, new_image):
        """
        Change the base image of the Button.
        """
        self.__original_image_copy = new_image
        
    def update(self, *events):
        super(Button, self).update(*events)
        self.image = self.__render()
        self.rect = self.get_rect()

    def check_events(self, *events):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.__text_on = True
        else:
            self.__text_on = False
            
        for event in events:
            if event.type == MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
                self.__button_down = True

            elif event.type == MOUSEBUTTONUP:
                if self.__button_down and self.rect.collidepoint(event.pos):
                    self.__text_on = False
                    # client code then checks to see if "clicked" is True
                    # and does whatever, then resets this value to False
                    # (if they don't want to just use the function variable
                    # instead)
                    self.clicked = True
                    if self.function:
                        self.function()
                        
                self.__button_down = False
                    
        
    def __render(self):
        surface = self.__original_image_copy.copy()
        
        if self.text and self.__text_on:
            f_im = self.__f.render(self.text, True, self.color)
            x = (surface.get_width() / 2) - (f_im.get_width() / 2)
            y = (surface.get_height() / 2) - (f_im.get_height() / 2)
            surface.blit(f_im, (x, y))
            
        return surface.convert()

class TextEntry(Widget):
    """
    Text entry widget.
    """
    
    def __init__(self, x, y, text, size, color, length):
        """
        x, y - coordinates of the TextEntry
        text - prompt
        size - size of prompt text and entry text
        color - color of text
        length - length (in pixels)
        """
        super(TextEntry, self).__init__()
        self.x = x
        self.y = y

        # text is the prompt plus anything the user types
        # original_text is the prompt
        # expr_text is whatever the user types (public so that it
        # can be used)
        self.text = text
        self.__original_text = text
        self.expr_text = ""
        self.length = length

        # we save a copy of the font so that we don't keep needing
        # to recreate one
        self.__f = pygame.font.Font(None, size)
        self.__cursor_width = self.__f.size("_")[0]
        
        # we first save the original image (prompt only)
        # so that we can refer to something
        self.color = color
        self.__original_image_copy = \
            pygame.Surface((length, self.__f.get_height()))
        self.__original_image_copy.set_colorkey((0, 0, 0))
        self.image = self.__original_image_copy
        self.rect = self.get_rect()
        
        self.__has_focus = False
        
    def update(self, *events):
        super(TextEntry, self).update(*events)
        self.image = self.__render()
        self.rect = self.get_rect()

    def check_events(self, *events): 
        for event in events:
            # add/remove end "cursor" (underscore)
            if event.type == MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    if not self.__has_focus:
                        self.__has_focus = True
                        self.text += "_"
                else:
                    if self.__has_focus:
                        self.__has_focus = False
                        self.text = self.text[:-1]


            elif event.type == KEYDOWN:
                if self.__has_focus:
                    # first remove underscore
                    self.text = self.text.rstrip("_")
                    # now add key
                    if event.key == K_BACKSPACE:
                        self.text = self.text[:-1]
                        if len(self.text) < len(self.__original_text):
                            self.text = self.__original_text
                        
                    else:
                        char = event.unicode
                        import string
                        if char in string.printable:
                            self.text += char

                    # prevent typing more text than permitted by sizing
                    text_w = self.__f.size(self.text)[0] + self.__cursor_width
                    if text_w > self.rect[2]:
                        self.text = self.text[:-1]
                        
                    self.expr_text = self.text[len(self.__original_text):]        
                    # then add underscore to the end
                    self.text += "_"
                    
    def __render(self):
        surface = self.__original_image_copy.copy()
        surface.blit(self.__f.render(self.text, True, self.color), (0, 0))
        return surface.convert()
    
        
