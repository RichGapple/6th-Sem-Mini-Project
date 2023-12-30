from visualization import *

path__ = "./IMG/tb_images/algorithm_1.png"

shapeMat = png2arr(path__)

out = outline_without_shape(shapeMat)

arr2png(out).show()

memX,memY = 100,100

ptLi = []

newOut = [[0]*len(out[0])]*len(out)

pts=[]

for i,row in enumerate(out):
    for j,col in enumerate(row):
        if(str(col)=="0.7" and (i>=memX or j>=memY)):
            pts.append((i,j))
        else:
            out[i][j]=0

for _ in pts:
    a,b = _
    out[a][b] = "r"

arr2png(out).show()