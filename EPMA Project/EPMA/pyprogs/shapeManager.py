from functions import *
from math import sin,cos,radians,pi
from visualization import arr2png, png2arr,rotate,s2p,showPNG,tranparencyFilter
from random import randint as ri
import svgBuilder
from shutil import copyfile
import konstants

class CutSheet:
    '''
    Give side in milli-meter( mm ) and angle in degrees( ° )
    '''
    def __init__(self,length,height,angle,uid):
        self.params = [length,height,angle,uid]
        self.uid = uid
        self.a3compat=False
        self.myShape="CutSheet"
        self.length = length
        self.height = height
        self.surfaceArea = length*height
        self.angle = 0
        self.cornerCompatible = 1
        self.triangleCompatible = 0
        self.a7compat=0
        self.diagonalSkipPercentage = 100
        self.pngPath = f"./PNG/{uid}.png"
        self.svgPath = f"./SVG/{uid}.svg"
        self.__generateShape__(length,height,angle)

    def __repr__(self):
        return(f"Object Shape \t: {self.myShape}\nObject UID \t: {self.uid}\nSide Length \t: {self.length} mm\nSide Height \t: {self.height} mm\nShape Tilt \t: {self.angle} °\nshapeFrameDimension \t: {self.shapeFrameDimension}")
    
    def print(self):
        '''
        Prints Object parameters to console
        '''
        print(repr(self))

    def tilt(self,angle):
        self.angle += angle
        self.shapeMatrix=rotate(evenize(self.shapeMatrix),angle)
        self.shapeFrameDimension = [len(self.shapeMatrix[0]),len(self.shapeMatrix)]

    def displayShape(self):
        '''
        Displays shape as a image
        '''
        (arr2png(self.shapeMatrix)).show()

    def printShape(self):
        '''
        Prints shape to console in binary 

        #### Warning : CPU intensive task
        '''
        temp = ""
        for li in self.shapeMatrix:
            for num in li:
                temp+=str(num)
            temp+="\n"
        print(temp)

    def __generateShape__(self,length,height,angle):
        '''
        Generates 2D binary shape matrix
        '''
        self.dimensions=[length,height,angle,'mm,mm,°']
        svgBuilder.Rectangle(length,height,angle,self.svgPath)
        s2p(self.svgPath,self.pngPath,konstants.svgScaleConstant)
        tranparencyFilter(self.pngPath)
        self.shapeMatrix = p2aBugFixFunction(png2arr(self.pngPath))
        self.shapeFrameDimension=list(np.shape(self.shapeMatrix))

class Circle:
    '''
    Give radius in milli-meter( mm )
    '''
    def __init__(self,radius,uid):
        self.params = [radius,uid]
        self.uid = uid
        self.myShape="Circle"
        self.angle=0
        self.a3compat=False
        self.a7compat=9999
        self.radius = radius
        self.cornerCompatible = 0
        self.triangleCompatible = 1
        self.surfaceArea = pi*radius*radius
        self.diagonalSkipPercentage = 71
        self.pngPath = f"./PNG/{uid}.png"
        self.svgPath = f"./SVG/{uid}.svg"
        self.__generateShapeMatrix__(radius)

    def __repr__(self):
        return(f"Object Shape \t: {self.myShape}\nObject UID \t: {self.uid}\nShape Radius \t: {self.radius} mm\nshapeFrameDimension \t: {self.shapeFrameDimension}")
    
    def print(self):
        '''
        Prints Object parameters to console
        '''
        print(repr(self))

    def tilt(self,angle):
        _=angle
        pass

    def printShape(self):
        '''
        Prints shape to console in binary 

        #### Warning : CPU intensive task
        '''
        temp = ""
        for li in self.shapeMatrix:
            for num in li:
                temp+=str(num)
            temp+="\n"
        print(temp)

    def displayShape(self):
        '''
        Displays shape as a image
        '''
        (arr2png(self.shapeMatrix)).show()
    
    def isPointInCircle(self,ptX,ptY,radius):
        if( (ptX-radius)**2 + (ptY-radius)**2 <= radius**2 ):
            return(True)
        else:
            return(False)

    def __generateShapeMatrix__(self,radius):
        '''
        Generates 2D binary shape matrix
        '''
        self.dimensions=[self.radius,'mm']
        svgBuilder.Circle(radius,self.svgPath)
        s2p(self.svgPath,self.pngPath,konstants.svgScaleConstant)
        tranparencyFilter(self.pngPath)
        self.shapeMatrix = p2aBugFixFunction(png2arr(self.pngPath))
        self.shapeFrameDimension=list(np.shape(self.shapeMatrix))

