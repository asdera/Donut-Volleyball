from colorsys import *

def hex(tup):
    H = ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]

    hexX = ""
    hexY = ""
    hexZ = ""
    x = int(tup[0]*255)
    y = int(tup[1]*255)
    z = int(tup[2]*255)
    
    while x != 0:
        q = int(x/16)
        r = x % 16
        hexX = H[r] + hexX
        x = q

    while y != 0:
        q = int(y/16)
        r = y % 16
        hexY = H[r] + hexY
        y = q

    while z != 0:
        q = int(z/16)
        r = z % 16
        hexZ = H[r] + hexZ
        z = q 

    
    return "#" + hexX.zfill(2) + hexY.zfill(2) + hexZ.zfill(2)

def getRainbow(hue):
    rgb = hsv_to_rgb(hue, 1, 1)
    return hex(rgb)

