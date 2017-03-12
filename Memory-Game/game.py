import random, pygame, sys, os, json
from pygame.locals import *

pygame.init()
pygame.mixer.init()

gamedata = dict() # Global dictionary Variable for storing game data to write to a file

GRAY = (100,100,100)
NAVYBLUE = (60,60,60)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
ORANGE = (255,128,0)
PURPLE = (255, 0, 255)
CYAN = (0,255,255)

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

A='A'
G='G'
T='T'
C='C'

COLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN, WHITE)
LETTERS = (A,G,T,C)

FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
REVEALSPEED = 8

def main1():
    global MOVES, BOXSIZE, GAPSIZE, BOARDWIDTH, BOARDHEIGHT, MARGIN_X, MARGIN_Y    
    BOXSIZE = 60
    GAPSIZE = 20
    BOARDWIDTH = 4
    BOARDHEIGHT = 4
    MARGIN_X = int((WINDOWWIDTH-(BOARDWIDTH*(BOXSIZE+GAPSIZE)))/2)
    MARGIN_Y = int((WINDOWHEIGHT-(BOARDHEIGHT*(BOXSIZE+GAPSIZE)))/2)
    startgame()
    
def main2():
    global MOVES, BOXSIZE, GAPSIZE, BOARDWIDTH, BOARDHEIGHT, MARGIN_X, MARGIN_Y
    BOXSIZE = 60
    GAPSIZE = 15
    BOARDWIDTH = 6
    BOARDHEIGHT = 5
    MARGIN_X = int((WINDOWWIDTH-(BOARDWIDTH*(BOXSIZE+GAPSIZE)))/2)
    MARGIN_Y = int((WINDOWHEIGHT-(BOARDHEIGHT*(BOXSIZE+GAPSIZE)))/2)
    startgame()

def main3():
    global MOVES, BOXSIZE, GAPSIZE, BOARDWIDTH, BOARDHEIGHT, MARGIN_X, MARGIN_Y
    BOXSIZE = 50
    GAPSIZE = 10
    BOARDWIDTH = 8
    BOARDHEIGHT = 7
    MARGIN_X = int((WINDOWWIDTH-(BOARDWIDTH*(BOXSIZE+GAPSIZE)))/2)
    MARGIN_Y = int((WINDOWHEIGHT-(BOARDHEIGHT*(BOXSIZE+GAPSIZE)))/2)
    startgame()


def startgame():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    pygame.mixer.music.load('bg.mp3')
    pygame.mixer.music.play(-1)
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    mousex = 0
    mousey = 0
    MOVES = 0
    pygame.display.set_caption('Memory Game')
    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)
    firstSelection = None
    DISPLAYSURF.fill(BGCOLOR)
    startGameAnimation(mainBoard)

    while True:
        pickup_music=pygame.mixer.Sound('pickup.wav')
        mouseClicked = False
        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(mainBoard, revealedBoxes)
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex,mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex,mousey = event.pos
                mouseClicked = True
                MOVES = MOVES + 1
                pickup_music.play()
        boxx, boxy = getBoxAtPixel(mousex,mousey)
        if boxx!=None and boxy!=None:
            if not revealedBoxes[boxx][boxy]:
                drawHighlightBox(boxx,boxy)
            if not revealedBoxes[boxx][boxy] and mouseClicked:
                revealBoxesAnimation(mainBoard, [(boxx,boxy)])
                revealedBoxes[boxx][boxy] = True

                if firstSelection == None:
                    firstSelection = (boxx,boxy)
                else:
                    icon1letter, icon1color = getLetterAndColor(mainBoard,firstSelection[0],firstSelection[1])
                    icon2letter, icon2color = getLetterAndColor(mainBoard,boxx,boxy)
                    if (icon1letter==A and icon2letter!=T) or (icon1letter==T and icon2letter!=A) or (icon1letter==C and icon2letter!=G) or (icon1letter==G and icon2letter!=C) or icon1color!=icon2color:
                        pygame.time.wait(1000)
                        coverBoxesAnimation(mainBoard,[(firstSelection[0],firstSelection[1]),(boxx,boxy)])
                        revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                        revealedBoxes[boxx][boxy] = False
                    elif hasWon(revealedBoxes):
                        gameWonAnimation(mainBoard)
                        pygame.time.wait(2000)
                        mainBoard = getRandomizedBoard()
                        revealedBoxes = generateRevealedBoxesData(False)
                        drawBoard(mainBoard,revealedBoxes)
                        pygame.display.update()
                        pygame.time.wait(1000)
                        startGameAnimation(mainBoard)
                    firstSelection = None
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(BOARDWIDTH):
        revealedBoxes.append([val]*BOARDHEIGHT)
    return revealedBoxes

def getRandomizedBoard():
    icons  = []
    icons1 = []
    for color in COLORS:
        for letter in LETTERS:
            icons.append((letter,color))            
    random.shuffle(icons)
    numIcons = int(BOARDWIDTH*BOARDHEIGHT/2)
    icons = icons[:numIcons]
    for iconLetter,iconColor in icons:
        if iconLetter == A:
            icons1.append((T,iconColor))
        elif iconLetter == T:
            icons1.append((A,iconColor))
        elif iconLetter == G:
            icons1.append((C,iconColor))
        elif iconLetter == C:
            icons1.append((G,iconColor))
    icons = icons + icons1
    random.shuffle(icons)
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(icons[0])
            del icons[0]
        board.append(column)
    return board