class Cone:
    '''
    Give cone-height & cone-radius in milli-meter( mm )
    '''
    def __init__(self,cone_height,cone_radius,angle,uid):
        self.params = [cone_height,cone_radius,angle,uid]
        self.uid = uid
        self.pngPath = f"./PNG/{uid}.png"
        self.svgPath = f"./SVG/{uid}.svg"
        self.myShape="cone"
        self.a3compat=True
        self.a7compat=8888
        self.angle = 0
        self.cone_radius = round(cone_radius)
        self.cone_height = round(cone_height)
        self.slantHeight = round((cone_radius**2 + cone_height**2)**0.5)
        self.theta = 2*180*cone_radius/self.slantHeight
        self.surfaceArea = pi*(self.slantHeight**2)*self.theta/360
        self.cornerCompatible = 0
        self.flatAngle = ((180 - self.theta)/2)+self.theta
        self.diagonalSkipPercentage = 71
        #print('theta = ',self.theta)
        if(self.theta>=360):
            pushError("Illegal Cone Dimensions")
            raise Exception("Illegal cone dimensions.")
            return(0)
        self.cone_type = 1 if self.theta<=180 else 2
        self.triangleCompatible = 3 if self.cone_type==1 else 2
        self.__generateShapeMatrix__(cone_height,cone_radius,angle)

    def __repr__(self):
        return(f"Object Shape \t: {self.myShape}\nObject UID \t: {self.uid}\nShape Radius \t: {self.cone_radius} mm\nShape Height \t: {self.cone_height} mm\nshapeFrameDimension \t: {self.shapeFrameDimension}")
    
    def tilt(self,angle):
        self.angle += angle
        self.shapeMatrix=rotate(evenize(self.shapeMatrix),angle)
        self.shapeFrameDimension = [len(self.shapeMatrix[0]),len(self.shapeMatrix)]

    def flaTilt(self,direction=1):
        self.shapeMatrix = evenize(self.shapeMatrix)
        if(self.cone_type==1):
            self.tilt((direction/abs(direction))*self.flatAngle)
        else:
            self.tilt(180)

    def print(self):
        '''
        Prints Object parameters to console
        '''
        print(repr(self))

    def printShape(self):
        '''
        Prints shape to console in binary 

        #### Warning : CPU intensive task
        '''
        temp = ""
        for li in self.shapeMatrix:
            for num in li:
                temp+=str(num)
            temp+="\n"
        print(temp)

    def displayShape(self):
        '''
        Displays shape as a image
        '''
        (arr2png(self.shapeMatrix)).show()
    
    def isPointInCircle(self,ptX,ptY,radius):
        if( (ptX-radius)**2 + (ptY-(self.width))**2 <= radius**2 ):
            return(True)
        else:
            return(False)

    def __generateShapeMatrix__(self,height,radius,angle):
        '''
        Generates 2D binary shape matrix
        '''
        self.dimensions=[height,radius,angle,'mm,mm,°']     # only angle of dimension changes on tilting
        svgBuilder.Cone(height,radius,angle,self.svgPath)
        s2p(self.svgPath,self.pngPath,konstants.svgScaleConstant)
        tranparencyFilter(self.pngPath)
        self.shapeMatrix = p2aBugFixFunction(png2arr(self.pngPath))
        self.shapeFrameDimension=list(np.shape(self.shapeMatrix))

