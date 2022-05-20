#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 12 11:09:41 2022

@author: jrouss

Wave collapse
https://terbium.io/2018/11/wave-function-collapse/
"""
import random
import io
import base64
from collections import namedtuple
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from IPython import display

from maths import find_true, Direction
from line import * 
from exception import noMorePattern
import math 
import traceback
def blend_many(ims):
    """
    Blends a sequence of images.
    """
    current, *ims = ims
    for i, im in enumerate(ims):
        current = Image.blend(current, im, 1/(i+2))
    return current

def blend_tiles(choices, tiles):
    """
    Given a list of states (True if ruled out, False if not) for each tile,
    and a list of tiles, return a blend of all the tiles that haven't been
    ruled out.
    """
    
    to_blend = [tiles[i].bitmap for i in range(len(choices)) if choices[i]]
    return blend_many(to_blend)

def show_state(potential, tiles):
    """
    Given a list of states for each tile for each position of the image, return
    an image representing the state of the global image.
    """
    rows = []
    for row in potential:
        rows.append([np.asarray(blend_tiles(t, tiles)) for t in row])

    rows = np.array(rows)
    
    n_rows, n_cols, tile_height, tile_width,number  = rows.shape
    
    images = np.swapaxes(rows, 1, 2)
    images = images.reshape(n_rows*tile_height, n_cols*tile_width, number) #Passer à 3 pour mes images et 4 pour le tuto
    return Image.fromarray(images)
def run_iteration(old_potential,weights,tiles,size_grid):
    potential = old_potential.copy()
    
    to_collapse = location_with_fewest_choices_neightbor(potential,size_grid,tiles) #3
    if to_collapse is None:                               #1
        raise StopIteration()
    elif to_collapse == "Blank":
        potential = blank_everything(potential, size_grid)   
        return potential
    elif not np.any(potential[to_collapse]):              #2
        raise noMorePattern(f"No choices left at {to_collapse}")
    else:                                                 #4 ↓
        nonzero = find_true(potential[to_collapse])
        tile_probs = weights[nonzero]/sum(weights[nonzero])
        selected_tile = np.random.choice(nonzero, p=tile_probs)
        potential[to_collapse] = False
        potential[to_collapse][selected_tile] = True
        propagate(potential, to_collapse,tiles)                 #5
    return potential
def run_iteration_middle(old_potential,weights,tiles,size_grid):
    potential = old_potential.copy()
    # print("potential init",potential[0])
    middle_grid = int((size_grid-1)/2)
    to_collapse = (middle_grid,middle_grid) #3
    if to_collapse is None:                               #1
        raise StopIteration()
    elif not np.any(potential[to_collapse]):              #2
        raise noMorePattern(f"No choices left at {to_collapse}")
    else:                                                 #4 ↓
        nonzero = find_true(potential[to_collapse])
        tile_probs = weights[nonzero]/sum(weights[nonzero])
        selected_tile = np.random.choice(nonzero, p=tile_probs)
        # print("potential after selected",potential[(4,3)])
        potential[to_collapse] = False
        potential[to_collapse][selected_tile] = True
        propagate(potential, to_collapse,tiles)                 #5
        # print("potential after propagate",potential[(4,3)])
    return potential
def location_with_fewest_choices(potential,size_grid,tiles=None):
    num_choices = np.sum(potential, axis=2, dtype='float32')
    num_choices[num_choices == 1] = np.inf
    # print("numchoices", num_choices)
    candidate_locations = find_true(num_choices == num_choices.min())
    candidate_locations = find_true(num_choices != np.inf)
    # print(candidate_locations)
    """It's more propbable to select a square close to the center"""
    if len(candidate_locations) == 0:
        return None
    dist = np.array([int(math.dist([c[0],c[1]] , [int((size_grid-1)/2),int((size_grid-1)/2)]))**3 for c in candidate_locations])
    # print(dist)
    #candidate_locations = find_true(dist == dist.min())
    
    weight_location = np.full(len(candidate_locations), 1)
    # for i in range(len(candidate_locations)):
        # print(i)
    
    weight_location = [200-int(math.dist([c[0],c[1]] , [int((size_grid-1)/2),int((size_grid-1)/2)]))**3 for c in candidate_locations]
    # print(dist.max())
    # print(weight_location)
    location = random.choices(candidate_locations,weights=weight_location,k=1)[0]
    # print("location ?", location)
    # print("size candiates", len(candidate_locations))
    # print("size numchoice", len(num_choices))
    if num_choices[location] == np.inf:
        return None
    return location
