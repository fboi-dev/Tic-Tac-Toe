from containers import *
import copy

#for reference
discard = None

class node :
    '''Defines a tree node'''
    def __init__(self,maxOrMin,tempALL,levelbit): #maxOrMin determines whether the node maximizies or minmizes the utility function
        self.containerList=[]
        self.maxOrMin=maxOrMin
        # child is list consisting of child nodes
        self.child=[]
        self.utility=None
        self.levelbit=levelbit
        #tempALL is the container list with the state at which cpu makes its decision

        if (tempALL is not None):
            self.containerList=tempALL
        else :
            initContainerList(self.containerList)

            
    def buildChildList(self):
        global discard
        sum=0
        for container in self.containerList :
            if(container.chk==0) :
                if(self.maxOrMin is 'MAX'):
                    tempALL=copy.deepcopy(self.containerList)
                    tempALL[sum].filler='x'
                    tempALL[sum].chk=1
                    self.child.append(node('MIN',tempALL,self.levelbit+1))
                else :
                    tempALL=copy.deepcopy(self.containerList)
                    tempALL[sum].filler='o'
                    tempALL[sum].chk=1
                    self.child.append(node('MAX',tempALL,self.levelbit+1))
            sum+=1



def maxMinUtil(child,bit): #bit decides whether to maximize(true) or minimize
    '''Maximize or minimize utility function'''
    sum=0
    max=-1000
    min=1000
    index = 0
    if (bit):
        for containerList in child :
           # if (containerList.utility is None):
            #    break
            if (max < containerList.utility):
                max=containerList.utility
                index=sum
            sum+=1
        return max,index
    else :
        for containerList in child :
            #if (containerList.utility is None):
             #   break
            if (min > containerList.utility):
                min=containerList.utility
                index=sum
            sum+=1
        return min,index

def staticEvaluation(n):
    x_value=0 # the number of rows columns and diagonals occupied by 'x'
    o_value=0 # the number of rows columns and diagonals occupied by 'y'
    for count in range(9) :
        if (n.containerList[count].chk ==1 ):
            if (n.containerList[count].filler is 'x'):
                if (count == 4):
                    x_value+=4
                elif (count==0 or count==2 or count==6 or count==8):
                    x_value+=3
                else :
                    x_value+=2
            if (n.containerList[count].filler is 'o'):
                if (count == 4):
                    o_value+=4
                elif (count==0 or count ==2 or count==6 or count==8):
                    o_value+=3
                else :
                    o_value+=2
    return (x_value-o_value)


def minimax(n,mode):#,alpha,beta,mode):
    #n is node
    global discard
    sum=0
    for container in n.containerList:
        if(container.chk==0):
            sum+=1
    if (n.levelbit >= mode or sum==0):
        return (staticEvaluation(n),0)

    else :
        if(n.child == []):
            n.buildChildList()

        for m in n.child :
            m.utility,discard=minimax(m,mode)

        if(n.maxOrMin is 'MAX'):
            max,index=maxMinUtil(n.child,True)
            return(max,index)
        else :
            min,index=maxMinUtil(n.child,False)
            return(min,index)

#for alpha beta pruning
'''
            value = maximin(m,alpha,beta,mode)
            m.utility=value
            if value<beta :
                beta=value
            if beta <= alpha:
                return alpha
    return beta
    '''
'''
def maximin(n,alpha,beta,mode):
    #n is node
    global searchDepth
    searchDepth+=1
    if (searchDepth >= mode):
        return staticEvaluation(n)
    else :
        if(n.child == []):
            n.buildChildList()
        for m in n.child :
            value = minimax(m,alpha,beta,mode)
            m.utility=value
            if value<alpha :
                alpha=value
            if beta <= alpha:
                return alpha
    return alpha
'''

def containerToChange(n,index):
    '''Gives the container index in presentBoard that needs to be changed by the cpu'''
    for j in range(9):
        if(n.containerList[j].filler != n.child[index].containerList[j].filler):
            return j


def intelligentMove(turn,presentBoard,mode=3):
    '''Determines the 'CPU' move'''
    if(turn is 'o'):
        root=node('MIN',presentBoard.copy(),0)#assumption MAX always plays first so 'x' is MAX
    else :
        root=node('MAX',presentBoard.copy(),0)

    root.utility,index=minimax(root,mode)#index is index of max utility child in root.child array
    
    return containerToChange(root,index)
    


if __name__ == "__main__":
    print("Not to executed alone.Intelligently decides moves for Tic Tac Toe game")

