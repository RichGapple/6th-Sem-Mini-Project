import numpy as np
import collections as c
import os

# pospl -> POSition Point Line
def pospl(pt1,pt2,pt3):
    '''
    Returns the position of the point pt3 according to the line vector pt1->pt2\n
    right hand fold => 1\n
    left hand fold => -1\n
    same line      =>  0
    '''
    x1,y1=pt1
    x2,y2=pt2
    xA,yA=pt3

    v1 = (x2-x1, y2-y1)   # Vector 1
    v2 = (x2-xA, y2-yA)   # Vector 2
    xp = v1[0]*v2[1] - v1[1]*v2[0]

    if(xp > 0):
        return(-1)#print('left hand fold')
    elif(xp < 0):
        return(1)#print('right hand fold')
    else:
        return(0)#print('same line')

# evenize -> makes arrays even in size for rotation compatibility
def evenize(a2dlist):
    '''
    Input and output are 2D list.
    If number of rows or columns is not even, this function fixes it.
    Used to achieve bug free rotation
    '''
    i,j = len(a2dlist),len(a2dlist[0])
    if(i%2==0 and j%2==0):
        return(a2dlist)
    if(i%2!=0):
        # if number of rows (height) is not even
        min_index = [int(sum(_)) for _ in a2dlist].index(min([int(sum(_)) for _ in a2dlist]))
        del(a2dlist[min_index])
        ret=a2dlist
    if(j%2!=0):
        # if number of cols (width) is not even
        a = a2dlist.copy()
        x = np.array(a).T.tolist()
        min_index = int(min([sum(_) for _ in x]))
        del(x[min_index])
        ret = np.array(x).T.tolist()
    return(ret)

def imgTrim(canva):
    if("shapes" in str(type(canva))):
        canva=canva.shapeMatrix
    r=np.array(canva,dtype=int)
    res=np.where(r==1)
    top=min(res[1])
    bottom=max(res[1])
    right=max(res[0])
    left=min(res[0])
    rotated=r[left:right+1,top:bottom+1]
    rotated = np.array(rotated,dtype=int)
    return(rotated.tolist())

def singleFit(canvas,objectList):
    returnDict = {}
    if(type(objectList)!=type([])):
        objectList = [objectList]
    for obj in objectList :
        cl,cb = canvas.shapeFrameDimension
        chypotunes = (cl**2 + cb**2)**0.5
        ol,ob = obj.shapeFrameDimension
        if(ol > cl and ob > cb):
            returnDict[obj]=(False,False)
        elif (ol <= cl and ob <= cb):
            returnDict[obj]=(True,0)
        elif (ol <= cl and ob > cb and ob <= cl and ol <= cb) or (ol > cl and ob <= cb and ol <= cb and ob <= cl):
            returnDict[obj]=(True,90)
        else:
            returnDict[obj]=(False,False)
    return(returnDict,objectList)

def sortA5(shapeList):
    rectDict = {}
    categ2 = {}
    categ3 = {}
    crcle = {}
    for shape in shapeList:
        if(shape.myShape=="CutSheet"):
            rectDict[shape]=shape.length
        elif(shape.myShape=="cone" or shape.myShape=="sector"):
            categ2[shape] = shape.slantHeight if shape.myShape=="cone" else shape.radius
        elif(shape.myShape=="frustum" or shape.myShape=="segment"):
            categ3[shape] = shape.R
        else:
            crcle[shape] = shape.shapeFrameDimension[0]
    retli = list(dict(sorted(rectDict.items(), key=lambda item: item[1])))[::-1]
    retli += list(dict(sorted(categ2.items(), key=lambda item: item[1])))[::-1]
    retli += list(dict(sorted(categ3.items(), key=lambda item: item[1])))[::-1]
    retli += list(dict(sorted(crcle.items(), key=lambda item: item[1])))[::-1]
    return(retli)

def sortA6(shapeList):
    d={}
    for shape in shapeList:
        d[shape] = shape.shapeFrameDimension[0]
    return(list(dict(sorted(d.items(), key=lambda item: item[1])))[::-1])

def sortA7(shapeList):
    d={}
    for shape in shapeList:
        d[shape] = shape.a7compat
    return(list(dict(sorted(d.items(), key=lambda item: item[1])))[::-1])

def fitAll(canvas,objectList,returnSum=False):
    '''
    This is a theoretical calculation and can sometimes fail to give practical results
    '''
    if(type(objectList)!=type([])):
        objectList = [objectList]
    canvasArea = canvas.surfaceArea
    objectArea = sum([_.surfaceArea for _ in objectList])
    if(returnSum):
        return(True if canvasArea >= objectArea else False,objectArea)
    return(True if canvasArea >= objectArea else False)

