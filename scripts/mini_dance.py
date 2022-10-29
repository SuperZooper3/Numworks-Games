from time import *
from kandinsky import *
from random import *
from ion import *
def dance():
	B=True;A=False;points=0;inputs=0;time=0;colors=[(0,255,0),(0,0,255),(255,0,0),(255,255,0)];fill_rect(125,30,50,50,colors[0]);fill_rect(125,130,50,50,colors[1]);fill_rect(75,80,50,50,colors[2]);fill_rect(175,80,50,50,colors[3]);correct=randint(0,3);direction=4;last_direction=direction;fill_rect(125,80,50,50,colors[correct]);read=B
	while B:
		if keydown(KEY_UP):direction=0;read=A
		if keydown(KEY_DOWN):direction=1;read=A
		if keydown(KEY_LEFT):direction=2;read=A
		if keydown(KEY_RIGHT):direction=3;read=A
		if read==A:
			if direction==correct:
				inputs+=1;last_direction=direction;points+=1;correct=randint(0,2)
				if correct==direction:correct+=1
				fill_rect(125,80,50,50,colors[correct])
			elif last_direction!=direction:inputs+=1;last_direction=direction
			read=B;draw_string(str(points)+'/'+str(inputs),5,10)