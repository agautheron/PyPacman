# -*- coding: utf-8 -*-
import random, csv

class Vector:
    def __init__(self,x=0,y=0):
        self.x=x
        self.y=y
        
    def __add__(self,vector):
        return Vector(self.x+vector.x,self.y+vector.y)
    ## Attention multiplication à droite par la constante
    def __mul__(self, constant):
        self.x=self.x*constant
        self.y=self.y*constant
        return self
    
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def interchange(self):
        return Vector(self.y,self.x)
    
    def __eq__(self,other):
        return self.x==other.x and self.y==other.y
    
    def __neg__(self):
        return Vector(-1*self.x, -1*self.y)
    
    def __sub__(self,vector):
        return Vector(self.x-vector.x,self.y-vector.y)
        
    
    def __repr__(self):
        return '({},{})'.format(self.x,self.y)

class Board:
    def __init__(self, lignes=20, colonnes=40, cavernHeight=3, cavernWidth=3):
        self.lignes = lignes
        self.colonnes = colonnes
        self.board=[[Bullet() for i in range(self.colonnes)] for j in range(self.lignes)]
        ## Borders
        for i in range(self.lignes):
            self.board[i][self.colonnes-1]='xxx '
            self.board[i][0]='xxx '
        for j in range(self.colonnes):
            self.board[0][j]='xxx '
            self.board[self.lignes-1][j]='xxx '
        ## ghostCavern
        if cavernHeight<2:
            cavernHeight=3
        if cavernWidth%2==0:
            cavernWidth+=1
