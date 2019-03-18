import pygame
import time
import random

pygame.init()
gameDisplay= pygame.display.set_mode((800,600))
pygame.display.set_caption('Tic Tac Toe')
clock=pygame.time.Clock()

#defining colors 
white=(255,255,255)
black=(0,0,0)
red=(200,0,0)
bright_red=(255,0,0)
green=(0,200,0)
bright_green=(0,255,0)
blue=(0,0,200)
bright_blue=(0,0,255)
yellow=(255,255,0)
gold=(255,190,0)

turn='x'
move=None #for singleplayer game determines who goes next
firstMove=None
msg=" "
win_row=None #stores the winning row tuple from WAYS_TO_WIN

def quitGame():
    '''Quits the game'''
    pygame.quit()
    quit()

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def drawBoard():
    ''' Draws game board '''
    gameDisplay.fill(black)
    pygame.draw.line(gameDisplay, blue,(300,499),(300,100),5)
    pygame.draw.line(gameDisplay, blue,(500,499),(500,100),5)
    pygame.draw.line(gameDisplay, blue,(100,366),(700,366),5)
    pygame.draw.line(gameDisplay, blue,(100,233),(700,233),5)

def button(msg,x,y,w,h,ic,ac,action=None):
    '''Draws inteactive buttons and binds them to corresponding funtions'''
    #msg =Message u want to display
    #w=width  h=height
    #ic=inactive colour  ac=active colour
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)

class containers:
    '''The nine places where X and O go are the containers'''
    count=-1
    def __init__(self,upper_x,lower_x,upper_y,lower_y):
        self.chk=0; # implies that 0 interactions have taken place
        containers.count+=1
        self.number=containers.count
        self.upper_x=upper_x
        self.upper_y=upper_y
        self.lower_x=lower_x
        self.lower_y=lower_y
        self.filler=None

    def drawCross(self):
        '''Draws crosses takes width and height of surrounding box as input'''
        #x,y are center of box
        self.filler='x'
        self.chk=1

    def drawNought(self):
        '''Draws nought takes center of box as argument'''
        self.filler='y'
        self.chk=1

# init ALL containing all the containers
ALL=[]
ALL.append(containers(300,100,233,100))
ALL.append(containers(500,300,233,100))
ALL.append(containers(700,500,233,100))
ALL.append(containers(300,100,366,233))
ALL.append(containers(500,300,366,233))
ALL.append(containers(700,500,366,233))
ALL.append(containers(300,100,499,366))
ALL.append(containers(500,300,499,366))
ALL.append(containers(700,500,499,366))


def reset():
    '''Resets all the global variables .Is called each time a new game starts'''
    global move,turn,firstMove,msg
    for container in ALL:
        container.chk=0
        container.filler=None
    move=None
    firstMove=None
    turn='x'
    win_row=None
    msg=" "

def drawRoutine(i):
    '''Calls the needed draw function of the needed class'''
    global turn
    if(ALL[i].chk==0):
        if(turn=='x'):
            ALL[i].drawCross()
            turn='o'
        else :
            ALL[i].drawNought()
            turn='x'

def chkInput():
    '''Determines user input and takes action'''
    mouse=pygame.mouse.get_pos()
    click=pygame.mouse.get_pressed()
    if click[0]==1 :
        for container in ALL:
            if(container.upper_x > mouse[0] > container.lower_x and container.upper_y>mouse[1]>container.lower_y):
                drawRoutine(container.number)
        return True # used in singleplayer to run chkInput till the a input isn't recieved 'True' means input recieved
    else :
        return False

WAYS_TO_WIN = ((ALL[0], ALL[1], ALL[2]),
               (ALL[3], ALL[4], ALL[5]),
               (ALL[6], ALL[7], ALL[8]),
               (ALL[0], ALL[3], ALL[6]),
               (ALL[1], ALL[4], ALL[7]),
               (ALL[2], ALL[5], ALL[8]),
               (ALL[0], ALL[4], ALL[8]),
               (ALL[2], ALL[4], ALL[6]))
def gameIntro():
    '''Introduction Screen'''
    intro=True
    while intro:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                quitGame()
        gameDisplay.fill(white)
        largeText = pygame.font.Font('freesansbold.ttf',115)
        TextSurf, TextRect = text_objects("Tic Tac Toe", largeText)
        TextRect.center = (400,200)
        gameDisplay.blit(TextSurf, TextRect)

        button("Singleplayer",170,450,110,40,green,bright_green,beforeSingle)
        button("Multiplayer",570,450,110,40,gold,yellow,multiGameLoop)
        button("QUIT",400,510,60,40,red,bright_red,quitGame)

        pygame.display.update()
        clock.tick(10)


def afterGame():
    '''After game screen displays winner'''

    gameDisplay.fill(white)
    largeText = pygame.font.Font('freesansbold.ttf',100)
    TextSurf, TextRect = text_objects(msg, largeText)
    TextRect.center = (400,200)
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()
    time.sleep(2)
    gameIntro()


