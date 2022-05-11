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
from patern import Patern
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
    size = 100
    image = Image.new("RGB", (size*3, size*3), "red")
    increment = 25
    number_points = 6
    
    #points = [(100, 100), (150, 200), (200, 50), (400, 400)]
    draw = ImageDraw.Draw(image)
    for i in range(0,3):
        for j in range(0,3):
            p1 = Patern(size,increment,number_points)
            points = p1.getPoints()
            points = [(x+size*(i),y+size*(j)) for (x,y) in points ]
            draw.point(points, fill="yellow")
            r=5
            Allpoints = []
            coinPoints = [(0+size*i,0+size*j),(size*(i+1),0+size*j),(size*(i+1),size*(j+1)),(0+size*i,size*(j+1))]
            for x in range(0,size+1,increment):
                for y in range(0,size+1,increment):
                    Allpoints.append((x+size*(i),y+size*(j)))
                    
            draw.line(coinPoints,width=2, fill="black")
            DrawCircles(Allpoints, r, draw, fill="pink")
            draw.line(points,width=5, fill="blue")
            #draw.line(second_point,width=5, fill="green", joint="curve")
            draw.line([(0+size*i,0+size*j)])
            DrawCircles(points,5,draw,"purple")
            DrawCircle(points[0],5,draw,"green")
            if p1.isTop():
                draw.polygon([(size/2+size*i,0+size*j),((size/2)-10+size*i,10+size*j),((size/2)+10+size*i,10+size*j)],fill="green")
                print("top")
            if p1.isBottom():
                draw.polygon([(size/2+size*i,size+size*j),(size/2-10+size*i,size-10+size*j),(size/2+10+size*i,size-10+size*j)],fill="green")
            if p1.isLeft():
                draw.polygon([(0+size*i,size/2+size*j),(10+size*i,(size/2)-10+size*j),(10+size*i,(size/2)+10+size*j)],fill="green")
            if p1.isRight():
                draw.polygon([(size+size*i,size/2+size*j),(size-10+size*i,size/2-10+size*j),(size-10+size*i,size/2+10+size*j)],fill="green")
            #draw.line(points, width=15, fill="green", joint="curve")
            """font_size=70
            font = ImageFont.truetype("Aaargh.ttf", size=font_size)
            draw.text((200-font_size,200-font_size),"LOGO", stroke_width=3,fill="blue", font=font)
            """
    image.show()
    image.save(output_path)
 
    
if __name__ == "__main__":
    symbol_weighted("jointed_lines.jpg")
    