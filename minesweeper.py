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

  if B_WIDTH * B_HEIGHT < 25: print("This is a small board. \n Consider making it larger.")
  # Define the number of bombs in the game
  N_BOMBS = int(B_HEIGHT*B_WIDTH*0.2)
  inp = input("# bombs (default "+str(N_BOMBS)+"):")
  if inp != "": N_BOMBS = int(inp)
  # Define the screen
  S_HEIGHT = 224
  S_WIDTH = 320
  
  # Space between each cell
  OFFSET = 3

  if N_BOMBS >= B_HEIGHT * B_WIDTH:
    print("The board would fill or overflow with bombs. Bring down the number of bombs or increas the size of the board.")
    return()
    
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
        
    def spawnBomb(self):
      while True:
        bombx = random.randint(0,B_WIDTH-1)
        bomby = random.randint(0,B_HEIGHT-1)
        if self.readBoard(bombx, bomby) != "X":
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
            #print("Failed at", x ,y, str(self.B[y][x]))
            return False
      return True      
    
    # If the board is complete, draw the rainbow pattern and exit
    def finish(self):
      good = self.check()
      #print(good)
      if good:
        # The dark black background
        if render: kandinsky.fill_rect(0,0,S_WIDTH,S_HEIGHT, colors["bg"])
        # The cells in which are stored the bombas
        block_width = int((S_WIDTH-(OFFSET*(B_WIDTH+1)))/B_WIDTH)
        block_height = int((S_HEIGHT-(OFFSET*(B_HEIGHT+1)))/B_HEIGHT)
        for y in range(B_HEIGHT): 
          ydraw = (block_height+OFFSET)*y+OFFSET
          for x in range(B_WIDTH):
            #print("Block heigh and width", block_height, block_width)
            xdraw = (block_width+OFFSET)*x+OFFSET
            # Get the colour to be used in the rainbow
            c = rainbow[(x + y ) % len(rainbow)]
            #if debug: print("Drawing",xdraw,ydraw,block_width,block_height, colors["cell"])
            if render: kandinsky.fill_rect(xdraw,ydraw,block_width,block_height, c)
            sleep(4 / (B_HEIGHT * B_WIDTH))
        
      
    def draw(self):
      # The dark black background
      if render: kandinsky.fill_rect(0,0,S_WIDTH,S_HEIGHT, colors["bg"])
      # The cells in which are stored the bombas
      block_width = int((S_WIDTH-(OFFSET*(B_WIDTH+1)))/B_WIDTH)
      block_height = int((S_HEIGHT-(OFFSET*(B_HEIGHT+1)))/B_HEIGHT)
      for y in range(B_HEIGHT): 
        ydraw = (block_height+OFFSET)*y+OFFSET
        for x in range(B_WIDTH):
          #print("Block heigh and width", block_height, block_width)
          xdraw = (block_width+OFFSET)*x+OFFSET
          #if debug: print("Drawing",xdraw,ydraw,block_width,block_height, colors["cell"])
          if render: kandinsky.fill_rect(xdraw,ydraw,block_width,block_height,colors["cell"])
          sleep(0.6 / (B_HEIGHT * B_WIDTH))
    
    # This process ensures that there are good starting cells where the pointer is at
    def gen(self, pointer):
      good = False
      print("Loading the bombs")
      while not good:
        self.__init__()
        for i in range(N_BOMBS):
          self.spawnBomb()
        good = (self.B[pointer.y][pointer.x] == 0)
      print("Safe spawn:", good)

  class Pointer():
    def __init__(self):
      # Create the pointer
      self.x = 0
      self.y = 0
    
    # All the moving directions
    def up(self):
      if self.y > 0:
        self.y -= 1
    
    def down(self):
      if self.y < B_HEIGHT - 1:
        self.y += 1
        
    def left(self):
      if self.x > 0:
        self.x -= 1
    
    def right(self):
      if self.x < B_WIDTH - 1:
        self.x += 1
    
    # Checks the cell for a bomb or a clear space
    def fire(self, board):
      # Need the block dimentions anyways so why not put it here :)
      block_width = int((S_WIDTH-(OFFSET*(B_WIDTH+1)))/B_WIDTH)
      block_height = int((S_HEIGHT-(OFFSET*(B_HEIGHT+1)))/B_HEIGHT)
      xprint = (block_width+OFFSET)*self.x+OFFSET
      yprint = (block_height+OFFSET)*(self.y)+OFFSET
      # Check if the cell has allready been looked at
      if (not (str(board.B[self.y][self.x])[0] == "D"))and [self.x,self.y] not in board.flagged:
        # Check to see if the cell where the pointer is at is empty
        if board.B[self.y][self.x] != "X":
          # We didnt find a bomb so draw the number
          if render:kandinsky.draw_string(str(board.B[self.y][self.x]),xprint, yprint)
          if debug: print(xprint, yprint)    
        # If we found a bomb, draw a red rectrangle on the cell
        else:
          if debug: print("Bomb found",xprint,yprint,block_width,block_height, colors["bomb"])
          if render: kandinsky.fill_rect(xprint,yprint,block_width,block_height,colors["bomb"])
        # Add it to the list of checked cells so you cant loose numbers or found bombs
        board.B[self.y][self.x] = "D" + str(board.B[self.y][self.x] )

    # Add a flag for where you think a bomb is
    def flag(self,on, board):
      if not str(board.B[self.y][self.x])[0] == "D":
        block_width = int((S_WIDTH-(OFFSET*(B_WIDTH+1)))/B_WIDTH)
        block_height = int((S_HEIGHT-(OFFSET*(B_HEIGHT+1)))/B_HEIGHT)
        ydraw = (block_height+OFFSET)*self.y+OFFSET
        xdraw = (block_width+OFFSET)*self.x+OFFSET
        if on:
          if debug: print("Bomb found",xdraw,ydraw,block_width,block_height, colors["flag"])
          if render: kandinsky.fill_rect(xdraw,ydraw,block_width,block_height,colors["flag"])
          # Add it to a list of flagged cells so you cant set if off by accident
          if [self.x,self.y] not in board.flagged: board.flagged.append([self.x,self.y])
          if debug: print(board.flagged)
        else:
          if debug: print("Bomb found",xdraw,ydraw,block_width,block_height, colors["cell"])
          if render: kandinsky.fill_rect(xdraw,ydraw,block_width,block_height,colors["cell"])
          # Remove it from the flagged list
          if [self.x,self.y] in board.flagged:board.flagged.pop(board.flagged.index([self.x,self.y]))
          if debug: print(board.flagged)
    # A funciton to draw the pointer on the board    
    def draw(self):
      if render:
        block_width = int((S_WIDTH-(OFFSET*(B_WIDTH+1)))/B_WIDTH)
        block_height = int((S_HEIGHT-(OFFSET*(B_HEIGHT+1)))/B_HEIGHT)
        colour = colors["pointer"]
        xdraw = (block_width+OFFSET)*self.x
        ydraw = (block_height+OFFSET)*self.y
        # Draw the top, bottom, left, right rectangles
        kandinsky.fill_rect(xdraw,ydraw,block_width+OFFSET,OFFSET, colour)
        kandinsky.fill_rect(xdraw,ydraw+block_height+OFFSET,block_width+OFFSET+OFFSET,OFFSET, colour)
        kandinsky.fill_rect(xdraw,ydraw,OFFSET,block_height+OFFSET, colour)
        kandinsky.fill_rect(xdraw+block_width+OFFSET,ydraw,OFFSET,block_height+OFFSET, colour)
      
    def erase(self):
      if render:
        block_width = int((S_WIDTH-(OFFSET*(B_WIDTH+1)))/B_WIDTH)
        block_height = int((S_HEIGHT-(OFFSET*(B_HEIGHT+1)))/B_HEIGHT)
        colour = colors["bg"]
        xdraw = (block_width+OFFSET)*self.x
        ydraw = (block_height+OFFSET)*self.y
        # Draw the top, bottom, left, right rectangles
        kandinsky.fill_rect(xdraw,ydraw,block_width+OFFSET,OFFSET, colour)
        kandinsky.fill_rect(xdraw,ydraw+block_height+OFFSET,block_width+OFFSET+OFFSET,OFFSET, colour)
        kandinsky.fill_rect(xdraw,ydraw,OFFSET,block_height+OFFSET, colour)
        kandinsky.fill_rect(xdraw+block_width+OFFSET,ydraw,OFFSET,block_height+OFFSET, colour)
    
  # Create the board and pointer
  board = Board() # Idk how to not need to add this and icba to check if i even need it
  pointer = Pointer()
  board.draw()
  pointer.draw()

  # Load the board with bomba
  
  # Prints a shown version of the board
  #if debug:
    #for i in range(B_HEIGHT):print(board.B[i])

  # Draw the board

  
  # Main gameplay loop
  ckey = "0"
  genned = False
  while True:
    sleep(0.1)
    if keydown(KEY_LEFT) and ckey != "L":
      ckey = "L"
      pointer.erase()
      pointer.left()
      pointer.draw()
    elif keydown(KEY_RIGHT) and ckey != "R":
      ckey = "R"
      pointer.erase()
      pointer.right()
      pointer.draw()
    elif keydown(KEY_UP) and ckey != "U":
      ckey = "U"
      pointer.erase()
      pointer.up()
      pointer.draw()
    elif keydown(KEY_DOWN) and ckey != "D":
      ckey = "D"
      pointer.erase()
      pointer.down()
      pointer.draw()
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