def chkWinner():
    '''Checks for winner for both multiplaye and singleplayer'''
    winner=None
    global msg,move
    global firstMove
    for container in ALL:
        if(container.chk==0):
            winner='EMPTY'
    for row in WAYS_TO_WIN:
        if(row[0].filler==row[1].filler==row[2].filler!=None):
            if(row[0].filler=='x'):
                winner='X'
                win_row=row
            else :
                winner='O'
                win_row=row
        if(winner is None):
            winner ='TIE'
            win_row=None

    if(move is None): #this one is for multiGameLoop (move is always reset and is not changed in multiGameLoop)
        if(winner=='X'):
            msg="X Won"
            return win_row
        elif(winner=='O'):
            msg="O Won"
            return win_row
        elif(winner=='TIE'):
            msg="TIE"
            win_row=None

    else : #this one is for singleplayer as its value will be changed and will not be none
        if(winner=='X'):
            if(firstMove=="HUMAN"):
                msg="You Won"
                return win_row
            else :
                msg="You Lost"
                return win_row
        elif(winner=='O'):
            if(firstMove=="CPU"):
                msg="You Won"
                return win_row
            else :
                msg="You Lost"
                return win_row
        elif(winner=='TIE'):
            msg="TIE"
            return win_row



def YES():
    '''sets 'move' the first time a singleplayer game is initiated'''
    global move,firstMove
    move = "HUMAN"
    firstMove="HUMAN"
    singleGameLoop()

def NO():
    ''' sets 'move' the first time  a singleplayer game is initiated'''
    global move,firstMove
    move="CPU"
    firstMove="CPU"
    singleGameLoop()

def computerMove():
    '''Determines the 'CPU' move'''
    LEGAL_MOVES=[]
    for container in ALL:
        if(container.chk==0):
            LEGAL_MOVES.append(container.number)
    k=random.choice(LEGAL_MOVES)
    drawRoutine(k)


def singleGameLoop():
    '''Singleplayer game mode'''
    gameDisplay.fill(white)
    largeText = pygame.font.Font('freesansbold.ttf',90)
    TextSurf, TextRect = text_objects("X GOES FIRST", largeText)
    TextRect.center = (400,200)
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(2)

    pygame.event.clear()
    global move
    k=False
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                quitGame()

        drawBoard()
        if(move=="HUMAN"):
            k=chkInput()
            if(k):
                move="CPU"    
        else :
            computerMove()
            move="HUMAN"
        

        for container in ALL:
            if(container.chk==1):
                if(container.filler=='x'):
                    pygame.draw.line(gameDisplay,white,(container.upper_x-15, container.lower_y+15),(container.lower_x+15,container.upper_y-15),5)
                    pygame.draw.line(gameDisplay,white,(container.upper_x-15,container.upper_y-15),(container.lower_x+15,container.lower_y+15),5)
                else:
                    pygame.draw.circle(gameDisplay, white,((container.upper_x+container.lower_x)//2,(container.lower_y+container.upper_y)//2),50,5)

        pygame.display.update()

        win_row=chkWinner()

        if win_row is None:
            if msg is 'TIE':
                time.sleep(0.5)
                afterGame()
        else :
            pygame.draw.line(gameDisplay,red,((win_row[0].upper_x+win_row[0].lower_x)//2,(win_row[0].lower_y+win_row[0].upper_y)//2),((win_row[2].upper_x+win_row[2].lower_x)//2,(win_row[2].lower_y+win_row[2].upper_y)//2),7)
            pygame.display.update()
            time.sleep(1.5)
            afterGame()

        clock.tick(10)
      
def beforeSingle():
    '''Checks who plays first'''
    reset()
    while True:
         for event in pygame.event.get():
            if event.type==pygame.QUIT:
                quitGame()

         gameDisplay.fill(white)
         largeText = pygame.font.Font('freesansbold.ttf',50)
         TextSurf, TextRect = text_objects("Would You like to go first?", largeText)
         TextRect.center = (400,120)
         gameDisplay.blit(TextSurf, TextRect)

         button("YES",170,370,110,40,green,bright_green,YES)
         button("NO",570,370,110,40,red,bright_red,NO)


         pygame.display.update()
         clock.tick(10)

def multiGameLoop():
    '''Multiplayer game mode'''
    reset()
    gameDisplay.fill(white)
    largeText = pygame.font.Font('freesansbold.ttf',90)
    TextSurf, TextRect = text_objects("X GOES FIRST", largeText)
    TextRect.center = (400,200)
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(2)
    while True:
        for event in pygame.event.get() :
            if event.type==pygame.QUIT:
                quitGame()
        drawBoard()
        chkInput()
        for container in ALL:
            if(container.chk==1):
                if(container.filler=='x'):
                    pygame.draw.line(gameDisplay,white,(container.upper_x-15, container.lower_y+15),(container.lower_x+15,container.upper_y-15),5)
                    pygame.draw.line(gameDisplay,white,(container.upper_x-15,container.upper_y-15),(container.lower_x+15,container.lower_y+15),5)
                else:
                    pygame.draw.circle(gameDisplay, white,((container.upper_x+container.lower_x)//2,(container.lower_y+container.upper_y)//2),50,5)
                    
        pygame.display.update()

        win_row=chkWinner()

        if win_row is None:
            if msg is 'TIE':
                time.sleep(0.5)
                afterGame()
        else :
            pygame.draw.line(gameDisplay,red,((win_row[0].upper_x+win_row[0].lower_x)//2,(win_row[0].lower_y+win_row[0].upper_y)//2),((win_row[2].upper_x+win_row[2].lower_x)//2,(win_row[2].lower_y+win_row[2].upper_y)//2),7)
            pygame.display.update()
            time.sleep(1.5)
            afterGame()

        clock.tick(10)



#main
gameIntro()