def location_with_fewest_choices_basic(potential,size_grid,tiles=None):
    
    num_choices = np.sum(potential, axis=2, dtype='float32')
    num_choices[num_choices == 1] = np.inf
    candidate_locations = find_true(num_choices == num_choices.min())
    location = random.choice(candidate_locations)
    if num_choices[location] == np.inf:
        return None
    return location
def location_with_fewest_choices_neightbor(potential,size_grid,tiles):
    height, width = potential.shape[:2]
    num_choices = np.sum(potential, axis=2, dtype='float32')
    num_choices[num_choices == 1] = np.inf
    #print(num_choices.shape)
    test = find_true(num_choices == np.inf)
    #print(test)
    
    voisins = []
    for c in test:
        neigh = neighbors(c, height, width)
        # print("potential c",potential[c])
       
        tile = find_true(potential[c])[0]
        
        # for n in neigh:
        #    print("direction voisin side : ", tiles[tile].sides[n[0].reverse().value])
        voisins = voisins +  [n for n in neigh if tiles[tile].sides[n[0].value]]
    # print("voisins possibles : ", voisins)
    # input("pause")
    candidate_locations = [(x,y) for (d,x,y) in voisins if num_choices[(x,y)] != np.inf]
    #print(candidate_locations)
    
    if len(candidate_locations )== 0:
        if len(num_choices[num_choices != np.inf])>0:
            print("Blank")
            return "Blank"
        return None
    #print(voisins)
    #candidate_locations = find_true(num_choices == num_choices.min())
    location = random.choice(candidate_locations)
    # print("num choices : ",num_choices[location], "location : ", location)
    if num_choices[location] == np.inf:
        return None
    # for (neighbor_direction, neighbor_x, neighbor_y) in neighbors(location, height, width):
    #     neighbor_location = (neighbor_x, neighbor_y)
    #     if num_choices[neighbor_location] == np.inf :
    #         tile = find_true(potential[neighbor_location])[0]
    #         if tiles.sides[neighbor_direction.reverse()] == False:
                
    return location
def blank_everything(potential, size_grid):
    height, width = potential.shape[:2]
    num_choices = np.sum(potential, axis=2, dtype='float32')
    num_choices[num_choices == 1] = np.inf
    test = find_true(num_choices != np.inf)
    for c in test:
        potential[c] = False
        potential[c][0] = True
    return potential
def neighbors(location, height, width):
    res = []
    x, y = location
    if x != 0:
        res.append((Direction.UP, x-1, y))
    if y != 0:
        res.append((Direction.LEFT, x, y-1))
    if x < height - 1:
        res.append((Direction.DOWN, x+1, y))
    if y < width - 1:
        res.append((Direction.RIGHT, x, y+1))
    return res
def propagate(potential, start_location,tiles):
    old_potential = potential.copy()
    height, width = old_potential.shape[:2]
    
    needs_update = np.full((height, width), False)
    needs_update[start_location] = True
    # print("potential beginning propagate: ", potential[(0,0)])
    while np.any(needs_update):
        
        needs_update_next = np.full((height, width), False)
        locations = find_true(needs_update)
        # print("start loc", start_location, "nb locations", len(locations))
        for location in locations:
            # print("location : ", location,"potential : ", potential[location])
            
            # find true find only one in potential ? :/
            # print("pot loc",potential[location], "start loc", start_location)
            # print("find true pot loc",find_true(potential[location] == True))
            # print("location : ", location)
            possible_tiles = [tiles[n] for n in find_true(potential[location])]
            # print("possible tiles", possible_tiles)
            #print("possible tiles",possible_tiles)
            for neighbor in neighbors(location, height, width):
                neighbor_direction, neighbor_x, neighbor_y = neighbor
                neighbor_location = (neighbor_x, neighbor_y)
                was_updated = add_constraint_continuous(potential, neighbor_location,
                                             neighbor_direction, possible_tiles,tiles)
                needs_update_next[neighbor_location] |= was_updated
        needs_update = needs_update_next
    
