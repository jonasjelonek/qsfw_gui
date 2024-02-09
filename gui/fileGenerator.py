# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 14:10:46 2023

@author: Laura & David
"""

from PyQt5 import QtWidgets, uic, QtGui, QtCore

from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QLineEdit,  QStyle, QLabel
from PyQt5.QtGui import QPixmap, QDrag
from PyQt5.QtCore import Qt, QMimeData

import sys



class fileGenerator():
    def __init__(self, fullPath):
        self.fullPath = fullPath
        self.namePath = []
    
    def getNames(self):
        for path in self.fullPath:
            names = []
            for p in path:
                names.append(p.name)
            self.namePath.append(names)
  
    
    def generateCircuitInstructions(self, elements):
        longest = len(max(elements, key=len))
        i = 0
        header = ''
        
        fullInstruction = []
        rememberElement = []
        rememberName = []
        
        while i <= longest:
            for element in elements:                
                try:
                    elementName = str(elements.index(element))
                    if i == 0:
                        header = '(' + str(len(elements)) + ')'
                    
                    if element[i].category == 'normalFunction1':
                        instruction = element[i].name + '(\'' + elementName + '\');\n'
                    
                    elif element[i].category == 'angleFunction1':
                        instruction = element[i].name + '(\'' + elementName + '\' , \'' + element[i].info + '\');\n'
                    
                    
                    elif element[i].category == 'normalFunction2':
                        if element[i] in rememberElement:
                            index = rememberElement.index(element[i])
                            instruction = element[i].name + '(\'' + rememberName[index] + '\' , \'' + elementName + '\');\n'
                            rememberElement.remove(element[i])
                            rememberName.pop(index)
    
                        elif element[i] not in rememberElement:
                            rememberElement.append(element[i])
                            rememberName.append(elementName)
                            element.insert(i+1, [])
                            if len(element) > longest: longest = len(element)
    
                        # else:
                        #     print("Da ist wohl etwas schief gelaufen bei normalFunction2!")
                    
                    elif element[i].category == 'angleFunction2':
                        if element[i] in rememberElement:
                            index = rememberElement.index(element[i])
                            instruction = element[i].name + '(\'' + rememberName[index] + '\' , \'' + elementName + '\' , \'' + element[i].info + '\');\n'
                            rememberElement.pop(index)
                            rememberName.pop(index)
    
                        elif element[i] not in rememberElement:
                            rememberElement.append(element[i])
                            rememberName.append(elementName)
                            element.insert(i+1, [])
                            if len(element) >= longest: longest = len(element)
    
                        # else:
                        #     print("Da ist wohl etwas schief gelaufen bei angleFunction2!")
                    
                    elif element[i].category == 'normalFunction3':
                        if rememberElement.count(element[i]) == 2:
                            indices = [j for j in range(len(rememberElement)) if rememberElement[j] == element[i]]
                            instruction = element[i].name + '(\'' + rememberName[indices[0]] + '\' , \'' + rememberName[indices[1]] + '\' , \'' + elementName + '\');\n'
                            rememberElement.pop(indices[0][1])
                            rememberElement.pop(indices[1][1])
                            rememberName.pop(indices[0][1])
                            rememberName.pop(indices[1][1])
    
                        elif rememberElement.count(element[i]) != 2:
                            rememberElement.append(element[i])
                            rememberName.append(elementName)
                            element.insert(i+1, [])
                            if len(element) > longest: longest = len(element)
    
                        # else:
                        #     print("Da ist wohl etwas schief gelaufen bei normalFunction3!")
                
                except Exception as e: 
                    pass
                    
                
                try: 
                    fullInstruction.append(instruction)
                    instruction = ''
                except: pass
            
            i += 1
        
        fullFile = 'circuit' + header + ';\n'
           
        for inst in fullInstruction:
            fullFile += inst
           
        return fullFile
    
    def generateQubitInstructions(self, elements):
        longest = len(max(elements, key=len))
        i = 0
        collectQubits = ''
        
        fullInstruction = []
        rememberElement = []
        rememberName = []
        
        while i <= longest:
            for element in elements:
                
                try:
                    elementName = str(elements.index(element))
                    if i == 0:
                        tupel = '(\'' + str(element[i].name) + '\', ' + str(element[i].info) + '),'
                        collectQubits += tupel 
                    
                    if element[i].category == 'normalFunction1':
                        instruction = element[i].name + '(\'' + element[0].name + '\');\n'
                    
                    elif element[i].category == 'angleFunction1':
                        instruction = element[i].name + '(\'' + element[0].name + '\' , \'' + element[i].info + '\');\n'
                    
                    elif element[i].category == 'normalFunction2':
                        if element[i] in rememberElement:
                            index = rememberElement.index(element[i])
                            instruction = element[i].name + '(\'' + rememberName[index] + '\' , \'' + element[0].name + '\');\n'
                            rememberElement.remove(element[i])
                            rememberName.pop(index)
    
                        elif element[i] not in rememberElement:
                            rememberElement.append(element[i])
                            rememberName.append(element[0].name)
                            element.insert(i+1, [])
                            if len(element) > longest: longest = len(element)
    
                        # else:
                        #     print("Da ist wohl etwas schief gelaufen bei normalFunction2!")
                    
                    elif element[i].category == 'angleFunction2':
                        if element[i] in rememberElement:
                            index = rememberElement.index(element[i])
                            instruction = element[i].name + '(\'' + rememberName[index] + '\' , \'' + element[0].name + '\' , \'' + element[i].info + '\');\n'
                            rememberElement.remove(element[i])
                            rememberName.pop(index)
    
                        elif element[i] not in rememberElement:
                            rememberElement.append(element[i])
                            rememberName.append(element[0].name)
                            element.insert(i+1, [])
                            if len(element) > longest: longest = len(element)
    
                        # else:
                        #     print("Da ist wohl etwas schief gelaufen bei angleFunction2!")
                    
                    elif element[i].category == 'normalFunction3':
                        if rememberElement.count(element[i]) == 2:
                            indices = [j for j in range(len(rememberElement)) if rememberElement[j] == element[i]]
                            instruction = element[i].name + '(\'' + rememberName[indices[0]] + '\' , \'' + rememberName[indices[1]] + '\' , \'' + element[0].name + '\');\n'
                            rememberElement.pop(indices[0][1])
                            rememberElement.pop(indices[1][1])
                            rememberName.pop(indices[0][1])
                            rememberName.pop(indices[1][1])
    
                        elif rememberElement.count(element[i]) != 2:
                            rememberElement.append(element[i])
                            rememberName.append(element[0].name)
                            element.insert(i+1, [])
                            if len(element) > longest: longest = len(element)
    
                        # else:
                        #     print("Da ist wohl etwas schief gelaufen bei normalFunction3!")
                
                except Exception as e: 
                    pass
                    
                
                try: 
                    fullInstruction.append(instruction)
                    instruction = ''
                except: pass
            i += 1
        
        fullFile = 'circuit(' + collectQubits[0:-1] + ');\n'
           
        for inst in fullInstruction:
            fullFile += inst
           
        return fullFile
        
        
    
    def generateFile(self, newPath):
        self.fullPath = newPath
        if self.fullPath[0][0].category == 'circuit':
            fileText = self.generateCircuitInstructions(self.fullPath)
        elif self.fullPath[0][0].category == 'qubit':
            fileText = self.generateQubitInstructions(self.fullPath)
        else: fileText = ''
        
        return fileText
    
    

                     
            
    
            
                
                
        
        
        
            
        
        
                
            