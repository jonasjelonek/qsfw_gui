# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 13:20:54 2023

@author: Laura & David
"""

from PyQt5 import QtWidgets, uic, QtGui, QtCore

from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QLineEdit,  QStyle, QLabel
from PyQt5.QtGui import QPixmap, QDrag
from PyQt5.QtCore import Qt, QMimeData

import sys

class dragNdropObject(QPushButton):
    def __init__(self, category, name, parent, inputs, outputs, info = None):
        super().__init__(name, parent)
        self.category = category
        self.name = name
        self.info = info
        self.inputs = self.createInputDict(inputs)
        self.outputs = self.createOutputDict(outputs)
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.dialog = parent
    
    def create(self, x, y, width, height):
        if len(self.inputs): x = x + 15
        self.setPosition(x, y, width, height)
        self.setGeometry(x, y, width, height)
        self.setPoints()
    
    def update(self, x, y, width, height):
        self.setPosition(x, y, width, height)
        self.setPoints()
        self.drawLines()
        
    def deletePoints(self):
        self.setPoints(delete=True)
    
    def setPosition(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    def setPoints(self, delete=False):
        pointX = self.x - self.dialog.label.x()
        pointY = self.y - self.dialog.label.y()
        
        inputScale = 1/(1 + len(self.inputs))
        for i in range(1, len(self.inputs) +1, 1):
            #point = Connections(self.dialog.label)
            positionX = pointX - 10          
            positionY = pointY + round(int(self.height * i * inputScale)/10)*10 - 5
            positionOfPoint = dict(posX=positionX, posY=positionY, typeOfConnect='input')
            self.inputs[f'{i-1}']['point'] = positionOfPoint
            if delete:
                self.drawPoint(positionX, positionY, 10, 'w')
            else:
                self.drawPoint(positionX, positionY, 10, 'g')
        
        outputScale = 1/(1 + len(self.outputs))
        for o in range(1, len(self.outputs)+1, 1):
            #point = Connections(self.dialog.label)
            positionX = pointX + self.width          
            positionY = pointY + round(int(self.height * o * outputScale)/10)*10 - 5
            positionOfPoint = dict(posX=positionX, posY=positionY, typeOfConnect='output')
            self.outputs[f'{o-1}']['point'] = positionOfPoint
            if delete:
                self.drawPoint(positionX, positionY, 10, 'w')
            else:
                self.drawPoint(positionX, positionY, 10, 'y')
        if not delete:
            self.dialog.label.update()
    
    def drawPoint(self, x, y, d, color):
        painter = QtGui.QPainter(self.dialog.label.pixmap())
        pen = QtGui.QPen()
        pen.setWidth(2)
        if color == 'w': pen.setColor(QtGui.QColor(255,255,255))
        else: pen.setColor(QtGui.QColor(0,0,0))  # r, g, b
        painter.setPen(pen)
        
        brush = QtGui.QBrush()
        ### set color
        if color == 'r': brush.setColor(QtGui.QColor(255,0,0))
        elif color == 'g': brush.setColor(QtGui.QColor(0,255,0))
        elif color == 'b': brush.setColor(QtGui.QColor(0,0,255))
        elif color == 'y': brush.setColor(QtGui.QColor(255,255,0))
        elif color == 'w': brush.setColor(QtGui.QColor(255,255,255))
        brush.setStyle(Qt.Dense1Pattern)
        painter.setBrush(brush)
        
        painter.drawEllipse(x,y,d,d)
        painter.end()
    
    def drawLines(self):
        counter = 0
        for key in self.inputs:
            if self.inputs[key]['line'] != 0:
                self.inputs[key]['line'].updatePositionOfPoint(self.inputs[key]['point'], self)
                counter += 1
        for key in self.outputs:
            if self.outputs[key]['line'] != 0:
                for line in self.outputs[key]['line']:
                    line.updatePositionOfPoint(self.outputs[key]['point'], self)
                counter += 1
    
    def updateLines(self):
        for key in self.inputs:
            if self.inputs[key]['line'] != 0:
                self.inputs[key]['line'].drawLine('black')
        for key in self.outputs:
            if self.outputs[key]['line'] != 0:
                for line in self.outputs[key]['line']:
                    line.drawLine('black')
                
                
    def overpaintLines(self):
        for key in self.inputs:
            if self.inputs[key]['line'] != 0:
                self.inputs[key]['line'].deleteLine()
        for key in self.outputs:
            if self.outputs[key]['line'] != 0:
                for line in self.outputs[key]['line']:
                    line.deleteLine()
    
    def checkIfPointWasHit(self, mousePos, mouseButton, label):
        for key in self.inputs:
            if mousePos.x() < self.inputs[key]['point']['posX'] + label.x(): continue
            elif mousePos.x() > self.inputs[key]['point']['posX'] + 10 + label.x(): continue
            elif mousePos.y() < self.inputs[key]['point']['posY'] + label.y(): continue
            elif mousePos.y() > self.inputs[key]['point']['posY'] + 10 + label.y(): continue
            elif mouseButton != Qt.RightButton and self.checkIfPointIsOccInputPoint(key): continue
            else: return self.inputs[key]['point']
        for key in self.outputs:
            if mousePos.x() < self.outputs[key]['point']['posX'] + label.x(): continue
            elif mousePos.x() > self.outputs[key]['point']['posX'] + 10 + label.x(): continue
            elif mousePos.y() < self.outputs[key]['point']['posY'] + label.y(): continue
            elif mousePos.y() > self.outputs[key]['point']['posY'] + 10 + label.y(): continue
            else: return self.outputs[key]['point']
        return False
    
    def checkIfPointIsOccInputPoint(self, key):
        if len(self.inputs) > 0:
            if self.inputs[key]['line'] != 0: return True
            
    def checkIfPointIsConnected(self, hitPoint):
        for key in self.inputs:
            if hitPoint['posX'] > self.inputs[key]['point']['posX']-5 and hitPoint['posX'] < self.inputs[key]['point']['posX']+5 and hitPoint['posY'] > self.inputs[key]['point']['posY']-5 and hitPoint['posY'] < self.inputs[key]['point']['posY']+5:
                if self.inputs[key]['line'] == 0: continue
                elif self.inputs[key]['line'].firstCon == self:
                    otherConnector = self.inputs[key]['line'].secondCon
                else:
                    otherConnector = self.inputs[key]['line'].firstCon
                for keyOut in otherConnector.outputs:
                    for index in range(len(otherConnector.outputs[keyOut]['line'])):
                        if otherConnector.outputs[keyOut]['line'][index] == self.inputs[key]['line']:
                            return dict(
                                    hit=True,
                                    firstConnector=self,
                                    firstConnectorKey=key,
                                    secondConnector=otherConnector,
                                    secondConnectorKey=keyOut,
                                    secondConnectorIndex=index                                    
                                )
        return dict(hit=False)

    def getType(self, point):
        for key in self.inputs:
            if self.inputs[key]['point'] == point:
                return 'input'
        for key in self.outputs:
            if self.outputs[key]['point'] == point:
                return 'output'                  
                    
    def connectWithLine(self, line, point):
        for key in self.inputs:
            if self.inputs[key]['point']['posX'] == point['posX'] and self.inputs[key]['point']['posY'] == point['posY']:
                self.inputs[key]['line'] = line
        for key in self.outputs:
            if self.outputs[key]['point']['posX'] == point['posX'] and self.outputs[key]['point']['posY'] == point['posY']:
                self.outputs[key]['line'].append(line)
            
    def createInputDict(self, numberOfConnections):
        dictionary = {}
        for i in range(numberOfConnections):
            inner_dict = dict(
                    point=0,
                    line=0
                )
            dictionary[f'{i}'] = inner_dict
        return dictionary
    
    def createOutputDict(self, numberOfConnections):
        dictionary = {}
        for i in range(numberOfConnections):
            inner_dict = dict(
                    point=0,
                    line=[]
                )
            dictionary[f'{i}'] = inner_dict
        return dictionary
    
    def getInputKey(self, line):
        for key in self.inputs:
            inpLine = self.inputs[str(key)]['line']
            if line == inpLine:
                return key

            
    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)
            drag.exec_(Qt.MoveAction)
    
    def dragEnterEvent(self, e):
        e.accept()
        



