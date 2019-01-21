# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 16:13:56 2018

@author: arthur.gautheron
"""
from math import pi

#MapSelector={0:self.defaultGame, 1:self.loadGame, 2:self.customGame}
RotationSelector = { 1: 270*pi/180, 2 : 0*pi/180, 3 : 90*pi/180,4 :180*pi/180}

class PacmanController:
    def __init__(self, model):
        self.model = model
        self.views = []
        self.joueurs= []
        self.board=self.model.Board(15,19,1,3)
        self.ghostIden=0;
        self.pacman=None;
        self.ghostsList=[]
        self.log=''
    

    def subscribe(self, viewWidget):
        self.views.append(viewWidget)
        
    def update(self):
        for viewWidget in self.views:
            viewWidget.refresh()
    
    def step(self):
        ghosts_position=[ghost.getPosition() for ghost in self.ghostsList]
        self.pacman.move(self.board,ghosts_position)
        for ghost in self.ghostsList:    
            if self.pacman.getState()==2 and ghost.getStatus()==2:
                ghost.setStatus(1)
            elif self.pacman.getState()==1:
                ghost.setStatus(2)
        if self.pacman.getPosition() in ghosts_position:
            iden=ghosts_position.index(self.pacman.getPosition())
            if self.pacman.getState()==2:
                self.ghostsList[iden].setStatus(0)
            else:
                self.pacman.setAlive(False)
        for ghost in self.ghostsList:
            ghost.move(self.board, self.pacman.getPosition())
        self.update()
            
    def stopGame(self):
        return not self.pacman.getState()
    
    def endGame(self):
        self.pacman=None
        
    def setPacmanDir(self,value):
        if value==1:
            self.pacman.setDirection(-1,0)  
        elif value==2:
            self.pacman.setDirection(0,1)
        elif value==3:
            self.pacman.setDirection(1,0)
        elif value==4:
            self.pacman.setDirection(0,-1)
        self.update()
    
    def getPacmanDir(self):
        direc=self.pacman.getDirection()
        xdir,ydir=direc.getX(),direc.getY()
        ans=0
        if xdir==-1:
            ans = RotationSelector[1]
        elif ydir==1:
            ans = RotationSelector[2]
        elif xdir==1:
            ans = RotationSelector[3]
        elif ydir==-1:
            ans = RotationSelector[4]
        return ans
    
    def getBoardSize(self):
        return self.board.getSize()
    
    def getCellValue(self,lignes,colonnes):
        rep=''
        position=self.model.Vector(lignes,colonnes)
        if type(self.pacman):
            rep=''
            ghosts_position=[ghost.getPosition() for ghost in self.ghostsList]
            if position==self.pacman.getPosition():
                rep=self.pacman.__repr__()
            elif position in ghosts_position:
                iden=ghosts_position.index(position)
                rep=self.ghostsList[iden].__repr__()
            else:
                rep=str(self.board.getElement(position))
        else:
            rep=str(self.board.getElement(position))
        return rep
    
    def getBoard(self):
        return str(self.board)
    
    def isGame(self):
        return type(self.pacman)!=None
            
    def listGhosts(self):
        return self.ghostsList
    
    def addWall(self, top_l_ligne,top_l_colonne,bottom_r_ligne,bottom_r_colonne):
        self.board.addWall(top_l_ligne,top_l_colonne,bottom_r_ligne,bottom_r_colonne)
        self.update()
        
    def saveBoard(self, filepath):
        self.board.save(filepath)
        
    def loadGame(self, filepath, pacmanType, GhostsType):
        self.gameType=1
        self.mapFilePath=filepath
        self.board.load(filepath)
        self.newGame(pacmanType,GhostsType)
        self.update()
    
    def defaultGame(self, pacmanType, GhostsType):
        self.gameType=0
        self.board = self.createBoard(15,19,1,3)
        self.newGame(pacmanType,GhostsType)
        self.update()
    
    def customGame(self, l_board,c_board,l_cavern,c_cavern,pacmanType, GhostsType):
        self.gameType=2
        self.mapSize={'l_board':l_board,'c_board':c_board,'l_cavern':l_cavern,'c_cavern':c_cavern}
        self.board = self.createBoard(l_board,c_board,l_cavern,c_cavern)
        self.newGame(pacmanType,GhostsType)
        self.update()
        
    def createBoard(self,l_board,c_board,l_cavern,c_cavern):
        self.board=self.model.Board(l_board,c_board,l_cavern,c_cavern)
        self.game=self.model.Game(self.board)

    def newGame(self,pacmanType="Human",ghostListType=[]):
        if pacmanType=="Human":
            self.pacman=self.model.Pacman(self.board)
        else:
            self.pacman=self.model.PacmanBot(self.board,int(pacmanType[-1]))
        self.board.eat(self.pacman.getPosition())
        self.ghostsList=[]
        for i in range(len(ghostListType)):
            if ghostListType[i]=="Human":
                self.ghostsList.append(self.model.Ghost(i,self.board))
            else:
                self.ghostsList.append(self.model.GhostBot(i, self.board,int(ghostListType[i][-1])))
        self.update()
    
       
    # def addGhost(self,ghost):
        # ghost.setPosition(self.board.getCavernPosition())
        # self.ghostsList.append(ghost)

    def getScore(self):
        return self.pacman.getScore()
            
    def setGhostDirection(self,identifier,xdir,ydir):
        self.ghostsList[identifier].setDirection(xdir,ydir)
    
    # def __repr__(self):
        # boardstring=''
        # ghosts_positions=[]
        # for ghost in self.ghostsList:
            # ghosts_positions.append(ghost.getPosition())
        # lignes,colonnes=self.board.getSize()
        # for i in range(lignes):
            # for j in range(colonnes):
                # if Vector(i,j) in ghosts_positions:
                    # indice = ghosts_positions.index(Vector(i,j))
                    # boardstring+=self.ghostsList[indice].__repr__()
                # elif Vector(i,j)==self.pacman.position:
                    # boardstring+=self.pacman.__repr__()
                # else:
                    # boardstring+=str(self.board.getElement(Vector(i,j)))
            # boardstring+='\n'
        # return boardstring
            
    
#    def getPlayerName(self,iden):
#        return self.joueurs[iden].getNom()
#    
#    def getPlayerHand(self,iden):
#        modelHand = self.joueurs[iden].getMain()
#        graphicHand =  []
#        for card in modelHand:
#            graphicHand.append('.\\cartes_png\\'+repr(card)+'.png')
#        if self.joueurs[iden].getTapis()==0:
#            for i in range(len(graphicHand)):
#                graphicHand[i]='.\\cartes_png\\dos.png'
#        return graphicHand
#    
#    def getPlayerCombinaison(self,iden):
#        return str(self.joueurs[iden].getCombinaison().name())
#    
#    def getPlayerAmount(self,iden):
#        return '{} €'.format(self.joueurs[iden].getTapis())
#    
#    def getNumberPlayers(self):
#        return 4
#    
#    def getLog(self):
#        return self.log
#        
#    def demarrer_partie(self):  
#        self.partie = self.model.Partie(self.joueurs)
#        self.log+='\n La partie démarre...\nQue le meilleur gagne \n'
#        
#    def creer_joueur(self, nom):
#        self.joueurs.append(self.model.Joueur(nom,20))
#        self.log+='{} a rejoint la table \n'.format(nom)
#        self.avertir()
#    
#    def joueurs_inscrits(self):
#        return len(self.joueurs)
#    
#    def inviter_abc(self):
#        self.joueurs.append(self.model.Joueur('Alice',20))
#        self.log+='Alice a rejoint la table \n'
#        self.joueurs.append(self.model.Joueur('Bob',20))
#        self.log+='Bob a rejoint la table \n'
#        self.joueurs.append(self.model.Joueur('Carl',20))
#        self.log+='Carl a rejoint la table \n'
#        self.avertir()
#    
#    def getGagnant(self):
#        return self.partie.getGagnant()
#    
#    def jouer_coup(self):
#        self.log+='Un coup a été joué\n'
#        nom_gagnant = self.partie.jouer()
#        self.log+='{} a gagné le coup\n\n'.format(nom_gagnant)
#        self.avertir()
#    
#    def fin_partie(self):
#        gagnant=self.partie.getGagnant()
#        self.joueurs=[]
#        self.croupier=self.model.Croupier()
#        self.partie=None
#        self.log=''
#        return gagnant.getNom()