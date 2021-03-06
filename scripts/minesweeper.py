import random
import kandinsky
from time import sleep
from ion import *

def minesweeper():
  # Define the board size
  B_HEIGHT = 8
  B_WIDTH = 17
  inp = input("Height (default "+str(B_HEIGHT)+"):")
  if inp != "": B_HEIGHT = int(inp)
  if B_HEIGHT > 11: print("> recommended max of 11")
  
  inp = input("Width (default "+ str(B_WIDTH)+"):")
  if inp != "": B_WIDTH = int(inp)
  if B_WIDTH > 21: print("> recommended max of 21")
  
  if B_WIDTH <= 3 and B_HEIGHT <= 3: print("Board too small for safe start.\n0,0 safe")
  elif B_WIDTH * B_HEIGHT < 25: print("This is a small board.\nConsider making it larger.")
  
  # Define the number of bombs in the game
  N_BOMBS = int(B_HEIGHT*B_WIDTH*0.2)
  inp = input("# bombs (default "+str(N_BOMBS)+"):")
  if inp != "": N_BOMBS = int(inp)
  # Define the screen
  S_HEIGHT = 224
  S_WIDTH = 320
  
  # Space between each cell, CHANGE IF NOT READABLE
  OFFSET = 2

  if N_BOMBS >= B_HEIGHT * B_WIDTH:
    print("The board would fill or overflow with bombs. Decrease the number of bombs or increase the size of the board.")
    return()
  
  # Precalculate this to not need to have it a million times
  block_width = int((S_WIDTH-(OFFSET*(B_WIDTH+1)))/B_WIDTH)
  block_height = int((S_HEIGHT-(OFFSET*(B_HEIGHT+1)))/B_HEIGHT)

  # Define the settings
  debug = False
  render = True 
  
  # Define all of the colors:
  colors = {"cell":(179, 179, 179), "bg":(82, 82, 82), "bomb":(255,0,0), "flag":(232, 179, 46), "pointer":(46, 232, 226)} 
  rainbow = [(255, 0, 0), (255, 145, 0), (255, 255, 0), (0, 224, 26), (0, 242, 186), (0, 27, 232), (146, 0, 237), (237, 0, 126)]
  
  class Board():
    def __init__(self):
      # Make to board array
      self.B = [[0 for row in range(B_WIDTH)] for column in range(B_HEIGHT)]
      self.flagged = []
      self.points = 0
  
    def readBoard(self, x,y):
      if not(x < 0 or x >= B_WIDTH or y < 0 or y >= B_HEIGHT):
        return self.B[y][x]
      return None 
      
    def writeBoard(self,x,y,data):
      if not(x < 0 or x >= B_WIDTH or y < 0 or y >= B_HEIGHT):
        self.B[y][x] = data
        return data
      return None 
    
    def incrementCell(self, x, y):
      orig = self.readBoard(x, y)
      try: 
        int(orig)
        self.writeBoard(x, y, orig+1)
        return()
      except:
        return()
    
    # This spawns a bomb and makes sure that it isnt adjacent to the pointer
    def spawnBomb(self, pointer):
      while True:
        bombx = random.randint(0,B_WIDTH-1)
        bomby = random.randint(0,B_HEIGHT-1)
        if self.readBoard(bombx, bomby) != "X" and not(abs(pointer.x-bombx)<=1 and abs(pointer.y-bomby)<=1) :
          self.B[bomby][bombx] = 'X'
          # ICBA to write code to do this in a loop :)
          self.incrementCell(bombx-1, bomby-1)
          self.incrementCell(bombx-1, bomby)
          self.incrementCell(bombx-1, bomby+1)
          self.incrementCell(bombx, bomby-1)
          self.incrementCell(bombx, bomby+1)
          self.incrementCell(bombx+1, bomby-1)
          self.incrementCell(bombx+1, bomby)
          self.incrementCell(bombx+1, bomby+1)
          # Bomb has been planted
          return()
          
    # This function checks the board to see if it's complete
    def check(self):
      for y in range(B_HEIGHT): 
        for x in range(B_WIDTH):
          # Checks for a checked cell then a flagged cell that hides a bomb
          if not(str(self.B[y][x])[0] == "D" or ([x,y] in self.flagged and str(self.B[y][x])[0] == "X")):
            return False
      return True      
    
    # If the board is complete, draw the rainbow pattern and exit
    def finish(self):
      good = self.check()
      if good:
        # The dark black background
        # The cells in which are stored the bombas
        for y in range(B_HEIGHT): 
          ydraw = (block_height+OFFSET)*y+OFFSET
          for x in range(B_WIDTH):
            xdraw = (block_width+OFFSET)*x+OFFSET
            # Get the colour to be used in the rainbow
            c = rainbow[(x + y ) % len(rainbow)]
            #if debug: print("Drawing",xdraw,ydraw,block_width,block_height, colors["cell"])
            if render: kandinsky.fill_rect(xdraw,ydraw,block_width,block_height, c)
            sleep(4 / (B_HEIGHT * B_WIDTH))
        # When we are done, wait for 5 second then end the function
        sleep(5)
      
    def draw(self):
      # The dark black background
      if render: kandinsky.fill_rect(0,0,S_WIDTH,S_HEIGHT, colors["bg"])
      # The cells in which are stored the bombas
      for y in range(B_HEIGHT): 
        ydraw = (block_height+OFFSET)*y+OFFSET
        for x in range(B_WIDTH):
          xdraw = (block_width+OFFSET)*x+OFFSET
          #if debug: print("Drawing",xdraw,ydraw,block_width,block_height, colors["cell"])
          if render: kandinsky.fill_rect(xdraw,ydraw,block_width,block_height,colors["cell"])
          sleep(0.6 / (B_HEIGHT * B_WIDTH))
    
    # This process ensures that there are good starting cells where the pointer is at
    def gen(self, pointer):
      good = False
      print("Loading the bombs")
      for i in range(N_BOMBS):
        self.spawnBomb(pointer)

  class Pointer():
    
    def __init__(self):
      # Create the pointer
      self.x = 0
      self.y = 0
      # Set it to the offset so the first pointer is correctly drawn
      self.xpointer = OFFSET
      self.ypointer = OFFSET
    
    # Less copy paste :)
    def updatePointer(self):
      self.xpointer = (block_width+OFFSET)*self.x+OFFSET
      self.ypointer = (block_height+OFFSET)*(self.y)+OFFSET

    # All the moving directions
    def up(self):
      if self.y > 0:
        self.y -= 1
        self.updatePointer()
    
    def down(self):
      if self.y < B_HEIGHT - 1:
        self.y += 1
        self.updatePointer()
        
    def left(self):
      if self.x > 0:
        self.x -= 1
        self.updatePointer()
    
    def right(self):
      if self.x < B_WIDTH - 1:
        self.x += 1
        self.updatePointer()

    
    # Checks the cell for a bomb or a clear space
    def fire(self, board, x=None, y=None, depth=0):
      if x == None: x = self.x
      if y == None: y = self.y
      xSpointer = (block_width+OFFSET)*x+OFFSET
      ySpointer = (block_height+OFFSET)*y+OFFSET
      # Check that the cell is valid 
      if x >= 0 and x < B_WIDTH and y >= 0 and y < B_HEIGHT:
        # Check if the cell has allready been looked at
        if (not (str(board.B[y][x])[0] == "D"))and [x,y] not in board.flagged:
          # Check to see if the cell where the pointer is at is empty
          if board.B[y][x] != "X":
            # We didnt find a bomb so draw the number
            if render:kandinsky.draw_string(str(board.B[y][x]),xSpointer, ySpointer)
            if debug: print(self.xpointer, self.ypointer)    
          # If we found a bomb, draw a red rectrangle on the cell
          else:
            if debug: print("Bomb found",xSpointer,ySpointer,block_width,block_height, colors["bomb"])
            if render: kandinsky.fill_rect(xSpointer,ySpointer,block_width,block_height,colors["bomb"])
          # Add it to the list of checked cells so you cant loose numbers or found bombs
          board.B[y][x] = "D" + str(board.B[y][x] )
          
          # This part of the code implements 0 collapse, through itteration
          # The depth check is to just make sure that python dosent get mad :)
          if board.B[y][x][-1] == "0" and depth < 80:
            #print(x, y, "is clear, going deeper")
            # For all of the cells agacent to this cell, fire at them
            self.fire(board,x - 1,y - 1, depth + 1)
            self.fire(board,x + 0,y - 1, depth + 1)
            self.fire(board,x + 1,y - 1, depth + 1)
            self.fire(board,x - 1,y + 0, depth + 1)
            self.fire(board,x + 1,y + 0, depth + 1)
            self.fire(board,x - 1,y + 1, depth + 1)
            self.fire(board,x + 0,y + 1, depth + 1)
            self.fire(board,x + 1,y + 1, depth + 1)

    # Add a flag for where you think a bomb is
    def flag(self,on, board):
      if not str(board.B[self.y][self.x])[0] == "D":
        if on:
          if debug: print("Bomb found",self.xpointer,self.ypointer,block_width,block_height, colors["flag"])
          if render: kandinsky.fill_rect(self.xpointer,self.ypointer,block_width,block_height,colors["flag"])
          # Add it to a list of flagged cells so you cant set if off by accident
          if [self.x,self.y] not in board.flagged: board.flagged.append([self.x,self.y])
          if debug: print(board.flagged)
        else:
          if debug: print("Bomb found",self.xpointer,self.ypointer,block_width,block_height, colors["cell"])
          if render: kandinsky.fill_rect(self.xpointer,self.ypointer,block_width,block_height,colors["cell"])
          # Remove it from the flagged list
          if [self.x,self.y] in board.flagged:board.flagged.pop(board.flagged.index([self.x,self.y]))
          if debug: print(board.flagged)

    # A funciton to draw the pointer on the board    
    def draw(self,n):
      if render:
        colour = (255,255,255)
        if n == 0: colour = colors["bg"]
        else: colour = colors["pointer"]
        # Draw the top, bottom, left, right rectangles
        if render: kandinsky.fill_rect(self.xpointer-OFFSET,self.ypointer-OFFSET,block_width+OFFSET,OFFSET, colour)
        if render: kandinsky.fill_rect(self.xpointer-OFFSET,self.ypointer+block_height,block_width+OFFSET+OFFSET,OFFSET, colour)
        if render: kandinsky.fill_rect(self.xpointer-OFFSET,self.ypointer-OFFSET,OFFSET,block_height+OFFSET, colour)
        if render: kandinsky.fill_rect(self.xpointer+block_width,self.ypointer-OFFSET,OFFSET,block_height+OFFSET, colour)

    
  # Create the board and pointer
  board = Board()
  pointer = Pointer()

  #Draw the board and pointer
  board.draw()
  pointer.draw(1)

  # Main gameplay loop
  ckey = "0"
  genned = False
  while True:
    sleep(0.1)
    if keydown(KEY_LEFT) and ckey != "L":
      ckey = "L"
      pointer.draw(0)
      pointer.left()
      pointer.draw(1)
    elif keydown(KEY_RIGHT) and ckey != "R":
      ckey = "R"
      pointer.draw(0)
      pointer.right()
      pointer.draw(1)
    elif keydown(KEY_UP) and ckey != "U":
      ckey = "U"
      pointer.draw(0)
      pointer.up()
      pointer.draw(1)
    elif keydown(KEY_DOWN) and ckey != "D":
      ckey = "D"
      pointer.draw(0)
      pointer.down()
      pointer.draw(1)
    else:
      ckey = "0"
    
    # If they select to check this square
    if keydown(KEY_OK):
      # On the first turn, gen the board
      if not genned:
        board.gen(pointer)
        genned = True
      pointer.fire(board)
      board.finish()
    
    # If they select to add or remove a flag
    if keydown(KEY_LEFTPARENTHESIS):
      pointer.flag(True, board)
      board.finish()
    if keydown(KEY_RIGHTPARENTHESIS):
      pointer.flag(False, board)