class Sector:
    '''
    Give sector radius & sector-angle in milli-meter( mm )
    '''
    def __init__(self,sector_radius,sector_angle,angle,uid):
        self.params = [sector_radius,sector_angle,angle,uid]
        self.uid = uid
        self.pngPath = f"./PNG/{uid}.png"
        self.svgPath = f"./SVG/{uid}.svg"
        self.myShape="sector"
        self.a3compat=True
        self.a7compat=7777
        self.radius = sector_radius
        self.sector_angle = sector_angle
        self.theta = sector_angle
        self.angle = 0
        self.surfaceArea = pi*(sector_radius**2)*sector_angle/360
        self.cornerCompatible = 0
        self.diagonalSkipPercentage = 71
        self.flatAngle = ((180 - self.theta)/2)+self.theta
        self.triangleCompatible = 3
        self.__generateShapeMatrix__(sector_radius,sector_angle,angle)

    def __repr__(self):
        return(f"Object Shape \t: {self.myShape}\nObject UID \t: {self.uid}\nShape Sector Radius \t: {self.radius} mm\nShape Sector Angle \t: {self.sector_angle} mm\nshapeFrameDimension \t: {self.shapeFrameDimension}")
    
    def tilt(self,angle):
        self.angle += angle
        self.shapeMatrix=rotate(evenize(self.shapeMatrix),angle)
        self.shapeFrameDimension = [len(self.shapeMatrix[0]),len(self.shapeMatrix)]

    def flaTilt(self,direction=1):
        if(self.theta<180):
            self.tilt((direction/abs(direction))*self.flatAngle)
        else:
            self.tilt(180)

    def print(self):
        '''
        Prints Object parameters to console
        '''
        print(repr(self))

    def printShape(self):
        '''
        Prints shape to console in binary 

        #### Warning : CPU intensive task
        '''
        temp = ""
        for li in self.shapeMatrix:
            for num in li:
                temp+=str(num)
            temp+="\n"
        print(temp)

    def displayShape(self):
        '''
        Displays shape as a image
        '''
        (arr2png(self.shapeMatrix)).show()
    
    def isPointInCircle(self,ptX,ptY,radius):
        if( (ptX-radius)**2 + (ptY-(self.width))**2 <= radius**2 ):
            return(True)
        else:
            return(False)

    def __generateShapeMatrix__(self,rad,sec_angle,angle):
        '''
        Generates 2D binary shape matrix
        '''
        svgBuilder.Sector(rad,sec_angle,angle,self.svgPath)
        s2p(self.svgPath,self.pngPath,konstants.svgScaleConstant)
        tranparencyFilter(self.pngPath)
        self.shapeMatrix = p2aBugFixFunction(png2arr(self.pngPath))
        self.shapeFrameDimension=list(np.shape(self.shapeMatrix))

class Frustum:
    '''
    Give sector radius & sector-angle in milli-meter( mm )
    '''
    def __init__(self,R,r,h,angle,uid):
        self.params = [R,r,h,angle,uid]
        self.uid = uid
        self.pngPath = f"./PNG/{uid}.png"
        self.svgPath = f"./SVG/{uid}.svg"
        self.myShape="frustum"
        self.a3compat=True
        self.a7compat=7777
        self.R = R
        self.r = r
        self.h = h
        self.H = abs(h*(1-(r/(r-R))))
        l = (h**2 + (R-r)**2)**0.5
        self.angle = 0
        self.surfaceArea = pi*l*(R+r)
        self.cornerCompatible = 0
        self.flatAngle = 180
        self.triangleCompatible = 2
        self.diagonalSkipPercentage = 71
        self.__generateShapeMatrix__(R,r,h,angle)

    def __repr__(self):
        return(f"Object Shape \t: {self.myShape}\nObject UID \t: {self.uid}\nshapeFrameDimension \t: {self.shapeFrameDimension}")
    
    def tilt(self,angle):
        self.angle += angle
        self.shapeMatrix=rotate(evenize(self.shapeMatrix),angle)
        self.shapeFrameDimension = [len(self.shapeMatrix[0]),len(self.shapeMatrix)]

    def flaTilt(self,direction=1):
        self.shapeMatrix = evenize(self.shapeMatrix)
        self.tilt(180)

    def print(self):
        '''
        Prints Object parameters to console
        '''
        print(repr(self))

    def printShape(self):
        '''
        Prints shape to console in binary 

        #### Warning : CPU intensive task
        '''
        temp = ""
        for li in self.shapeMatrix:
            for num in li:
                temp+=str(num)
            temp+="\n"
        print(temp)

    def displayShape(self):
        '''
        Displays shape as a image
        '''
        (arr2png(self.shapeMatrix)).show()
    
    def isPointInCircle(self,ptX,ptY,radius):
        if( (ptX-radius)**2 + (ptY-(self.width))**2 <= radius**2 ):
            return(True)
        else:
            return(False)

    def __generateShapeMatrix__(self,R,r,h,angle):
        '''
        Generates 2D binary shape matrix
        '''
        svgBuilder.Frustum(R,r,h,angle,self.svgPath)
        s2p(self.svgPath,self.pngPath,konstants.svgScaleConstant)
        tranparencyFilter(self.pngPath)
        self.shapeMatrix = p2aBugFixFunction(png2arr(self.pngPath))
        self.shapeFrameDimension=list(np.shape(self.shapeMatrix))

