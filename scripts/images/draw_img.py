from imgdta import ALBUM_DATA, COLOUR_PALLETS
from math import sqrt, floor, ceil
import kandinsky

int2B64 = {0:"A",1:"B",2:"C",3:"D",4:"E",5:"F",6:"G",7:"H",8:"I",9:"J",10:"K",11:"L",12:"M",13:"N",14:"O",15:"P",16:"Q",17:"R",18:"S",19:"T",20:"U",21:"V",22:"W",23:"X",24:"Y",25:"Z",26:"a",27:"b",28:"c",29:"d",30:"e",31:"f",32:"g",33:"h",34:"i",35:"j",36:"k",37:"l",38:"m",39:"n",40:"o",41:"p",42:"q",43:"r",44:"s",45:"t",46:"u",47:"v",48:"w",49:"x",50:"y",51:"z",52:"0",53:"1",54:"2",55:"3",56:"4",57:"5",58:"6",59:"7",60:"8",61:"9",62:"+",63:"-",64:"="}
b642int = {y:x for x,y in int2B64.items()}

def draw_img():
  i = int(input("Image ID:"))
  IMAGE_DATA = ALBUM_DATA[i]
  COLOUR_DATA = COLOUR_PALLETS[i]
  ratio = 320/224 # width on height, aspect ratio of orginal picture
  n = len(IMAGE_DATA) # Three characters per pixel, should be an int
  width = ceil(sqrt(n*ratio))
  height = floor(width / ratio)
  width = floor(width)
  size = (int(width),int(height))
  scale = floor(320/width)
  
  # Reverse conversion
  for y in range(size[1]):
      for x in range(size[0]):
          try:
            chars = IMAGE_DATA[(size[0]*y)+x]
            colour = COLOUR_DATA[b642int[chars]]
            kandinsky.fill_rect(x*scale,y*scale,scale,scale,colour)
          except: pass