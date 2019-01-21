# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 16:20:59 2018

@author: Arthur Gautheron
"""

import pacman2 as model

c=''

def Affiche_menu(string):
    c=''
    print(string)
    c=input()
    return c

def start():
    string="Que souhaitez vous faire ? \n"
    string+="0. Charger le plateau de jeu par défaut\n"
    string+="1. Créer le plateau de jeu\n"
    string+="2. Charger une grille \n"
    iden=0;
    game=None;
    string+="Q. Quitter "
    c=Affiche_menu(string)
    while c!='Q':
        if c=='V':
            print(game)
        if c=='0':
            board = model.Board(15,19,1,3)
            board.addWall(2,2,2,16)
            board.addWall(3,8,7,10)
            game=model.Game(board)
            string="Que souhaitez vous faire ? \n"
            string+="V. Voir la grille \n"
            string+="3. Sauvegarder la grille \n"
            string+="4. Ajouter un mur \n"
            string+="5. Ajouter un fantôme \n"
            string+="6. Lister les fantômes existants \n"
            string+="7. Démarrer la partie \n"
            string+="Q. Quitter "
        if c=='1':
            l_board=int(Affiche_menu('Nombre de lignes du plateau ?'))
            c_board=int(Affiche_menu('Nombre de colonnes du plateau ?'))
            l_cavern=int(Affiche_menu('Nombre de lignes de la caverne des fantômes ?'))
            c_cavern=int(Affiche_menu('Nombre de colonnes de la caverne des fantômes ?'))
            board=model.Board(l_board,c_board,l_cavern,c_cavern)
            game=model.Game(board)
            string="Que souhaitez vous faire ? \n"
            string+="V. Voir la grille \n"
            string+="3. Sauvegarder la grille \n"
            string+="4. Ajouter un mur \n"
            string+="5. Ajouter un fantôme \n"
            string+="6. Lister les fantômes existants \n"
            string+="7. Démarrer la partie \n"
            string+="Q. Quitter "
        if c=='2' :
            filepath=str(Affiche_menu('Chemin du fichier à charger ?'))
            board = model.Board(15,19,1,3)
            game=model.Game(board)
            game.loadBoard(filepath)
            print("Grille chargée \n\n")
            string="Que souhaitez vous faire ? \n"
            string+="V. Voir la grille \n"
            string+="3. Sauvegarder la grille \n"
            string+="4. Ajouter un mur \n"
            string+="5. Ajouter un fantôme \n"
            string+="6. Lister les fantômes existants \n"
            string+="7. Démarrer la partie \n"
            string+="Q. Quitter "
        elif c=='3' :
            filepath=str(Affiche_menu('Chemin du fichier de sauvegarde ?'))
            game.saveBoard(filepath)
            print("Grille sauvegardée \n\n")
        elif c=='4':
            top_l_ligne = int(Affiche_menu('Indice de ligne de l\'angle supérieur gauche ?'))
            top_l_colonne = int(Affiche_menu('Indice de colonne de l\'angle supérieur gauche ?'))
            bottom_r_ligne = int(Affiche_menu('Indice de ligne de l\'angle inférieur droit ?'))
            bottom_r_colonne = int(Affiche_menu('Indice de colonne de l\'angle inférieur droit ?'))
            board.addWall(top_l_ligne,top_l_colonne,bottom_r_ligne,bottom_r_colonne)
        elif c=='5':
            game.addGhost(model.Ghost(iden,board))
            iden+=1
        elif c=='6' :
            print(game.getGhosts())
        elif c=='7' :
            game.playStep()
            print(game)
            string="Que souhaitez vous faire ? \n"
            string+="7. Jouer un coup \n"
            string+="8. Changer la direction du pacman \n"
            if len(game.getGhosts()):
                string+="9. Changer la direction d'un fantôme \n"
            string+="Q. Quitter "
        #Changement de la direction du pacman
        elif c=='8':
            dir_y = int(Affiche_menu('Mouvement selon les lignes ?'))
            dir_x = int(Affiche_menu('Mouvement selon les colonnes ?'))
            game.setPacmanDirection(dir_x,dir_y)
        #Changement de la direction du fantôme
        elif c=='9':
            print(game.getGhosts())
            identifier = int(Affiche_menu('Identifiant du fantôme ?'))
            dir_y = int(Affiche_menu('Mouvement selon les lignes ?'))
            dir_x = int(Affiche_menu('Mouvement selon les colonnes ?'))
            game.setGhostDirection(identifier,dir_x,dir_y)
        if not(game.goAhead()):
            c='Q'
            print('Vous avez perdu !')
        else:
            c=Affiche_menu(string)
    print('A plus!')
    
    
if __name__=='__main__':
    start()