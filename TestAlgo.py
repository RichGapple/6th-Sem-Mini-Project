from PIL import Image, ImageDraw

def shelf_first_fit(images, canvas_width, canvas_height, gap_size=3, padding=3):
    shelves = []
    current_shelf = []
    shelf_height = 0

    # Sort images in descending order based on height
    images = sorted(images, key=lambda x: x[1][1], reverse=True)

    for image, dimensions in images:import myPackman
from svgBuilder import svgPlacer,svgRotate
from shapeManager import *
from functions import *
import algorithm1,algorithm2,algorithm3,algorithm4,algorithm5,algorithm6
from visualization import *
import sys,shutil
from json import loads as jsonparser
import math
from winsound import Beep as beep
import konstants
from zipper import zipFiles

objList,cc=[],[]
thickness=[]
alg = []
canvas__=None

def RUN(jsonString):
    db = (jsonparser(jsonString))
    for objectkey in db:
        if("__data__" == objectkey):
            thickness .append( float((db["__data__"])["t"]) )
            try:
                alg .append( int((db["__data__"])["a"]) )
                konstants.svgScaleConstant = int(thickness[0]-1)
            except Exception as e:
                alg.append(5)
            cc .append( int((db["__data__"])["cc"]) )
            continue
        obj = db[objectkey]
        id_ = objectkey
        name_ = obj["shape_name"]
        dim_ = obj["dimensions"]
        _kount_ = obj["kount"]
        for _ in dim_:
            if(_ in ([chr(i) for i in range(65,91)]+[chr(i) for i in range(97,123)]+[":"])):
                dim_ = dim_.replace(_,"")
        dim_ = dim_.split(";")
        print(f"shape_name : {name_} ; id : {id_} ; dimensions : {dim_}")
        
        if(name_=="Canvas"):
            w,h,t = list(map(float,dim_))
            canvas__=Canvas(w,h)
            pushNotification("Canvas Created")
        elif(name_=="Cut-Sheet"):
            w,h = list(map(float,dim_))
            for _ in range(int(_kount_)):
                objList.append(CutSheet(w,h,0,id_+str(_)))
                pushNotification("Cut-Sheet Created")
        elif(name_=="Circle"):
            r = float(dim_[0])
            for _ in range(int(_kount_)):
                objList.append(Circle(r,id_+str(_)))
                pushNotification("Circle Created")
        elif(name_=="Cone"):
            h,r = list(map(float,dim_))
            for _ in range(int(_kount_)):
                objList.append(Cone(h,r,0,id_+str(_)))
                pushNotification("Cone Created")
        elif(name_=="Sector"):
            r,t = list(map(float,dim_))
            for _ in range(int(_kount_)):
                objList.append(Sector(r,t,0,id_+str(_)))
                pushNotification("Sector Created")
        elif(name_=="Frustum"):
            h,R,r = list(map(float,dim_))
            for _ in range(int(_kount_)):
                objList.append(Frustum(R,r,h,0,id_+str(_)))
                pushNotification("Frustum Created")
        elif(name_=="Segment"):
            R,r,t = list(map(float,dim_))
            for _ in range(int(_kount_)):
                objList.append(Segment(R,r,t,0,id_+str(_)))
                pushNotification("Segment Created")
        elif(name_.startswith("CUSTOM-")):
            count_ = int(obj["kount"])
            with open("./SVG/"+id_+"0.svg","r") as f:
                fd=f.read()
            for _ in range(count_):
                objList.append(Custom(fd,id_+str(_)))
                pushNotification("Custom Object Created")
        elif(name_=="Flange"):
            for _ in range(int(_kount_)):
                objList.append(Flange(obj["dimensions"],id_+str(_)))
                pushNotification("Flange Created")
    pushNotification("Object Creation Completed")

    print("algorithm:",alg[0])
    print("thickness:",thickness[0])
    for obj in objList:
        if(thickness[0]<6):
            obj.shapeMatrix = outline_with_shape(obj,int(thickness[0]//4)+1)
        else:
            obj.shapeMatrix = outline_with_shape(obj,int(thickness[0]//2+1)*2)
            print("else thickness executed")
    print("Starting low level algorithm")
    pushNotification("Starting low level positioning")
    if(alg[0] == 1):
        out,shapes,up = binaryFilter(algorithm1.run(canvas__,objList,log_=True,constCompute=cc[0],returnOrder=True))
    elif(alg[0] == 2):
        out,shapes,up = binaryFilter(algorithm2.run(canvas__,objList,log_=True,constCompute=cc[0],returnOrder=True))
    elif(alg[0] == 3):
        out,shapes,up = binaryFilter(algorithm3.run(canvas__,objList,log_=True,constCompute=cc[0],returnOrder=True))
    elif(alg[0] == 4):
        out,shapes,up = binaryFilter(algorithm4.run(canvas__,objList,log_=True,constCompute=cc[0],returnOrder=True))
    elif(alg[0] == 5):
        out,shapes,up = binaryFilter(algorithm5.run(canvas__,objList,log_=True,constCompute=cc[0],returnOrder=True))
    elif(alg[0] == 6):
        out,shapes,up = binaryFilter(algorithm6.run(canvas__,objList,log_=True,constCompute=cc[0],returnOrder=True))
    else:
        pushError("Invalid Algorithm")
        raise Exception("Invalid Algorithm")
    arr2png(out).save("./PNG/output_.png")
    pushNotification("Low level positioning completed")
    if(alg[0] in [3,5,6]):
        print("Starting svg rotation")
        pushNotification("Starting svg rotation")
        for shape in shapes:
            if(shape.placed==False):
                continue
            if(shape.angle==0 or shape.angle%360==0):
                continue
            svgRotate(shape.svgPath,shape.angle)
    print("Starting svg positioning")
    pushNotification("Starting SVG Positioning")
    xl,yl=[],[]
    cx,cy = canvas__.length,canvas__.height
    for shape in shapes:
        if shape.placed==False:
            continue
        print(shape.myShape,shape.low_res_pos)
        px , py , _ = shape.low_res_pos
        px,py = math.floor(px/100*cx),math.floor(py/100*cy)
        xl.append(px)
        yl.append(py)
    #svgPlacer(canvas__.svgPath,[_.svgPath for _ in shapes],xl,yl,thickness[0])
    print("\nUnplaced :")
    for _ in up:
        print(_,end="\n\n")
        shutil.move(_.svgPath,f"./unplaced/{_.uid}.svg")
    #os.system("python zipper.py")
    zipFiles()


if len(sys.argv)>1:
    RUN((sys.argv[1]).replace("^",'"'))

        width, height = dimensions

        if len(current_shelf) == 0 or shelf_height + height + gap_size <= canvas_height:
            current_shelf.append((image.copy(), (padding, shelf_height + padding)))
            shelf_height += height + gap_size
        else:
            shelves.append(current_shelf)
            current_shelf = [(image.copy(), (padding, padding))]
            shelf_height = height + gap_size

    if current_shelf:
        shelves.append(current_shelf)

    # Create the canvas image
    canvas = Image.new('RGB', (canvas_width, canvas_height), 'white')

    # Paste the images onto the canvas
    for shelf in shelves:
        for image, position in shelf:
            canvas.paste(image, position)

    return canvas

# Example usage
canvas_width = 500
canvas_height = 500

# List of tuples: (image, dimensions)
images = [
    (Image.open('output_rectangle.png'), (200, 100)),
    (Image.open('output_rectangle.png'), (200, 100)),
    (Image.open('output_rectangle.png'), (200, 100)),
    (Image.open('output_rectangle.png'), (200, 100)),
    (Image.open('output_rectangle.png'), (200, 100)),
    (Image.open('output_rectangle.png'), (200, 100)),
    # Add more images with their dimensions
]

result_canvas = shelf_first_fit(images, canvas_width, canvas_height)
result_canvas.save('output_canvas.png')
