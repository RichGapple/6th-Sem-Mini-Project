import os
import cairo
from numpy import pi, sqrt
import bs4 as bs
from math import cos,sin

def mm2pt(x):
    #surface.set_document_unit(7)
    return(x*2.83465)

def svgResize2Drawing(path):
    if("./" in path):
        pass
    else:
        if("/" in path):
            p = path[:path.rindex("/")+1]
            path = path[path.rindex("/")+1:]
        else:
            pass
    os.system(f'cd ../../Inkscape/inkscape-1.1.1_2021-09-20_3bf5ae0d25-x64/idir/bin/SVG && inkscape.exe --batch-process --actions="FitCanvasToDrawing;export-filename:{path};export-do;" {path}')

def svgRotate(path,angle):
    if("./" in path):
        pass
    else:
        if("/" in path):
            p = path[:path.rindex("/")+1]
            path = path[path.rindex("/")+1:]
        else:
            pass
    os.system(f'cd ../../Inkscape/inkscape-1.1.1_2021-09-20_3bf5ae0d25-x64/idir/bin/SVG && inkscape.exe --batch-process --actions="select-all:all;transform-rotate:{str(-angle)};FitCanvasToDrawing;export-filename:{path};export-do;" {path}')

def createCanvas(width,height,path):
    width = mm2pt(width)
    height = mm2pt(height)
    with cairo.SVGSurface(path, width,height) as surface:
        context = cairo.Context(surface)
        context.scale(700, 700)

def Rectangle(l,b,angle=0,filename=""):
    if(filename==""):
        raise Exception("Empty file name svgBuilder rectangle")
    l = mm2pt(l)
    b = mm2pt(b)
    with cairo.SVGSurface(filename,sqrt(l**2 + b**2) , sqrt(l**2+b**2)) as surface:
        cr = cairo.Context(surface)
        cr.rectangle(0,0,l,b)
        cr.fill()
    svgRotate(filename,angle)

def Circle(radius,filename):
    radius = mm2pt(radius)
    with cairo.SVGSurface(filename,2.5*radius , 2.5*radius) as surface:
        cr = cairo.Context(surface)
        theta1=0
        theta2=2*pi
        cr.arc(radius+2,radius+2,radius,theta1,theta2)
        cr.fill()
    svgResize2Drawing(filename) 

def Cone(height,radius,angle=0,filename=""):
    if(filename==""):
        raise Exception("Empty file name svgBuilder cone")
    radius = mm2pt(radius)
    height = mm2pt(height)
    l=sqrt(radius**2 + height**2)
    theta1=0
    theta2=(radius/l)*(2*pi)
    theta = (radius/l)*(2*180)
    with cairo.SVGSurface(filename,2.5*l,2.5*l) as surface:
        cr = cairo.Context(surface)
        cr.move_to(l+2,l+2)
        cr.arc(l+2,l+2,l,theta1,theta2)
        cr.close_path()
        cr.fill()
    svgRotate(filename,angle+theta/2+90)

def objectExtractor(path):
    with open(path,"r") as f:
        data = f.read()
    file = bs.BeautifulSoup(data, "lxml")
    g1 = file.find("g")
    return(str(g1))

def canvasExtracter(path):
    with open(path,"r") as f:
        data = f.read()
    file = bs.BeautifulSoup(data, "lxml")
    g1 = file.find("g")
    gMain = str(g1)
    half1=(data[:data.index("<g")+gMain.index(">")+1])
    half2=(data[data.index("<g")+gMain.index(">")+1:])
    return(half1,half2)

