import functions as func
import numpy as np
from math import ceil

def fitting(canvas,shapeList,col=True,log_=False,constCompute=False):
    cArray = np.array(canvas.shapeMatrix,dtype=float) #cArray => canvasArray
    cx,cy = np.shape(cArray)
    unplacedShapes=[]
    placedShapes=[]
    stepX = constCompute if constCompute else 1
    stepY = constCompute if constCompute else 1
    memoryX = 0
    memoryY = 0
    if(col==False):
        for shape in shapeList:
            sArray = np.array(shape.shapeMatrix,dtype=float)
            sx,sy = np.shape(sArray)
            newCanvas = np.copy(cArray)
            isObjectPlaced = False
            if(shape.cornerCompatible==1):
                for row in range(0,cx-sx,stepX):
                    col=0
                    if(row<memoryX and col<memoryY):
                        continue
                    newCanvas = np.copy(cArray)
                    newCanvas[row:row+sx,col:col+sy]+=sArray
                    if(func.isInterfering(newCanvas)):
                        pass
                    else:
                        isObjectPlaced=True
                        shape.low_res_pos = [round(row/cx*100,2),round(col/cy*100,2),0]
                        memoryX=row+(shape.diagonalSkipPercentage/100*sx)
                        memoryY=col+(shape.diagonalSkipPercentage/100*sy)
                        #print("row changes")
                        break
                if(isObjectPlaced==False):
                    for col in range(0,cy-sy,stepY):
                        row=0
                        if(row<memoryX and col<memoryY):
                            continue
                        newCanvas = np.copy(cArray)
                        newCanvas[row:row+sx,col:col+sy]+=sArray
                        if(func.isInterfering(newCanvas)):
                            pass
                        else:
                            isObjectPlaced=True
                            shape.low_res_pos = [round(row/cx*100,2),round(col/cy*100,2),0]
                            memoryX=row+(shape.diagonalSkipPercentage/100*sx)
                            memoryY=col+(shape.diagonalSkipPercentage/100*sy)
                            #print("col changes")
                            break
                if(isObjectPlaced==False):
                    for row in range(0,cx-sx,stepX):
                        doublebreak=False
                        for col in range(0,cy-sy,stepY):
                            if(row<memoryX and col<memoryY):
                                continue
                            newCanvas = np.copy(cArray)
                            newCanvas[row:row+sx,col:col+sy]+=sArray
                            if(func.isInterfering(newCanvas)):
                                pass
                            else:
                                isObjectPlaced=True
                                doublebreak=True
                                shape.low_res_pos = [round(row/cx*100,2),round(col/cy*100,2),0]
                                memoryX=row+(shape.diagonalSkipPercentage/100*sx)
                                memoryY=col+(shape.diagonalSkipPercentage/100*sy)
                                break
                        if(doublebreak==True):
                            break
            else:
                for row in range(0,cx-sx,stepX):
                    doublebreak=False
                    for col in range(0,cy-sy,stepY):
                        if(row<memoryX and col<memoryY):
                            continue
                        newCanvas = np.copy(cArray)
                        newCanvas[row:row+sx,col:col+sy]+=sArray
                        if(func.isInterfering(newCanvas)):
                            pass
                        else:
                            doublebreak=True
                            isObjectPlaced=True
                            shape.low_res_pos = [round(row/cx*100,2),round(col/cy*100,2),0]
                            memoryX=row+(shape.diagonalSkipPercentage/100*sx)
                            memoryY=col+(shape.diagonalSkipPercentage/100*sy)
                            break
                    if(doublebreak==True):
                        break
            if(log_ and isObjectPlaced):
                shape.placed=True
                placedShapes.append(shape)
                cArray = np.copy(newCanvas)
                print(f"Completed placing {shape.myShape}")
                func.pushNotification(f"Completed placing {shape.myShape}")
            else:
                unplacedShapes.append(shape)
                shape.placed=False
    else:
        for shape in shapeList:
            sArray = np.array(shape.shapeMatrix,dtype=float)
            sx,sy = np.shape(sArray)
            newCanvas = np.copy(cArray)
            isObjectPlaced = False
            if(shape.cornerCompatible==1):
                for row in range(0,cx-sx,stepX):
                    col=0
                    if(row<memoryX and col<memoryY):
                        continue
                    newCanvas = np.copy(cArray)
                    newCanvas[row:row+sx,col:col+sy]+=sArray
                    if(func.isInterfering(newCanvas)):
                        pass
                    else:
                        isObjectPlaced=True
                        shape.low_res_pos = [round(col/cy*100,2),round(row/cx*100,2),0]
                        memoryX=row+(shape.diagonalSkipPercentage/100*sx)
                        memoryY=col+(shape.diagonalSkipPercentage/100*sy)
                        #print("row changes")
                        break
                if(isObjectPlaced==False):
                    for col in range(0,cy-sy,stepY):
                        row=0
                        if(row<memoryX and col<memoryY):
                            continue
                        newCanvas = np.copy(cArray)
                        newCanvas[row:row+sx,col:col+sy]+=sArray
                        if(func.isInterfering(newCanvas)):
                            pass
                        else:
                            isObjectPlaced=True
                            shape.low_res_pos = [round(col/cy*100,2),round(row/cx*100,2),0]
                            memoryX=row+(shape.diagonalSkipPercentage/100*sx)
                            memoryY=col+(shape.diagonalSkipPercentage/100*sy)
                            #print("col changes")
                            break
                if(isObjectPlaced==False):
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
                                isObjectPlaced = True
                                shape.low_res_pos = [round(col/cy*100,2),round(row/cx*100,2),0]
                                memoryX=row+(shape.diagonalSkipPercentage/100*sx)
                                memoryY=col+(shape.diagonalSkipPercentage/100*sy)
                                break
                        if(doublebreak==True):
                            break
            else:
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
                            isObjectPlaced = True
                            shape.low_res_pos = [round(col/cy*100,2),round(row/cx*100,2),0]
                            memoryX=row+(shape.diagonalSkipPercentage/100*sx)
                            memoryY=col+(shape.diagonalSkipPercentage/100*sy)
                            break
                    if(doublebreak==True):
                        break
            if(log_ and isObjectPlaced):
                shape.placed=True
                placedShapes.append(shape)
                cArray = np.copy(newCanvas)
                print(f"Completed placing {shape.myShape}")
                func.pushNotification(f"Completed placing {shape.myShape}")
            else:
                unplacedShapes.append(shape)
                shape.placed=False
    ret = cArray.tolist()
    return(ret,placedShapes,unplacedShapes)

def run(canvas,shapeList,col=True,log_=False,constCompute=False,returnOrder=False):
    shapeList=func.sortEdgeCorners(shapeList)
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
    return(fitting(canvas,shapeList,col,log_,constCompute))