class Segment:
    '''
    Give sector radius & sector-angle in milli-meter( mm )
    '''
    def __init__(self,R,r,t,angle,uid):
        self.params = [R,r,t,angle,uid]
        self.uid = uid
        self.pngPath = f"./PNG/{uid}.png"
        self.svgPath = f"./SVG/{uid}.svg"
        self.myShape="segment"
        self.a3compat=True
        self.a7compat=6666
        self.R = R
        self.r = r
        self.t = t
        self.angle = 0
        self.surfaceArea = pi*(t/360)*(R**2-r**2)
        self.cornerCompatible = 0
        self.flatAngle = 180
        self.triangleCompatible = 2
        self.diagonalSkipPercentage = 71
        self.__generateShapeMatrix__(R,r,t,angle)

    def __repr__(self):
        return(f"Object Shape \t: {self.myShape}\nObject UID \t: {self.uid}\nshapeFrameDimension \t: {self.shapeFrameDimension}")
    
    def tilt(self,angle):
        self.angle += angle
        self.shapeMatrix=rotate(evenize(self.shapeMatrix),angle)
        self.shapeFrameDimension = [len(self.shapeMatrix[0]),len(self.shapeMatrix)]

    def flaTilt(self,direction=1):
        self.shapeMatrix = evenize(self.shapeMatrix)
        self.tilt(180)

    def print(self):
        '''
        Prints Object parameters to console
        '''
        print(repr(self))

    def printShape(self):
        '''
        Prints shape to console in binary 

        #### Warning : CPU intensive task
        '''
        temp = ""
        for li in self.shapeMatrix:
            for num in li:
                temp+=str(num)
            temp+="\n"
        print(temp)

    def displayShape(self):
        '''
        Displays shape as a image
        '''
        (arr2png(self.shapeMatrix)).show()
    
    def isPointInCircle(self,ptX,ptY,radius):
        if( (ptX-radius)**2 + (ptY-(self.width))**2 <= radius**2 ):
            return(True)
        else:
            return(False)

    def __generateShapeMatrix__(self,R,r,t,angle):
        '''
        Generates 2D binary shape matrix
        '''
        svgBuilder.Segment(R,r,t,angle,self.svgPath)
        s2p(self.svgPath,self.pngPath,konstants.svgScaleConstant)
        tranparencyFilter(self.pngPath)
        self.shapeMatrix = p2aBugFixFunction(png2arr(self.pngPath))
        self.shapeFrameDimension=list(np.shape(self.shapeMatrix))

class Canvas:
    '''
    Give side in milli-meter( mm )
    '''
    def __init__(self,length,height):
        self.params = [length,height]
        self.uid = "Canvas"
        self.myShape="Canvas"
        self.a3compat=False
        self.length = length
        self.height = height
        self.surfaceArea = length*height
        self.diagonalSkipPercentage = 100
        self.pngPath = f"./PNG/{self.uid}.png"
        self.svgPath = f"./SVG/{self.uid}.svg"
        self.__generateShape__(length,height)

    def __repr__(self):
        return(f"Object Shape \t: {self.myShape}\nObject UID \t: {self.uid}\nSide Length \t: {self.length} mm\nSide Height \t: {self.height} mm\nshapeFrameDimension \t: {self.shapeFrameDimension}")
    
    def print(self):
        '''
        Prints Object parameters to console
        '''
        print(repr(self))

    def displayShape(self):
        '''
        Displays shape as a image
        '''
        (arr2png(self.shapeMatrix)).show()

    def printShape(self):
        '''
        Prints shape to console in binary 

        #### Warning : CPU intensive task
        '''
        temp = ""
        for li in self.shapeMatrix:
            for num in li:
                temp+=str(num)
            temp+="\n"
        print(temp)

    def __generateShape__(self,length,height):
        '''
        Generates 2D binary shape matrix
        '''
        self.dimensions=[length,height,'mm,mm']
        svgBuilder.createCanvas(length,height,self.svgPath)
        s2p(self.svgPath,self.pngPath,konstants.svgScaleConstant)
        tranparencyFilter(self.pngPath)
        self.shapeMatrix = p2aBugFixFunction(png2arr(self.pngPath))
        self.shapeFrameDimension=list(np.shape(self.shapeMatrix))

