#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 11 14:28:09 2022

@author: jrouss
"""
import random
class Patern:
    def __init__(self,size=300,increment=100,number_points=6):
        points = []
        for i in range(0,size+1,increment):
            for j in range(0,size+1,increment):
                points.append((i,j))
        
        self.actual_point = []
        
        current_point = random.choice(points)
        for i in range(0,number_points):
            close_points = [point for point in points if( point  not in self.actual_point) and ((point[0]-current_point[0])**2 <= increment**2 ) 
                            and  ((point[1]-current_point[1])**2 <= increment**2 )]
            
            self.actual_point.append(current_point)
            if len(close_points )== 0:
                break
            current_point = random.choice(close_points)
        self.left = [point for point in self.actual_point if point[0] == 0]
        self.right = [point for point in self.actual_point if point[0] == size]
        
        self.top = [point for point in self.actual_point if point[1] == 0]
        self.bottom = [point for point in self.actual_point if point[1] == size]
    
    def getPoints(self):
        return self.actual_point
    def isLeft(self):
        return len(self.left) >0
    def isRight(self):
        return len(self.right) >0
    def isTop(self):
        return len(self.top) >0
    def isBottom(self):
        return len(self.bottom) >0