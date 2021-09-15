import kandinsky
import random
from ion import *
from time import *

def tetris():
  # Define the screen
  S_HEIGHT = 224
  S_WIDTH = 320
  
  # Define the board size
  B_HEIGHT = 15
  B_WIDTH = 20
  
  # A tick system similar to MC, where events are handeled each tick
  # Starts at the number given for tick
  tick = 0
  # Define the time between steps
  tick_time = 0.7
  tps = 20
  # Tick per action
  tpa = 3
  # Ticks per rotation, minimun delay between rotations
  tpr = 5
  
  # Define the settings
  debug = False
  render = True
  
  # Define all of the block shapes and colors
  blocks = [[[1,1,1,1]],[[1,0,0],[1,1,1],[0,0,0]], [[0,0,1],[1,1,1],[0,0,0]],[[1,1],[1,1]],[[0,1,1],[1,1,0],[0,0,0]],[[0,1,0],[1,1,1],[0,0,0]],[[1,1,0],[0,1,1],[0,0,0]]]
  colors = [(0,255,0),(0,0,255),(255,0,0),(255,255,0),(255,128,0),(127,0,255), (0,255,255)]
  white = (255,255,255)
  
  class Board():
    def __init__(self):
      # Make to board array
      # IMPORTANT NOTE: It is 2 wider becuase I can crash when tryint to write when the block is too far left or right so there is 1 digit padding on each side and above
      self.B = [[0 for x in range(B_WIDTH)] for y in range(B_HEIGHT)]
      self.points = 0
      self.speed = 1
      self.blocks = []
      self.combo = 0
      
    # A funciton that checks if the block colides with the bottom of the map, another block, or with the walls
    def checkCollision(self, block, d_x, d_y):
      for i in range(len(block.shape)):
        # Checks if the block too low
        if block.y+d_y+i > B_HEIGHT:
          if debug and render: kandinsky.draw_string(str("collision"),0,15)
          if debug: print("Collision")
          return True
        for n in range(len(block.shape[i])):
          try:
              # Check if it hits the wall
              if block.shape[i][n] == 1 and (block.x+d_x+n > B_WIDTH or block.x+n+d_x < 0):
                if debug and render: kandinsky.draw_string(str("collision"),0,15)
                if debug: print("Collision")
                return True
              # Looks for a colision between the active block and a peice on the board
              if (block.shape[i][n] == 1 and self.B[i+block.y+d_y][n+block.x+d_x] != 0):
                if debug and render: kandinsky.draw_string(str("collision"),0,15)
                if debug: print("Block Collision")
                return True
          except:
              return True
      return False
    
    # A function to write the block to the board  
    def writeBlock(self, block):
      if debug: print("writing")
      for i in range(len(block.shape)):
        for n in range(len(block.shape[i])):
          # If we fell when we are at the top, stop the game
          if block.y == 0:
            if render: kandinsky.draw_string("Game over! Points: " + str(board.points),50,100)
            if render: kandinsky.draw_string("Press OK to replay.",60,130)
            if debug: print("Game Over")
            while True:
              if keydown(KEY_OK):
                tetris()
          #Make sure that we are not writing outside of the board
          if not(n+block.x < 0 or n+block.x >= B_WIDTH or i+block.y >= B_HEIGHT):
            if debug: print("y="+str(i+block.y))
            # Write the block to the board
            if block.shape[i][n] != 0: self.B[i+block.y][n+block.x] = block.shape[i][n] * block.type
      
    # A function to check for tetrices
    def checkTetris(self):
      for i in range(len(self.B)):
        if self.B[i].count(0) == 0:
          self.combo += 1
          self.points += 2000 * (board.speed * 1.5) * (self.combo**2)
          self.speed += 0.1
          #if debug and render: kandinsky.draw_string("Tetris!",0,15)          
          #Remove the data from the list and add back a clean part at the start of tha array
          del self.B[i]
          self.B.insert(0, [0 for x in range(B_WIDTH)]) 
          # Make the board look like the blocks dissapeared
          self.redraw()
          if not(debug) and render and self.combo > 1: kandinsky.draw_string("Combo x" + str(self.combo),50,100)
          if not(debug) and render: kandinsky.draw_string(("Points: " + str(round(self.points))),0,0)
          sleep(tick_time)
          self.redraw()
        else:
          self.combo = 0
          
    # Redraw the entire board if needed
    def redraw(self):
      kandinsky.fill_rect(0,0, S_WIDTH, S_HEIGHT, white)
      if debug: print("redraw")
      for i in range(len(self.B)):
        for n in range(len(self.B[i])):
          if self.B[i][n] != 0: kandinsky.fill_rect(int((S_WIDTH/B_WIDTH)*(n)),int((S_HEIGHT/B_HEIGHT)*(i)),int(S_WIDTH/B_WIDTH),int(S_HEIGHT/B_HEIGHT), colors[(self.B[i][n])-1])

      
  # Make the board so that block funcitons can use it
  board = Board()
  
  #Reset the board
  board.redraw()
    
  class Block:
    def __init__(self):
      if debug: print("init block")
      i = random.randint(0, len(blocks) - 1) + 1
      if len(board.blocks) == len(blocks):
        board.blocks.clear()
      # This part ensures that every peice is pulled before pulling one twice
      while board.blocks.count(i) > 0:
        i = random.randint(0, len(blocks) - 1) + 1
        if debug: print("i =" + str(i) + " blocks = " + str(board.blocks))
      board.blocks.append(i)
      #if debug and render: kandinsky.draw_string("write i = "+ str(i),0,15)
      self.type = i
      # All the other settings
      self.shape = blocks[self.type-1]
      self.color = colors[self.type-1]
      self.x = int(B_WIDTH/2)
      self.y = 0
      self.lastAction = tpa * -1
      self.lastRotate = tpr * -1
    
    # Draws the block on the board
    def draw(self):
      for i in range(len(self.shape)):
        for n in range(len(self.shape[i])):
          if self.shape[i][n] == 1:
            kandinsky.fill_rect(int((S_WIDTH/B_WIDTH)*(n+ self.x)),int((S_HEIGHT/B_HEIGHT)*(i+ self.y)),int(S_WIDTH/B_WIDTH),int(S_HEIGHT/B_HEIGHT), self.color)
    # Erases where the block is
    def erase(self):
      for i in range(len(self.shape)):
        for n in range(len(self.shape[i])):
          if self.shape[i][n] == 1:
            kandinsky.fill_rect(int((S_WIDTH/B_WIDTH)*(n+ self.x)),int((S_HEIGHT/B_HEIGHT)*(i+ self.y)),int(S_WIDTH/B_WIDTH),int(S_HEIGHT/B_HEIGHT), white)
    # A function that rotates all of the shape data in a block
    def rotate(self):
      if debug: print("rotate")
      self.shape = list(zip(*self.shape[::-1]))
        
    # All the actions that can be run
    def down(self, board):
      if debug: print("down")
      #Check if the block can move cleanly down (indicated by the x=0 and y=1)
      if debug: print("collision = " + str(board.checkCollision(self, 0, 1)))
      if not board.checkCollision(self, 0, 1):
        # If it dosent, move the actual block
        self.y = self.y+1
        
    def left(self, board):
      if debug: print("left")
      if not board.checkCollision(self, -1, 0):
        self.x = self.x-1
        
    def right(self, board):
      if debug: print("left")
      if not board.checkCollision(self, 1, 0):
        self.x = self.x+1
        
  # The main game loop
  if not(debug) and render: kandinsky.draw_string(("Points: " + str(board.points)),0,0)
  
  # Create the original block and draw it at spawn
  block = Block()
  if render: block.draw()
  
  while True:
    # Wait until the next tick
    sleep(tick_time/tps/board.speed)
    tick += 1
    
    # Debuging
    if debug and render: kandinsky.draw_string(str(tick),0,0)
    
    # Left and Right Key presses
    # Checks that tpa is respected
    if tick - block.lastAction >= tpa:
        block.lastAction = tick
        if keydown(KEY_LEFT): 
          if render: block.erase()
          block.left(board)
          if render: block.draw()
        if keydown(KEY_RIGHT): 
          if render: block.erase()
          block.right(board)
          if render: block.draw()
    # Rotate key
    if tick - block.lastRotate >= tpr:
      block.lastRotate = tick
      if keydown(KEY_UP): 
        if render: block.erase()
        block.rotate()
        if render: block.draw()
    # Down key
    if keydown(KEY_DOWN): 
      board.points += 5 * (board.speed * 1.5)
      # THIS COULD BE MORE EFFICIENT BUT ICBA TO CHANGE IT
      if board.checkCollision(block, 0, 1):
        board.writeBlock(block)
        board.checkTetris()
        del block
        block = Block()
        if render: block.draw()
      else:
        if render: block.erase()
        block.down(board)
        if render: block.draw()
      
    if keydown(KEY_OK):
      press = False
      if not(debug) and render: kandinsky.draw_string("Pause",100,100)
      sleep(1)
      while not press:
         if keydown(KEY_OK):
            press = True
      sleep(0.5)
      board.redraw()
        
    # Checks if its time to bring down the block
    if tick % tps == 0:
      board.points += 5 * (board.speed * 1.5)
      if not(debug) and render: kandinsky.draw_string(("Points: " + str(round(board.points))),0,0)
      # If the block has a colision, delete the current one (will still stay rendered)
      # and then create a new one to replace it
      if board.checkCollision(block, 0, 1):
        board.writeBlock(block)
        board.checkTetris()
        del block
        block = Block()
        if render: block.draw()
      else:
        if render: block.erase()
        block.down(board)
        if render: block.draw()