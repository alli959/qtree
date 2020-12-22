import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from collections.abc import Sequence
from itertools import chain, count
import numpy as np
import tree
from random import random
testData = '''(  (IP-MAT
    (NP-SBJ (PRO-D Honum))
    (VBDI blöskraði)
    (PP
      (P þegar)
      (CP-ADV
        (C 0)
        (IP-SUB
          (NP-SBJ (NP (D-D þessi) (N-D niðurstaða)))
          (RDDI varð)
          (ADJP (ADJ-N ljós)))))))'''




testVal = tree.Tree([testData], 0)

print(testVal.tree)


class App(QWidget):

    def __init__(self, text):
        super().__init__()
        self.title = 'PyQt5 button - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 700
        self.height = 700
        self.bWidth = 80
        self.bHeight = 40
        self.margin = 20

        self.depth = self.findDepth(text)
        self.initUI(text)
    
    def initUI(self, text):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        buttons = self.createButtons(text)
        for b in buttons:
            button = QPushButton(b["name"], self)
            button.setGeometry(int(b["xpos"]),int(b["ypos"]),self.bWidth,self.bHeight)


        


        #button1.clicked.connect(self.on_click)
        #button2.clicked.connect(self.on_click)
        
        self.show()

    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')

    def createButtons(self,text):
        buttons = []
        
        yPos = 10
        #below is temp, change later
        sent = text[0][1]
        depth = self.findDepth(sent)
        maxHeight = self.height // depth
        button = {
                    "name" : sent[0],
                    "xpos" : self.width/2,
                    "ypos" : self.bHeight + 20
                }
        buttons.append(button)

        buttons2 = self.createLayout(sent,self.width/2)
        buttons = buttons + buttons2

        return buttons
        
        

    def findDepth(self, text):
        depth = lambda L: isinstance(L, list) and max(map(depth, L))+1
        return depth(text)


    def createLayout(self, sentence, xPos, depth=2, buttons=[], prevx = -1):
        
        xPositions = self.defaultxPos(sentence, xPos)
        if prevx == -1:
            prevx = xPositions[-1]
        prevRightMost = xPositions[-1]
        print(prevRightMost)
        
        for i in range(1,len(sentence)):
            if isinstance(sentence[i], list):
                if len(sentence[i]) == 2 and isinstance(sentence[i][0], str) and isinstance(sentence[i][1], str):
                    #HEADER
                    header = {
                        "id": i,
                        "name" : sentence[i][0],
                        "xpos" : xPositions[i-1],
                        "ypos" : (self.bHeight + 20)*depth
                    }

                    buttons.append(header)

                    #VALUE
                    value = {
                        "id": i,
                        "name" : sentence[i][1],
                        "xpos" : xPositions[i-1],
                        "ypos" : (self.bHeight + 20)*(depth+1)
                    }
                    buttons.append(value)
                else:
                    tempxPos = xPositions[i-1]
                    xPos = self.findXPos(buttons, sentence[i], tempxPos)
                    
                    header = {
                        "id": i,
                        "name" : sentence[i][0],
                        "xpos" : xPos,
                        "ypos" : (self.bHeight + 20)*depth
                    }
                    buttons.append(header)
                    

                    self.createLayout(sentence[i], xPos, depth+1, buttons)

        return buttons
            #else:
    def defaultxPos(self, sentence, xPos):
            #find how many notes are in this depth excluding the head

        length = len(sentence)-1
        xPositions = []

        rightxpos = 0


        if length%2 == 0:



            left = []
            right = []

            #left list
            for i in range(int(length/2)):
                if not left:
                    left.append(xPos-(self.bWidth + 20))
                else:
                    left.append(left[-1]-(self.bWidth + 20))

            #right list
            for i in range(int(length/2)):
                if not right:
                    right.append(xPos+(self.bWidth + 20))
                else:
                    right.append(right[-1]+(self.bWidth + 20))

            left.reverse()
            xPositions = left + right
        else:


            cnotelength = int((len(sentence[1]))-1)/2

            tempLeftXPos = xPos - (cnotelength*(self.bWidth+20))


            mid = [xPos]
            left = []
            right = []

            #left list
            for i in range(int((length-1)/2)):
                if not left:
                    left.append(xPos-(self.bWidth + 20))
                else:
                    left.append(left[-1]-(self.bWidth + 20))

            #right list
            for i in range(int((length-1)/2)):
                if not right:
                    right.append(xPos+(self.bWidth + 20))
                else:
                    right.append(right[-1]+(self.bWidth + 20))
            left.reverse()
            xPositions = left + mid + right
        
        return xPositions

    def findXPos(self, buttons, sentence, xPos):
        if buttons:

            rightMost = self.rightMostX(buttons)
            leftMost = self.leftMostX(sentence, xPos, xPos)
            #print("sentence",sentence)
            #print("rightMost", rightMost)
            #print("leftMost", leftMost)
            #print("xPosBefore",xPos)

            #how much we should move each note
            mover = 0
            if rightMost > leftMost:
                while rightMost > leftMost:
                    leftMost += (self.bWidth + 20)
                    xPos += (self.bWidth + 20)
            
            
        return xPos


    def rightMostX(self, buttons):
        maxX = 0
        for i in buttons:
            if i["xpos"] > maxX:
                maxX = i["xpos"]
                print(i["id"])
        return maxX
    


    #input sentence[i]
    def leftMostX(self,sentence, xpos, leftmost):
        leftX = - (self.bWidth + 20)
        rightX = (self.bWidth + 20)
        length = len(sentence)

        #check current row
        if length%2 == 0:
            xpos = xpos + int((length/2)*leftX)
            if xpos < leftmost:
                leftmost = xpos
        else:
            xpos = xpos + int((length-1/2)*leftX)
            if xpos < leftmost:
                leftmost = xpos
        
            
        for i in range(1,length):
            xpos = xpos + rightX
            if isinstance(sentence[i], str):
                return leftmost
            else:
                self.leftMostX(sentence[i], xpos, leftmost)

        return leftmost




            









if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App(testVal.tree)
    sys.exit(app.exec_())