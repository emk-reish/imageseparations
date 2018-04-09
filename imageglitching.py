from PIL import Image
import os.path

fname = input("Image file (ex 'name.png'): ")
while not os.path.isfile(fname):
    fname = input("Could not find file. Please make sure there is a valid image file (png or jpeg) of that name in the current directory.\n\rImage file: ")

img = Image.open(fname)
while img.format != "JPEG" and img.format != "PNG": 
    fname = input("File not in a valid format. Please make sure the file is a standard image file.\n\rImage file (ex 'name.png'): ")
    img = Image.open(fname)

def ismodificationvalid(modstring):
    allvalid = len(modstring) > 0
    for char in modstring:
        if char not in "0123":
            return False
    return allvalid

modification = input("Modification options:\n\r  0. Isolate RGB values.\n\r  1. Isolate RBG values, exlusionary.\n\r  2. Isolate and Maximize RBG values.\n\r  3. Isolate Secondary values.\n\rPlease select from the numbers above (as many as desired): ")
while not ismodificationvalid(modification):
    modification = input("Please select valid number(s) from the list above (ex '1', '012', '13'): ")

width, height = img.size
pixels = list(img.getdata())
pixels = [pixels[i * width:(i + 1) * width] for i in range(0,height)]
newpixels = []

def isolatergbimages():
    for row in pixels:
        redrow = []
        greenrow = []
        bluerow = []
        for p in row:
            r,g,b = isolatergbpixel(p)
            redrow.append(r)
            greenrow.append(g)
            bluerow.append(b)
        newpixels.extend(redrow)
        newpixels.extend(greenrow)
        newpixels.extend(bluerow)

def isolateexclusivergbimages():
    for row in pixels:
        redrow = []
        greenrow = []
        bluerow = []
        for p in row:
            r,g,b = isolateexclusivergbpixel(p)
            redrow.append(r)
            greenrow.append(g)
            bluerow.append(b)
        newpixels.extend(redrow)
        newpixels.extend(greenrow)
        newpixels.extend(bluerow)

def isolateandmaxrgbimages():
    for row in pixels:
        redrow = []
        greenrow = []
        bluerow = []
        for p in row:
            r,g,b = isolateandmaxrgbpixel(p)
            redrow.append(r)
            greenrow.append(g)
            bluerow.append(b)
        newpixels.extend(redrow)
        newpixels.extend(greenrow)
        newpixels.extend(bluerow)

def isolatesecondaryimages():
    for row in pixels:
        redgreenrow = []
        redbluerow = []
        greenbluerow = []
        for p in row:
            rg,rb,gb = isolatesecondarypixel(p)
            redgreenrow.append(rg)
            redbluerow.append(rb)
            greenbluerow.append(gb)
        newpixels.extend(redgreenrow)
        newpixels.extend(redbluerow)
        newpixels.extend(greenbluerow)

def isolatergbpixel(pixel):
    r,g,b = 0,0,0
    if len(pixel) == 4: #to avoid error with png images, we won't use alpha
        r,g,b,a = pixel
    else:
        r,b,g = pixel
    return (r,0,0,255), (0,g,0,255), (0,0,b,255)

def isolateexclusivergbpixel(pixel):
    r,g,b = 0,0,0
    if len(pixel) == 4: #to avoid error with png images, we won't use alpha
        r,g,b,a = pixel
    else:
        r,g,b = pixel
    na = (0,0,0,0)
    if r > b and r > g:
        return (r,0,0,255), na, na
    if g > r and g > b:
        return na, (0,g,0,255), na
    if  b > r and b > g:
        return na, na, (0,0,b,255)
    return na, na, na

def isolateandmaxrgbpixel(pixel):
    r,g,b = 0,0,0
    if len(pixel) == 4: #to avoid error with png images, we won't use alpha
        r,g,b,a = pixel
    else:
        r,g,b= pixel
    na = (0,0,0,0)
    if r > b and r > g:
        return (255,0,0,255), na, na
    if g > r and g > b:
        return na, (0,255,0,255), na
    if  b > r and b > g:
        return na, na, (0,0,255,255)
    return na, na, na

def isolatesecondarypixel(pixel):
    r,g,b = 0,0,0
    if len(pixel) == 4: #to avoid error with png images, we won't use alpha
        r,g,b,a = pixel
    else:
        r,g,b = pixel
    return (r,g,0,255), (r,0,b,255), (0,g,b,255)

def makenewimagefromnewpixels(mod, width, height):
    outname = "output_" + mod
    if hasattr(img, 'filename'):
        fn = img.filename
        outname = fn[:fn.index('.')] + "_" + outname
    newimg = Image.new('RGBA', (width, height))
    newimg.putdata(newpixels)
    print("\n\rMade modification " + mod + ".")
    try:
        newimg.save(outname + ".png")
        print("Saved output image as " + outname)
    except:
        print("Failed to save image. Please check inputs.")
    del newpixels[:]

if "0" in modification:
    isolatergbimages()
    makenewimagefromnewpixels("0", width * 3, height)
if "1" in modification:
    isolateexclusivergbimages()
    makenewimagefromnewpixels("1", width * 3, height)
if "2" in modification:
    isolateandmaxrgbimages()
    makenewimagefromnewpixels("2", width * 3, height)
if "3" in modification:
    isolatesecondaryimages()
    makenewimagefromnewpixels("3", width * 3, height)
if not ismodificationvalid(modification):
    print("Did not find modification.")