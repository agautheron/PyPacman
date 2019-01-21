# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 16:20:59 2018

@author: Arthur Gautheron
"""

import model1 as model

c=''

def Affiche_menu(string):
    c=''
    print(string)
    c=input()
    return c

def start():
    liste_joueurs = []
    string="Que souhaitez vous faire ? \n"
    string+="0. Charger le plateau de jeu par défaut\n"
    string+="1. Créer le plateau de jeu\n"
    iden=1;
    game=None;
    string+="Q. Quitter "
    c=Affiche_menu(string)
    while c!='Q':
        if c=='0':
            board = model.Board(15,19,1,3)
            board.addWall(2,2,2,16)
            board.addWall(3,8,7,10)
            game=model.Game(board)
            string="Que souhaitez vous faire ? \n"
            string+="2. Ajouter un mur \n"
            string+="3. Ajouter un fantôme \n"
            string+="4. Lister les fantômes existants \n"
            string+="5. Démarrer la partie \n"
            string+="Q. Quitter "
        if c=='1':
            l_board=int(Affiche_menu('Nombre de lignes du plateau ?'))
            c_board=int(Affiche_menu('Nombre de colonnes du plateau ?'))
            l_cavern=int(Affiche_menu('Nombre de lignes de la caverne des fantômes ?'))
            c_cavern=int(Affiche_menu('Nombre de colonnes de la caverne des fantômes ?'))
            board=model.Board(l_board,c_board,l_cavern,c_cavern)
            game=model.Game(board)
            string="Que souhaitez vous faire ? \n"
            string+="2. Ajouter un mur \n"
            string+="3. Ajouter un fantôme \n"
            string+="4. Lister les fantômes existants \n"
            string+="5. Démarrer la partie \n"
            string+="Q. Quitter "
        if c=='2':
            top_l_ligne = int(Affiche_menu('Indice de ligne de l\'angle supérieur gauche ?'))
            top_l_colonne = int(Affiche_menu('Indice de colonne de l\'angle supérieur gauche ?'))
            bottom_r_ligne = int(Affiche_menu('Indice de ligne de l\'angle inférieur droit ?'))
            bottom_r_colonne = int(Affiche_menu('Indice de colonne de l\'angle inférieur droit ?'))
            board.addWall(top_l_ligne,top_l_colonne,bottom_r_ligne,bottom_r_colonne)
        elif c=='3':
            game.addGhost(model.Ghost(iden,board))
            iden+=1
        elif c=='4' :
            print(game.getGhosts())
        elif c=='5' :
            game.playStep()
            print(game)
            string="Que souhaitez vous faire ? \n"
            string+="5. Jouer un coup \n"
            string+="6. Changer la direction du pacman \n"
            string+="7. Changer la direction d'un fantôme \n"
            string+="Q. Quitter "
        #Changement de la direction du pacman
        elif c=='6':
            dir_y = int(Affiche_menu('Mouvement selon les lignes ?'))
            dir_x = int(Affiche_menu('Mouvement selon les colonnes ?'))
            game.setPacmanDirection(dir_x,dir_y)
        #Changement de la direction du pacman
        elif c=='7':
            print(game.getGhosts())
            identifier = int(Affiche_menu('Identifiant du fantôme ?'))
            dir_y = int(Affiche_menu('Mouvement selon les lignes ?'))
            dir_x = int(Affiche_menu('Mouvement selon les colonnes ?'))
            game.setGhostDirection(identifier,dir_x,dir_y)
        c=Affiche_menu(string)
    print('A plus!')
    
    
if __name__=='__main__':
    start()