import png
import sys
from colorama import init, Fore
def fit_part(array, x, y, length, maxWidth):
    count = 0
    while count < length :
        if (x + count) < maxWidth :
            if array[y][x] != array[y][x + count] :
                return 0
        else :
            return 0
        count = count + 1
    return 1

# the source png file must have dimensions that are multiples of 5 for x and multiples of 2 for y.
r=png.Reader('logo_18.png')
# height is in plates
height = r.read()[1]
width = r.read()[0]
print "width =", width, "height =", height
print r.read()
l=list(r.read()[2])
# this image will be the plated version of original: note the aspect ratio is off (squeezed sideways).
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
        # use a majority to decide if a given plate (made of 10 pixels) should be black or white.
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
# This file uses four colors: black for black plates, dark grey for black bricks, white for white plates, light grey for white bricks.
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

# Display the logo using characters to show lines of plates versus bricks
i = 0.0
while i < int(height / 2) :
    j = 0
    while j < int(width / 5) :
        if output[int(i)][j] == 0 :
            sys.stdout.write('#')
        if output[int(i)][j] == 64 :
            # bricks are made of three rows.
            if (i / 3) == int (i / 3) :
                sys.stdout.write('T')
            else :
                if ((i - 1) / 3) == int((i - 1) / 3) :
                    sys.stdout.write('|')
                else :
                    sys.stdout.write('=')
                
        if output[int(i)][j] == 192 :
            # bricks are made of three rows.
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

# split rows into bricks or plates. Available lengths are 8, 6, 4, 3, 2 and 1.

print " "
print " "
print " "
sizesOfBricks = [8, 6, 4, 3, 2, 1]
whiteplateStrings = ["8======8","6====6","4==4","3=3","==","~"]
blackplateStrings = ["88888888","666666","4444","333","__","."]
whitetopBrickStrings = ["I------I","I----I","I--I","I-I","--","I"]
whitemedBrickStrings = ["I 8888 I","I 66 I","I44I","I3I","II","I"]
whitebotBrickStrings = ["I______I","I____I","I__I","I_I","__","I"]
blacktopBrickStrings = ["|------|","|----|","|--|","|-|","--","1"]
blackmedBrickStrings = ["| 8888 |","| 66 |","|44|","|3|","22","1"]
blackbotBrickStrings = ["|______|","|____|","|__|","|_|","__","1"]
i = 0.0
while i < int(height / 2) :
    j = 0
    while j < int(width / 5) :
        if output[int(i)][j] == 0 :
            # Black plates
            sCnt = 0
            while sCnt < len(sizesOfBricks) and j < int(width / 5) and output[int(i)][j] == 0:
                if 1 == fit_part(output, j, int(i), sizesOfBricks[sCnt], int(width / 5)) :
                    j = j + sizesOfBricks[sCnt]
                    sys.stdout.write(Fore.RED + blackplateStrings[sCnt])
                else :
                    sCnt = sCnt + 1
        else :
            if output[int(i)][j] == 64 :
                # Black bricks
                sCnt = 0
                while sCnt < len(sizesOfBricks) and j < int(width / 5) and output[int(i)][j] == 64:
                    if 1 == fit_part(output, j, int(i), sizesOfBricks[sCnt], int(width / 5)) :
                        j = j + sizesOfBricks[sCnt]
                        if (i / 3) == int (i / 3) :
                            sys.stdout.write(Fore.RED + blacktopBrickStrings[sCnt])
                        else :
                            if ((i - 1) / 3) == int((i - 1) / 3) :
                                sys.stdout.write(Fore.RED + blackmedBrickStrings[sCnt])
                            else :
                                sys.stdout.write(Fore.RED + blackbotBrickStrings[sCnt])
                    else :
                        sCnt = sCnt + 1
            else :                
                if output[int(i)][j] == 192 :
                    # White bricks
                    sCnt = 0
                    while sCnt < len(sizesOfBricks) and j < int(width / 5) and output[int(i)][j] == 192:
                        if 1 == fit_part(output, j, int(i), sizesOfBricks[sCnt], int(width / 5)) :
                            j = j + sizesOfBricks[sCnt]
                            if (i / 3) == int (i / 3) :
                                sys.stdout.write(Fore.WHITE + whitetopBrickStrings[sCnt])
                            else :
                                if ((i - 1) / 3) == int((i - 1) / 3) :
                                    sys.stdout.write(Fore.WHITE + whitemedBrickStrings[sCnt])
                                else :
                                    sys.stdout.write(Fore.WHITE + whitebotBrickStrings[sCnt])
                        else :
                            sCnt = sCnt + 1
                else :
                    if output[int(i)][j] == 255 :
                        # white plates
                        sCnt = 0
                        while sCnt < len(sizesOfBricks) and j < int(width / 5) and output[int(i)][j] == 255:
                            if 1 == fit_part(output, j, int(i), sizesOfBricks[sCnt], int(width / 5)) :
                                j = j + sizesOfBricks[sCnt]
                                sys.stdout.write(Fore.WHITE + whiteplateStrings[sCnt])
                            else :
                                sCnt = sCnt + 1
    print " "
    i = i + 1.0     
print int(width / 5), int(height /2)
       
