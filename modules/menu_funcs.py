# menu_funcs.py

######################################################################
## Setup
######################################################################

from __future__ import division

# In case of Python 2.5 users
from __future__ import with_statement

import colors, draw_funcs, constants, utils, gui

import os
import re
import pygame
from pygame.locals import *

os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

SCREEN = None
BACKGROUND = None
GRAPH = {}
COLOR_LIST = []
COL_POS_LIST = []
text_entries = []
button_entries = []

######################################################################
## Functions
######################################################################

def setup():
    """
    Initialization.
    """
    global COLOR_LIST, COL_POS_LIST, text_entries, button_entries

    # essential for text entry input
    pygame.key.set_repeat(500, 20)
    
    # graph settings
    GRAPH["width"] = constants.SCR_WIDTH
    GRAPH["height"] = constants.SCR_HEIGHT
    GRAPH["axis_thickness"] = 4
    
    with utils.load_tfile("settings.txt", "rU") as f:
        for line in f:
            l = line.rstrip("\n")
            if l.startswith("x") or l.startswith("y"):
                components = l.split(" ")
                GRAPH[components[0]] = float(components[1])
            elif l.startswith("GRAPH_ANIM"):
                components = l.split(" ")
                GRAPH[components[0]] = bool(int(components[1]))
                
    GRAPH["x_dist"] = GRAPH["x_right"] - GRAPH["x_left"]
    GRAPH["y_dist"] = GRAPH["y_bottom"] - GRAPH["y_top"]

    text_entry_y_pos = 100
    text_entry_text_size = 30

    y_positions = range(text_entry_y_pos,
                        constants.SCR_HEIGHT - text_entry_text_size,
                        text_entry_text_size)

    COLOR_LIST = [getattr(colors, c) for c in dir(colors) if not c.startswith("_")]
    # don't use black, as that's typically the background color
    COLOR_LIST.remove(colors.black)

    COL_POS_LIST = [0] * len(y_positions)
    button_size = 20
    button_x_pos = 10
    col = pygame.Surface((button_size, button_size))
    col.fill(COLOR_LIST[0])

    text_entries = [gui.TextEntry(50, y, "f(x)=", text_entry_text_size, colors.white, 700) for y in y_positions]
    button_entries = [gui.Button(button_x_pos, y, col, "", color = COLOR_LIST[0]) for y in y_positions]

def init_screen():
    global SCREEN, BACKGROUND
    # minimum screen resolution requirements
    assert constants.SCR_WIDTH >= 800, "screen width < 800"
    assert constants.SCR_HEIGHT >= 600, "screen height < 600"

    # icon
    icon_image = pygame.image.load(os.path.join("images", "icon.bmp"))
    pygame.display.set_icon(icon_image)

    # display screen
    SCREEN = pygame.display.set_mode(constants.RESOLUTION)
    pygame.display.set_caption(">> 1-X Graph Machine")
    pygame.mouse.set_cursor(*pygame.cursors.diamond)
    # image credit: NASA
    BACKGROUND = utils.load_image("hubbles_universe_3d.jpg")
    # scale background image if not correctly sized
    if BACKGROUND.get_size() != constants.RESOLUTION:
        BACKGROUND = pygame.transform.scale(BACKGROUND, constants.RESOLUTION)

def blit_background():
    utils.cls(SCREEN)
    SCREEN.blit(BACKGROUND, (0, 0))
    
def menu():  
    box = gui.Container()
    box.add(
        gui.Button(100, 50, utils.load_image("sphere.bmp", True),
                   "Graph", 30, colors.white, get_func_exprs))
    box.add(
        gui.Button(300, 200, utils.load_image("sphere.bmp", True),
                   "Settings", 30, colors.white, settings))
    box.add(
        gui.Button(500, 350, utils.load_image("sphere.bmp", True),
                   "Help", 30, colors.white, xhelp))
    
    while True:
        if pygame.event.peek(QUIT):
            utils.quit()

        events = pygame.event.get()
        box.update(*events)
        blit_background()
        box.draw(SCREEN)
        pygame.display.update()

