#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 11 09:09:45 2022

@author: jrouss
"""
import random
from maths import * 
# draw_jointed_line.py
from PIL import Image, ImageDraw, ImageFont
from patern import Patern, Patern_max

import timeit
def symbol_random(output_path):
    image = Image.new("RGB", (400, 400), "red")
    points = []
    for i in range(0,401,100):
        for j in range(0,401,100):
            points.append((i,j))
    
    actual_point = random.sample(points,5)    
    #points = [(100, 100), (150, 200), (200, 50), (400, 400)]
    draw = ImageDraw.Draw(image)
    draw.point(points, fill="yellow")
    draw.line(actual_point,width=5, fill="blue")
    points = [point for point in points if point not in actual_point]
    second_point = random.sample(points,2)
    second_point.append(random.choice(actual_point))
    draw.line(second_point,width=5, fill="green", joint="curve")
    image.show()
    image.save(output_path)
    
    #draw.line(points, width=15, fill="green", joint="curve")
    """font_size=70
    font = ImageFont.truetype("Aaargh.ttf", size=font_size)
    draw.text((200-font_size,200-font_size),"LOGO", stroke_width=3,fill="blue", font=font)
    """
    
def symbol_weighted(output_path):
    size = 300
    image = Image.new("RGB", (size*3+1, size*3+1), "white")
    increment = int(size/4)
    number_points = int(size/30)
    show_triangle = True
    show_point = True
    show_grid = True
    
    #points = [(100, 100), (150, 200), (200, 50), (400, 400)]
    draw = ImageDraw.Draw(image)
    for i in range(0,3):
        for j in range(0,3):
            p1 = Patern(size=size,increment=increment,number_points=number_points,long_line=1)
            points = p1.getPoints()
            points = [(x+size*(i),y+size*(j)) for (x,y) in points ]
            draw.point(points, fill="yellow")
            r=size/60
            Allpoints = []
            """Draw grid"""
            if show_grid:
                coinPoints = [(0+size*i,0+size*j),(size*(i+1),0+size*j),(size*(i+1),size*(j+1)),(0+size*i,size*(j+1))]
                draw.line(coinPoints,width=2, fill="black")
            
            """Draw all points"""
            for x in range(0,size+1,increment):
                for y in range(0,size+1,increment):
                    Allpoints.append((x+size*(i),y+size*(j)))
            DrawCircles(Allpoints, r, draw, fill="pink")
            
            """Draw the lines of the patern, and the consistuant point"""
            draw.line(points,width=2, fill="blue")
            #draw.line(second_point,width=5, fill="green", joint="curve")
            
            if show_point:
                DrawCircles(points,r,draw,"purple")
                DrawCircle(points[0],r,draw,"green")
            
            """triangle to show the touching sizes"""
            
            if show_triangle:
                if p1.isTop():
                    draw.polygon([(size/2+size*i,0+size*j),((size/2)-(r*2)+size*i,(r*2)+size*j),((size/2)+(r*2)+size*i,(r*2)+size*j)],fill="green")
                if p1.isBottom():
                    draw.polygon([(size/2+size*i,size+size*j),(size/2-(r*2)+size*i,size-(r*2)+size*j),(size/2+(r*2)+size*i,size-(r*2)+size*j)],fill="green")
                if p1.isLeft():
                    draw.polygon([(0+size*i,size/2+size*j),((r*2)+size*i,(size/2)-(r*2)+size*j),((r*2)+size*i,(size/2)+(r*2)+size*j)],fill="green")
                if p1.isRight():
                    draw.polygon([(size+size*i,size/2+size*j),(size-(r*2)+size*i,size/2-(r*2)+size*j),(size-(r*2)+size*i,size/2+(r*2)+size*j)],fill="green")
               
            
           #draw.line(points, width=15, fill="green", joint="curve")
            """font_size=70
            font = ImageFont.truetype("Aaargh.ttf", size=font_size)
            draw.text((200-font_size,200-font_size),"LOGO", stroke_width=3,fill="blue", font=font)
            """
    image.show()
    image.save(output_path)

def generate_patern(n=1,size=100,number_points = 5,show_triangle = False,show_point = False,show_grid = False,show_all_point = False):
    
    increment =  int(size/4)
    
    
    patterns = []
    nb_complete = 0
    
    start = timeit.timeit()
    nb_left = 0
    nb_right = 0
    nb_top =0
    nb_bottom = 0
    for i in range(n):
        image = Image.new("RGB", (size, size), "white")
        draw = ImageDraw.Draw(image)
        output_path = "patterns/pattern_"+str(i)+".bmp"
        #Generate a blank pattern
        if i ==0:
            p = Patern(size=size,number_points=0)
            image.save(output_path)
            print(p.side)
            patterns.append(p)
            continue
        goal_nb_complete = 5 if n<=50 else n/10
        #print("goal nb complete : ",goal_nb_complete)
        if nb_complete < goal_nb_complete:
            while True:
                p = Patern_max(size=size,increment=increment,number_points=number_points*2,long_line=1)
                
                if p.isComplete():
                    break
        else:
            # print("nombre before complete",i)
            while True:
                p = Patern(size=size,increment=increment,number_points=number_points,long_line=1)
                if not p.isContained():
                    if not p.isLeft():
                        nb_left = nb_left +1
                    if not p.isRight():
                        nb_right = nb_right +1
                    if not p.isTop():
                        nb_top = nb_top +1
                    if not p.isBottom():
                        nb_bottom = nb_bottom +1
                    break
                
        points = p.getPoints()
        if p.isComplete():
            nb_complete = nb_complete +1
        r=size/30
        Allpoints = []
        """Draw grid"""
        if show_grid:
            coinPoints = [(0.1,0.1),(size-0.1,0.1),(size-0.1,size-0.1),(0.1,size-0.1),(0.1,0.1)]
            draw.line(coinPoints,width=1, fill="black")
            
        """Draw all points"""
        if show_all_point:
            for x in range(0,size+1,increment):
                for y in range(0,size+1,increment):
                    Allpoints.append((x,y))
            DrawCircles(Allpoints, r, draw, fill="pink")
        
        
        
        if show_triangle:
            if p.isTop():
                draw.polygon([(size/2,0),((size/2)-(r*2),(r*2)),((size/2)+(r*2),(r*2))],fill="green")
            if p.isBottom():
                draw.polygon([(size/2,size),(size/2-(r*2),size-(r*2)),(size/2+(r*2),size-(r*2))],fill="green")
            if p.isLeft():
                draw.polygon([(0,size/2),((r*2),(size/2)-(r*2)),((r*2),(size/2)+(r*2))],fill="green")
            if p.isRight():
                draw.polygon([(size,size/2),(size-(r*2),(size/2-(r*2))),((size-(r*2),size/2+(r*2)))],fill="green")
              
        """Draw the lines of the patern, and the consistuant point"""
        if p.isContained():
            draw.line( [(0.1,0.1),(size-0.1,size-0.1),(size-0.1,0.1),(0.1,size-0.1),(0.1,0.1)],width=4,fill="blue")
            print("contained one")
        else:
            draw.line(points,width=2, fill="red")
        #draw.line(second_point,width=5, fill="green", joint="curve")
        
        if show_point:
            DrawCircles(points,r,draw,"purple")
            DrawCircle(points[0],r,draw,"green")
            DrawCircle(points[len(points)-1],r,draw,"blue")
        #image.show()
        image.save(output_path)
        
        patterns.append(p)
    end = timeit.timeit()
    print("temps generation pattern_max : " + str(end - start))
    print("nb not right",nb_right,"nb not left",nb_left,"not nb_top",nb_top,"not nb_bottom",nb_bottom)
    print("nb complete : ", nb_complete)
    return patterns

if __name__ == "__main__":
    #symbol_weighted("jointed_lines.jpg")
    size = 100
    nb_pattern = 50
    number_points = 6
    show_triangle = True
    show_point = True
    show_grid = True
    show_all_point = True
    size_grid = 5
    generate_patern(nb_pattern,size,number_points,show_triangle,show_point,show_grid,show_all_point)
    img = Image.open("patterns/pattern_0.bmp")
    img.show()
    