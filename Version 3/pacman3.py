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
    
    def __eq__(self,other):
        return self.x==other.x and self.y==other.y
    
    def __neg__(self):
        return Vector(-1*self.x, -1*self.y)
    
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
        self.direction=Vector(0,0)
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
    def __init__(self,board):
        super().__init__(board)
        self.name="IA"
        
    def computeOptDirection(self,board):
        while (not type(board.getElement(self.position+self.direction))==type(Bullet(0))) or self.direction==Vector(0,0):
            self.direction=random.choice([Vector(0,1),Vector(0,-1),Vector(1,0),Vector(-1,0)])
        
    
    def move(self,board, ghosts_list):
        self.computeOptDirection(board)
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
        
    def move(self, board):
        if board.getElement(self.position+self.direction)!="CCC " and board.getElement(self.position+self.direction)!="xxx ":
            self.position=self.position + self.direction


    def __repr__(self):
        return 'G.{}.{} '.format(self.status, self.id)
    
class Bullet:
    def __init__(self,state=1):
        self.state = state
        
    def getState(self):
        return self.state
    
    def isEaten(self):
        self.state=0
           
    def __repr__(self):
        return 'b.{} '.format(self.state)
    
    
class Game:
    def __init__(self,board,pacman=None,nbGhosts=0):
        self.board=board
        self.pacman=pacman
        if not(self.pacman):
            self.pacman=Pacman(self.board)
        initial_bullet= self.board.getElement(self.pacman.getPosition())
        initial_bullet.isEaten()
        self.ghosts_list=[Ghost(i, self.board) for i in range (nbGhosts)]
    
    def playStep(self):
        ghosts_position=[ghost.getPosition() for ghost in self.ghosts_list]
        self.pacman.move(self.board,ghosts_position)
        for ghost in self.ghosts_list:    
            if self.pacman.getState()==2 and ghost.getStatus()==2:
                ghost.setStatus(1)
            elif self.pacman.getState()==1:
                ghost.setStatus(2)
            ghost.move(self.board)
        ghosts_position=[ghost.getPosition() for ghost in self.ghosts_list]
        if self.pacman.getPosition() in ghosts_position:
            iden=ghosts_position.index(self.pacman.getPosition())
            if self.pacman.getState()==2:
                self.ghosts_list[iden].setStatus(0)
                print(self.ghosts_list[iden])
            else:
                self.pacman.setAlive(False)
    
    def getElement(self,position):
        rep=''
        ghosts_position=[ghost.getPosition() for ghost in self.ghosts_list]
        if position==self.pacman.getPosition():
            rep=self.pacman.__repr__()
        elif position in ghosts_position:
            iden=ghosts_position.index(position)
            rep=self.ghosts_list[iden].__repr__()
#            rep=rep[:-1]+'.'+str(self.ghosts_list[iden].getStatus())+' '
        else:
            rep=str(self.board.getElement(position))
        return rep
    
    def goAhead(self):
        return self.pacman.getState()
    
    def getGhosts(self):
        return self.ghosts_list
    
    def addGhost(self,ghost):
        ghost.setPosition(self.board.getCavernPosition())
        self.ghosts_list.append(ghost)
    
    def addWall(self,top_l_ligne,top_l_colonne,bottom_r_ligne,bottom_r_colonne):
        self.board.addWall(top_l_ligne,top_l_colonne,bottom_r_ligne,bottom_r_colonne)
        
    def saveBoard(self, filepath):
        self.board.save(filepath)
    
    def loadBoard(self, filepath):
        brd = Board()
        brd.load(filepath)
        self = self.__init__(brd)
        
    def getScore(self):
        return self.pacman.getScore()
    
    def setPacmanDirection(self,xdir,ydir):
        self.pacman.setDirection(xdir,ydir)
        
    def getPacmanDirection(self):
        direc=self.pacman.getDirection()
        return [direc.x, direc.y]
        
    def setGhostDirection(self,identifier,xdir,ydir):
        self.ghosts_list[identifier].setDirection(xdir,ydir)
    
    def __repr__(self):
        boardstring=''
        ghosts_positions=[]
        for ghost in self.ghosts_list:
            ghosts_positions.append(ghost.getPosition())
        lignes,colonnes=self.board.getSize()
        for i in range(lignes):
            for j in range(colonnes):
                if Vector(i,j) in ghosts_positions:
                    indice = ghosts_positions.index(Vector(i,j))
                    boardstring+=self.ghosts_list[indice].__repr__()
                elif Vector(i,j)==self.pacman.position:
                    boardstring+=self.pacman.__repr__()
                else:
                    boardstring+=str(self.board.getElement(Vector(i,j)))
            boardstring+='\n'
        return boardstring
            
    
if __name__=="__main__":
    board = Board(15,19,1,3)
    board.addWall(2,2,2,16)
    print(board)
    board.save('test2')
    board.addWall(3,8,7,10)
    print(board)
    board.load('test2')
    print(board)
    print('\n')
    board.addWall(3,8,7,10)
    game=Game(board)
    print(game)
    for k in range(10):
        game.playStep()
        print(game)
    print(game.getScore())
    g=Ghost(0,board)
    print(g, g.getStatus())
    g.setStatus(0)
    print(g, g.getStatus())
    
    