def add_constraint(potential, location, incoming_direction, possible_tiles,tiles):
    neighbor_constraint = {t.sides[incoming_direction.value] for t in possible_tiles}
    #print(potential[location])
    # print("neighbor_constraint", neighbor_constraint)
    outgoing_direction = incoming_direction.reverse()
    changed = False
    for i_p, p in enumerate(potential[location]):
        # print("i_p",i_p)
        # print("p",p)
        if not p:
            continue
        
        if tiles[i_p].sides[outgoing_direction.value] not in neighbor_constraint:
            potential[location][i_p] = False
            changed = True
    if not np.any(potential[location]):
        raise noMorePattern(f"No patterns left at {location}")
    return changed
def add_constraint_continuous(potential, location, incoming_direction, possible_tiles,tiles):
    # print("potential constraint", potential[0])
    neighbor_constraint = {t.sides[incoming_direction.value] for t in possible_tiles}
    # print("nb possible : ",len(possible_tiles), "neigthbor constraint", neighbor_constraint)
    outgoing_direction = incoming_direction.reverse()
    changed = False
    for i_p, p in enumerate(potential[location]):
        # print("i_p",i_p)
        # print("p",p)
        if not p:
            continue
                 
        # Must change for point to point, tile need to have one point in neighbor constraint
        if tiles[i_p].sides[outgoing_direction.value] not in neighbor_constraint :
            potential[location][i_p] = False
            changed = True
            
    if not np.any(potential[location]):
        raise noMorePattern(f"No patterns left at {location}")

    return changed
