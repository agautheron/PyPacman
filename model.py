# -*- coding: utf-8 -*-
import random

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
        self.position=Vector(random.randint(0,lignes-1), random.randint(0,colonnes-1))
        self.direction=Vector(0,1)
        while board.getElement(self.position)=='xxx ':
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
    def move(self,board):
        if type(board.getElement(self.position+self.direction))==type(Bullet(0)):
            self.position=self.position + self.direction
            bullet_status=board.eat(self.position)
            self.score+=bullet_status
            if bullet_status>1:
                self.status=2
            
    def getScore(self):
        return self.score
    
    def getPosition(self):
        return self.position
    
    def __repr__(self):
        return 'PAC '    
    
class Ghost:
    def __init__(self, identifier, board):
        self.alive = True
        self.id= identifier
        self.position=board.getCavernPosition()
        self.direction=Vector(-1,0)

    def getPosition(self):
        return self.position
    
    def getDirection(self):
        return self.direction
    
    def getState(self):
        return self.alive
    
    def setPosition(self,pos):
        self.position = pos
    
    def setDirection(self, x,y):
        self.direction=Vector(x,y)
    
    def setAlive(self, alive):
        self.alive = alive

    def move(self,board):
        if board.getElement(self.position+self.direction)!="CCC " and board.getElement(self.position+self.direction)!="xxx ":
            self.position=self.position + self.direction
#            bullet = board.getElement(self.position)
#            if bullet.getState()>0:
#                self.score+=bullet.getState()
#                bullet.isEaten()
                

    def __repr__(self):
        return 'G.{} '.format(self.id)
    
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
    def __init__(self,board,pacman=None,nbGhosts=1):
        self.board=board
        self.pacman=pacman
        if not(self.pacman):
            self.pacman=Pacman(self.board)
        initial_bullet= self.board.getElement(self.pacman.getPosition())
        initial_bullet.isEaten()
        self.ghosts_list=[Ghost(i, self.board) for i in range (nbGhosts)]
    
    def playStep(self):
        self.pacman.move(self.board)
        for ghost in self.ghosts_list:
            ghost.move(self.board)
    
    def getGhosts(self):
        return self.ghosts_list
        
    def addGhost(self,ghost):
        ghost.setPosition(self.board.getCavernPosition())
        self.ghosts_list.append(ghost)
        
    def getScore(self):
        return self.pacman.getScore()
    
    def setPacmanDirection(self,xdir,ydir):
        self.pacman.setDirection(xdir,ydir)
        
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
                if Vector(i,j)==self.pacman.position:
                    boardstring+=self.pacman.__repr__()
                elif Vector(i,j) in ghosts_positions:
                    indice = ghosts_positions.index(Vector(i,j))
                    boardstring+=self.ghosts_list[indice].__repr__()
                else:
                    boardstring+=str(self.board.getElement(Vector(i,j)))
            boardstring+='\n'
        return boardstring
            
    
if __name__=="__main__":
    import random
    board = Board(15,19,1,3)
    board.addWall(2,2,2,16)
    board.addWall(3,8,7,10)
    print(board)
    print('\n')
    game=Game(board)
    print(game)
    for k in range(10):
        game.playStep()
        print(game)
    print(game.getScore())