#        self.cavern=Vector(random.randint(1,self.lignes-cavernHeight-1),random.randint(0,self.colonnes-cavernWidth-1))
        self.cavernPosition = Vector(2,8)
        self.cavernWidth = cavernWidth
        self.cavernHeight = cavernHeight
        self.drawCavern()

    def drawCavern(self):
        for j in range(self.cavernWidth):
            self.board[self.cavernPosition.x+self.cavernHeight-1][self.cavernPosition.y+j]="CCC "
            self.board[self.cavernPosition.x][self.cavernPosition.y+j]="CCC "
        ## Top Wall
        self.cavernMiddle = Vector(self.cavernPosition.x+self.cavernHeight//2,self.cavernPosition.y+self.cavernWidth//2)
        self.board[self.cavernPosition.x][self.cavernMiddle.y]="    "#Bullet(0)
        for i in range(self.cavernHeight):
            self.board[self.cavernPosition.x+i][self.cavernPosition.y]='CCC '
            self.board[self.cavernPosition.x+i][self.cavernPosition.y+self.cavernWidth-1]='CCC '
        ##Inside
        for i in range(1,self.cavernHeight-1):
            for j in range(1,self.cavernWidth-1):
                self.board[self.cavernPosition.x+i][self.cavernPosition.y+j]="    "
        ##Exit of the cavern
        for j in range(0,self.cavernWidth-1):
            self.board[self.cavernPosition.x-1][self.cavernMiddle.y+j]=Bullet(1)
            
    def getElement(self, vector):
        if vector.x<self.lignes and vector.y<self.colonnes and vector.x>=0 and vector.y>=0:
            return self.board[vector.x][vector.y]
    
    def getCavernPosition(self):
        return self.cavernMiddle

    def getSize(self):
        return (self.lignes, self.colonnes)
    
    def eat(self,vector):
        bullet = self.board[vector.x][vector.y]
        value = bullet.getState()
        bullet.isEaten()
        return value
    
    def addWall(self,x_init,y_init,x_final,y_final):
        for i in range(max(0,x_init), min(x_final+1,self.lignes+1)):
            for j in range(max(0,y_init), min(y_final+1,self.colonnes+1)):
                if self.board[i][j]!='CCC ':
                    self.board[i][j]='xxx '
        self.drawCavern()

    def save(self, filename):
        dico = dict((key, value) for (key, value) in self.__dict__.items())
        if filename[-4:]!='.csv':
            filename=filename+'.csv'
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            for k in dico.keys():
                if k!='board':
                    writer.writerow([k,dico[k]])
                else:
                    stri=str(self)
                    writer.writerow([k,stri])  

    def load(self, filename):
        dico = dict((key, value) for (key, value) in self.__dict__.items())
        if filename[-4:]!='.csv':
            filename=filename+'.csv'
        with open(filename, newline='') as csvfile:
            filereader = csv.reader(csvfile, delimiter=';')    
            for row in filereader:
               if row[0]=='board': #Reconstruct the board 
                    string=row[1]
                    brd=string.split('\n')
                    xyBrd=[]
                    for l in range(len(brd)):
                        columns=brd[l].split()
                        ## Case of white cell inside the cavern
                        result=1+brd[l].find("   ") #Search the backspace word in the string and add 1 to get a multiple of 4
                        if (result)>0: #If backspace word then  the line above is stricly positive
                            columns.insert(result//4,"   ") #The entire part of a forth of the result value give the index where a backspace word is required
                        for i in range(len(columns)):
                            if columns[i][0]=='b':
                                columns[i]=Bullet(int(columns[i][-1]))
                            else:
                                columns[i]=columns[i]+' '
                                
                        xyBrd.append(columns)
                    setattr(self,row[0],xyBrd)
               elif row[0]=='cavernMiddle':
                    setattr(self,row[0],Vector(int(row[1][1]),int(row[1][3])))
               elif row[0]=='cavernPosition':
                    setattr(self,row[0],Vector(int(row[1][1]),int(row[1][3])))                    
               else:
                    setattr(self,row[0],(type(dico[row[0]]))(row[1])) #Set Attribute and cast type
 
  
    def __str__(self):
        string=''
        for ligne in self.board:
            for j in ligne:
                string+=str(j)
            string+='\n'
        string=string[:-1]
        return string

class Pacman:
    def __init__(self, board,score=0):
        lignes, colonnes = board.getSize()
        self.score=score
        self.name = "Human"
        self.position=Vector(random.randint(0,lignes-1), random.randint(0,colonnes-1))
        self.direction=Vector(0,1)
        while board.getElement(self.position)=='xxx ' or board.getElement(self.position)=='CCC ' or board.getElement(self.position)=='    ' :
            self.position=Vector(random.randint(0,lignes-1), random.randint(0,colonnes-1))
        self.status = 1
        self.score = 0
        
    def setDirection(self,x,y):
        self.direction=Vector(x,y)
        
        #ancienne fonction move
#    def move(self,board):
#        if type(board.getElement(self.position+self.direction))==type(Board(0)):
#            self.position=self.position + self.direction
#            bullet = board.getElement(self.position)
#            if bullet.getState()>0:
#                self.score+=bullet.getState()
#                bullet.isEaten()
        #nouvelle fonction move
    def move(self,board, ghosts_list):
        if type(board.getElement(self.position+self.direction))==type(Bullet(0)):
            self.position=self.position + self.direction
            bullet_status=board.eat(self.position)
            self.score+=bullet_status
            if bullet_status==2:
                self.status=2
                
    def setAlive(self, alive):
        if not(alive):
            self.status=0
            
    def getState(self):
        return self.status
    
    def getDirection(self):
        return self.direction
    
    def getName(self):
        return self.name
    
    def getScore(self):
        return self.score
    
    def getPosition(self):
        return self.position
    
    def __repr__(self):
        return 'PAC ' 
    
class PacmanBot(Pacman):
    def __init__(self,board, level=1):
        super().__init__(board)
        self.name="IA"
        self.level=level
        self.IaFcts={0:self.computeOptDirection0,1:self.computeOptDirection1}
        
    def computeOptDirection0(self,board):
        while (not type(board.getElement(self.position+self.direction))==type(Bullet(0))) or self.direction==Vector(0,0):
            self.direction=random.choice([Vector(0,1),Vector(0,-1),Vector(1,0),Vector(-1,0)])
            
    def computeOptDirection1(self,board):
        while (not type(board.getElement(self.position+self.direction))==type(Bullet(0))) or self.direction==Vector(0,0) or board.getElement(self.position+self.direction)<board.getElement(self.position-self.direction) or board.getElement(self.position+self.direction)<board.getElement(self.position+self.direction.interchange()) or board.getElement(self.position+self.direction)<board.getElement(self.position-self.direction.interchange()) :
            self.direction=random.choice([Vector(0,1),Vector(0,-1),Vector(1,0),Vector(-1,0)])
    
    def move(self,board, ghosts_list):
        self.IaFcts[self.level](board)
        if type(board.getElement(self.position+self.direction))==type(Bullet(0)):
            self.position=self.position + self.direction
            bullet_status=board.eat(self.position)
            self.score+=bullet_status
            if bullet_status==2:
                self.status=2

class Ghost:
    def __init__(self, identifier, board):
        self.status = 2
        self.id= identifier
        self.position=board.getCavernPosition()
        self.direction=Vector(-1,0)
        self.name="Human"

    def getPosition(self):
        return self.position
    
    def getDirection(self):
        return self.direction
    
    def getStatus(self):
        return self.status
    
    def setPosition(self,pos):
        self.position = pos
    
    def setDirection(self, x,y):
        self.direction=Vector(x,y)
           
    def setStatus(self, newStatus):
        self.status = newStatus
        
    def move(self, board, pacmanPos):
        if board.getElement(self.position+self.direction)!="CCC " and board.getElement(self.position+self.direction)!="xxx ":
            self.position=self.position + self.direction


    def __repr__(self):
        return 'G.{}.{} '.format(self.status, self.id)
    
class GhostBot(Ghost):
    def __init__(self,iden,board,level=0):
        super().__init__(iden,board)
        self.name="IA"
        self.level=level
        self.IaFcts={0:self.computeOptDirection0,1:self.computeOptDirection1}
        
    def computeOptDirection0(self,board,pacmanPos):
        while board.getElement(self.position+self.direction)=="CCC " or board.getElement(self.position+self.direction)=="xxx " or self.direction==Vector(0,0):
            self.direction=random.choice([Vector(0,1),Vector(0,-1),Vector(1,0),Vector(-1,0)])
            
    def computeOptDirection1(self,board,pacmanPos):
        pass
#        while board.getElement(self.position+self.direction)=="CCC " or board.getElement(self.position+self.direction)=="xxx " or self.direction==Vector(0,0) or norm(moi)>norm or norm(moi)>norm() or norm(moi)>norm:
#            self.direction=random.choice([Vector(0,1),Vector(0,-1),Vector(1,0),Vector(-1,0)])
#    écrire une fonction norm et faire les cas.
    def move(self,board, pacmanPos):
        self.IaFcts[self.level](board,pacmanPos)
        if board.getElement(self.position+self.direction)!="CCC " and board.getElement(self.position+self.direction)!="xxx ":
            self.position=self.position + self.direction
                

class Bullet:
    def __init__(self,state=1):
        self.state = state
    
    def __lt__(self,bullet2):#self>=bullet2
        if type(bullet2)==type(Bullet()):
            ans=self.state<bullet2.getState()
        else:
            ans = False # on considère qu'un mur est plus faible qu'une bullet, ça nous arrange dans nos tests
        return ans
        
    def getState(self):
        return self.state
    
    def isEaten(self):
        self.state=0
           
    def __repr__(self):
        return 'b.{} '.format(self.state)
    
    
    
if __name__=="__main__":
    board = Board(9,13,1,3)
    print(board)
    print('\n')
    board.addWall(3,8,7,10)
    print(-Vector(1,5))
    p=PacmanBot(board)
    g=Ghost(0,board)
    print(g, g.getStatus())
    g.setStatus(0)
    print(g, g.getStatus())
    b1=Bullet()
    b2=Bullet(2)
    c3='text'
    print(b1<b2)
    print(b2<b1)
    print(b1<c3)    
 