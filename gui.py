# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 13:59:24 2023

@author: Laura & David
"""

from PyQt5 import QtWidgets, uic, QtGui, QtCore

from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QLineEdit,  QSpinBox, QStyle, QLabel
from PyQt5.QtGui import QPixmap, QDrag
from PyQt5.QtCore import Qt, QMimeData

import sys
import os

from gui.Line import Line
from gui.dragNdropObject import *
from gui.fileGenerator import *

class GUI(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

        self.window = self
        self.elements = []
        self.blockMode = False
        self.currentMode = 'dragANDdrop'
        self.filename = ''
        self.currentPath = os.getcwd()
        self.connection = {'firstConnectorSelected': False, 'position': {}, 'element': 0}
        
        
        (QtGui.QIcon('gui/quanten.png'))
        self.ui = uic.loadUi("gui/qsfw.ui", self)
        
        self.prepareLabel()
        self.loadMode()
        
        self.ui.btn_circuit.clicked.connect(self.create)
        self.ui.btn_qubit.clicked.connect(self.create)
        self.ui.btn_ident.clicked.connect(self.create)
        self.ui.btn_hadamard.clicked.connect(self.create)
        self.ui.btn_phase.clicked.connect(self.create)
        self.ui.btn_pauliX.clicked.connect(self.create)
        self.ui.btn_pauliY.clicked.connect(self.create)
        self.ui.btn_pauliZ.clicked.connect(self.create)
        self.ui.btn_sphase.clicked.connect(self.create)
        self.ui.btn_tphase.clicked.connect(self.create)
        self.ui.btn_measure.clicked.connect(self.create)
        self.ui.btn_cnot.clicked.connect(self.create)
        self.ui.btn_swap.clicked.connect(self.create)
        self.ui.btn_cz.clicked.connect(self.create)
        self.ui.btn_cphase.clicked.connect(self.create)
        self.ui.btn_toffoli.clicked.connect(self.create)
        self.ui.btn_cswap.clicked.connect(self.create)
        
        self.ui.btn_dragANDdrop.clicked.connect(self.changeMode)
        self.ui.btn_connect.clicked.connect(self.changeMode)
        self.ui.btn_compile.clicked.connect(self.changeMode)
        
        self.ui.btn_calculation.clicked.connect(self.startCompile)
    
        try: self.ui.btn_createFile.clicked.connect(self.compileQSFW)
        except: self.ui.label_error.setText('Something went wrong.\nPlease check your circuit and file name!')
    
    def startCompile(self):
        filePath = os.path.join(self.currentPath, 'files/')
        qsfwPath = os.path.join(self.currentPath, 'qsfw')
        my_os = str(sys.platform)        
           
        try:
            os.chdir(qsfwPath)
            if my_os.startswith('win') or my_os.startswith('Win') or my_os.startswith('WIN'):
                command = 'start cmd /C "python -m qsfw -s '+ os.path.join(filePath, self.filename) + ' & timeout 300\"'
            else:
                command = 'python3 -m qsfw -s '+  os.path.join(filePath, self.filename)
            os.system(command)
            return
        except Exception as e:
            print(e)

    
    def loadMode(self):
        if self.currentMode == 'dragANDdrop':
            self.filename = ''
            self.ui.btn_dragANDdrop.setEnabled(False)
            self.ui.btn_connect.setEnabled(True)
            self.ui.btn_compile.setEnabled(True)
           
            self.ui.label_mode.setText('Drag and Drop')
            self.ui.label_error.setText('')
            
            self.ui.menubox.setEnabled(True)
            self.ui.lbl_dropBar.setEnabled(True)
            self.ui.compileElements.setEnabled(False)
            
            for elem in self.elements:
                elem.setEnabled(True)
                elem.setPoints()
            
            if any(elem.category == 'circuit' for elem in self.elements):
                self.ui.btn_circuit.setEnabled(False)
                self.ui.btn_qubit.setEnabled(False)
            elif any(elem.category == 'qubit' for elem in self.elements):
                self.ui.btn_circuit.setEnabled(False)
            else:
                self.ui.btn_circuit.setEnabled(True)
                self.ui.btn_qubit.setEnabled(True)
 
        
        elif self.currentMode == 'connect':
            self.filename = ''
            self.ui.btn_dragANDdrop.setEnabled(True)
            self.ui.btn_connect.setEnabled(False)
            self.ui.btn_compile.setEnabled(True)
            
            self.ui.label_mode.setText('Connect')
            self.ui.label_error.setText('')
            
            self.ui.menubox.setEnabled(False)
            self.ui.lbl_dropBar.setEnabled(True)
            self.ui.compileElements.setEnabled(False)
            
            for elem in self.elements:
                elem.setEnabled(False)
        
        elif self.currentMode == 'compile':
            self.filename = ''
            self.ui.btn_dragANDdrop.setEnabled(True)
            self.ui.btn_connect.setEnabled(True)
            self.ui.btn_compile.setEnabled(False)
            
            self.ui.label_mode.setText('Compile')
            self.ui.label_error.setText('')
            self.ui.btn_createFile.setEnabled(True)
            self.ui.lineEdit_filename.setEnabled(True)
            self.ui.btn_calculation.setEnabled(False)
            
            self.ui.menubox.setEnabled(False)
            self.ui.lbl_dropBar.setEnabled(False)
            self.ui.compileElements.setEnabled(True)
            
            for elem in self.elements:
                elem.setEnabled(False)
                
    
    def changeMode(self):
        sender = self.sender()
       
        if sender.objectName() == 'btn_dragANDdrop' and not self.blockMode:
            self.currentMode = 'dragANDdrop'
            self.connection['firstConnectorSelected'] = False

        elif sender.objectName() == 'btn_connect':
            self.currentMode = 'connect'
        
        elif sender.objectName() == 'btn_compile':
            self.currentMode = 'compile'
            
        self.loadMode()
    
    def getStart(self):
        quants = []
        for element in self.elements:
            if element.category == 'circuit':
                quants.append(element)
            elif element.category == 'qubit':
                quants.append(element)
        return quants
   

    def compileQSFW(self):
        fullPath = []
        quants = self.getStart()
        
        if len(quants) > 1: ### qubits
            fullPath = self.getPathQubit()
            
        if len(quants) == 1: ### circuits
            fullPath = self.getPathCircuit()

        self.createFile(fullPath)
    
    
    def getPathCircuit(self):
        elements = self.getStart()
        newElements = []
        nameElements = []
        
        for element in elements:
            for key in element.outputs:
                newElements.append(element)
                nameElements.append(element.name)
        
        allElements = newElements
        
        index = -1
        finaList = []
        finalNames = []
        for startElement in allElements:
            part = []
            names = []
            index += 1

            key = index
            element = startElement
            part.append(element)
            names.append(element.name)
            while True:
                if len(element.outputs[str(key)]['line']) < 1: break
                else:
                    for line in element.outputs[str(key)]['line']:
                        if line.firstCon == element:
                            nextElement = line.secondCon
                            nextKey = nextElement.getInputKey(line)
                        else:
                            nextElement = line.firstCon
                            nextKey = nextElement.getInputKey(line)
                        
                        part.append(nextElement)
                        names.append(nextElement.name)
                        
                    element = nextElement
                    key = nextKey
            finaList.append(part)
            finalNames.append(names)
        return finaList
        
    def getPathQubit(self):
        elements = self.getStart()
        allElements = elements
        
        finaList = []
        finalNames = []
        for startElement in allElements:
            part = []
            names = []
            
            key = 0
            element = startElement
            part.append(element)
            names.append(element.name)
            while True:
                if len(element.outputs[str(key)]['line']) < 1: break
                else:
                    for line in element.outputs[str(key)]['line']:
                        if line.firstCon == element:
                            nextElement = line.secondCon
                            nextKey = nextElement.getInputKey(line)
                            part.append(nextElement)
                            names.append(nextElement.name)
                        else:
                             nextElement = line.firstCon
                             nextKey = nextElement.getInputKey(line)
                        
                    element = nextElement
                    key = nextKey
            finaList.append(part)
            finalNames.append(names)
        return finaList
                    
    
    def createFile(self, allPathes):       
        try:
            os.chdir(self.currentPath)
            file = fileGenerator(allPathes)
            fileText = file.generateFile(allPathes) 
            self.filename = str(self.ui.lineEdit_filename.text()) + '.txt'
           
            with open('files/' + self.filename, "w") as text_file:
                text_file.write(fileText)
            ##text_file.close()
            
            if fileText != '': 
                self.ui.label_error.setText('The file was created successfully!')
                self.ui.lineEdit_filename.setEnabled(False)
                self.ui.btn_calculation.setEnabled(True)
            
            else: self.ui.label_error.setText('Something went wrong.\nPlease check your circuit and file name!')
        except Exception as e:
            self.ui.label_error.setText('Something went wrong.\nPlease check your circuit and file name!')
        
    
    def prepareLabel(self):
        self.label = self.ui.lbl_dropBar
       
        canvas = QtGui.QPixmap(self.label.width(), self.label.height())
        canvas.fill(Qt.white)
        self.label.setPixmap(canvas)        
        
    
    def inLabel(self, pos, element):
        if pos.x() - element.height/2 < self.label.x(): return False
        elif pos.x() + element.height/2 > self.label.x() + self.label.width(): return False
        elif pos.y() - element.width/2 < self.label.y(): return False
        elif pos.y() + element.width/2 > self.label.y() + self.label.height(): return False
        else: return True
  
        
    def mouseInLabel(self, pos):
        if pos.x() < self.label.x(): return False
        elif pos.x() > self.label.x() + self.label.width(): return False
        elif pos.y() < self.label.y(): return False
        elif pos.y() > self.label.y() + self.label.height(): return False
        else: return True
    
    
    def create(self, QMouseEvent):
        sender = self.sender()
        ### Basics
        if sender.objectName() == 'btn_circuit': element = dragNdropObject('circuit', sender.text(), self, 0, 1, 0)
        elif sender.objectName() == 'btn_qubit':
            number = 0 
            for elem in self.elements:
                if elem.category == 'qubit':
                    number += 1
            element = dragNdropObject('qubit', 'q'+ str(number), self, 0, 1, 0)
        ### 1-Qubit-Gate
        elif sender.objectName() == 'btn_ident': element = dragNdropObject('normalFunction1', sender.text(), self, 1, 1)
        elif sender.objectName() == 'btn_hadamard': element = dragNdropObject('normalFunction1', sender.text(), self, 1, 1)
        elif sender.objectName() == 'btn_phase': element = dragNdropObject('angleFunction1', sender.text(), self, 1, 1, '2*\u03A0')
        elif sender.objectName() == 'btn_pauliX': element = dragNdropObject('normalFunction1', sender.text(), self, 1, 1)
        elif sender.objectName() == 'btn_pauliY': element = dragNdropObject('normalFunction1', sender.text(), self, 1, 1)
        elif sender.objectName() == 'btn_pauliZ': element = dragNdropObject('normalFunction1', sender.text(), self, 1, 1)
        elif sender.objectName() == 'btn_sphase': element = dragNdropObject('normalFunction1', sender.text(), self, 1, 1)
        elif sender.objectName() == 'btn_tphase': element = dragNdropObject('normalFunction1', sender.text(), self, 1, 1)
        elif sender.objectName() == 'btn_measure': element = dragNdropObject('normalFunction1', sender.text(), self, 1, 1)
        ### 2-Qubit-Gate
        elif sender.objectName() == 'btn_cnot': element = dragNdropObject('normalFunction2', sender.text(), self, 2, 2)
        elif sender.objectName() == 'btn_swap': element = dragNdropObject('normalFunction2', sender.text(), self, 2, 2)
        elif sender.objectName() == 'btn_cz': element = dragNdropObject('normalFunction2', sender.text(), self, 2, 2)
        elif sender.objectName() == 'btn_cphase': element = dragNdropObject('angleFunction2', sender.text(), self, 2, 2, '2*\u03A0')
        ### 3-Qubit-Gate
        elif sender.objectName() == 'btn_toffoli': element = dragNdropObject('normalFunction3', sender.text(), self, 3, 3)
        elif sender.objectName() == 'btn_cswap': element = dragNdropObject('normalFunction3', sender.text(), self, 3, 3)
        
        element.create(self.label.x(), self.label.y(), sender.width(), sender.height())
        element.show()
        self.elements.append(element)
        ### makeBoxForCircuit -> number: inputBox; value: label (const. 0);
        if element.category == "circuit": element.clicked.connect(self.makeBoxForCircuit)
        ### makeBoxForQubit -> name: inputBox; value: inputBox;
        elif element.category == "qubit": element.clicked.connect(self.makeBoxForQubit)
        ### makeBoxForAngleFunction -> angle: inputBox;
        elif element.category[0:-1] == "angleFunction": element.clicked.connect(self.makeBoxForAngleFunction)
        ### deleteElements normalFunction
        else: element.clicked.connect(lambda: self.makeBoxForElem([]))
        
        
        self.loadMode()        
                      
        
    def makeBoxForCircuit(self):
        sender = self.sender()
        sender.setEnabled(False)
        index = self.elements.index(sender)
        
        valueLabel = QLabel('values: ' + str(sender.info), self)
        valueLabel.move(sender.x, sender.y-80)
        valueLabel.setFixedHeight(20)
        valueLabel.setStyleSheet("background-color: white") 
        
        numberLabel = QLabel('number: ', self)
        numberLabel.move(sender.x, sender.y-60)
        numberLabel.setFixedHeight(20)
        numberLabel.adjustSize()
        numberLabel.setStyleSheet("background-color: white") 
        
        numberBox = QSpinBox(self)
        numberBox.setGeometry(numberLabel.x() + numberLabel.width(), numberLabel.y(), 50, numberLabel.height())
        numberBox.setRange(1,5)
        numberBox.setValue(len(sender.outputs))
        
        valueLabel.show()
        numberLabel.show()
        numberBox.show()
        self.makeBoxForElem([valueLabel, numberLabel, numberBox])
        
        
    def makeBoxForQubit(self):
        sender = self.sender()
        sender.setEnabled(False)
        index = self.elements.index(sender)
        
        nameLabel = QLabel('name: ' , self)  
        nameLabel.move(sender.x, sender.y-80)
        nameLabel.setFixedHeight(20)
        nameLabel.adjustSize()
        nameLabel.setStyleSheet("background-color: white") 
        
        nameBox = QLineEdit(self)
        nameBox.setGeometry(nameLabel.x() + nameLabel.width(), nameLabel.y(), 50, nameLabel.height())
        nameBox.setText(sender.text())
        
        valueLabel = QLabel('value: ', self)
        valueLabel.move(sender.x, sender.y-60)
        valueLabel.setFixedHeight(20)
        valueLabel.adjustSize()
        valueLabel.setStyleSheet("background-color: white") 
        
        valueBox = QSpinBox(self)
        valueBox.setGeometry(valueLabel.x() + valueLabel.width(), valueLabel.y(), 50, valueLabel.height())
        valueBox.setRange(0,1)
        valueBox.setValue(sender.info)
        
        
        nameLabel.show()
        nameBox.show()
        valueLabel.show()
        valueBox.show()
        self.makeBoxForElem([nameLabel, nameBox, valueLabel, valueBox])
        
    def makeBoxForAngleFunction(self):
        sender = self.sender()
        sender.setEnabled(False)
        index = self.elements.index(sender)
        
        angleLabel = QLabel('angle: ', self)     
        angleLabel.move(sender.x, sender.y-60)
        angleLabel.setFixedHeight(20)
        angleLabel.adjustSize()
        angleLabel.setStyleSheet("background-color: white")         
        
        angleBox = QLineEdit(self)
        angleBox.setGeometry(angleLabel.x() + angleLabel.width(), angleLabel.y(), 50, angleLabel.height())
        angleBox.setText(sender.info)
        
        angleLabel.show()
        angleBox.show()
        self.makeBoxForElem([angleLabel, angleBox])


    def makeBoxForElem(self, deleteList):
        sender = self.sender()
        sender.setEnabled(False)
        index = self.elements.index(sender)
        
        
        acceptLabel = QLabel('Accept Settings: ', self)       
        acceptLabel.move(sender.x, sender.y-40)
        acceptLabel.setFixedHeight(20)
        acceptLabel.adjustSize()
        acceptLabel.setStyleSheet("background-color: white") 
        
        acceptButton = QPushButton('OK',self)
        acceptButton.setObjectName('acceptButton')
        acceptButton.setGeometry(acceptLabel.x() + acceptLabel.width(), acceptLabel.y(), 30, acceptLabel.height())
        
        acceptLabel.show()
        acceptButton.show()
        
        deleteLabel = QLabel('Delete Object: ', self)       
        deleteLabel.move(sender.x, sender.y-20)
        deleteLabel.setFixedHeight(20)
        deleteLabel.adjustSize()
        deleteLabel.setStyleSheet("background-color: white") 
        
        deleteButton = QPushButton('',self)
        deleteButton.setObjectName('deleteButton')
        pixmapi = QStyle.SP_DialogCancelButton
        icon = self.style().standardIcon(pixmapi)
        deleteButton.setIcon(icon)
        deleteButton.setGeometry(deleteLabel.x() + deleteLabel.width(), deleteLabel.y(), 30, deleteLabel.height())
       

        deleteLabel.show()
        deleteButton.show()
        

        deleteList += [acceptLabel, acceptButton, deleteLabel, deleteButton]
        acceptButton.clicked.connect(lambda: self.editElement(sender,  deleteList))
        deleteButton.clicked.connect(lambda: self.deleteElements(sender,  deleteList))
    
     
        
    def editElement(self, sender, deleteList):
        if sender.category == "circuit":
            sender.setPoints(delete=True)
            try: self.deleteLinesOutputs(sender)
            except: pass
            sender.outputs = sender.createOutputDict(deleteList[2].value())
            sender.update(sender.x, sender.y, sender.width, sender.height)
            
        
        if sender.category == "qubit":
            sender.name = deleteList[1].text()
            sender.info = deleteList[3].value()
            sender.setText(sender.name)
        
        if sender.category[0:-1] == "angleFunction":
            sender.info = deleteList[1].text()
        
        self.deleteElements(sender, deleteList, False)

    
    def deleteElements(self, sender, deleteList, deleteAll = True):
        sender.setEnabled(True)
               
        if deleteAll:
            try: self.deleteLinesInputs(sender)
            except: pass
            try: self.deleteLinesOutputs(sender)
            except: pass
            self.elements.remove(sender)
            sender.deletePoints()
            self.label.update()
            sender.deleteLater()
        
        for i in deleteList:
            i.deleteLater()
        
        self.loadMode()
    
    def checkIfConnectorIsSameElem(self, firstConnector, secondConnector):
        if firstConnector == secondConnector: return True
    
    def deleteLinesInputs(self, element):
        for key in element.inputs:
            point_info = element.checkIfPointIsConnected(element.inputs[key]['point'])
            if point_info['hit']:
                point_info['firstConnector'].inputs[point_info['firstConnectorKey']]['line'].editLine(point_info, delete= True)
    
    def deleteLinesOutputs(self, element):
        for i in range(len(element.outputs)):
            for key in element.outputs:
                # if len(element.outputs[key]['line']) == 0:
                #     return quant.name  
                for output in element.outputs[key]['line']:
                    line = output
                    if line.firstCon == element:
                        elem = line.secondCon
                    else:
                        elem = line.firstCon
            self.deleteLinesInputs(elem)
            elem.setPoints()                         
         
    
    def dragEnterEvent(self, event):
        element = event.source()
        element.deletePoints()
        element.overpaintLines()
        event.accept()
      
        
    def dropEvent(self, event):
        element = event.source()
        if self.inLabel(event.pos(), element):
            position = event.pos()
            element.move(position.x() - int(element.width/2), position.y() - int(element.height/2))
            element.update(position.x() - int(element.width/2), position.y() - int(element.height/2), element.width, element.height)
            for elem in self.elements:
                elem.updateLines()
            event.accept()
      
        
    def mousePressEvent(self, event):
        if self.mouseInLabel(event.pos()) and self.currentMode == 'connect':
            for elem in self.elements:
                point = elem.checkIfPointWasHit(event.pos(), event.button(), self.label)
                if type(point) == dict:
                    if event.button() == Qt.RightButton:
                        point_info = elem.checkIfPointIsConnected(point)
                        if point_info['hit']:
                            if not point_info['firstConnector'].inputs[point_info['firstConnectorKey']]['line'].getVisibility():
                                point_info['firstConnector'].inputs[point_info['firstConnectorKey']]['line'].makeBoxForLine(point_info)
                    elif self.connection['firstConnectorSelected']:
                        if self.connection['type'] != elem.getType(point):
                            if not self.checkIfConnectorIsSameElem(self.connection['element'], elem):
                                line = Line(self.connection['element'], self.connection['position'], elem, point, self.label, self.window)
                                self.connection['element'].connectWithLine(line, self.connection['position'])
                                elem.connectWithLine(line, point)
                                self.connection['firstConnectorSelected'] = False
                    else:
                        self.connection['firstConnectorSelected'] = True
                        self.connection['element'] = elem
                        self.connection['type'] = elem.getType(point)
                        self.connection['position'] = point
    

    
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = GUI()
    w.show()
    sys.exit(app.exec_())
