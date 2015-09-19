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

# split rows into bricks or plates. Available lengths are 10, 8, 6, 4, 3, 2 and 1.

print " "
print " "
print " "
sizesOfBricks = [10, 8, 6, 4, 3, 2, 1]
whiteplateStrings = ["X========X","8======8","6====6","4==4","3=3","==","~"]
blackplateStrings = ["XXXXXXXXXX","88888888","666666","4444","333","__","."]
whitetopBrickStrings = ["I--------I","I------I","I----I","I--I","I-I","--","I"]
whitemedBrickStrings = ["I  1010  I","I 8888 I","I 66 I","I44I","I3I","II","I"]
whitebotBrickStrings = ["I________I","I______I","I____I","I__I","I_I","__","I"]
blacktopBrickStrings = ["|--------|","|------|","|----|","|--|","|-|","--","1"]
blackmedBrickStrings = ["|  1010  |","| 8888 |","| 66 |","|44|","|3|","22","1"]
blackbotBrickStrings = ["|________|","|______|","|____|","|__|","|_|","__","1"]
i = 0.0
PieceCounter = 0
white2plateCnt = [0, 0, 0, 0 ,0 ,0, 0]
white1plateCnt = [0, 0, 0, 0 ,0 ,0, 0]
blackplateCnt = [0, 0, 0, 0 ,0 ,0, 0]
blackbrickCnt = [0, 0, 0, 0 ,0 ,0, 0]
white2brickCnt = [0, 0, 0, 0 ,0 ,0, 0]
white1brickCnt = [0, 0, 0, 0 ,0 ,0, 0]

