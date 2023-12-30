import functions as func
from math import ceil
import numpy as np

def fitting(canvas,shapeList,log_=False,constCompute=False):
    cArray = np.array(canvas.shapeMatrix,dtype=float) #cArray => canvasArray
    cx,cy = np.shape(cArray)
    stepX = constCompute if constCompute else 1
    stepY = constCompute if constCompute else 1
    memoryX = 0
    memoryY = 0
    unplacedShapes=[]
    placedShapes=[]
    for shape in shapeList:
        sArray = np.array(shape.shapeMatrix,dtype=float)
        sx,sy = np.shape(sArray)
        newCanvas = np.copy(cArray)
        isObjectPlaced=False
        for col in range(0,cy-sy,stepY):
            row=0
            newCanvas = np.copy(cArray)
            newCanvas[row:row+sx,col:col+sy]+=sArray
            if(func.isInterfering(newCanvas)):
                pass
            else:
                isObjectPlaced=True
                shape.low_res_pos = [round(col/cy*100,2),round(row/cx*100,2),0]
                #print("choice 2")
                break
        if(isObjectPlaced==False):
            if(shape.a3compat==True):
                shape.tilt(90)
            sArray = np.array(shape.shapeMatrix,dtype=float)
            sx,sy = np.shape(sArray)
            for row in range(0,cx-sx,stepX):
                col=0
                newCanvas = np.copy(cArray)
                newCanvas[row:row+sx,col:col+sy]+=sArray
                if(func.isInterfering(newCanvas)):
                    pass
                else:
                    isObjectPlaced=True
                    shape.low_res_pos = [round(col/cy*100,2),round(row/cx*100,2),0]
                    #print("choice 1")
                    break
        if(isObjectPlaced==False):
            if(shape.a3compat==True):
                shape.tilt(180)
            sArray = np.array(shape.shapeMatrix,dtype=float)
            sx,sy = np.shape(sArray)
            for row in range(0,cx-sx,stepX):
                col=cy-sy
                newCanvas = np.copy(cArray)
                newCanvas[row:row+sx,col:col+sy]+=sArray
                if(func.isInterfering(newCanvas)):
                    pass
                else:
                    isObjectPlaced=True
                    shape.low_res_pos = [round(col/cy*100,2),round(row/cx*100,2),0]
                    #print("choice 3")
                    break
        if(isObjectPlaced==False):
            if(shape.a3compat==True):
                shape.tilt(-90)
            sArray = np.array(shape.shapeMatrix,dtype=float)
            sx,sy = np.shape(sArray)
            for col in range(0,cy-sy,stepY):
                row=cx-sx
                newCanvas = np.copy(cArray)
                newCanvas[row:row+sx,col:col+sy]+=sArray
                if(func.isInterfering(newCanvas)):
                    pass
                else:
                    isObjectPlaced=True
                    shape.low_res_pos = [round(col/cy*100,2),round(row/cx*100,2),0]
                    #print("choice 4")
                    break
        if(isObjectPlaced==False):
            if(shape.a3compat==True):
                shape.tilt(180)
            sArray = np.array(shape.shapeMatrix,dtype=float)
            sx,sy = np.shape(sArray)
            for col in range(0,cy-sy,stepY):
                doublebreak=False
                for row in range(0,cx-sx,stepX):
                    if(row<memoryX and col<memoryY):
                        continue
                    newCanvas = np.copy(cArray)
                    newCanvas[row:row+sx,col:col+sy]+=sArray
                    if(func.isInterfering(newCanvas)):
                        pass
                    else:
                        doublebreak=True
                        isObjectPlaced=True
                        shape.low_res_pos = [round(col/cy*100,2),round(row/cx*100,2),0]
                        memoryX=row+(shape.diagonalSkipPercentage/100*sx)
                        memoryY=col+(shape.diagonalSkipPercentage/100*sy)
                        break
                if(doublebreak==True):
                    break
        if(log_ and isObjectPlaced):
            print(f"Completed placing {shape.myShape}")
            func.pushNotification(f"Completed placing {shape.myShape}")
            shape.placed=True
            placedShapes.append(shape)
            cArray = np.copy(newCanvas)
        else:
            unplacedShapes.append(shape)
            shape.placed=False
    ret = cArray.tolist()
    return(ret,placedShapes,unplacedShapes)

def run(canvas,shapeList,log_=False,constCompute=False,returnOrder=False):
    shapeList=func.triangleSort(shapeList)
    d,_=func.singleFit(canvas,shapeList)
    l1 = [d[_][0] for _ in d]
    try:
        if(all(l1)==False):
            tooLarge=[]
            for _ in shapeList:
                if(d[_.uid][0]==False):
                    tooLarge.append((_.uid,_.myShape,_.dimensions))
    except Exception as e:
        func.pushError(f"* shapes are too large to fit the given canvas...")
        raise Exception(f"{tooLarge} shapes are too large to fit the given canvas...")
    # If program passes till here, 
    # All the given shapes can individually fit in the given canvas.
    if(func.fitAll(canvas,shapeList)==False):
        func.pushError(f"Fitting all shapes in the given canvas is mathematically impossible.")
        #raise Exception(f"Fitting all shapes in the given canvas is mathematically impossible.")
    # If program passes till here,
    # All the given shapes can be theoretically arranged in the canvas. Practically, I doubt it
    #print(d)
    for shape in shapeList:
        if(shape.a3compat):
            shape.flaTilt(1)
    return(fitting(canvas,shapeList,log_,constCompute))