from PIL import Image
import numpy as np
from imgdta import ALBUM_DATA, COLOUR_PALLETS
from math import ceil, floor, sqrt

int2B64 = {0:"A",1:"B",2:"C",3:"D",4:"E",5:"F",6:"G",7:"H",8:"I",9:"J",10:"K",11:"L",12:"M",13:"N",14:"O",15:"P",16:"Q",17:"R",18:"S",19:"T",20:"U",21:"V",22:"W",23:"X",24:"Y",25:"Z",26:"a",27:"b",28:"c",29:"d",30:"e",31:"f",32:"g",33:"h",34:"i",35:"j",36:"k",37:"l",38:"m",39:"n",40:"o",41:"p",42:"q",43:"r",44:"s",45:"t",46:"u",47:"v",48:"w",49:"x",50:"y",51:"z",52:"0",53:"1",54:"2",55:"3",56:"4",57:"5",58:"6",59:"7",60:"8",61:"9",62:"+",63:"-",64:"="}
b642int = {y:x for x,y in int2B64.items()}
cComScale = 4

def rehydrate(s): # Turns a reduced string back into the full one
    o,n="",""
    for v in s:
        if not v.isalpha(): n += v
        else:
            if n != "":
                o += v*int(n)
                n = ""
            else:o += v
    return o

def decompColour(c):
    r = (ord(c[0])-32)*cComScale
    g = (ord(c[1])-32)*cComScale
    b = (ord(c[2])-32)*cComScale
    return (r,g,b)

def unsquishPallet(p):
    op = []
    for i in range(len(p)//3):
        op.append(decompColour(p[i*3:(i+1)*3]))
    return op

i = int(input("Image ID:"))
IMAGE_DATA = rehydrate(ALBUM_DATA[i])
COLOUR_DATA = unsquishPallet(COLOUR_PALLETS[i])
ratio = 320/224 # width on height, aspect ratio of orginal picture
n = len(IMAGE_DATA) # Three characters per pixel, should be an int
width = ceil(sqrt(n*ratio))
height = floor(width / ratio)
width = floor(width)
size = (int(width),int(height))
scale = floor(320/width)

print(COLOUR_DATA)

# Reverse conversion
rev_rgb = []
for y in range(size[1]):
    row = []
    for x in range(size[0]):
        chars = IMAGE_DATA[(size[0]*y)+x]
        colour = COLOUR_DATA[b642int[chars]]
        row.append(colour)
    rev_rgb.append(row)

# VISUALISATION OF CONVERTED
# Convert the pixels into an array using numpy
array = np.array(rev_rgb, dtype=np.uint8)

# Use PIL to create an image from the new array of pixels
new_image = Image.fromarray(array)
new_image.save('rev.png')