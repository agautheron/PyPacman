# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 16:54:51 2018

@author: arthur.gautheron
"""

import sys, os
from pacman6c import *
import pacman6 as pacman
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *# QApplication, QMainWindow
    
CELL_PIXMAP = dict()

STATUS_PIXMAP = dict()
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
        self.loadPixmaps()
        self.setWindowTitle("New Game - Settings")
        self.mainLayout=QVBoxLayout()
        # Player View
        self.playersGroupBox = QGroupBox("Players")
        self.playersGroupBox.setStyleSheet("QGroupBox{ color: white;}")
        self.playersLayout = QFormLayout()
        self.input=[]
        self.input.append(QComboBox())
        self.input[0].addItem("Human")
        self.input[0].addItem("IA 0")
        self.input[0].addItem("IA 1")
        self.labels=[]
        self.shortcuts=[]
        self.labels.append(QLabel())
        self.labels[0].setScaledContents(True)
        self.labels[0].setPixmap(STATUS_PIXMAP['PAC '].scaled(25,25,Qt.KeepAspectRatio))
        self.playersLayout.addRow(self.labels[0],self.input[0])
        self.ghostID=1
        self.buttons=[]
        for i in range(4):
            if i==0:
                self.labels.append(QLabel("Ghost "+str(i)+" : "))
                self.labels[-1].setScaledContents(True)
                self.labels[-1].setPixmap(STATUS_PIXMAP['G.2.'+str(i)+' '].scaled(25,25,Qt.KeepAspectRatio))
                self.labels[-1].hide()
                self.input.append(QComboBox())
                self.input[i+1].addItem("IA 1")
                self.input[i+1].addItem("IA 0")
                self.input[i+1].addItem("Human")
                self.input[i+1].hide()
            else:
                self.labels.append(QLabel("Ghost "+str(i)+" : "))
                self.labels[-1].setScaledContents(True)
                self.labels[-1].setPixmap(STATUS_PIXMAP['G.2.'+str(i)+' '].scaled(25,25,Qt.KeepAspectRatio))
                self.labels[-1].hide()
                self.input.append(QComboBox())
                self.input[i+1].addItem("IA 0")
                self.input[i+1].addItem("IA 1")
                self.input[i+1].hide()
            self.playersLayout.addRow(self.labels[-1],self.input[-1])
        self.buttons.append(QPushButton('Add Ghost'))
        self.buttons[0].setToolTip("Add Ghost to the Game")
        self.buttons[0].clicked.connect(self.addingGhost)
        self.shortcuts.append(QShortcut(Qt.Key_Plus,self))
        self.shortcuts[0].activated.connect(self.addingGhost)
        self.buttons.append(QPushButton('Remove Ghost'))
        self.buttons[1].setToolTip("Remove Ghost from the Game")
        self.buttons[1].clicked.connect(self.removingGhost)
        self.shortcuts.append(QShortcut(Qt.Key_Minus,self))
        self.shortcuts[1].activated.connect(self.removingGhost)
        self.buttons[1].setEnabled(False)
        self.playersLayout.addRow(self.buttons[1],self.buttons[0])
        self.playersGroupBox.setLayout(self.playersLayout)
        self.mainLayout.addWidget(self.playersGroupBox)
        # Board View
        self.boardGroupBox = QGroupBox("Board")
        self.boardGroupBox.setStyleSheet("QGroupBox{ color: white;}")
        self.boardLayout=QVBoxLayout()
        self.boardLayoutRadioButtons=QHBoxLayout()
        self.DefaultMap = QRadioButton("Default Map")
        self.DefaultMap.setStyleSheet("QRadioButton{ color: white;}")
        self.DefaultMap.toggled.connect(lambda:self.btnstate(self.DefaultMap))
        self.boardLayoutRadioButtons.addWidget(self.DefaultMap)

        self.SavedMap = QRadioButton("Saved Map")
        self.SavedMap.setStyleSheet("QRadioButton{ color: white;}")
        self.SavedMap.toggled.connect(lambda:self.btnstate(self.SavedMap))
        self.boardLayoutRadioButtons.addWidget(self.SavedMap)

        self.CustomMap = QRadioButton("Custom Map")
        self.CustomMap.setStyleSheet("QRadioButton{ color: white;}")
        self.CustomMap.toggled.connect(lambda:self.btnstate(self.CustomMap))
        self.boardLayoutRadioButtons.addWidget(self.CustomMap)
        
        self.boardUserInputWidget=QWidget()
        self.boardLayout.addLayout(self.boardLayoutRadioButtons)
        self.boardLayout.addWidget(self.boardUserInputWidget)
        self.boardGroupBox.setLayout(self.boardLayout)
        self.mainLayout.addWidget(self.boardGroupBox)
        
        # Bottom Buttons Row
        self.buttonsLayout=QHBoxLayout()
        self.buttons.append(QPushButton('Ok'))
        self.buttons[2].setToolTip("Start the Game")
        self.buttons[2].clicked.connect(self.validation)
        self.shortcuts.append(QShortcut(Qt.Key_Return,self))
        self.shortcuts[2].activated.connect(self.validation)
        self.buttons.append(QPushButton('Cancel'))
        self.buttons[3].clicked.connect(self.cancelation)
        self.shortcuts.append(QShortcut(Qt.Key_Escape,self))
        self.shortcuts[3].activated.connect(self.cancelation)
        self.buttonsLayout.addWidget(self.buttons[3])
        self.buttonsLayout.addWidget(self.buttons[2])
        self.mainLayout.addLayout(self.buttonsLayout)
        # Main View Settings
        self.setLayout(self.mainLayout)
        self.adjustSize()
        p = self.palette()
        p.setColor(self.foregroundRole(), Qt.white)
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)
    
    def removingGhost(self):
        if self.ghostID>1:    
            self.input[self.ghostID-1].hide()
            self.input[self.ghostID-1].setCurrentIndex(0)
            self.labels[self.ghostID-1].hide()
            if self.ghostID==2:
                self.buttons[1].setEnabled(False)
            self.ghostID-=1
            self.update()
            self.buttons[0].setEnabled(True)
        else:
            self.buttons[1].setEnabled(False)
            self.buttons[0].setEnabled(True)
        
    def btnstate(self,b):
        if b.text() == "Custom Map" and b.isChecked() == True:
                print(b.text()+" is selected")
                self.customMapLayout = QFormLayout()
                self.e1 = QSpinBox()
                self.e1.setSingleStep(1)
                self.e1.setMinimum(0)
                self.e1.setValue(15)
                self.e1.setMaximum(100)
                self.l1=QLabel("Nombre de lignes du plateau ?")
                self.l1.setStyleSheet("QLabel{ color: white;}")
                self.customMapLayout.addRow(self.l1,self.e1)
                self.e2 = QSpinBox()
                self.e2.setSingleStep(1)
                self.e2.setMinimum(0)
                self.e2.setValue(19)
                self.e2.setMaximum(100)
                self.l2=QLabel("Nombre de colonnes du plateau ?")
                self.l2.setStyleSheet("QLabel{ color: white;}")
                self.customMapLayout.addRow(self.l2,self.e2)
                self.e3 = QSpinBox()
                self.e3.setSingleStep(1)
                self.e3.setMinimum(0)
                self.e3.setValue(1)
                self.e3.setMaximum(self.e1.value())
                self.l3=QLabel("Nombre de lignes de la caverne des fantômes ?")
                self.l3.setStyleSheet("QLabel{ color: white;}")
                self.customMapLayout.addRow(self.l3,self.e3)
                self.e4 = QSpinBox()
                self.e4.setSingleStep(1)
                self.e4.setMinimum(0)
                self.e4.setValue(3)
                self.e4.setMaximum(self.e2.value())
                self.l4=QLabel("Nombre de colonnes de la caverne des fantômes ?")
                self.l4.setStyleSheet("QLabel{ color: white;}")
                self.customMapLayout.addRow(self.l4,self.e4)
                self.boardUserInputWidget.setLayout(self.customMapLayout)
                self.update()
                
        if b.text() == "Saved Map" and b.isChecked() == True:
                print(b.text()+" is selected")
                self.boardUserInputWidget=QLabel(' ')
                self.update()
                
        if b.text() == "Default Map" and b.isChecked() == True:
                print(b.text()+" is selected")
                self.boardUserInputWidget=QLabel(' ')
                self.update()

    def addingGhost(self):
        if self.ghostID<5:
            self.input[self.ghostID].show()
            self.input[self.ghostID].setCurrentIndex(0)
            self.labels[self.ghostID].show()
            self.buttons[1].setEnabled(True)
            if self.ghostID==4:
                self.buttons[0].setEnabled(False)    
            self.ghostID+=1
            self.update()
        else:
            self.buttons[0].setEnabled(False)
            self.buttons[1].setEnabled(True)
        
    def loadPixmaps(self):
            STATUS_PIXMAP['PAC '] = QPixmap('Data\\PAC.png')
            STATUS_PIXMAP['G.0.0 '] = QPixmap('Data\\G.0.0.png')
            STATUS_PIXMAP['G.1.0 '] = QPixmap('Data\\G.1.0.png')
            STATUS_PIXMAP['G.2.0 '] = QPixmap('Data\\G.2.0.png')
            STATUS_PIXMAP['G.0.1 '] = QPixmap('Data\\G.0.1.png')
            STATUS_PIXMAP['G.1.1 '] = QPixmap('Data\\G.1.1.png')
            STATUS_PIXMAP['G.2.1 '] = QPixmap('Data\\G.2.1.png')
            STATUS_PIXMAP['G.0.2 '] = QPixmap('Data\\G.0.2.png')
            STATUS_PIXMAP['G.1.2 '] = QPixmap('Data\\G.1.2.png')
            STATUS_PIXMAP['G.2.2 '] = QPixmap('Data\\G.2.2.png')
            STATUS_PIXMAP['G.0.3 '] = QPixmap('Data\\G.0.3.png')
            STATUS_PIXMAP['G.1.3 '] = QPixmap('Data\\G.1.3.png')
            STATUS_PIXMAP['G.2.3 '] = QPixmap('Data\\G.2.3.png')
            
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
            self.setPixmap(self.pixmap)
            self.setScaledContents(True)
            
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
        CELL_PIXMAP['G.0.2 '] = QPixmap('Data\\G.0.2.png')
        CELL_PIXMAP['G.1.2 '] = QPixmap('Data\\G.1.2.png')
        CELL_PIXMAP['G.2.2 '] = QPixmap('Data\\G.2.2.png')
        CELL_PIXMAP['G.0.3 '] = QPixmap('Data\\G.0.3.png')
        CELL_PIXMAP['G.1.3 '] = QPixmap('Data\\G.1.3.png')
        CELL_PIXMAP['G.2.3 '] = QPixmap('Data\\G.2.3.png')
        CELL_PIXMAP['    '] = QPixmap()
        
    def refresh(self):
        for row in range(self.lignes):
            for column in range(self.colonnes):
                cell=self.cells[row][column]
                boardValue=self.controller.getCellValue(row,column)
                if cell.getValue()!=boardValue:
                    cell.refresh(boardValue)
        self.setLayout(self.layout)

class StatusWidget(QWidget):
    def __init__(self,parent, controller):
        super().__init__(parent)
        self.controller=controller
        self.bgPixmaps=[]
        self.labels=[]
        self.layout=QHBoxLayout()
        self.setLayout(self.layout)
        
    def create(self,choices):
        self.controller.subscribe(self)
        for index in range(len(choices)):
            self.labels.append(QLabel())
        
            if index==0:
                name="PAC "
            else:
                name="G.2."+str(index-1)+' '
            self.bgPixmaps.append(STATUS_PIXMAP[name].scaled(25,25,Qt.KeepAspectRatio))
#            painter = QPainter()
#            painter.begin(self.bgPixmaps[-1])
#            print(self.bgPixmaps[-1].rect())
#            painter.drawText(self.bgPixmaps[-1].rect(),Qt.AlignCenter, choices[index])
#            painter.end()
            
            self.labels[-1].setPixmap(self.bgPixmaps[-1])
            self.labels[-1].setScaledContents(True)
            self.labels[-1].setStatusTip(choices[index])
            self.labels[-1].adjustSize()
            self.layout.addWidget(self.labels[-1])
        
    def refresh(self):
        pass
#        self.parent.showMessage(self.controller.getLog(),self.controller.getLogTimer())
#        list_ghosts=self.controller.listGhosts()
#        layout=QHBoxLayout()
#        for index in range(len(list_ghosts)):
#            name=str(list_ghosts[index])
#            self.bgPixmaps[index+1]=STATUS_PIXMAP[name].scaled(25,25,Qt.KeepAspectRatio)
           # self.labels[index+1].setPixmap()

class HomeWindow(QMainWindow):

    def __init__(self, app, controller, windowTitle):
        super().__init__()
        self.setVisible(True)
        self.setWindowTitle(windowTitle)
        self.app = app
        self.controller = controller
        self.controller.subscribe(self)
        self.playTimer=QTimer()
        self.playTimer.setSingleShot(False)
        self.playTimer.setInterval(50)
        self.playTimer.stop()
        self.mainMenu = self.menuBar()
        self.statusWidget = StatusWidget(self,self.controller)
        self.statusBar=QStatusBar()
        self.init_menu()
        self.initUi()
        self.initial_status=self.saveState()

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
                self.controller.showMessage("Pause",0)
            else:
                self.playTimer.start()
                self.controller.showMessage("",0)
    
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
        
#        gameMenuGhostAction = QAction("&Add Ghost", self)
#        gameMenuGhostAction.setShortcut("Ctrl+G")
#        gameMenuGhostAction.setStatusTip('Ajouter un fantôme')
#        gameMenuGhostAction.triggered.connect(self.addGhost)
#
#        gameMenu.addAction(gameMenuGhostAction)
#        
#        gameMenuListGhostAction = QAction("&List Ghost", self)
#        gameMenuListGhostAction.setShortcut("Ctrl+Shift+G")
#        gameMenuListGhostAction.setStatusTip('Liste les fantômes')
#        gameMenuListGhostAction.triggered.connect(self.listGhosts)
#
#        gameMenu.addAction(gameMenuListGhostAction)
        
        
        gameMenuStartAction = QAction("&Start Game", self)
        gameMenuStartAction.setShortcut("Ctrl+Return")
        gameMenuStartAction.setStatusTip('Créer la partie')
        gameMenuStartAction.triggered.connect(self.newGame)

        gameMenu.addAction(gameMenuStartAction)
        
    def home(self):
        self.playTimer.stop()
        QMessageBox.about(self, self.windowTitle(), "Vous avez perdu")
        self.reset()
        
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
        self.playTimer.timeout.connect(self.step)
        self.playTimer.start()
    
    def step(self):
        if self.controller.stopGame():
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
    
    def refresh(self):
        pass
    
    def initUi(self):
        self.center = QWidget()
        self.centerLayout=QVBoxLayout()
        self.welcomeScreen=QLabel("")
        self.welcomeScreen.setScaledContents(True)
        self.welcomeScreen.setPixmap(QPixmap('Data\\WelcomeScreen.jpeg'))
        self.buttonsLayout=QHBoxLayout()
        self.newGameButton=QPushButton('New Game')
        self.newGameButton.clicked.connect(self.loadSavedMap)
        self.buttonsLayout.addWidget(self.newGameButton)
        self.quitButton=QPushButton('Quit')
        self.quitButton.clicked.connect(self.close)
        self.buttonsLayout.addWidget(self.quitButton)
        self.centerLayout.addWidget(self.welcomeScreen)
        self.centerLayout.addLayout(self.buttonsLayout)
        self.center.setLayout(self.centerLayout)
        self.setCentralWidget(self.center)
        self.statusBar.addPermanentWidget(self.statusWidget)
        self.setStatusBar(self.statusBar)
        p = self.palette()
        p.setColor(self.foregroundRole(), Qt.white)
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)
    
    def loadStandardMap(self):
        choices=[]
        d=NewGameDialog()
        if (d.exec()== QDialog.Accepted):
            for i in range(d.ghostID):
                choices.append(d.input[i].currentText())
            self.statusWidget.create(choices)
            self.controller.defaultGame(choices[0],choices[1:])
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
        else:
            self.reset()

    def loadSavedMap(self):
        fileName = QFileDialog.getOpenFileName(self, 'Open file', os.getcwd(),"CSV files (*.csv)")
        choices=[]
        d=NewGameDialog()
        if (d.exec()== QDialog.Accepted):
            for i in range(d.ghostID):
                choices.append(d.input[i].currentText())
        if len(choices)>0:
            self.statusWidget.create(choices)
            self.controller.loadGame(fileName[0],choices[0],choices[1:])
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
        else:
            self.reset()
        
    def loadCustomMap(self):
        choices=[]
        d = CustomMapDialog()
        if (d.exec()== QDialog.Accepted):
            l_board,c_board,l_cavern,c_cavern = d.e1.value(), d.e2.value(), d.e3.value(), d.e4.value()
        d=NewGameDialog()
        if (d.exec()== QDialog.Accepted):
            for i in range(d.ghostID):
                choices.append(d.input[i].currentText())
        if len(choices)>0:
            self.statusWidget.create(choices)
            self.controller.customGame(l_board,c_board,l_cavern,c_cavern,choices[0],choices[1:])
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
        else:
            self.reset()
    
    def reset(self):
        self.controller.reset()
        self.controller.subscribe(self)
        self.playTimer=QTimer()
        self.playTimer.setSingleShot(False)
        self.playTimer.setInterval(50)
        self.playTimer.stop()
        self.mainMenu.clear()
        self.statusWidget = StatusWidget(self,self.controller)
        self.statusBar=QStatusBar()
        self.init_menu()
        self.initUi()
        self.show()
        
def main():
    pacmanCtrl = PacmanController(pacman)
    app = QApplication(sys.argv)

    fenetre = HomeWindow(app, pacmanCtrl, 'Pacman 3')
    fenetre.setWindowIcon(QIcon('Data\PAC.png'))
    fenetre.setVisible(True)
    fenetre.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()