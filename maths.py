#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 11 13:41:32 2022

@author: jrouss
"""
def DrawCircle(center, r, draw, fill=None):
    draw.ellipse((center[0]-r, center[1]-r, center[0]+r,center[1]+r), fill= fill  )
    
def DrawCircles(points, r, draw, fill=None):
    for point in points:
        DrawCircle(point, r, draw,fill)