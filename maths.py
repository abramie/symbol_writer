#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 11 13:41:32 2022

@author: jrouss
"""
import numpy as np

def DrawCircle(center, r, draw, fill=None):
    draw.ellipse((center[0]-r, center[1]-r, center[0]+r,center[1]+r), fill= fill  )
    
def DrawCircles(points, r, draw, fill=None):
    for point in points:
        DrawCircle(point, r, draw,fill)
        
"""
 From https://terbium.io/2018/11/wave-function-collapse/
 I think Numpy’s default nonzero method doesn’t make a ton of sense. 
 Or maybe I just don’t understand how to use it. In any case, here’s a version I like better:
 I’ve called it find_true because we’re only going to use it to find the indices of cells that are True in boolean arrays.
"""       
def find_true(array):
    """
    Like np.nonzero, except it makes sense.
    """
    transform = int if len(np.asarray(array).shape) == 1 else tuple
    return list(map(transform, np.transpose(np.nonzero(array))))


from enum import Enum, auto

class Direction(Enum):
    RIGHT = 0; UP = 1; LEFT = 2; DOWN = 3
    
    def reverse(self):
        return {Direction.RIGHT: Direction.LEFT,
                Direction.LEFT: Direction.RIGHT,
                Direction.UP: Direction.DOWN,
                Direction.DOWN: Direction.UP}[self]
