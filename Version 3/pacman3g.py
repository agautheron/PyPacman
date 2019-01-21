# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 16:54:51 2018

@author: arthur.gautheron
"""

import sys, os
from pacman3c import *
import pacman3 as pacman
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *# QApplication, QMainWindow
    
CELL_PIXMAP = dict()

#CELL_PIXMAP={'b.1 ': QPixmap('Data\\b.1.png'),
#             'b.2 ': QPixmap('Data\\b.2.png'),
#             'b.3 ': QPixmap('Data\\b.3.png'),
#             'CCC ': QPixmap('Data\\CCC.png'),
#             'xxx ': QPixmap('Data\\XXX.png'),
#             'PAC ': QPixmap('Data\\PAC.png'),
#             'G.0.0 ': QPixmap('Data\\G.0.0.png'),
#             'G.1.0 ': QPixmap('Data\\G.1.0.png'),
#             'G.2.0 ': QPixmap('Data\\G.2.0.png'),
#             'G.0.1 ': QPixmap('Data\\G.0.1.png'),
#             'G.1.1 ': QPixmap('Data\\G.1.1.png'),
#             'G.2.1 ': QPixmap('Data\\G.2.1.png')
#        }


class NewGameDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setVisible(True)
        self.setWindowTitle("New Game - Settings")
        self.layout = QFormLayout()
        self.e1 = QSpinBox()
        self.e1.setSingleStep(1)
        self.e1.setMinimum(0)
        self.e1.setValue(15)
        self.e1.setMaximum(100)
        self.layout.addRow("Nombre de lignes du plateau ?",self.e1)
        self.e2 = QSpinBox()
        self.e2.setSingleStep(1)
        self.e2.setMinimum(0)
        self.e2.setValue(19)
        self.e2.setMaximum(100)
        self.layout.addRow("Nombre de colonnes du plateau ?",self.e2)
        self.e3 = QSpinBox()
        self.e3.setSingleStep(1)
        self.e3.setMinimum(0)
        self.e3.setValue(1)
        self.e3.setMaximum(self.e1.value())
        self.layout.addRow("Nombre de lignes de la caverne des fantômes ?",self.e3)
        self.e4 = QSpinBox()
        self.e4.setSingleStep(1)
        self.e4.setMinimum(0)
        self.e4.setValue(3)
        self.e4.setMaximum(self.e2.value())
        self.layout.addRow("Nombre de colonnes de la caverne des fantômes ?",self.e4)
        self.validButton = QPushButton('Ok')
        self.validButton.clicked.connect(self.validation)
        self.cancelButton = QPushButton('Cancel')
        self.cancelButton.clicked.connect(self.cancelation)
        self.layout.addRow(self.cancelButton,self.validButton)
        self.setLayout(self.layout)
        self.adjustSize()
    
    def addingGhost(self):
        pass
    
    def validation(self):
        return self.accept()
    
    def cancelation(self):
        self.reject()
        

class CustomMapDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setVisible(True)
        self.setWindowTitle("Custom Map - Settings")
        self.layout = QFormLayout()
        self.e1 = QSpinBox()
        self.e1.setSingleStep(1)
        self.e1.setMinimum(0)
        self.e1.setValue(15)
        self.e1.setMaximum(100)
        self.layout.addRow("Nombre de lignes du plateau ?",self.e1)
        self.e2 = QSpinBox()
        self.e2.setSingleStep(1)
        self.e2.setMinimum(0)
        self.e2.setValue(19)
        self.e2.setMaximum(100)
        self.layout.addRow("Nombre de colonnes du plateau ?",self.e2)
        self.e3 = QSpinBox()
        self.e3.setSingleStep(1)
        self.e3.setMinimum(0)
        self.e3.setValue(1)
        self.e3.setMaximum(self.e1.value())
        self.layout.addRow("Nombre de lignes de la caverne des fantômes ?",self.e3)
        self.e4 = QSpinBox()
        self.e4.setSingleStep(1)
        self.e4.setMinimum(0)
        self.e4.setValue(3)
        self.e4.setMaximum(self.e2.value())
        self.layout.addRow("Nombre de colonnes de la caverne des fantômes ?",self.e4)
        self.validButton = QPushButton('Ok')
        self.validButton.clicked.connect(self.validation)
        self.cancelButton = QPushButton('Cancel')
        self.cancelButton.clicked.connect(self.cancelation)
        self.layout.addRow(self.cancelButton,self.validButton)
        self.setLayout(self.layout)
        self.adjustSize()
        
    def validation(self):
        return self.accept()
    
    def cancelation(self):
        self.reject()
        
class AddWallDialog(QDialog):
    def __init__(self,lines, columns):
        super().__init__()
        self.setVisible(True)
        self.setWindowTitle("Add Wall - Settings")
        self.layout = QFormLayout()
        self.e1 = QSpinBox()
        self.e1.setSingleStep(1)
        self.e1.setMaximum(lines)
        self.e1.valueChanged.connect(self.update_e3)
        self.layout.addRow('Indice de ligne de l\'angle supérieur gauche ?',self.e1)
        self.e2 = QSpinBox()
        self.e2.setSingleStep(1)
        self.e2.setMaximum(columns)
        self.e2.valueChanged.connect(self.update_e4)
        self.layout.addRow('Indice de colonne de l\'angle supérieur gauche ?',self.e2)
        self.e3 = QSpinBox()
        self.e3.setSingleStep(1)
        self.e3.setMinimum(int(self.e1.value()))
        self.e3.setMaximum(lines)
        self.layout.addRow('Indice de ligne de l\'angle inférieur droit ?',self.e3)
        self.e4 = QSpinBox()
        self.e4.setSingleStep(1)
        self.e4.setMinimum(int(self.e2.value()))
        self.e4.setMaximum(columns)
        self.layout.addRow('Indice de colonne de l\'angle inférieur droit ?',self.e4)
        self.validButton = QPushButton('Ok')
        self.validButton.clicked.connect(self.validation)
        self.cancelButton = QPushButton('Cancel')
        self.cancelButton.clicked.connect(self.cancelation)
        self.layout.addRow(self.cancelButton,self.validButton)
        self.setLayout(self.layout)
        self.adjustSize()
        
    def update_e3(self):
        self.e3.setMinimum(int(self.e1.value()))
        
    def update_e4(self):
        self.e4.setMinimum(int(self.e2.value()))
        
        
    def validation(self):
        return self.accept()
    
    def cancelation(self):
        self.reject()
        
class CellWidget(QLabel):


    def __init__(self,parent,controller,value):
        super().__init__(parent)
        self.controller=controller
        self.pixmap=QPixmap()
        self.setScaledContents(True)
        self.setPixmap(self.pixmap)
        self.path=''
        self.value=''
        
    def refresh(self,value):
        if type(value):
            self.value=value
            self.pixmap=CELL_PIXMAP[value]#QPixmap(self.path)
            if value=="PAC ":
                T = QTransform()
                T.rotateRadians(self.controller.getPacmanDir())
                self.pixmap=self.pixmap.transformed(T)
            self.setScaledContents(True)
            self.setPixmap(self.pixmap)
            
    def getValue(self):
        return self.value
    
class BoardWidget(QWidget):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.loadPixmaps()
        self.parent = parent
        self.controller = controller
        self.controller.subscribe(self)
        self.layout = QGridLayout()
        self.layout.setHorizontalSpacing(0)
        self.layout.setVerticalSpacing(0)
        self.lignes, self.colonnes =self.controller.getBoardSize()
        self.cells=[[CellWidget(self,self.controller,'') for j in range(self.colonnes)] for i in range(self.lignes)]
        for row in range(self.lignes):
            for column in range(self.colonnes):
                self.layout.addWidget(self.cells[row][column],row,column)
        self.setLayout(self.layout)

    def loadPixmaps(self):
        CELL_PIXMAP['b.0 '] = QPixmap()
        CELL_PIXMAP['b.1 '] = QPixmap('Data\\b.1.png')
        CELL_PIXMAP['b.2 '] = QPixmap('Data\\b.2.png')
        CELL_PIXMAP['b.3 '] = QPixmap('Data\\b.3.png')
        CELL_PIXMAP['CCC '] = QPixmap('Data\\CCC.png')
        CELL_PIXMAP['xxx '] = QPixmap('Data\\XXX.png')
        CELL_PIXMAP['PAC '] = QPixmap('Data\\PAC.png')
        CELL_PIXMAP['G.0.0 '] = QPixmap('Data\\G.0.0.png')
        CELL_PIXMAP['G.1.0 '] = QPixmap('Data\\G.1.0.png')
        CELL_PIXMAP['G.2.0 '] = QPixmap('Data\\G.2.0.png')
        CELL_PIXMAP['G.0.1 '] = QPixmap('Data\\G.0.1.png')
        CELL_PIXMAP['G.1.1 '] = QPixmap('Data\\G.1.1.png')
        CELL_PIXMAP['G.2.1 '] = QPixmap('Data\\G.2.1.png')
        CELL_PIXMAP['    '] = QPixmap()

    def refresh(self):
        for row in range(self.lignes):
            for column in range(self.colonnes):
                cell=self.cells[row][column]
                boardValue=self.controller.getCellValue(row,column)
                if cell.getValue()!=boardValue:
                    cell.refresh(boardValue)
        self.setLayout(self.layout)

class HomeWindow(QMainWindow):

    def __init__(self, app, controller, windowTitle):
        super().__init__()
        self.setVisible(True)
        self.setWindowTitle(windowTitle)
        self.app = app
        self.controller = controller
        self.playTimer=QTimer()
        self.playTimer.stop()
        self.playTimer.setSingleShot(False)
        self.playTimer.timeout.connect(self.step)
        self.playTimer.setInterval(100)
        self.mainMenu = self.menuBar()
        self.init_menu()
        self.initUi()
    
    def keyPressEvent(self, event):
        touche = event.key()
        if touche == Qt.Key_Down:
            self.controller.setPacmanDir(3)
        if touche == Qt.Key_Right:
            self.controller.setPacmanDir(2)
        if touche == Qt.Key_Up:
            self.controller.setPacmanDir(1)
        if touche == Qt.Key_Left:
            self.controller.setPacmanDir(4)
        if touche == Qt.Key_P:
            if self.playTimer.isActive():
                self.playTimer.stop()
            else:
                self.playTimer.start()
    
    def game_menu(self):
        self.mainMenu.clear()
        
        fileMenu = self.mainMenu.addMenu('&File')
        
        fileMenuResetAction = QAction("&Home", self)
        fileMenuResetAction.setShortcut("Ctrl+H")
        fileMenuResetAction.setStatusTip('Home of the App')
        fileMenuResetAction.triggered.connect(self.home)
        fileMenu.addAction(fileMenuResetAction)
                
        fileMenuSaveAction = QAction('&Save Map', self)
        fileMenuSaveAction.setShortcut("Ctrl+S")
        fileMenuSaveAction.setStatusTip('Save current Map')
        fileMenuSaveAction.triggered.connect(self.saveMap)
        fileMenu.addAction(fileMenuSaveAction)
        
        fileMenuQuitAction = QAction("&Quit", self)
        fileMenuQuitAction.setShortcut("Ctrl+Q")
        fileMenuQuitAction.setStatusTip('Leave The App')
        fileMenuQuitAction.triggered.connect(self.close)

        fileMenu.addAction(fileMenuQuitAction)
        
        gameMenu = self.mainMenu.addMenu('&Game')
        gameMenuWallAction = QAction("&Add Wall", self)
        gameMenuWallAction.setShortcut("Ctrl+W")
        gameMenuWallAction.setStatusTip('Ajouter un mur')
        gameMenuWallAction.triggered.connect(self.addWall)

        gameMenu.addAction(gameMenuWallAction)
        
        gameMenuGhostAction = QAction("&Add Ghost", self)
        gameMenuGhostAction.setShortcut("Ctrl+G")
        gameMenuGhostAction.setStatusTip('Ajouter un fantôme')
        gameMenuGhostAction.triggered.connect(self.addGhost)

        gameMenu.addAction(gameMenuGhostAction)
        
        gameMenuListGhostAction = QAction("&List Ghost", self)
        gameMenuListGhostAction.setShortcut("Ctrl+Shift+G")
        gameMenuListGhostAction.setStatusTip('Liste les fantômes')
        gameMenuListGhostAction.triggered.connect(self.listGhosts)

        gameMenu.addAction(gameMenuListGhostAction)
        
        
        gameMenuStartAction = QAction("&New Game", self)
        gameMenuStartAction.setShortcut("Ctrl+Return")
        gameMenuStartAction.setStatusTip('Créer la partie')
        gameMenuStartAction.triggered.connect(self.newGame)

        gameMenu.addAction(gameMenuStartAction)
        
    def home(self):
        self.close()
        self.__init__(self.app, self.controller, self.windowTitle())
        
    def saveMap(self):
        fileName = QFileDialog.getSaveFileName(self, 'Save Map', os.getcwd(),"CSV files (*.csv)")
        self.controller.saveBoard(fileName[0])
        
    def addWall(self):
        lines,columns = self.controller.getBoardSize()
        d = AddWallDialog(lines,columns)
        if (d.exec()== QDialog.Accepted):
            top_l_ligne,top_l_colonne,bottom_r_ligne,bottom_r_colonne = d.e1.value(), d.e2.value(), d.e3.value(), d.e4.value()
            self.controller.addWall(top_l_ligne,top_l_colonne,bottom_r_ligne,bottom_r_colonne)
    
    def newGame(self):
        
        self.playTimer.start()
    
    def step(self):
        if self.controller.stopGame():
            self.playTimer.stop()
            self.home()
        else:
            self.controller.step()
            
    def addGhost(self):
        self.controller.addGhost()
        
    def listGhosts(self):
        list_ghosts=self.controller.listGhosts()
        d=QDialog()
        d.setWindowTitle('Ghosts in the Game')
        layout=QHBoxLayout()
        for ghost in list_ghosts:
            name=str(ghost)[:-1]
            ghostView=QVBoxLayout()
            label=QLabel()
            label.setScaledContents(True)
            label.setPixmap(QPixmap('Data\\'+name+'.png'))
            ghostView.addWidget(label)
            ghostView.addWidget(QLabel("Ghost n°{}".format(int(name[-1]))))
            layout.addLayout(ghostView)
        d.setLayout(layout)
        d.exec()
    
    def init_menu(self):
        
        fileMenu = self.mainMenu.addMenu('&File')
        # Define the action for a new game
        newMenu = fileMenu.addMenu('&New')
        newMenuStandardMapAction = QAction('&Standard Map', self)
        newMenuStandardMapAction.setShortcut("Ctrl+Shift+N")
        newMenuStandardMapAction.setStatusTip('Load a Standard Map')
        newMenuStandardMapAction.triggered.connect(self.loadStandardMap)
        newMenu.addAction(newMenuStandardMapAction)
        
        newMenuLoadMapAction = QAction('&Load Map', self)
        newMenuLoadMapAction.setShortcut("Ctrl+O")
        newMenuLoadMapAction.setStatusTip('Load a saved Map')
        newMenuLoadMapAction.triggered.connect(self.loadSavedMap)
        newMenu.addAction(newMenuLoadMapAction)
        
        newMenuCustomMapAction = QAction('&Custom Map', self)
        newMenuCustomMapAction.setShortcut("Ctrl+N")
        newMenuCustomMapAction.setStatusTip('Create a Custom Map')
        newMenuCustomMapAction.triggered.connect(self.loadCustomMap)
        newMenu.addAction(newMenuCustomMapAction)
        # Define the action for exit
        fileMenuQuitAction = QAction("&Quit", self)
        fileMenuQuitAction.setShortcut("Ctrl+Q")
        fileMenuQuitAction.setStatusTip('Leave The App')
        fileMenuQuitAction.triggered.connect(self.close)

        fileMenu.addAction(fileMenuQuitAction)
    
    
    def initUi(self):
        self.center = QLabel("")
        self.setCentralWidget(self.center)
    
    def loadStandardMap(self):
        self.center = BoardWidget(self, self.controller)
        self.controller.createBoard(15,19,1,3)
        self.setWindowTitle("Pacman V3")
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.foregroundRole(), Qt.white)
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)
        self.center.refresh()
        self.game_menu()
        self.setCentralWidget(self.center)

    def loadSavedMap(self):
        fileName = QFileDialog.getOpenFileName(self, 'Open file', os.getcwd(),"CSV files (*.csv)")
        self.controller.loadBoard(fileName[0])
        self.center = BoardWidget(self, self.controller)
        self.setWindowTitle("Pacman V3")
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.foregroundRole(), Qt.white)
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)
        self.center.refresh()
        self.game_menu()
        self.setCentralWidget(self.center)
        
    def loadCustomMap(self):
#        l_board,ok = QInputDialog.getInt(self,"Custom Map",'Nombre de lignes du plateau ?')
#        c_board,ok = QInputDialog.getInt(self,"Custom Map",'Nombre de colonnes du plateau ?')
#        l_cavern,ok = QInputDialog.getInt(self,"Custom Map",'Nombre de lignes de la caverne des fantômes ?')
#        c_cavern,ok = QInputDialog.getInt(self,"Custom Map",'Nombre de colonnes de la caverne des fantômes ?')
        d = CustomMapDialog()
        if (d.exec()== QDialog.Accepted):
            l_board,c_board,l_cavern,c_cavern = d.e1.value(), d.e2.value(), d.e3.value(), d.e4.value()
        self.center = BoardWidget(self, self.controller)
        self.controller.createBoard(l_board,c_board,l_cavern,c_cavern)
        self.setWindowTitle("Pacman V3")
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.foregroundRole(), Qt.white)
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)
        self.center.refresh()
        self.game_menu()
        self.setCentralWidget(self.center)
        
def main():
    pacmanCtrl = PacmanController(pacman)
    app = QApplication(sys.argv)

    fenetre = HomeWindow(app, pacmanCtrl, 'Pacman 2')
    fenetre.setWindowIcon(QIcon('Data\PAC.png'))
    fenetre.setVisible(True)
    fenetre.show()
    app.exec()

if __name__ == '__main__':
    main()