def svgPlacer(canvas,svgObjects,x,y,thickness):
    print("///////////////////////////////////////////////")
    print("///////////////////////////////////////////////")
    print("Test")
    print("///////////////////////////////////////////////")
    print("///////////////////////////////////////////////")
    prev_x,prev_y=None,None
    mfx,mfy=1,1
    movex,movey=1,1
    if(type(svgObjects)==type([])):
        if(not(len(svgObjects)==len(x)==len(y))):
            raise Exception("Unequal Array Length - SVGPLACER")
    else:
        x,y,svgObjects=[x],[y],[svgObjects]
    h1,h2=canvasExtracter(canvas)
    st=""
    print("///////////////////////////////////////////////")
    print("///////////////////////////////////////////////")
    print("output")
    print("///////////////////////////////////////////////")
    print("///////////////////////////////////////////////")
    for i,svg in enumerate(svgObjects):
        st+=f'<g id="{str(i)}" transform="translate({mm2pt(x[i])},{mm2pt(y[i])})">'+objectExtractor(svg)+"</g>"
        '''
        if(i!=0 and x[i]!=prev_x and y[i]!=prev_y):
            print(x[i],prev_x,"\n",y[i],prev_y,"\nif 1")
            mfx+=1
            mfy+=1
            movex=1/mfx
            movey=1/mfy
        elif(i!=0 and x[i]==prev_x and y[i]!=prev_y):
            print(x[i],prev_x,"\n",y[i],prev_y,"\nif 2")
            mfx+=0
            mfy+=1
            movex=0
            movey=1/mfy
        elif(i!=0 and x[i]!=prev_x and y[i]==prev_y):
            print(x[i],prev_x,"\n",y[i],prev_y,"\nif 3")
            mfx+=0
            mfy+=1
            movex=1/mfx
            movey=0
        elif(1==0):
            mfx,mfy=1,1
        print("-------")
        st+=f'<g id="{str(i)}" transform="translate({mm2pt(x[i])+(mm2pt(thickness)*(mfx*movex))},{mm2pt(y[i])+(mm2pt(thickness)*(mfy*movey))})">'+objectExtractor(svg)+"</g>"
        prev_x,prev_y = x[i],y[i]
        '''
    output = h1+st+h2
    print("///////////////////////////////////////////////")
    print("///////////////////////////////////////////////")
    print(output)
    print("///////////////////////////////////////////////")
    print("///////////////////////////////////////////////")

    with open(canvas,"w") as f:
        f.write(output)

def Sector(radius,sector_angle,angle=0,filename=""):
    if(filename==""):
        raise Exception("Empty file name svgBuilder Sector")
    l=mm2pt(radius)
    sector_angle=sector_angle*pi/180
    with cairo.SVGSurface(filename,2.5*l,2.5*l) as surface:
        cr = cairo.Context(surface)
        cr.move_to(l+2,l+2)
        cr.arc(l+2,l+2,l,0,sector_angle)
        cr.close_path()
        cr.fill()
    if(angle==0):
        if(sector_angle<=180):
            svgRotate(filename,angle+90+(sector_angle/2*(180/pi)))
    else:
        svgRotate(filename,angle)

def Frustum(R,r,h,angle=0,filename=""):
    if(filename==""):
        raise Exception("Empty file name svgBuilder frustum")
    R=mm2pt(R)
    r=mm2pt(r)
    h=mm2pt(h)
    t=sqrt(h**2 + (R-r)**2)
    L=t*R/(R-r)
    theta=(R/L)*(2*pi)
    trot = (R/L)*(2*180)
    l=L-t
    with cairo.SVGSurface(filename,2.5*L,2.5*L) as surface:
        cr = cairo.Context(surface)
        X1,Y1=xy(L,0,L,L)
        X2,Y2=xy(L,theta,L,L)
        x2,y2=xy(l,theta,L,L)
        x1,y1=xy(l,0,L,L)
        cr.arc(L,L,L,0,theta)
        cr.line_to(x2,y2)
        cr.arc_negative(L,L,l,theta,0)
        cr.line_to(X1,Y1)
        cr.set_line_width(0.2)
        cr.stroke_preserve()
        cr.fill()
    if(angle==0):
        svgRotate(filename,(trot/2)+90)
    else:
        svgRotate(filename,angle)

def xy(r,theta,centre_x,centre_y):
      X=centre_x + r* cos(theta)
      Y=centre_y + r*sin(theta)
      return X,Y

def Segment(R,r,segment_angle,angle=0,filename=""):
    if(filename==""):
        raise Exception("Empty file name svgBuilder segment")
    R=mm2pt(R)
    r=mm2pt(r)
    theta=segment_angle*pi/180
    trot=segment_angle
    with cairo.SVGSurface(filename,2.5*R,2.5*R) as surface:
        cr = cairo.Context(surface)
        X1,Y1=xy(R,0,R,R)
        X2,Y2=xy(R,theta,R,R)
        x2,y2=xy(r,theta,R,R)
        x1,y1=xy(r,0,R,R)
        cr.arc(R,R,R,0,theta)
        cr.line_to(x2,y2)
        cr.arc_negative(R,R,r,theta,0)
        cr.line_to(X1,Y1)
        cr.set_line_width(0.2)
        cr.stroke_preserve()
        cr.fill()
    if(angle==0):
        svgRotate(filename,(trot/2)+90)
    else:
        svgRotate(filename,angle)