Welcome to our little hell hole. This is an unfinised project where god only knows when will it get finished, To get started

EPMA\front-end  --> frontend code

EPMA\pyprogs    --> core python program files which contain all algos and libraries

EPMA\pyprogs\myPackman.py -->  import/installs all the python dependencies to your setup 

EPMA.py --> this file automatically runs the above file and starts the server

EPMA\Pendrive\Inkscape   --> Inkscape software used for png to svg conversion

EPMA\Pendrive\NodePortable  --> Node JS software for running backend server

Main issues:-
1) PNG Created has too much whitespace boarder (Fixed)
2) Algorithm efficiency takes a toll due to that useless white boundary (Found out to be not true, Need to figure out the root cause still) -> Proved False
3) Tried giving 5 images(W/O White boarder) to be sorted, Program froze/Program takes too long to run indicating issues somewhere in the code
4) The error about shapeFrameDimension has been fixed and the issue of image showing out of bounds does not occur anymore
5) Found a new major issue in algorithm that the canvas array (cArray) when being initiliazed from canvas.shapeMatrix is what's changing the size of the canvas and as far as i can tell this is the final major issue to be resolved
6) The same issue is with the shapes as well, when creating shape array (sArray) from shape.shapeMatix the matrix conversion is what's causing the issue, if the array can be fixed i believe the algorithms will be fixed
7) Now this is just a guess but i believe that the Matrix values are being derived from the SVG file as SVG files get created first and then the PNG files get created

Thanks for letting me rant
~Goodbye, Vishal
