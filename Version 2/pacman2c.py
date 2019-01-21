# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 16:13:56 2018

@author: arthur.gautheron
"""
from math import pi

RotationSelector = { 1: 270*pi/180, 2 : 0*pi/180, 3 : 90*pi/180,4 :180*pi/180}

class PacmanController:
    def __init__(self, model):
        self.model = model
        self.views = []
        self.joueurs= []
        self.board=self.model.Board(15,19,1,3)
        self.ghostIden=0;
        self.game=None;
        self.log=''
    

    def subscribe(self, viewWidget):
        self.views.append(viewWidget)
        
    def update(self):
        for viewWidget in self.views:
            viewWidget.refresh()
    
    def step(self):
            self.game.playStep()
            self.update()
            
    def stopGame(self):
        return not self.game.goAhead()
    
    def endGame(self):
        self.game=None
        
    def setPacmanDir(self,value):
        if value==1:
            self.game.setPacmanDirection(-1,0)  
        elif value==2:
            self.game.setPacmanDirection(0,1)
        elif value==3:
            self.game.setPacmanDirection(1,0)
        elif value==4:
            self.game.setPacmanDirection(0,-1)
        self.update()
    
    def getPacmanDir(self):
        xdir,ydir=self.game.getPacmanDirection()
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
        ans=''
        if type(self.game):
            ans=self.game.getElement(self.model.Vector(lignes,colonnes))
        else:
            ans=self.board.getElement(self.model.Vector(lignes,colonnes))
        return ans
    
    def getBoard(self):
        return str(self.board)
    
    def isGame(self):
        return type(self.game)!=None
    
    def addGhost(self):
        self.game.addGhost(self.model.Ghost(self.ghostIden,self.board))
        self.ghostIden+=1
        self.update()
        
    def listGhosts(self):
        return self.game.getGhosts()
    
    def addWall(self, top_l_ligne,top_l_colonne,bottom_r_ligne,bottom_r_colonne):
        self.game.addWall(top_l_ligne,top_l_colonne,bottom_r_ligne,bottom_r_colonne)
        self.update()
    
    def saveBoard(self, filepath):
        self.game.saveBoard(filepath)
        
    def loadBoard(self, filepath):
        self.game=self.model.Game(self.board)
        self.game.loadBoard(filepath)
    
    def createBoard(self,l_board,c_board,l_cavern,c_cavern):
        self.board=self.model.Board(l_board,c_board,l_cavern,c_cavern)
        self.game=self.model.Game(self.board)

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