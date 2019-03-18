from containers import *

#for reference
'''
root = None
previousBoard=[]
currentNode=None
'''
discard = None

class node :
    '''Defines a tree node'''
    def __init__(self,maxOrMin,tempALL,pos): #maxOrMin determines whether the node maximizies or minmizes the utility function
        self.ALL=[]
        self.maxOrMin=maxOrMin
        # child is list consisting of child nodes
        self.child=[]
        self.utility=None
        #tempALL is the container list from ancestor which has the ancestor's state(filler's of different container)

        #pos is the index of tempALL list which needs to be filled with 'x' or 'o' depending on whether the node is MAX or MIN
        
        #MAX node fills 'x' in all of its child nodes vice-versa for MIN
        
        #if the node is MAX 'o ' is filled at pos
        
        #pos/tempALL is none for root node 
        
        #root node is always MAX
        print("HEY")
        if (tempALL is not None):
            self.ALL=tempALL
            if(self.maxOrMin is 'MAX'):
                tempALL[pos].filler='o'
                tempALL[pos].chk=1
            else :
                tempALL[pos].filler='x'
                tempALL[pos].chk=1
        else :
            initContainerList(self.ALL)

        self.buildChildList()
            
    def buildChildList(self):
        global discard
        sum=0
        for container in self.ALL :
            if(container.chk==0) :
                if(self.maxOrMin is 'MAX'):
                    self.child.append(node('MIN',self.ALL,sum))
                else :
                    self.child.append(node('MAX',self.ALL,sum))
                sum+=1

        #assigning utility
        if (sum==0):
            if(chkWinner2(self.ALL)is not None):
                if(chkWinner2 is 'TIE'):
                    self.utility=0
                elif(chkWinner2 is 'X'):
                    self.utility=1
                else:
                    self.utility=-1
        else :
            if (self.maxOrMin is 'MAX'):
                self.utility,discard = maxMinUtil(self.child,True)
            else:
                self.utility,discard = maxMinUtil(self.child,False)


def maxMinUtil(child,bit): #bit decides whether to maximize(true) or minimize
    '''Maximize or minimize utility function'''
    max=None
    min=None
    sum=0
    index = 0
    if (bit):
        for containerList in child :
            if (max is None):
                max=containerList.utility
                index=sum
            else :
                if (max < containerList.utility):
                    max=containerList.utility
                    index=sum
            sum+=1
        return max,index
    else :
        for containerList in child :
            if (min is None):
                min=containerList.utility
                index=sum
            else :
                if (min > containerList.utility):
                    min=containerList.utility
                    index=sum
            sum+=1
        return min,index


def buildGameTree(): #builds game tree
    global root
    root=node('MAX',None,None)

def chkWinner2(containerList):
    '''Almost same as chkWinner implemented separately(to remove confusion)'''
    WAYS_TO_WIN = ((containerList[0], containerList[1], containerList[2]),
               (containerList[3], containerList[4], containerList[5]),
               (containerList[6], containerList[7], containerList[8]),
               (containerList[0], containerList[3], containerList[6]),
               (containerList[1], containerList[4], containerList[7]),
               (containerList[2], containerList[5], containerList[8]),
               (containerList[0], containerList[4], containerList[8]),
               (containerList[2], containerList[4], containerList[6]))

    winner=None
    for container in containerList:
        if(container.chk==0):
            winner='EMPTY'
    for row in WAYS_TO_WIN:
        if(row[0].filler==row[1].filler==row[2].filler!=None):
            if(row[0].filler=='x'):
                winner='X'
            else :
                winner='O' 
        if(winner is None):
            winner ='TIE'

        return winner

def intelligentMove2(pos,firstMove):
    global discard,currentNode
    '''Identify the child of the currentNode which game's present state'''
    '''Then find the best option from available child nodes'''

    #'index' is index of best option in child array
    if (pos is None): # case when computer makes first move
        discard,index=maximizeUtil(currentNode.child,True)

    else :
        for node in currentNode.child :
            if node.ALL[pos].chk==1 :
                currentNode = node
                break

        #implementing the second part
        if (firstMove is 'HUMAN') : #machine minimizes the utility function
            discard,index=maxMinUtil(currentNode.child,False)
            #print(index)
            currentNode=currentNode.child[index]
        else : # machine maximizes the utility function
            discard,index=maxMinUtil(currentNode.child,True)
            currentNode=currentNode.child[index]

    return index


def intelligentMove1(firstMove,presentBoard):
    '''Determines the 'CPU' move'''
    pos = None # this is the position at which the user placed X or O

    global previousBoard,currentNode,root
    if previousBoard == [] :
        previousBoard=presentBoard
        currentNode=root
        for count in range(0,9) :
            if (presentBoard[count].chk==1):
                pos=count

    else :
        for count in range(0,9):
            if (previousBoard[count].chk==0 and presentBoard[count].chk==1):
                pos=count

    return (intelligentMove2(pos,firstMove))
            



if __name__ == "__main__":
    print("Not to executed alone.Intelligently decides moves for Tic Tac Toe game")

