import os
try:
    import bs4
    import PIL
    import cv2
    import lxml
    import ezdxf
    os.environ['path'] += f';'+os.path.abspath("../../Inkscape/inkscape-1.1.1_2021-09-20_3bf5ae0d25-x64/idir/bin/")
    import cairosvg
    import matplotlib
    import numpy
    import cairo
except Exception as e:
    print(e)
    libraries = ["ezdxf","lxml","cairosvg","pillow","opencv-python","matplotlib","numpy","pycairo","beautifulsoup4"]
    for lib in libraries:
        os.system(f"python -m pip install {lib}")