def xhelp():
    """
    Show help. Prefixed with an "x" to avoid confusion with builtin.
    """
    def load():
        """load help text files"""
        for i in range(5):
            parts.append([])
            with utils.load_tfile("help%d.txt" % (i + 1), "rU") as f:
                for line in f:
                    parts[i].append(line.rstrip("\n"))
                    
    def update():
        """update with new text"""
        help_labels.empty()
        y = 100
        help_labels.add(gui.Label(100, 10, parts[current_part][0], 30))
        for t in parts[current_part][2:]:
            help_labels.add(gui.Label(10, y, t, 20))
            y += 20
            
    box = gui.Container()
    help_labels = gui.Container()
    
    box.add(
        gui.Button(10, 10, utils.load_image("cube.bmp", True), "Back"))
    box.add(
        gui.Button(constants.SCR_WIDTH - 70, 10,
                   utils.load_image("cube.bmp", True), "Next"))
    
    parts = []
    current_part = 0
    load()
    update()
    
    while True:
        if pygame.event.peek(QUIT):
            utils.quit()

        events = pygame.event.get()
        box.update(*events)
        help_labels.update(*events)

        for item in box:
            if isinstance(item, gui.Button) and item.clicked:
                item.clicked = False
                if item.text == "Back":
                    current_part -= 1
                    if current_part < 0:
                        return
                    update()
                    
                elif item.text == "Next":
                    current_part += 1
                    if current_part >= len(parts):
                        return
                    update()
        
        blit_background()
        box.draw(SCREEN)
        help_labels.draw(SCREEN)
        pygame.display.update()

def settings():
    """
    Options for graphing.

    New settings are only saved after you press Accept. This way,
    we can also have a Cancel button (that discards all changes made).
    """
    def save():
        # the file is assumed to be small enough to
        # fit in memory all at once (which it should)
        with utils.load_tfile("settings.txt", "rU") as f:
            stuff = f.read()

        # read old data and modify our new copy
        new_lines = []
        for line in stuff.split("\n"):
            l = line.split()
            if l[0] == "GRID_ON":
                l[1] = str(int(grid_setting))
            elif l[0] == "AXES_ON":
                l[1] = str(int(axis_setting))
            elif l[0] == "GRAPH_ANIM":
                l[1] = str(int(graph_anim_setting))
            elif l[0].startswith("x") or l[0].startswith("y"):
                for t_entry in xy_t_entries:
                    if t_entry.text.startswith(l[0]):
                        l[1] = t_entry.expr_text
                        GRAPH[l[0]] = float(l[1])
                        break
            new_lines.append(" ".join(l))
        GRAPH["x_dist"] = GRAPH["x_right"] - GRAPH["x_left"]
        GRAPH["y_dist"] = GRAPH["y_bottom"] - GRAPH["y_top"]
                            
        # now overwrite the old file with our new copy
        with utils.load_tfile("settings.txt", "w") as f:
            f.write("\n".join(new_lines))

            
    box = gui.Container()
    box.add(
        gui.Button(10, 10, utils.load_image("cube.bmp", True), "Cancel"))
    box.add(
        gui.Button(constants.SCR_WIDTH - 70, 10,
                   utils.load_image("cube.bmp", True), "Accept"))
    
    xy_settings = []
    with utils.load_tfile("settings.txt", "rU") as f:
        for line in f:
            l = line.rstrip("\n")
            if l.startswith("GRID_ON"):
                grid_setting = bool(int(l.split()[1]))
            elif l.startswith("AXES_ON"):
                axis_setting = bool(int(l.split()[1]))
            elif l.startswith("GRAPH_ANIM"):
                graph_anim_setting = bool(int(l.split()[1]))
            elif l.startswith("x") or l.startswith("y"):
                xy_settings.append(l)

    # grid
    box.add(
        gui.Label(10, 120, "Grid:"))
    grid_button = \
        gui.Button(70, 100, utils.load_image("cube.bmp", True),
                   "On" if grid_setting else "Off")
    box.add(grid_button)
    
    # axes
    box.add(
        gui.Label(210, 120, "Axes:"))
    axis_button = \
        gui.Button(270, 100, utils.load_image("cube.bmp", True),
                   "On" if axis_setting else "Off")
    box.add(axis_button)

    # graph animation
    box.add(
        gui.Label(410, 120, "Graph animation: "))
    graph_anim_button = \
                      gui.Button(570, 100, utils.load_image("cube.bmp", True),
                                 "On" if graph_anim_setting else "Off")
    box.add(graph_anim_button)
    
    # x/y settings
    y = 200
    xy_t_entries = []
    for item in xy_settings:
        t_entry = \
            gui.TextEntry(10, y, item.split()[0] + ": ", 30, colors.white, 300)
        box.add(t_entry)
        t_entry.text += item.split()[1]
        t_entry.expr_text = item.split()[1]
        xy_t_entries.append(t_entry)
        y += 50
        
    
    while True:
        if pygame.event.peek(QUIT):
            utils.quit()
            
        box.update(*pygame.event.get())
        for item in box:
            if isinstance(item, gui.Button) and item.clicked:
                item.clicked = False
                if item is grid_button:
                    grid_setting = not grid_setting
                    item.text = "On" if grid_setting else "Off"
                elif item is axis_button:
                    axis_setting = not axis_setting
                    item.text = "On" if axis_setting else "Off"
                elif item is graph_anim_button:
                    graph_anim_setting = not graph_anim_setting
                    item.text = "On" if graph_anim_setting else "Off"
                elif item.text == "Cancel":
                    # changes are merely discarded
                    return
                elif item.text == "Accept":
                    save()
                    return

        blit_background()
        box.draw(SCREEN)
        pygame.display.update()