minScnt = 0
while i < int(height / 2) :
    j = 0
    while j < int(width / 5) :
        if output[int(i)][j] == 0 :
            # Black plates
            sCnt = minScnt
            while sCnt < len(sizesOfBricks) and j < int(width / 5) and output[int(i)][j] == 0:
                if 1 == fit_part(output, j, int(i), sizesOfBricks[sCnt], int(width / 5)) :
                    j = j + sizesOfBricks[sCnt]
                    sys.stdout.write(Fore.RED + blackplateStrings[sCnt])
                    PieceCounter = PieceCounter + 2
                    blackplateCnt[sCnt] = blackplateCnt[sCnt] + 1
                    white1plateCnt[sCnt] = white1plateCnt[sCnt] + 1
                else :
                    sCnt = sCnt + 1
        else :
            if output[int(i)][j] == 64 :
                # Black bricks
                sCnt = minScnt
                while sCnt < len(sizesOfBricks) and j < int(width / 5) and output[int(i)][j] == 64:
                    if 1 == fit_part(output, j, int(i), sizesOfBricks[sCnt], int(width / 5)) :
                        j = j + sizesOfBricks[sCnt]
                        if (i / 3) == int (i / 3) :
                            sys.stdout.write(Fore.RED + blacktopBrickStrings[sCnt])
                            PieceCounter = PieceCounter + 2
                            blackbrickCnt[sCnt] = blackbrickCnt[sCnt] + 1
                            white1brickCnt[sCnt] = white1brickCnt[sCnt] + 1
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
                    sCnt = minScnt
                    while sCnt < len(sizesOfBricks) and j < int(width / 5) and output[int(i)][j] == 192:
                        if 0 == j :
                            # special case for the start of line: insert a 1x4 every other line of brick to create the space to hide the hanging structure.
                            if ((i / 6) == int(i / 6)) or (((i - 1) / 6) == int((i - 1) / 6)) or  (((i - 2) / 6) == int((i - 2) / 6)):
                                j = 1
                                sys.stdout.write(Fore.WHITE + "S")
                            if (i / 6) == int(i / 6) :
                                white1brickCnt[3] = white1brickCnt[3] + 1
                            if (((i - 3) / 6) == int((i - 3) / 6)) :
                                # the other line of brick gets an invisible 1x2
                                white1brickCnt[4] = white1brickCnt[5] + 1
                                
                        if 1 == fit_part(output, j, int(i), sizesOfBricks[sCnt], int(width / 5)) :
                            j = j + sizesOfBricks[sCnt]
                            eol = 0
                            if j == int(width / 5) :
                                # Special case for the end of line: insert a 1x4 every other line of brick to create the space to hide the hanging structure.
                                if ((i / 6) == int(i / 6)) or (((i - 1) / 6) == int((i - 1) / 6)) or  (((i - 2) / 6) == int((i - 2) / 6)):
                                    eol = 1
                                if (i / 6) == int(i / 6) :
                                    white1brickCnt[3] = white1brickCnt[3] + 1
                                if (((i - 3) / 6) == int((i - 3) / 6)) :
                                    # the other line of brick gets an invisible 1x2
                                    white1brickCnt[4] = white1brickCnt[5] + 1
                                
                            if (i / 3) == int (i / 3) :
                                if 1 == eol :
                                    if sCnt < len(sizesOfBricks) - 1 :
                                        sys.stdout.write(Fore.WHITE + whitetopBrickStrings[sCnt + 1])
                                        white2brickCnt[sCnt + 1] = white2brickCnt[sCnt + 1] + 1
                                        if (sizesOfBricks[sCnt] - sizesOfBricks[sCnt + 1]) == 2 :
                                            # Insert a 1x2 to fit between the shorter regular brick and the side one
                                            sys.stdout.write(Fore.WHITE + "I")
                                            white2brickCnt[len(sizesOfBricks) - 1] = white2brickCnt[len(sizesOfBricks) - 1] + 1
                                            
                                    sys.stdout.write(Fore.WHITE + "S")
                                else :
                                    sys.stdout.write(Fore.WHITE + whitetopBrickStrings[sCnt])
                                    white2brickCnt[sCnt] = white2brickCnt[sCnt] + 1
                                PieceCounter = PieceCounter + 1
                            else :
                                if ((i - 1) / 3) == int((i - 1) / 3) :
                                    if 1 == eol :
                                        if sCnt < len(sizesOfBricks) - 1 :
                                            sys.stdout.write(Fore.WHITE + whitemedBrickStrings[sCnt + 1])
                                            if (sizesOfBricks[sCnt] - sizesOfBricks[sCnt + 1]) == 2 :
                                                # Insert a 1x2 to fit between the shorter regular brick and the side one
                                                sys.stdout.write(Fore.WHITE + "I")
                                        sys.stdout.write(Fore.WHITE + "S")
                                    else :
                                        sys.stdout.write(Fore.WHITE + whitemedBrickStrings[sCnt])
                                else :
                                    if 1 == eol :
                                        if sCnt < len(sizesOfBricks) - 1 :
                                            sys.stdout.write(Fore.WHITE + whitebotBrickStrings[sCnt + 1])
                                            if (sizesOfBricks[sCnt] - sizesOfBricks[sCnt + 1]) == 2 :
                                                # Insert a 1x2 to fit between the shorter regular brick and the side one
                                                sys.stdout.write(Fore.WHITE + "I")
                                        sys.stdout.write(Fore.WHITE + "S")
                                    else :
                                        sys.stdout.write(Fore.WHITE + whitebotBrickStrings[sCnt])
                        else :
                            sCnt = sCnt + 1
                else :
                    if output[int(i)][j] == 255 :
                        # white plates
                        sCnt = minScnt
                        while sCnt < len(sizesOfBricks) and j < int(width / 5) and output[int(i)][j] == 255:
                            if 1 == fit_part(output, j, int(i), sizesOfBricks[sCnt], int(width / 5)) :
                                j = j + sizesOfBricks[sCnt]
                                sys.stdout.write(Fore.WHITE + whiteplateStrings[sCnt])
                                white2plateCnt[sCnt] = white2plateCnt[sCnt] + 1
                                PieceCounter = PieceCounter + 1
                            else :
                                sCnt = sCnt + 1
    print " "
    i = i + 1.0     
print "Total: ", PieceCounter
print "                    10   8   6   4  3  2  1"
print "White 2x plates: ", white2plateCnt
print "White 1x plates: ", white1plateCnt
print "White 2x bricks: ", white2brickCnt
print "White 1x bricks: ", white1brickCnt
print "Black 2x plates: ", blackplateCnt
print "Black 2x bricks: ", blackbrickCnt
       
