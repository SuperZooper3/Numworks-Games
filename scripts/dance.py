from time import *
from kandinsky import *
from random import *
from ion import *

def dance():
  points = 0
  inputs = 0
  time = 0
  
  colors = [(0,255,0),(0,0,255),(255,0,0),(255,255,0)]
  # Init the board
  fill_rect(125,30,50,50, colors[0])
  fill_rect(125,130,50,50, colors[1])
  fill_rect(75,80,50,50, colors[2])
  fill_rect(175,80,50,50, colors[3])
  
  correct = randint(0,3)
  direction = 4
  last_direction = direction
  fill_rect(125,80,50,50, colors[correct])
  read = True
  while True:
    if keydown(KEY_UP): 
      direction = 0
      read = False
    if keydown(KEY_DOWN) :
      direction = 1
      read = False
    if keydown(KEY_LEFT): 
      direction = 2
      read = False
    if keydown(KEY_RIGHT): 
      direction = 3
      read = False
    
    if read == False:
      if direction == correct:
        inputs += 1
        last_direction = direction
        points += 1
        correct = randint(0,2)
        if correct == direction:
          correct += 1
        fill_rect(125,80,50,50, colors[correct])
      else:
        if last_direction != direction:
          inputs += 1
          last_direction = direction
      read = True
      draw_string(str(points) + "/" + str(inputs),5,10)