def get_func_exprs():
    """
    Prompt for a list of functions the user wants to see graphed.

    As mentioned previously, anything entered remains for the duration
    of the program, so you can graph something, change the settings, and
    return to find your functions still there.
    """
    def change_colors(item):
        # index new color
        item_index = button_entries.index(item)
        COL_POS_LIST[item_index] += 1 
        # reset index if gone too far
        if COL_POS_LIST[item_index] >= len(COLOR_LIST):
            COL_POS_LIST[item_index] = 0
        # create new Button image
        col = item.image.copy()
        col.fill(COLOR_LIST[COL_POS_LIST[item_index]])
        # update Button
        item.set_new_image(col)
        item.color = COLOR_LIST[COL_POS_LIST[item_index]]
        
    box = gui.Container()
    box.add(
        gui.Button(10, 10, utils.load_image("cube.bmp", True), "Back"))
    box.add(
        gui.Button(constants.SCR_WIDTH - 70, 10,
                   utils.load_image("cube.bmp", False), "Graph!"))
    
    box.add(text_entries)
    box.add(button_entries)
    
    while True:
        if pygame.event.peek(QUIT):
            utils.quit()

        box.update(*pygame.event.get())
        for item in box:
            if isinstance(item, gui.Button) and item.clicked:
                item.clicked = False
                if item.text == "Back":
                    return
                elif item.text == "":
                    change_colors(item)
                elif item.text == "Graph!":
                    exprs = [(x.expr_text, y.color) for x, y in zip(text_entries, button_entries) if x.expr_text]
                    draw_graph(exprs)

        blit_background()
        box.draw(SCREEN)
        pygame.display.update()
        

def draw_graph(exprs):
    """
    Draw all functions in |exprs|: each element should supply a tuple
    (or any iterable thing), first element being the expression
    to be eval'd(), second element being a color.
    """

    utils.cls(SCREEN)
    draw_grid = False
    draw_axes = False
    
    with utils.load_tfile("settings.txt", "rU") as f:
        for line in f:
            l = line.rstrip("\n").split()
            if l[0] == "GRID_ON" and l[1] == "1":
                draw_grid = True
            elif l[0] == "AXES_ON" and l[1] == "1":
                draw_axes = True
            elif l[0] == "GRAPH_ANIM":
                GRAPH["GRAPH_ANIM"] = bool(int(l[1]))
    
    if draw_grid:
        draw_funcs.draw_grid(GRAPH, SCREEN, colors.white)
    if draw_axes:
        draw_funcs.draw_axes(GRAPH, SCREEN, colors.silver)
    pygame.display.update()
    
    for expr, col in exprs:
        # automatically add in multiplication signs
        a = re.findall(r"[0-9]+x", expr)
        for pattern in a:
            expr = expr.replace(pattern, "".join(pattern.split("x") + ["*x"]))
        # change ^ to **
        expr = expr.replace("^", "**")
        draw_funcs.draw_function(
            GRAPH, SCREEN, expr, col)
    pygame.event.clear()
    
    # save a copy of the current screen for performance reasons
    # (extremely slow to constantly replot functions)
    graphed_surface = SCREEN.copy()

    box = gui.Container()
    pos_label = gui.Label(0, 0, "(0, 0)", 20, colors.lime)
    pos_label_pos = (0, 0)
          
    while True:
        if pygame.event.peek(QUIT):
            utils.quit()
        
        events = pygame.event.get()
        for event in events:
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == KEYUP and event.key == K_BACKQUOTE:
                import time
                t = time.strftime("%b%d %I_%M_%S")
                del time
                pygame.image.save(graphed_surface, "graph_%s.bmp" % (t))

            elif event.type == MOUSEMOTION:
                pos_label_pos = event.pos

            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                if pos_label in box:
                    box.remove(pos_label)
                else:
                    box.add(pos_label)
        
        box.update(*events)
        pos_label.x, pos_label.y = pos_label_pos
        pos_label.text = "(%.3f, %.3f)" % (
            draw_funcs.to_graph(GRAPH, *pos_label_pos))

        utils.cls(SCREEN)
        SCREEN.blit(graphed_surface, (0, 0))
        box.draw(SCREEN)
        pygame.display.update()
