# draw_funcs.py



# All functions require a dictionary as their first parameter,
# which specifies:
# - width (width of screen)
# - height (height of screen)
# - GRAPH_ANIM (whether to delay graphing or not)
# - x_left (leftmost graphing coordinate)
# - x_right (rightmost graphing coordinate)
# - x_inc (horizontal "zoning" of grid)
# - y_bottom (bottommost graphing coordinate)
# - y_top (topmost graphing coordinate)
# - y_inc (vertical "zoning" of grid)
# - axis_thickness (thickness, in pixels, of the axes)
# - x_dist (x_right - x_left)
# - y_dist (y_bottom - y_top)

import constants, math_funcs
import pygame
pygame.init()

EVAL_GLOBAL_DICT = {"__builtins__" : None}
EVAL_GLOBAL_DICT.update(math_funcs.CONSTANTS)
EVAL_GLOBAL_DICT.update(math_funcs.FUNCTIONS)

def frange(start, end=None, inc=1.0):
    """float version of xrange() builtin"""
    if end == None:
        end = start + 0.0
        start = 0.0
    else:
        start += 0.0

    count = int((end-start)/inc)
    if start + (count * inc) != end:
        count += 1
    
    for i in xrange(count):
        yield start + (i * inc)

# conversion functions
def to_pixel(graph_info, g_x, g_y):
    """returns the screen pixel equivalents of the x, y graph coords"""
    ratio_x = graph_info["width"] / graph_info["x_dist"]
    ratio_y = graph_info["height"] / graph_info["y_dist"]
    
    s_x = (g_x - graph_info["x_left"]) * ratio_x
    s_y = (g_y - graph_info["y_top"]) * ratio_y
    
    return s_x, s_y

def to_graph(graph_info, s_x, s_y):
    """returns the graphing equivalents of the x, y screen coords"""
    ratio_x = float(s_x) / (graph_info["width"])
    ratio_y = float(s_y) / (graph_info["height"])

    g_x = graph_info["x_left"] + (graph_info["x_dist"] * ratio_x)
    g_y = graph_info["y_top"] + (graph_info["y_dist"] * ratio_y)

    return g_x, g_y


# drawing functions
def draw_axes(graph_info, surface, color):
    """Draws the axes of a 2D Cartesian grid."""
    # some calculations
    xaxis_x1, xaxis_y1 = to_pixel(graph_info, graph_info["x_left"], 0)
    xaxis_x2, xaxis_y2 = to_pixel(graph_info, graph_info["x_right"], 0)

    yaxis_x1, yaxis_y1 = to_pixel(graph_info, 0, graph_info["y_top"])
    yaxis_x2, yaxis_y2 = to_pixel(graph_info, 0, graph_info["y_bottom"])
    
    # x-axis
    if (xaxis_y1 > 0 and xaxis_y2 < constants.SCR_HEIGHT):
        pygame.draw.line(surface, color,
                         (xaxis_x1, xaxis_y1), (xaxis_x2, xaxis_y2),
                         graph_info["axis_thickness"])
    
    # y-axis
    if (yaxis_x1 > 0 and yaxis_x2 < constants.SCR_WIDTH):
        pygame.draw.line(surface, color,
                         (yaxis_x1, yaxis_y1), (yaxis_x2, yaxis_y2),
                         graph_info["axis_thickness"])
    
    
def draw_grid(graph_info, surface, color):
    """
    Draws a 2D Cartesian grid.

    The grid aligns itself to the axes.
    """
    
    # vertical lines
##    yaxis_x = to_pixel(graph_info, 0, graph_info["y_top"])[1]
##
##    for x in frange(yaxis_x, 0, -graph_info["x_inc"]):
##        pygame.draw.line(surface, color,
##                         to_pixel(graph_info, x, graph_info["y_top"]),
##                         to_pixel(graph_info, x, graph_info["y_bottom"]))
##
##    for x in frange(yaxis_x, 
    for x in frange(graph_info["x_left"],
                    graph_info["x_right"] + 1,
                    graph_info["x_inc"]):
        pygame.draw.line(surface, color,
                         to_pixel(graph_info, x, graph_info["y_top"]),
                         to_pixel(graph_info, x, graph_info["y_bottom"]))

    # horizontal lines
    for y in frange(graph_info["y_bottom"],
                    graph_info["y_top"] + 1,
                    graph_info["y_inc"]):
        pygame.draw.line(surface, color,
                         to_pixel(graph_info, graph_info["x_left"], y),
                         to_pixel(graph_info, graph_info["x_right"], y))
        

def draw_function(graph_info, surface, function, color):
    """
    Draws the graph of the function (an expression) provided.

    If any input value is invalid, nothing will be drawn for that input value.
    """
    
    EVAL_LOCAL_DICT = {
        "x" : None,
        }
    
    for screen_x in range(1, constants.SCR_WIDTH - 1):
        # get graph_x coords of current pixel and adjacent pixels
        # - we need the adjacent pixels because we use lines instead
        # of pixels in order to graph - this way, for graphs with
        # large vertical shifting (think tangent or high degree
        # polynomials), we're not staring at scattered pixels
        graph_x = to_graph(graph_info, screen_x, 0)[0]
        graph_x_ladj = to_graph(graph_info, screen_x - 1, 0)[0]
        graph_x_radj = to_graph(graph_info, screen_x + 1, 0)[0]
        
        EVAL_LOCAL_DICT["x"] = graph_x
        
        try:
            # get graph_y coord of current pixel
            graph_y = eval(function, EVAL_GLOBAL_DICT, EVAL_LOCAL_DICT)

            # get graph_y coord of left adjacent pixel
            EVAL_LOCAL_DICT["x"] = graph_x_ladj
            graph_y_l = eval(function, EVAL_GLOBAL_DICT, EVAL_LOCAL_DICT)

            # get graph_y coord of right adjacent pixel
            EVAL_LOCAL_DICT["x"] = graph_x_radj
            graph_y_r = eval(function, EVAL_GLOBAL_DICT, EVAL_LOCAL_DICT)

            g_top = graph_info["y_top"]
            g_bot = graph_info["y_bottom"]
            
            # disregard anything beyond the graph limits
            if graph_y > g_top or graph_y < g_bot:
                raise OverflowError

            # extend lines only up to the graph limits
            graph_y_l = g_top if graph_y_l > g_top else graph_y_l
            graph_y_l = g_bot if graph_y_l < g_bot else graph_y_l
            graph_y_r = g_top if graph_y_r > g_top else graph_y_r
            graph_y_r = g_bot if graph_y_r < g_bot else graph_y_r
        
        except(Exception):
            # in the case of any error (raised by incorrect user input
            # or any internal purpose), we simply ignore
            pass
        
        else:
            # calculate screen y-coords
            screen_y = int(to_pixel(graph_info, graph_x, graph_y)[1])
            screen_y_l = int(to_pixel(graph_info, graph_x_ladj, graph_y_l)[1])
            screen_y_r = int(to_pixel(graph_info, graph_x_radj, graph_y_r)[1])

            # plot graph
            r1 = pygame.draw.line(surface, color,
                                  (screen_x, screen_y),
                                  (screen_x, screen_y_l))
            r2 = pygame.draw.line(surface, color,
                                  (screen_x, screen_y),
                                  (screen_x, screen_y_r))

            # animate by time delay if desired
            if graph_info["GRAPH_ANIM"]:
                pygame.time.wait(2)
                pygame.display.update([r1, r2])
