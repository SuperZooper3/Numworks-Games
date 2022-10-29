from imgdta import ALBUM_DATA, COLOUR_PALLETS, IMG_SIZE
from math import sqrt, floor, ceil
import kandinsky

int2B64 = {0:"A",1:"B",2:"C",3:"D",4:"E",5:"F",6:"G",7:"H",8:"I",9:"J",10:"K",11:"L",12:"M",13:"N",14:"O",15:"P",16:"Q",17:"R",18:"S",19:"T",20:"U",21:"V",22:"W",23:"X",24:"Y",25:"Z",26:"a",27:"b",28:"c",29:"d",30:"e",31:"f",32:"g",33:"h",34:"i",35:"j",36:"k",37:"l",38:"m",39:"n",40:"o",41:"p",42:"q",43:"r",44:"s",45:"t",46:"u",47:"v",48:"w",49:"x",50:"y",51:"z",52:"*",53:"^",54:"@",55:"!",56:"_",57:"~",58:"`",59:":",60:";",61:"$",62:"+",63:"-",64:"="}
b642int = {y:x for x,y in int2B64.items()}
cComScale = 4
def decompColour(c):return ((ord(c[0])-32)*cComScale,(ord(c[1])-32)*cComScale,(ord(c[2])-32)*cComScale)
def unsquishPallet(p):return [decompColour(p[i*3:(i+1)*3]) for i in range(len(p)//3)]

def DRAW_IMG():
	i = int(input("Image ID 0-"+str(len(ALBUM_DATA)-1)+": "))
	if i >= len(ALBUM_DATA):
		print("Invalid image ID, outside range")
		return
	IMAGE_DATA = ALBUM_DATA[i]
	COLOUR_DATA = unsquishPallet(COLOUR_PALLETS[i])
	size = IMG_SIZE
	scale = floor(320/size[0])  
	# Reverse conversion
	current = []
	i = 0
	for y in range(size[1]):
		for x in range(size[0]):
			if len(current) == 0:
				w,n="",""
				while len(w) == 0 or not w[-1] in int2B64.values() and i < len(IMAGE_DATA):
					w += IMAGE_DATA[i]
					i += 1
				n = ""
				for v in w:
					if not v in int2B64.values(): n += v
					else:
						if n != "":
							current+= [v]*int(n)
							n = ""
						else:current.append(v)
			try:
				chars = current.pop(0)
				colour = COLOUR_DATA[b642int[chars]]
				kandinsky.fill_rect(x*scale,y*scale,scale,scale,colour)
			except: pass