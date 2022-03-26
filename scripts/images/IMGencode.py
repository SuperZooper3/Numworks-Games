from PIL import Image
import numpy as np
import os

int2B64 = {0:"A",1:"B",2:"C",3:"D",4:"E",5:"F",6:"G",7:"H",8:"I",9:"J",10:"K",11:"L",12:"M",13:"N",14:"O",15:"P",16:"Q",17:"R",18:"S",19:"T",20:"U",21:"V",22:"W",23:"X",24:"Y",25:"Z",26:"a",27:"b",28:"c",29:"d",30:"e",31:"f",32:"g",33:"h",34:"i",35:"j",36:"k",37:"l",38:"m",39:"n",40:"o",41:"p",42:"q",43:"r",44:"s",45:"t",46:"u",47:"v",48:"w",49:"x",50:"y",51:"z",52:"*",53:"^",54:"@",55:"!",56:"_",57:"~",58:"`",59:":",60:";",61:"$",62:"+",63:"-",64:"="}
b642int = {y:x for x,y in int2B64.items()}

directory = 'images'

scale = 4
palletDepth = 7
size = (320//scale,224//scale)

def pxr(p): return p[0],p[2],p[1]
def pxg(p): return p[1],p[0],p[2]
def pxb(p): return p[2],p[0],p[1]

def reduce(s):
    o = ""
    curr = s[0]
    n = 0
    for c in s:
        if c == curr: n += 1
        else:
            if n > 1: o += str(n)
            o += curr
            curr = c
            n = 1
    if n > 1: o += str(n)
    o += curr
    curr = c
    n = 1
    return o

def rehydrate(s): # Turns a reduced string back into the full one
    o,n="",""
    for v in s:
        if v.isnumeric(): n += v
        else:
            if n != "":
                o += v*int(n)
                n = ""
            else:o += v
    return o

def compColour(c):
    r,g,b=c
    xr = chr(r//4+32)
    xg = chr(g//4+32)
    xb = chr(b//4+32)
    if xg == "\"": xg = chr(g//4+31)
    return xr+xg+xb

def squishPallet(p):
    op = ""
    for v in p: op += compColour(v)
    return op

def decompColour(c):
    r = (ord(c[0])-32)*4
    g = (ord(c[1])-32)*4
    b = (ord(c[2])-32)*4
    return (r,g,b)

def unsquishPallet(p):
    op = []
    for i in range(len(p)//3):
        op.append(decompColour(p[i*3:(i+1)*3]))
    return op

def generatePallet(bucket,d,f): # d is the recursio depth, f is depth of pallet so 2^d-1 colours
    # Calculate the dominant channel
    nd = d + 1
    r = []
    g = []
    b = []
    for px in bucket:
        r.append(px[0])
        g.append(px[1])
        b.append(px[2])
    r.sort()
    g.sort()
    b.sort()
    stdR = np.std(r)
    stdG = np.std(g)
    stdB = np.std(b)
    # print(stdR,stdG,stdB)
    b1 = []
    b2 = []
    nBucket = []
    if max(stdR,stdG,stdB) == stdR:
        nBucket = sorted(bucket, key=pxr)
    elif max(stdR,stdG,stdB) == stdG:
        nBucket = sorted(bucket, key=pxg)
    elif max(stdR,stdG,stdB) == stdB:
        nBucket = sorted(bucket, key=pxb)
    b1 = nBucket[0:len(nBucket)//2+1]
    b2 = nBucket[len(nBucket)//2+1:len(bucket)+1]
    # print(len(nBucket),len(b1), len(b2))
    if nd < f:
        colours1 = generatePallet(b1,nd,f)
        colours2 = generatePallet(b2,nd,f)
        return colours1 + colours2
    else:
        return [(int(np.average(r)),int(np.average(g)),int(np.average(b)))]

def convertRGBtoChar(rgb):
    r = chr((rgb[0]//4)+32)
    g = chr((rgb[1]//4)+32)
    b = chr((rgb[2]//4)+32)
    if g == "\"":
        g = chr((rgb[1]//4)+31)
    return(r,g,b)

def convertChartoRGB(char):
    r = (ord(char[0]) - 32) * 4
    g = (ord(char[1]) - 32) * 4
    b = (ord(char[2]) - 32) * 4
    return r,g,b

album = []
colours = []
for filename in os.listdir(directory):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        im = Image.open(directory+"/"+filename)
        rgb_im = im.convert('RGBA')
        f_im = rgb_im.resize(size,Image.ANTIALIAS)
        # Generate the pallet
        bucket_im = []
        for y in range(size[1]):
            for x in range(size[0]):
                bucket_im.append(f_im.getpixel((x,y)))
        pallet = generatePallet(bucket_im,0,palletDepth)
        s = ""      
        for y in range(size[1]):
            for x in range(size[0]):
                px = f_im.getpixel((x,y))
                # Find the nearest pixel
                closest = 0
                closestDist = 999999999999999999
                if px[3] == 0:
                    if len(pallet) == 2**(palletDepth-1):
                        pallet.append((255,255,255))
                    s += int2B64[64]
                else: 
                    for id, candidate in enumerate(pallet):
                        dist = np.sqrt((candidate[0]-px[0])**2+(candidate[1]-px[1])**2+(candidate[2]-px[2])**2)
                        if dist < closestDist:
                            closest = id
                            closestDist = dist
                    # print("Closest to x is y:",px,pallet[closest])
                    s += int2B64[closest]
        album.append(reduce(s))
        colours.append(squishPallet(pallet))

f = open("imgdta.py","w")
f.write("IMG_SIZE="+size.__repr__()+"\n")
f.write("ALBUM_DATA="+album.__repr__()+"\n")
f.write("COLOUR_PALLETS=[r\"\"\""+"\"\"\",r\"\"\"".join(colours)+"\"\"\" ]")
f.close()
