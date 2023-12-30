from zipfile import ZipFile
import os
import functions as func
import cairo

def png_to_svg(png_file, svg_file):
    # Open the PNG image using Cairo
    with cairo.ImageSurface.create_from_png(png_file) as surface:
        width = surface.get_width()
        height = surface.get_height()

        # Create an SVG context
        with cairo.SVGSurface(svg_file, width, height) as svg_surface:
            context = cairo.Context(svg_surface)

            # Render the PNG image onto the SVG context
            context.set_source_surface(surface)
            context.paint()

def zipFiles():
    with ZipFile('./IMG/Output.zip', 'w') as zipObj:
        os.chdir("./SVG/")
        #zipObj.write('Canvas.svg')
        os.chdir("./../")
        os.chdir("./PNG/")
        zipObj.write('output_.png')
        png_to_svg('output_.png','output_.svg')
        zipObj.write('output_.svg')
        os.chdir("./../") 
        for folderName, subfolders, filenames in os.walk("./unplaced"):
            for filename in filenames:
                filePath = os.path.join(folderName, filename)
                zipObj.write(filePath)
        func.pushNotification("Zip File Created")
        