import png
import sys

r=png.Reader('logo_18.png')
height = r.read()[1]
width = r.read()[0]
print "width =", width, "height =", height
print r.read()
l=list(r.read()[2])
i = 0
while i < height :
    j = 0
    topLine = l[i]
    bottomLine = l[i + 1]
    while j < (width * 3) :
        if (topLine[j] + topLine[j + 3] + topLine[j + 6] + topLine[j + 9] + topLine[j + 12] + bottomLine[j] + bottomLine[j + 3] + bottomLine[j + 6] + bottomLine[j + 9] + bottomLine[j + 12]) < (10 * 255) :
            sys.stdout.write('#')
        else :
            sys.stdout.write('.')
        j = j + 15
    print " "
    i = i + 2
    
