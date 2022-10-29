S=int
L=range
C=ord
B=len
from imgdta import ALBUM_DATA as I,COLOUR_PALLETS as N,IMG_SIZE as O
from math import sqrt,floor,ceil
import kandinsky as P
J={0:'A',1:'B',2:'C',3:'D',4:'E',5:'F',6:'G',7:'H',8:'I',9:'J',10:'K',11:'L',12:'M',13:'N',14:'O',15:'P',16:'Q',17:'R',18:'S',19:'T',20:'U',21:'V',22:'W',23:'X',24:'Y',25:'Z',26:'a',27:'b',28:'c',29:'d',30:'e',31:'f',32:'g',33:'h',34:'i',35:'j',36:'k',37:'l',38:'m',39:'n',40:'o',41:'p',42:'q',43:'r',44:'s',45:'t',46:'u',47:'v',48:'w',49:'x',50:'y',51:'z',52:'*',53:'^',54:'@',55:'!',56:'_',57:'~',58:'`',59:':',60:';',61:'$',62:'+',63:'-',64:'='}
Q={B:A for(A,B)in J.items()}
A=4
def D(c):return(C(c[0])-32)*A,(C(c[1])-32)*A,(C(c[2])-32)*A
def R(p):return[D(p[A*3:(A+1)*3])for A in L(B(p)//3)]
def DRAW_IMG():
	H='';A=S(input('Image ID 0-'+str(B(I)-1)+': '))
	if A>=B(I):print('Invalid image ID, outside range');return
	M=I[A];T=R(N[A]);K=O;D=floor(320/K[0]);E=[];A=0
	for U in L(K[1]):
		for V in L(K[0]):
			if B(E)==0:
				F,C=H,H
				while B(F)==0 or not F[-1]in J.values()and A<B(M):F+=M[A];A+=1
				C=H
				for G in F:
					if not G in J.values():C+=G
					elif C!=H:E+=[G]*S(C);C=H
					else:E.append(G)
			try:W=E.pop(0);X=T[Q[W]];P.fill_rect(V*D,U*D,D,D,X)
			except:pass