import random,kandinsky
from time import sleep
from ion import *
def minesweeper():
	Q='U';P='R';O='L';N='pointer';M='0';L='Bomb found';K='flag';J='bomb';I='bg';H='';G='):';F='X';E='cell';D=False;C='D';B=None;A=True;B_HEIGHT=8;B_WIDTH=17;inp=input('Height (default '+str(B_HEIGHT)+G)
	if inp!=H:B_HEIGHT=int(inp)
	if B_HEIGHT>11:print('> recommended max of 11')
	inp=input('Width (default '+str(B_WIDTH)+G)
	if inp!=H:B_WIDTH=int(inp)
	if B_WIDTH>21:print('> recommended max of 21')
	if B_WIDTH<=3 and B_HEIGHT<=3:print('Board too small for safe start.\n0,0 safe')
	elif B_WIDTH*B_HEIGHT<25:print('This is a small board.\nConsider making it larger.')
	N_BOMBS=int(B_HEIGHT*B_WIDTH*0.2);inp=input('# bombs (default '+str(N_BOMBS)+G)
	if inp!=H:N_BOMBS=int(inp)
	S_HEIGHT=224;S_WIDTH=320;OFFSET=2
	if N_BOMBS>=B_HEIGHT*B_WIDTH:print('The board would fill or overflow with bombs. Decrease the number of bombs or increase the size of the board.');return()
	block_width=int((S_WIDTH-OFFSET*(B_WIDTH+1))/B_WIDTH);block_height=int((S_HEIGHT-OFFSET*(B_HEIGHT+1))/B_HEIGHT);debug=D;render=A;colors={E:(179,179,179),I:(82,82,82),J:(255,0,0),K:(232,179,46),N:(46,232,226)};rainbow=[(255,0,0),(255,145,0),(255,255,0),(0,224,26),(0,242,186),(0,27,232),(146,0,237),(237,0,126)]
	class Board:
		def __init__(self):self.B=[[0 for row in range(B_WIDTH)]for column in range(B_HEIGHT)];self.flagged=[];self.points=0
		def readBoard(self,x,y):
			if not(x<0 or x>=B_WIDTH or y<0 or y>=B_HEIGHT):return self.B[y][x]
			return B
		def writeBoard(self,x,y,data):
			if not(x<0 or x>=B_WIDTH or y<0 or y>=B_HEIGHT):self.B[y][x]=data;return data
			return B
		def incrementCell(self,x,y):
			orig=self.readBoard(x,y)
			try:int(orig);self.writeBoard(x,y,orig+1);return()
			except:return()
		def spawnBomb(self,pointer):
			while A:
				bombx=random.randint(0,B_WIDTH-1);bomby=random.randint(0,B_HEIGHT-1)
				if self.readBoard(bombx,bomby)!=F and not(abs(pointer.x-bombx)<=1 and abs(pointer.y-bomby)<=1):self.B[bomby][bombx]=F;self.incrementCell(bombx-1,bomby-1);self.incrementCell(bombx-1,bomby);self.incrementCell(bombx-1,bomby+1);self.incrementCell(bombx,bomby-1);self.incrementCell(bombx,bomby+1);self.incrementCell(bombx+1,bomby-1);self.incrementCell(bombx+1,bomby);self.incrementCell(bombx+1,bomby+1);return()
		def check(self):
			for y in range(B_HEIGHT):
				for x in range(B_WIDTH):
					if not(str(self.B[y][x])[0]==C or[x,y]in self.flagged and str(self.B[y][x])[0]==F):return D
			return A
		def finish(self):
			good=self.check()
			if good:
				for y in range(B_HEIGHT):
					ydraw=(block_height+OFFSET)*y+OFFSET
					for x in range(B_WIDTH):
						xdraw=(block_width+OFFSET)*x+OFFSET;c=rainbow[(x+y)%len(rainbow)]
						if render:kandinsky.fill_rect(xdraw,ydraw,block_width,block_height,c)
						sleep(4/(B_HEIGHT*B_WIDTH))
				sleep(5)
		def draw(self):
			if render:kandinsky.fill_rect(0,0,S_WIDTH,S_HEIGHT,colors[I])
			for y in range(B_HEIGHT):
				ydraw=(block_height+OFFSET)*y+OFFSET
				for x in range(B_WIDTH):
					xdraw=(block_width+OFFSET)*x+OFFSET
					if render:kandinsky.fill_rect(xdraw,ydraw,block_width,block_height,colors[E])
					sleep(0.6/(B_HEIGHT*B_WIDTH))
		def gen(self,pointer):
			good=D;print('Loading the bombs')
			for i in range(N_BOMBS):self.spawnBomb(pointer)
	class Pointer:
		def __init__(self):self.x=0;self.y=0;self.xpointer=OFFSET;self.ypointer=OFFSET
		def updatePointer(self):self.xpointer=(block_width+OFFSET)*self.x+OFFSET;self.ypointer=(block_height+OFFSET)*self.y+OFFSET
		def up(self):
			if self.y>0:self.y-=1;self.updatePointer()
		def down(self):
			if self.y<B_HEIGHT-1:self.y+=1;self.updatePointer()
		def left(self):
			if self.x>0:self.x-=1;self.updatePointer()
		def right(self):
			if self.x<B_WIDTH-1:self.x+=1;self.updatePointer()
		def fire(self,board,x=B,y=B,depth=0):
			if x==B:x=self.x
			if y==B:y=self.y
			xSpointer=(block_width+OFFSET)*x+OFFSET;ySpointer=(block_height+OFFSET)*y+OFFSET
			if x>=0 and x<B_WIDTH and y>=0 and y<B_HEIGHT:
				if not str(board.B[y][x])[0]==C and[x,y]not in board.flagged:
					if board.B[y][x]!=F:
						if render:kandinsky.draw_string(str(board.B[y][x]),xSpointer,ySpointer)
						if debug:print(self.xpointer,self.ypointer)
					else:
						if debug:print(L,xSpointer,ySpointer,block_width,block_height,colors[J])
						if render:kandinsky.fill_rect(xSpointer,ySpointer,block_width,block_height,colors[J])
					board.B[y][x]=C+str(board.B[y][x])
					if board.B[y][x][-1]==M and depth<80:self.fire(board,x-1,y-1,depth+1);self.fire(board,x+0,y-1,depth+1);self.fire(board,x+1,y-1,depth+1);self.fire(board,x-1,y+0,depth+1);self.fire(board,x+1,y+0,depth+1);self.fire(board,x-1,y+1,depth+1);self.fire(board,x+0,y+1,depth+1);self.fire(board,x+1,y+1,depth+1)
		def flag(self,on,board):
			if not str(board.B[self.y][self.x])[0]==C:
				if on:
					if debug:print(L,self.xpointer,self.ypointer,block_width,block_height,colors[K])
					if render:kandinsky.fill_rect(self.xpointer,self.ypointer,block_width,block_height,colors[K])
					if[self.x,self.y]not in board.flagged:board.flagged.append([self.x,self.y])
					if debug:print(board.flagged)
				else:
					if debug:print(L,self.xpointer,self.ypointer,block_width,block_height,colors[E])
					if render:kandinsky.fill_rect(self.xpointer,self.ypointer,block_width,block_height,colors[E])
					if[self.x,self.y]in board.flagged:board.flagged.pop(board.flagged.index([self.x,self.y]))
					if debug:print(board.flagged)
		def draw(self,n):
			if render:
				colour=255,255,255
				if n==0:colour=colors[I]
				else:colour=colors[N]
				if render:kandinsky.fill_rect(self.xpointer-OFFSET,self.ypointer-OFFSET,block_width+OFFSET,OFFSET,colour)
				if render:kandinsky.fill_rect(self.xpointer-OFFSET,self.ypointer+block_height,block_width+OFFSET+OFFSET,OFFSET,colour)
				if render:kandinsky.fill_rect(self.xpointer-OFFSET,self.ypointer-OFFSET,OFFSET,block_height+OFFSET,colour)
				if render:kandinsky.fill_rect(self.xpointer+block_width,self.ypointer-OFFSET,OFFSET,block_height+OFFSET,colour)
	board=Board();pointer=Pointer();board.draw();pointer.draw(1);ckey=M;genned=D
	while A:
		sleep(0.1)
		if keydown(KEY_LEFT)and ckey!=O:ckey=O;pointer.draw(0);pointer.left();pointer.draw(1)
		elif keydown(KEY_RIGHT)and ckey!=P:ckey=P;pointer.draw(0);pointer.right();pointer.draw(1)
		elif keydown(KEY_UP)and ckey!=Q:ckey=Q;pointer.draw(0);pointer.up();pointer.draw(1)
		elif keydown(KEY_DOWN)and ckey!=C:ckey=C;pointer.draw(0);pointer.down();pointer.draw(1)
		else:ckey=M
		if keydown(KEY_OK):
			if not genned:board.gen(pointer);genned=A
			pointer.fire(board);board.finish()
		if keydown(KEY_LEFTPARENTHESIS):pointer.flag(A,board);board.finish()
		if keydown(KEY_RIGHTPARENTHESIS):pointer.flag(D,board)