class Custom:
    '''
    Give side in milli-meter( mm )
    '''
    def __init__(self,filecontents,uid):
        self.params = [filecontents,uid]
        self.uid = uid
        self.myShape="Custom"
        self.a3compat=True
        self.a7compat=0
        self.fileContents = filecontents
        self.angle = 0
        self.pngPath = f"./PNG/{self.uid}.png"
        self.svgPath = f"./SVG/{self.uid}.svg"
        self.__generateShape__()
        self.cornerCompatible=-1
        self.triangleCompatible=-1
        self.flatAngle = 0
        self.diagonalSkipPercentage = 71

    def __repr__(self):
        return(f"Object Shape \t: {self.myShape}\nObject UID \t: {self.uid}\nShape Tilt \t: {self.angle} °\nshapeFrameDimension \t: {self.shapeFrameDimension}")
    
    def print(self):
        '''
        Prints Object parameters to console
        '''
        print(repr(self))

    def tilt(self,angle):
        self.angle += angle
        self.shapeMatrix=rotate(evenize(self.shapeMatrix),angle)
        self.shapeFrameDimension = [len(self.shapeMatrix[0]),len(self.shapeMatrix)]

    def flaTilt(self,direction=1):
        pass

    def displayShape(self):
        '''
        Displays shape as a image
        '''
        (arr2png(self.shapeMatrix)).show()

    def printShape(self):
        '''
        Prints shape to console in binary 

        #### Warning : CPU intensive task
        '''
        temp = ""
        for li in self.shapeMatrix:
            for num in li:
                temp+=str(num)
            temp+="\n"
        print(temp)

    def __generateShape__(self):
        '''
        Generates 2D binary shape matrix
        '''
        #with open(self.svgPath,"w") as f:
        #    f.write(fc)
        s2p(self.svgPath,self.pngPath,konstants.svgScaleConstant)
        tranparencyFilter(self.pngPath)
        self.shapeMatrix = p2aBugFixFunction(png2arr(self.pngPath))
        self.shapeFrameDimension=list(np.shape(self.shapeMatrix))
        self.surfaceArea = self.shapeFrameDimension[0]*self.shapeFrameDimension[1]

class Flange:
    '''
    Give side in milli-meter( mm )
    '''
    def __init__(self,namestring,uid):
        self.params = [namestring,uid]
        self.uid = uid
        self.namestring = namestring
        self.myShape="flange"
        self.a3compat=False
        self.a7compat=9999
        self.angle = 0
        self.pngPath = f"./PNG/{self.uid}.png"
        self.svgPath = f"./SVG/{self.uid}.svg"
        self.__generateShape__()
        self.cornerCompatible=-1
        self.triangleCompatible=-1
        self.flatAngle = 0
        self.diagonalSkipPercentage = 71

    def __repr__(self):
        return(f"Object Shape \t: {self.myShape}\nObject UID \t: {self.uid}\nShape Tilt \t: {self.angle} °\nshapeFrameDimension \t: {self.shapeFrameDimension}")
    
    def print(self):
        '''
        Prints Object parameters to console
        '''
        print(repr(self))

    def tilt(self,angle):
        pass

    def flaTilt(self,direction=1):
        pass

    def displayShape(self):
        '''
        Displays shape as a image
        '''
        (arr2png(self.shapeMatrix)).show()

    def printShape(self):
        '''
        Prints shape to console in binary 

        #### Warning : CPU intensive task
        '''
        temp = ""
        for li in self.shapeMatrix:
            for num in li:
                temp+=str(num)
            temp+="\n"
        print(temp)

    def __generateShape__(self):
        '''
        Generates 2D binary shape matrix
        type:tbee_95_6
        '''
        x = self.namestring
        self.category,self.od,self.thickness = (x[x.index(":")+1:]).split("_")
        actPath = os.getcwd()
        referenceFlangePath = "./Flanges_Library/"
        if(self.category=="tbee"):
            referenceFlangePath+="Table_E/"
        elif(self.category=="c150"):
            referenceFlangePath+="Class_150/"
        elif(self.category=="pn16"):
            referenceFlangePath+="PN_16/"
        os.chdir(referenceFlangePath)
        files = os.listdir()
        for file in files:
            if(file.startswith(self.od) and file.endswith(self.thickness+".svg")):
                referenceFlangePath+=file
                self.referenceFileName = file
        os.chdir(actPath)
        copyfile(referenceFlangePath,f"./SVG/{self.uid}.svg")
        #common stuff below
        s2p(self.svgPath,self.pngPath,konstants.svgScaleConstant)
        tranparencyFilter(self.pngPath)
        self.shapeMatrix = p2aBugFixFunction(png2arr(self.pngPath))
        self.shapeFrameDimension=list(np.shape(self.shapeMatrix))
        self.surfaceArea = int(pi*((int(self.od)/2)**2))