Tile = namedtuple('Tile', ('name', 'bitmap', 'sides', 'weight'))
empty_tile = Tile("empty",None,[False,False,False,False],0)
empty_tile_adjacent = Tile("empty",None,[True,True,True,True],0)
def waveCollapse(n=26,size_grid=5,patterns=[]):
    
    tiles = []
    
    
    for i in range(n):
        img = Image.open("patterns/pattern_"+str(i)+".bmp")
        tiles.append(Tile("pat_"+str(i),img,patterns[i].side,1))
    
    
    # print("initial pot",potential[0])
    # print(empty_tile)
    
   
    # print("removed top bord")
    # print("pot whithout top",potential[0])
    # display.display(show_state(potential, tiles))
    

    # straight_image = Image.open(io.BytesIO(base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAMklEQVQYlWNQVrT9r6xo+988UfN/0yqN/4evOP0/fMXpf9Mqjf/miZr/YfIMowrpqxAAjKLGXfWE8ZAAAAAASUVORK5CYII=')))
    # bend_image = Image.open(io.BytesIO(base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAANklEQVQYlWNQVrT9TwxmIFmheaImXoyisGmVBk6MofDwFSesmHKFRFvdtEoDv2fQFWINHnwKAQHMxl1/fce/AAAAAElFTkSuQmCC')))
    # blank_image = Image.open(io.BytesIO(base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAFElEQVQYlWNQVrT9TwxmGFVIX4UAoDOWARI9hF0AAAAASUVORK5CYII=')))
    # cross_image = Image.open(io.BytesIO(base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAU0lEQVQYlWNQVrT9r6xo+988UfN/0yqN/4evOP0/fMXpf9Mqjf/miZr/YfIMRCs0T9T8D8PYFMIwQ9Mqjf/IGFkhMmaASRDCxCsk2mqiPUP1cAQAKI/idfPNuccAAAAASUVORK5CYII=')))
    # t_image = Image.open(io.BytesIO(base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAWUlEQVQYlWNQVrT9r6xo+988UfN/0yqN/4evOP0/fMXpf9Mqjf/miZr/YfIMRCs0T9T8D8PYFMIwQ9Mqjf/IGFkhMmaASRDCxCtEtwIXRvEMPgwPHkKYaIUAow/UaQFDAc4AAAAASUVORK5CYII=')))

    # tiles = [
    # Tile('straight_ud', straight_image,
    #       [False, True, False, True], 1/2),
    # Tile('straight_lr', straight_image.transpose(Image.ROTATE_90),
    #       [True, False, True, False], 1/2),
    # Tile('bend_br', bend_image,
    #       [True, False, False, True], 1/4),
    # Tile('bend_tr', bend_image.transpose(Image.ROTATE_90),
    #       [True, True, False, False], 1/4),
    # Tile('bend_tl', bend_image.transpose(Image.ROTATE_180),
    #       [False, True, True, False], 1/4),
    # Tile('bend_bl', bend_image.transpose(Image.ROTATE_270),
    #       [False, False, True, True], 1/4),
    # Tile('t_u', t_image,
    #       [True, True, True, False], 1/4),
    # Tile('t_l', t_image.transpose(Image.ROTATE_90),
    #       [False, True, True, True], 1/4),
    # Tile('t_d', t_image.transpose(Image.ROTATE_180),
    #       [True, False, True, True], 1/4),
    # Tile('t_r', t_image.transpose(Image.ROTATE_270),
    #       [True, True, False, True], 1/4),
    # Tile('blank', blank_image,
    #       [False, False, False, False], 1),
    # Tile('cross', cross_image,
    #       [True, True, True, True], 1)
    # ]
    # (3, 3, 40, 40, 3)
    # reshape : (120, 120, 4)
     
    #display.display(show_state(potential, tiles))
    weights = np.asarray([t.weight for t in tiles])

    potential = np.full((size_grid,size_grid, len(tiles)), True)
    #Add constraint so that the exterior tile can't connect to outside
    for i in range(size_grid):
        #Directions are reverse because for add_constraint it take the incoming direction (aka the outside to the tile)
        add_constraint(potential, (0,i),Direction.DOWN , [empty_tile], tiles)
        add_constraint(potential, (size_grid-1,i),Direction.UP , [empty_tile], tiles)
        add_constraint(potential, (i,0),Direction.RIGHT , [empty_tile], tiles)
        add_constraint(potential, (i,size_grid-1),Direction.LEFT , [empty_tile], tiles)
        # potential[(i,0)] = False
        # potential[(i,0)][0] = True
    middle_grid = int((size_grid-1)/2)
    
    #Add constraint to the center grid
    add_constraint(potential, (middle_grid,middle_grid), Direction.DOWN, [empty_tile_adjacent], tiles)
    add_constraint(potential, (middle_grid,middle_grid), Direction.LEFT, [empty_tile_adjacent], tiles)
    add_constraint(potential, (middle_grid,middle_grid), Direction.RIGHT, [empty_tile_adjacent], tiles)
    add_constraint(potential, (middle_grid,middle_grid), Direction.UP, [empty_tile_adjacent], tiles)
    
    p = potential
    images = [show_state(p, tiles)]
    try:
        p = run_iteration_middle(p,weights,tiles,size_grid)
        images.append(show_state(p, tiles))  # Move me for speed
    except Exception as e:
        print(e)
    while True:
        try:
            p = run_iteration(p,weights,tiles,size_grid)
            images.append(show_state(p, tiles))  # Move me for speed
        except StopIteration as e:
            break
        except noMorePattern as e:
            images.append(show_state(p, tiles))  # Move me for speed
            display.display(images[len(images)-1])   
            raise
            
        except Exception as e:
            print("exception",e)
            print (traceback.format_exc())
            break
    images.append(show_state(p, tiles))
    display.display(images[len(images)-1])    
    out = io.BytesIO()
    
    images[0].save("gid_result.gif", format='gif', save_all=True, append_images=images[1:],
                   duration=200, loop=0)
    images[len(images)-1].save("resultat.jpg")
    images[-1]

    display.HTML('<img src="data:image/gif;base64,{0}">'
                 .format(base64.b64encode(out.getvalue()).decode('utf8')))

    print("wave")
    
    


if __name__ == "__main__":
    size = 100
    nb_pattern = 200
    number_points = 6
    show_triangle = False
    show_point = False
    show_grid = False
    show_all_point = False
    size_grid = 10
    #symbol_weighted("jointed_lines.jpg")
    patterns = generate_patern(nb_pattern,size,number_points,show_triangle,show_point,show_grid,show_all_point)
    print("patterns generated ! ")
    for i in range(4):
        try:
            
            waveCollapse(nb_pattern,size_grid,patterns)
            break
        except noMorePattern as e:
            print("error no more pattern",e)
































