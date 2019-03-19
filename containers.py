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
        #filler is the value that is in the container
        self.filler=None

    def drawCross(self):
        '''Draws crosses takes width and height of surrounding box as input'''
        #x,y are center of box
        self.filler='x'
        self.chk=1

    def drawNought(self):
        '''Draws nought takes center of box as argument'''
        self.filler='o'
        self.chk=1

# init ALL containing all the containers

def initContainerList(ALL):
    ALL.append(containers(300,100,233,100))
    ALL.append(containers(500,300,233,100))
    ALL.append(containers(700,500,233,100))
    ALL.append(containers(300,100,366,233))
    ALL.append(containers(500,300,366,233))
    ALL.append(containers(700,500,366,233))
    ALL.append(containers(300,100,499,366))
    ALL.append(containers(500,300,499,366))
    ALL.append(containers(700,500,499,366))

if __name__ == "__main__":
    print("Not to executed alone. Stores Data Structures for Tic Tac Toe game")

