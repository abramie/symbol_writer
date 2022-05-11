#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 11 14:04:15 2022

@author: jrouss
"""
UP = (0, -1)
LEFT = (-1, 0)
DOWN = (0, 1)
RIGHT = (1, 0)
UP_LEFT = (-1, -1)
UP_RIGHT = (1, -1)
DOWN_LEFT = (-1, 1)
DOWN_RIGHT = (1, 1)
dirs = [UP, DOWN, LEFT, RIGHT, UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]


def valid_dirs(pos):
    x, y = pos
    
    validDirections = []
    if x == 0:
        validDirections.extend([RIGHT])
        if y == 0:
            validDirections.extend([DOWN, DOWN_RIGHT])
        elif y == output_size[1]-1:
            validDirections.extend([UP, UP_RIGHT])
        else:
            validDirections.extend([DOWN, DOWN_RIGHT, UP, UP_RIGHT])
    elif x == output_size[0]-1:
        validDirections.extend([LEFT])
        if y == 0:
            validDirections.extend([DOWN, DOWN_LEFT])
        elif y == output_size[1]-1:
            validDirections.extend([UP, UP_LEFT])
        else:
            validDirections.extend([DOWN, DOWN_LEFT, UP, UP_LEFT])
    else:
        validDirections.extend([LEFT, RIGHT])
        if y == 0:
            validDirections.extend([DOWN, DOWN_LEFT, DOWN_RIGHT])
        elif y == output_size[1]-1:
            validDirections.extend([UP, UP_LEFT, UP_RIGHT])
        else: 
            validDirections.extend([UP, UP_LEFT, UP_RIGHT, DOWN, DOWN_LEFT, DOWN_RIGHT])
    
    return validDirections