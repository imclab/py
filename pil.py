from PIL import Image

if __name__ == "__main__":
    
    image = Image.open('sam.jpg')
    image.load()
    
    width, height = image.size
    
    if width >= height:
        short_edge = height
        long_edge = width
        orientation = "l"
        print "height is shortest side"
    else:
        short_edge = width
        long_edge = height
        orientation = "p"
        print "width is shortest side"
        
    delta = long_edge - short_edge
    
    if orientation == "p":
        crop_box = (0, int(delta/2), width, height - int(delta/2) )
    elif orientation == "l":
        crop_box = ( int(delta/2), 0, width - int(delta/2), height )
        
    cropped = image.crop(crop_box)
    cropped.load()
    cropped.save("thumb.jpg")