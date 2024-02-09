# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 14:10:46 2023

@author: Laura & David
"""

from PyQt5 import QtGui
from PyQt5.QtWidgets import QPushButton,  QStyle, QLabel

class Line():
    def __init__(self, firstConnector, pointOfFirstConnector, secondConnector, pointOfSecondConnector, label, dialog):
        self.firstCon = firstConnector
        self.secondCon = secondConnector
        self.pointOfFirstCon = pointOfFirstConnector.copy()
        self.pointOfSecondCon = pointOfSecondConnector.copy()
        self.editPoints()
        self.deleteViewVisible = False
        self.label = label
        self.dialog = dialog
        self.drawLine('black')
    
    def getPainter(self, color):
        painter = QtGui.QPainter(self.label.pixmap())
        pen = QtGui.QPen()
        pen.setWidth(2)
        if color == 'black':
            pen.setColor(QtGui.QColor(0,0,0))
        else:
            pen.setColor(QtGui.QColor(255,255,255))
        painter.setPen(pen)
        return painter
        
    def drawLine(self, color, deleteLine=False):
        self.checkPositionOfPoints()
        painter = self.getPainter(color)
        if self.pointOfFirstCon['posY'] == self.pointOfSecondCon['posY']:
            painter.drawLine(self.pointOfFirstCon['posX'], self.pointOfFirstCon['posY'], self.pointOfSecondCon['posX'], self.pointOfSecondCon['posY'])
        else:
            if self.pointOfFirstCon['posX'] + 25 < self.pointOfSecondCon['posX']:
                halfLine = self.pointOfFirstCon['posX'] + int((self.pointOfSecondCon['posX'] - self.pointOfFirstCon['posX']) / 2)
                painter.drawLine(self.pointOfFirstCon['posX'], self.pointOfFirstCon['posY'], halfLine, self.pointOfFirstCon['posY'])
                painter.drawLine(halfLine, self.pointOfFirstCon['posY'], halfLine, self.pointOfSecondCon['posY'])
                painter.drawLine(halfLine, self.pointOfSecondCon['posY'], self.pointOfSecondCon['posX'], self.pointOfSecondCon['posY'])
            else:
                painter.drawLine(self.pointOfFirstCon['posX'], self.pointOfFirstCon['posY'], self.pointOfFirstCon['posX'] + 30, self.pointOfFirstCon['posY'])
                if self.pointOfFirstCon['posY'] < self.pointOfSecondCon['posY']:
                    painter.drawLine(self.pointOfFirstCon['posX'] + 30, self.pointOfFirstCon['posY'], self.pointOfFirstCon['posX'] + 30, self.pointOfFirstCon['posY'] + 30)
                    painter.drawLine(self.pointOfFirstCon['posX'] + 30, self.pointOfFirstCon['posY'] + 30, self.pointOfSecondCon['posX'] - 20, self.pointOfFirstCon['posY'] + 30)
                    painter.drawLine(self.pointOfSecondCon['posX'] - 20, self.pointOfFirstCon['posY'] + 30, self.pointOfSecondCon['posX'] - 20, self.pointOfSecondCon['posY'])
                else:
                    painter.drawLine(self.pointOfFirstCon['posX'] + 30, self.pointOfFirstCon['posY'], self.pointOfFirstCon['posX'] + 30, self.pointOfFirstCon['posY'] - 30)
                    painter.drawLine(self.pointOfFirstCon['posX'] + 30, self.pointOfFirstCon['posY'] - 30, self.pointOfSecondCon['posX'] - 20, self.pointOfFirstCon['posY'] - 30)
                    painter.drawLine(self.pointOfSecondCon['posX'] - 20, self.pointOfFirstCon['posY'] - 30, self.pointOfSecondCon['posX'] - 20, self.pointOfSecondCon['posY'])
                painter.drawLine(self.pointOfSecondCon['posX'] - 20, self.pointOfSecondCon['posY'], self.pointOfSecondCon['posX'], self.pointOfSecondCon['posY'])
        painter.end()
        if not deleteLine:
            self.dialog.label.update()
            
    def makeBoxForLine(self, line_info):
        label = QLabel(self.dialog)
        label.move(line_info['firstConnector'].x - 40, line_info['firstConnector'].y - 18)
        #label.setStyleSheet("background-color: black; color: white") 
        label.setText('Delete Line?')
        
        acceptButton = QPushButton('', self.dialog)
        acceptButton.setObjectName('acceptButton')
        pixmapi = QStyle.SP_DialogOkButton
        icon = self.dialog.style().standardIcon(pixmapi)
        acceptButton.setIcon(icon)
        acceptButton.setGeometry(line_info['firstConnector'].x + 20, line_info['firstConnector'].y-20, 30, 20)
        
        deleteButton = QPushButton('',self.dialog)
        deleteButton.setObjectName('deleteButton')
        pixmapi = QStyle.SP_DialogCancelButton
        icon = self.dialog.style().standardIcon(pixmapi)
        deleteButton.setIcon(icon)
        deleteButton.setGeometry(line_info['firstConnector'].x + 50, line_info['firstConnector'].y-20, 30, 20)
       
        label.show()
        acceptButton.show()
        deleteButton.show()
        self.dialog.blockMode = True
        self.deleteViewVisible = True
        
        
        acceptButton.clicked.connect(lambda: self.editLine(line_info, label, acceptButton, deleteButton))
        deleteButton.clicked.connect(lambda: self.editLine(line_info, label, acceptButton, deleteButton))
        
    def editLine(self, line_info, inputBox = None, acceptButton = None, deleteButton = None, delete = False):
        source = self.dialog.sender()
        if source.objectName() == 'acceptButton' or delete:
            line_info['firstConnector'].inputs[line_info['firstConnectorKey']]['line'].deleteLine()
            if not delete: 
                line_info['firstConnector'].setPoints()
                line_info['secondConnector'].setPoints()
            line_info['secondConnector'].outputs[line_info['secondConnectorKey']]['line']. remove(line_info['secondConnector'].outputs[line_info['secondConnectorKey']]['line'][line_info['secondConnectorIndex']])
            del line_info['firstConnector'].inputs[line_info['firstConnectorKey']]['line']
            line_info['firstConnector'].inputs[line_info['firstConnectorKey']]['line'] = 0
            line_info['firstConnector'].drawLines()
        
        elif source.objectName() == 'deleteButton':
            pass
        
        if not delete:
            inputBox.deleteLater()
            acceptButton.deleteLater()
            deleteButton.deleteLater()
            self.dialog.blockMode = False
            self.deleteViewVisible = False
                
    def checkPositionOfPoints(self):
        if self.pointOfFirstCon['posX'] > self.pointOfSecondCon['posX'] and self.pointOfSecondCon['typeOfConnect'] != 'input':
            point = self.pointOfFirstCon 
            self.pointOfFirstCon = self.pointOfSecondCon
            self.pointOfSecondCon = point
        elif self.pointOfSecondCon['typeOfConnect'] != 'input':
            point = self.pointOfFirstCon 
            self.pointOfFirstCon = self.pointOfSecondCon
            self.pointOfSecondCon = point
    
    def updatePositionOfPoint(self, position, parent):
        if parent == self.firstCon:
            self.pointOfFirstCon = position.copy()
            self.pointOfFirstCon['posX'] += 5
            self.pointOfFirstCon['posY'] += 5
        else:
            self.pointOfSecondCon = position.copy()
            self.pointOfSecondCon['posX'] += 5
            self.pointOfSecondCon['posY'] += 5
        self.drawLine('black')
        
    def deleteLine(self):
        self.drawLine('white', deleteLine=True)
        
    def editPoints(self):
        self.pointOfFirstCon['posX'] += 5
        self.pointOfFirstCon['posY'] += 5
        self.pointOfSecondCon['posX'] += 5
        self.pointOfSecondCon['posY'] += 5
        
    def getVisibility(self):
        return self.deleteViewVisible