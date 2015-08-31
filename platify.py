import png
import sys

def draw8():
    sys.stdout.write('P------|')
    sys.stdout.write('|   8  |')
    sys.stdout.write('L______|')

def draw6():
    sys.stdout.write('P----|')
    sys.stdout.write('| 8  |')
    sys.stdout.write('L____|')

def draw4():
    sys.stdout.write('P--|')
    sys.stdout.write('|8 |')
    sys.stdout.write('L__|')

def draw3():
    sys.stdout.write('P-|')
    sys.stdout.write('|8|')
    sys.stdout.write('L_|')

def draw2():
    sys.stdout.write('22')
    sys.stdout.write('22')
    sys.stdout.write('22')
    
def draw1():
    sys.stdout.write('1')
    sys.stdout.write('1')
    sys.stdout.write('1')

r=png.Reader('logo_18.png')
height = r.read()[1]
width = r.read()[0]
print "width =", width, "height =", height
print r.read()
l=list(r.read()[2])

f = open('plates.png', 'wb')
w = png.Writer(width / 5, height / 2, greyscale=True)
output = [None] *(height / 2)
i = 0
while i < height :
    j = 0
    topLine = l[i]
    bottomLine = l[i + 1]
    outputRow = [None]*(width / 5)
    while j < (width * 3) :
        if (topLine[j] + topLine[j + 3] + topLine[j + 6] + topLine[j + 9] + topLine[j + 12] + bottomLine[j] + bottomLine[j + 3] + bottomLine[j + 6] + bottomLine[j + 9] + bottomLine[j + 12]) < (10 * 255) :
            sys.stdout.write('#')
            outputRow[int(j / 15)] = 0
        else :
            sys.stdout.write('.')
            outputRow[int(j / 15)] = 255
        j = j + 15
    print " "
    output[int(i / 2)] = outputRow
    i = i + 2
w.write(f, output)
f.close()

i = 0

print " "
print " "
print " "
f = open('platesNbricks.png', 'wb')
w = png.Writer(width / 5, height / 2, greyscale=True)

while i < (int(height / 2) - 2) :
    j = 0
    while j < int(width / 5) :
        if output[i][j] == output[i + 1][j] and output[i][j] == output[i + 2][j] :
            if output[i][j] == 0 :
                color = 64
            else :
                color = 192
            output[i][j] = color
            output[i + 1][j] = color
            output[i + 2][j] = color
        j = j + 1
    i = i + 3

w.write(f, output)
f.close()

i = 0.0
while i < int(height / 2) :
    j = 0
    while j < int(width / 5) :
        if output[int(i)][j] == 0 :
            sys.stdout.write('#')
        if output[int(i)][j] == 64 :
            if (i / 3) == int (i / 3) :
                sys.stdout.write('T')
            else :
                if ((i - 1) / 3) == int((i - 1) / 3) :
                    sys.stdout.write('|')
                else :
                    sys.stdout.write('=')
                
        if output[int(i)][j] == 192 :
            if (i / 3) == int (i / 3) :
                sys.stdout.write('.')
            else :
                if ((i - 1) / 3) == int((i - 1) / 3) :
                    sys.stdout.write(':')
                else :
                    sys.stdout.write('`')
        if output[int(i)][j] == 255 :
            sys.stdout.write('_')
        j = j + 1
    print " "
    i = i + 1.0            
