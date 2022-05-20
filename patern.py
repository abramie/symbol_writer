#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 11 14:28:09 2022

@author: jrouss
Class Patern
Generate a single line that goes throught multiples points
define if the line touch one of the side with the "isLeft/isRight/isTop/isBottom" accessor 
"""

import random
import numpy as np
class Patern:
    def __init__(self,size=300,increment=100,number_points=6,long_line=1):
        self.points = []
        
        self.size = size
        self.create_point(size,increment,number_points,long_line)
        
        self.left = [point for point in self.actual_point if point[0] == 0 and point[1] != 0 and point[1] != self.size]
        self.right = [point for point in self.actual_point if point[0] == self.size and point[1] != 0 and point[1] != self.size]
        self.top = [point for point in self.actual_point if point[1] == 0 and point[0] != 0 and point[0] != self.size ]
        self.bottom = [point for point in self.actual_point if point[1] == self.size and point[0] != 0 and point[0] != self.size]
        self.side = [self.isRight(),self.isTop(),self.isLeft(),self.isBottom()]
    def create_point(self,size,increment,number_points,long_line):
        for i in range(0,size+1,increment):
            for j in range(0,size+1,increment):
                self.points.append((i,j))
        
        self.actual_point = []
        
        current_point = random.choice(self.points)
        for i in range(0,number_points):
            close_points = [point for point in self.points if( point  not in self.actual_point) and ((point[0]-current_point[0])**2 <= (increment**2)*long_line**2 ) 
                            and  ((point[1]-current_point[1])**2 <= (increment**2 )*long_line**2)]
            
            self.actual_point.append(current_point)
            if len(close_points )== 0:
                break
            try:
                current_point = random.choice(close_points)
            except Exception as e:
                print(e)
                continue
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
    def isComplete(self):
        return self.isLeft() and self.isRight() and self.isTop() and self.isBottom()
    def isContained(self):
        return not (self.isLeft() or self.isRight() or self.isTop() or self.isBottom())
    def isLineLeft(self):
        return len(self.left) >1
    def isLineRight(self):
        return len(self.right) >1
    def isLineTop(self):
        return len(self.top) >1
    def isLineBottom(self):
        return len(self.bottom) >1
class Patern_max(Patern):
    def create_point(self,size,increment,number_points,long_line):
        actif_ll = long_line
        for i in range(0,size+1,increment):
            for j in range(0,size+1,increment):
                self.points.append((i,j))
        
        self.actual_point = []
        
        current_point = random.choice(self.points)
        for i in range(0,number_points):
            close_points = [point for point in self.points if( point  not in self.actual_point) and ((point[0]-current_point[0])**2 <= (increment**2)*actif_ll**2 ) 
                            and  ((point[1]-current_point[1])**2 <= (increment**2 )*actif_ll**2)]
            
            self.actual_point.append(current_point)
            
            if len(close_points )== 0 and not self.isComplete() :
                if actif_ll == long_line:
                    actif_ll = long_line*2
                    continue
                else:
                    break
            weight = np.full(len(close_points), 5)
            for i in range(len(close_points)):
                
                p = close_points[i]
                
                self.left = [point for point in self.actual_point if point[0] == 0]
                self.right = [point for point in self.actual_point if point[0] == size]
                
                self.top = [point for point in self.actual_point if point[1] == 0]
                self.bottom = [point for point in self.actual_point if point[1] == size]
                
                if (current_point[0] == 0 and p[0] == 0) or (current_point[1] == 0 and p[1] == 0) \
                    or (current_point[0] == size and p[0] == size) or (current_point[1] == size and p[1] == size):
                        weight[i] = 1
                if not self.isLeft() and p[0] < current_point[0]:
                    weight[i] = 10
                if not self.isRight() and p[0] > current_point[0]:
                    weight[i] = 10
                if not self.isTop() and p[1] < current_point[1]:
                    weight[i] = 10
                if not self.isBottom() and p[1] > current_point[1]:
                    weight[i] = 10
                
            try:
                current_point = random.choices(close_points, weights=weight,k=1)[0]
            except Exception as e:
                print(e)
                continue
        #print("Pattern generate")