def splitIntoGroupsOf(groupSize, theList):
    result = []
    for i in range(0,len(theList),groupSize):
        result.append(theList[i:i+groupSize])
    return result

def leftTopCoordsOfBox(boxx,boxy):
    left = boxx*(BOXSIZE+GAPSIZE)+MARGIN_X
    top  = boxy*(BOXSIZE+GAPSIZE)+MARGIN_Y
    return (left,top)

def getBoxAtPixel(x,y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left,top = leftTopCoordsOfBox(boxx,boxy)
            boxRect = pygame.Rect(left,top,BOXSIZE,BOXSIZE)
            if boxRect.collidepoint(x,y):
                return (boxx,boxy)
    return (None,None)

def drawIcon(letter,color,boxx,boxy):
    quarter = int(BOXSIZE*0.25)
    half = int(BOXSIZE*0.5)
    left,top=leftTopCoordsOfBox(boxx,boxy)
    fontObj = pygame.font.Font('freesansbold.ttf',50)
    if letter == A:
        textSurfaceObj = fontObj.render('A',True,color)
    elif letter == G:
        fontObj = pygame.font.Font('freesansbold.ttf',50)
        textSurfaceObj = fontObj.render('G',True,color)
    elif letter == T:
        fontObj = pygame.font.Font('freesansbold.ttf',50)
        textSurfaceObj = fontObj.render('T',True,color)
    elif letter == C:
        fontObj = pygame.font.Font('freesansbold.ttf',50)
        textSurfaceObj = fontObj.render('C',True,color)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (left+half,top+half)
    DISPLAYSURF.blit(textSurfaceObj,textRectObj)
        
def getLetterAndColor(board,boxx,boxy):
    return board[boxx][boxy][0], board[boxx][boxy][1]

def drawBoxCovers(board,boxes,coverage):
    for box in boxes:
        left,top=leftTopCoordsOfBox(box[0],box[1])
        pygame.draw.rect(DISPLAYSURF,BGCOLOR,(left,top,BOXSIZE,BOXSIZE))
        letter,color=getLetterAndColor(board,box[0],box[1])
        drawIcon(letter,color,box[0],box[1])
        if coverage>0:
            pygame.draw.rect(DISPLAYSURF,BOXCOLOR,(left,top,coverage,BOXSIZE))
    pygame.display.update()
    FPSCLOCK.tick(FPS)

def revealBoxesAnimation(board,boxesToReveal):
    for coverage in range(BOXSIZE,(-REVEALSPEED)-1,-REVEALSPEED):
        drawBoxCovers(board,boxesToReveal, coverage)

def coverBoxesAnimation(board,boxesToCover):
    for coverage in range(0,BOXSIZE+REVEALSPEED,REVEALSPEED):
        drawBoxCovers(board,boxesToCover,coverage)

def drawBoard(board,revealed):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left,top=leftTopCoordsOfBox(boxx,boxy)
            if not revealed[boxx][boxy]:
                pygame.draw.rect(DISPLAYSURF,BOXCOLOR,(left,top,BOXSIZE,BOXSIZE))
            else:
                letter,color=getLetterAndColor(board,boxx,boxy)
                drawIcon(letter,color,boxx,boxy)


def drawHighlightBox(boxx,boxy):
    left,top=leftTopCoordsOfBox(boxx,boxy)
    pygame.draw.rect(DISPLAYSURF,HIGHLIGHTCOLOR,(left-5,top-5,BOXSIZE+10,BOXSIZE+10),4)

def startGameAnimation(board):
    coveredBoxes=generateRevealedBoxesData(False)
    boxes=[]
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            boxes.append((x,y))
    random.shuffle(boxes)
    boxGroups=splitIntoGroupsOf(8,boxes)
    drawBoard(board,coveredBoxes)
    for boxGroup in boxGroups:
        revealBoxesAnimation(board,boxGroup)
        coverBoxesAnimation(board,boxGroup)

def gameWonAnimation(board):
    pygame.mixer.music.stop()
    coveredBoxes=generateRevealedBoxesData(True)
    color1=LIGHTBGCOLOR
    color2=BGCOLOR
    for i in range(13):
        color1,color2=color2,color1
        DISPLAYSURF.fill(color1)
        fontObj = pygame.font.Font('freesansbold.ttf',70)
        textSurfaceObj = fontObj.render('You Won !',True, YELLOW)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (WINDOWWIDTH/2,WINDOWHEIGHT/2)
        DISPLAYSURF.blit(textSurfaceObj,textRectObj)
        pygame.display.update()
        pygame.time.wait(300)

def hasWon(revealedBoxes):
    for i in revealedBoxes:
        if False in i:
            return False
    return True

def save_datafile():
    """
    Saves the data dictionary to a file named data_file
    """
    global gamedata
    data_file = os.path.join(os.path.dirname(__file__),"data.json")
    with open(data_file, "w") as dataf:
        json.dump(gamedata, dataf)


def load_datafile():
    """
    Loads the data dictionary form a file named data_file
    """
    global gamedata
    data_file = os.path.join(os.path.dirname(__file__),"data.json")
    try:
        with open(data_file) as dataf:
            gamedata = json.load(dataf)
    except IOError:
        return # Returns nothing if file is not found. Willnot cause an error.
    except:
        # JSON unable to parse. Just delete the corrupted file
        try:
            os.remove(data_file)
        except:
            pass


if __name__=='__main__':
    main2()
        
