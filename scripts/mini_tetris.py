import kandinsky,random
from ion import *
from time import *
def tetris():
	D='left';C='Points: ';B=False;A=True;S_HEIGHT=224;S_WIDTH=320;B_HEIGHT=15;B_WIDTH=20;tick=0;tick_time=0.7;tps=20;tpa=3;tpr=5;debug=B;render=A;blocks=[[[1,1,1,1]],[[1,0,0],[1,1,1],[0,0,0]],[[0,0,1],[1,1,1],[0,0,0]],[[1,1],[1,1]],[[0,1,1],[1,1,0],[0,0,0]],[[0,1,0],[1,1,1],[0,0,0]],[[1,1,0],[0,1,1],[0,0,0]]];colors=[(0,255,0),(0,0,255),(255,0,0),(255,255,0),(255,128,0),(127,0,255),(0,255,255)];white=255,255,255
	class Board:
		def __init__(self):self.B=[[0 for x in range(B_WIDTH)]for y in range(B_HEIGHT)];self.points=0;self.speed=1;self.blocks=[];self.combo=0
		def checkCollision(self,block,d_x,d_y):
			D='Collision';C='collision'
			for i in range(len(block.shape)):
				if block.y+d_y+i>B_HEIGHT:
					if debug and render:kandinsky.draw_string(str(C),0,15)
					if debug:print(D)
					return A
				for n in range(len(block.shape[i])):
					try:
						if block.shape[i][n]==1 and(block.x+d_x+n>B_WIDTH or block.x+n+d_x<0):
							if debug and render:kandinsky.draw_string(str(C),0,15)
							if debug:print(D)
							return A
						if block.shape[i][n]==1 and self.B[i+block.y+d_y][n+block.x+d_x]!=0:
							if debug and render:kandinsky.draw_string(str(C),0,15)
							if debug:print('Block Collision')
							return A
					except:return A
			return B
		def writeBlock(self,block):
			if debug:print('writing')
			for i in range(len(block.shape)):
				for n in range(len(block.shape[i])):
					if block.y==0:
						if render:kandinsky.draw_string('Game over! Points: '+str(board.points),50,100)
						if render:kandinsky.draw_string('Press OK to replay.',60,130)
						if debug:print('Game Over')
						while A:
							if keydown(KEY_OK):tetris()
					if not(n+block.x<0 or n+block.x>=B_WIDTH or i+block.y>=B_HEIGHT):
						if debug:print('y='+str(i+block.y))
						if block.shape[i][n]!=0:self.B[i+block.y][n+block.x]=block.shape[i][n]*block.type
		def checkTetris(self):
			for i in range(len(self.B)):
				if self.B[i].count(0)==0:
					self.combo+=1;self.points+=2000*(board.speed*1.5)*self.combo**2;self.speed+=0.1;del self.B[i];self.B.insert(0,[0 for x in range(B_WIDTH)]);self.redraw()
					if not debug and render and self.combo>1:kandinsky.draw_string('Combo x'+str(self.combo),50,100)
					if not debug and render:kandinsky.draw_string(C+str(round(self.points)),0,0)
					sleep(tick_time);self.redraw()
				else:self.combo=0
		def redraw(self):
			kandinsky.fill_rect(0,0,S_WIDTH,S_HEIGHT,white)
			if debug:print('redraw')
			for i in range(len(self.B)):
				for n in range(len(self.B[i])):
					if self.B[i][n]!=0:kandinsky.fill_rect(int(S_WIDTH/B_WIDTH*n),int(S_HEIGHT/B_HEIGHT*i),int(S_WIDTH/B_WIDTH),int(S_HEIGHT/B_HEIGHT),colors[self.B[i][n]-1])
	board=Board();board.redraw()
	class Block:
		def __init__(self):
			if debug:print('init block')
			i=random.randint(0,len(blocks)-1)+1
			if len(board.blocks)==len(blocks):board.blocks.clear()
			while board.blocks.count(i)>0:
				i=random.randint(0,len(blocks)-1)+1
				if debug:print('i ='+str(i)+' blocks = '+str(board.blocks))
			board.blocks.append(i);self.type=i;self.shape=blocks[self.type-1];self.color=colors[self.type-1];self.x=int(B_WIDTH/2);self.y=0;self.lastAction=tpa*-1;self.lastRotate=tpr*-1
		def draw(self):
			for i in range(len(self.shape)):
				for n in range(len(self.shape[i])):
					if self.shape[i][n]==1:kandinsky.fill_rect(int(S_WIDTH/B_WIDTH*(n+self.x)),int(S_HEIGHT/B_HEIGHT*(i+self.y)),int(S_WIDTH/B_WIDTH),int(S_HEIGHT/B_HEIGHT),self.color)
		def erase(self):
			for i in range(len(self.shape)):
				for n in range(len(self.shape[i])):
					if self.shape[i][n]==1:kandinsky.fill_rect(int(S_WIDTH/B_WIDTH*(n+self.x)),int(S_HEIGHT/B_HEIGHT*(i+self.y)),int(S_WIDTH/B_WIDTH),int(S_HEIGHT/B_HEIGHT),white)
		def rotate(self):
			if debug:print('rotate')
			self.shape=list(zip(*self.shape[::-1]))
		def down(self,board):
			if debug:print('down')
			if debug:print('collision = '+str(board.checkCollision(self,0,1)))
			if not board.checkCollision(self,0,1):self.y=self.y+1
		def left(self,board):
			if debug:print(D)
			if not board.checkCollision(self,-1,0):self.x=self.x-1
		def right(self,board):
			if debug:print(D)
			if not board.checkCollision(self,1,0):self.x=self.x+1
	if not debug and render:kandinsky.draw_string(C+str(board.points),0,0)
	block=Block()
	if render:block.draw()
	while A:
		sleep(tick_time/tps/board.speed);tick+=1
		if debug and render:kandinsky.draw_string(str(tick),0,0)
		if tick-block.lastAction>=tpa:
			block.lastAction=tick
			if keydown(KEY_LEFT):
				if render:block.erase()
				block.left(board)
				if render:block.draw()
			if keydown(KEY_RIGHT):
				if render:block.erase()
				block.right(board)
				if render:block.draw()
		if tick-block.lastRotate>=tpr:
			block.lastRotate=tick
			if keydown(KEY_UP):
				if render:block.erase()
				block.rotate()
				if render:block.draw()
		if keydown(KEY_DOWN):
			board.points+=5*(board.speed*1.5)
			if board.checkCollision(block,0,1):
				board.writeBlock(block);board.checkTetris();del block;block=Block()
				if render:block.draw()
			else:
				if render:block.erase()
				block.down(board)
				if render:block.draw()
		if keydown(KEY_OK):
			press=B
			if not debug and render:kandinsky.draw_string('Pause',100,100)
			sleep(1)
			while not press:
				if keydown(KEY_OK):press=A
			sleep(0.5);board.redraw()
		if tick%tps==0:
			board.points+=5*(board.speed*1.5)
			if not debug and render:kandinsky.draw_string(C+str(round(board.points)),0,0)
			if board.checkCollision(block,0,1):
				board.writeBlock(block);board.checkTetris();del block;block=Block()
				if render:block.draw()
			else:
				if render:block.erase()
				block.down(board)
				if render:block.draw()