def sortSurfaceArea(objectList):
    if(type(objectList)!=type([])):
        objectList = [objectList]
    ret = {}
    for obj in objectList:
        ret[obj] = obj.surfaceArea
    ret = dict(sorted(ret.items(),key = lambda item:item[1]))
    return(list(ret.keys())[::-1])

def sortEdgeCorners(objectList):
    if(type(objectList)!=type([])):
        objectList = [objectList]
    ret = {}
    for obj in objectList:
        ret[obj] = {"sa":obj.surfaceArea,"cc":obj.cornerCompatible}
    ret = dict(sorted(ret.items(),key = lambda item:item[1]["cc"]))
    return(list(ret.keys())[::-1])

def isInterfering(c):
    x = c.reshape(-1)
    x = x.tolist()
    if(sum(i>1 for i in x)>0):
        return(True)
    else:
        return(False)

def countShapes(shapeList,myShapeName):
    '''
    count the given type of shape in a given shapeList
    '''
    x = [_.myShape for _ in shapeList]
    return(x.count(myShapeName))

def countShapesProperties(shapeList,propertyValue):
    '''
    count the given type of shape in a given shapeList
    '''
    x = [_.a3compat for _ in shapeList]
    return(x.count(propertyValue))

def triangleSort(objectList):
    if(type(objectList)!=type([])):
        objectList = [objectList]
    ret = {}
    for obj in objectList:
        ret[obj] = {"sa":obj.surfaceArea,"cc":obj.triangleCompatible}
    ret = dict(sorted(ret.items(),key = lambda item:item[1]["cc"]))
    return(list(ret.keys()))

def typeToggle(li):
    retli=[]
    for _ in li:
        try:
            retli.append(float(_))
        except Exception as e:
            retli.append(_)
    return(retli)

def typeToggle2d(li):
    retli=[]
    for row in li:
        retli.append(typeToggle(row))
    return(retli)

def liCompress(li):
    retli = [[str(li[0]),1]]
    for i in range(1,len(li)):
        if(str(li[i])==(retli[-1])[0]):
            (retli[-1])[1]+=1
        else:
            retli.append([str(li[i]),1])
    return(retli)

def liDecompress(li):
    retli = []
    for subList in li:
        retli+=([subList[0]]*subList[1])
    return(typeToggle(retli))

def toggle2dArray(arr2d):
    '''
    Toggles row major 2D array to column major and vice-versa
    '''
    return(np.array(arr2d).T.tolist())

def npAnalyse(nparray,display=True):
    if(display):
        print(c.Counter((nparray.reshape(-1)).tolist()))
    else:
        return(c.Counter((nparray.reshape(-1)).tolist()))

def liAnalyse(li,display=True):
    nparray = np.array(li)
    if(display):
        print(c.Counter((nparray.reshape(-1)).tolist()))
    else:
        return(c.Counter((nparray.reshape(-1)).tolist()))

def outlineBugFixFunction(li2d):
    retli=[]
    for row in li2d:
        templi=[]
        for col in row:
            if(col==''):
                templi.append('0.7')
            else:
                templi.append(col)
        retli.append(templi)
    return(retli)

def binaryFilter(canvas):
    optionalShapeList=None
    if(type(canvas)==type((1,2,3))):
        canvas,optionalShapeList,up = canvas[0],canvas[1],canvas[2]
    a = np.array(canvas)
    a[a==1]=1
    a[a!=1]=0
    if(optionalShapeList!=None):
        return((np.array(a,int)).tolist(),optionalShapeList,up)
    return((np.array(a,int)).tolist())

def p2aBugFixFunction(li2d):
    retli=[]
    for row in li2d:
        templi=[]
        for col in row:
            if(str(col)=='1'):
                templi.append(1)
            else:
                templi.append(0)
        retli.append(templi)
    return(retli)

def freeSpace():
    os.system("python free_space.py")

def pushNotification(msg):
    os.system(f'cd ../../NodePortable && node.exe ../EPMA/pyprogs/mod.js "{msg}"')

def pushError(msg):
    os.system(f'cd ../../NodePortable && node.exe ../EPMA/pyprogs/exception.js "{msg}"')

def typeScaler(li,scale,kount=1,div=False):
    retli = []
    if(div):
        scale = 1/scale
    i = 0
    for _ in li:
        if(i>=kount):
            retli.append(_)
        else:
            try:
                retli.append(_*scale)
            except Exception as e:
                retli.append(_)
        i+=1
    return(retli)