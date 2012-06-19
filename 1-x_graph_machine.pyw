#! /usr/bin/env python
#
# 1-X Graph Machine
#
# Author: Nicholas Kim
#
# 1-X Graph Machine is a tool designed for plotting functions.
# Refer to the README for details.

from __future__ import division

def main():
    from modules import menu_funcs
    menu_funcs.setup()
    menu_funcs.init_screen()
    
    import sys
    if len(sys.argv) == 1:
        # default
        menu_funcs.menu()
    else:
        # quick graph
        expr = "".join([s.replace("^", "**") for s in sys.argv[1:]])
        menu_funcs.draw_graph([(expr, (0, 255, 255))])
        
if __name__ == "__main__":
    import pygame
    try:
        main()
    finally:
        pygame.quit()
