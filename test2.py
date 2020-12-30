import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QButtonGroup
from PyQt5.QtGui import QIcon, QPainter, QBrush, QPen
from PyQt5.QtCore import pyqtSlot, Qt
from collections.abc import Sequence
from itertools import chain, count
import numpy as np
import tree





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



class App(QWidget):

    def __init__(self, text):
        super().__init__()
        self.rightmostX = 0
        self.paintPos = []
        self.currentID = 1
        self.parentX = 0
        self.parentY = 0
        self.currentPosition = [0]
        self.buttongroup = QButtonGroup()
        self.title = 'Tree'
        self.left = 10
        self.top = 10
        self.width = 700
        self.height = 700
        self.bWidth = 80
        self.bHeight = 40
        self.margin = 20
        self.selected = []

        self.depth = self.findDepth(text)
        self.initUI(text)
    
    def increseID(self):
        self.currentID += 1


    #draws a arrow from parent to child
    def paintEvent(self, event):
        for i in self.paintPos:
            qp = QPainter()
            pxPos = int(i["pxPos"])
            pyPos = int(i["pyPos"])
            cxPos = int(i["cxPos"])
            cyPos = int(i["cyPos"])


            qp.begin(self)

            qp.setPen(Qt.red)

            qp.setBrush(Qt.white)

            #painter.drawLine(400, 100, 100, 100)
            qp.drawLine(pxPos, pyPos, cxPos, cyPos)
        qp.end()

    def initUI(self, text):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.buttongroup.buttonClicked[int].connect(self.on_button_clicked)
        if not self.buttongroup.buttons():

            buttons = self.createButtons(text)
            for b in buttons:
                button = QPushButton(b["name"], self)
                button.setGeometry(int(b["xpos"]),int(b["ypos"]),self.bWidth,self.bHeight)
                self.buttongroup.addButton(button,b["id"])
        


        #button1.clicked.connect(self.on_click)
        #button2.clicked.connect(self.on_click)
        self.paintEvent("test")
        self.show()

    def on_button_clicked(self,ID):
        print(ID)

    def createButtons(self,text):
        buttons = []
        
        yPos = 10
        #below is temp, change later
        sent = text[0][1]
        depth = self.findDepth(sent)
        maxHeight = self.height // depth

        self.parentX = self.width/2 
        self.parentY = self.bHeight + 40

        button = {
                    "id": self.currentID,
                    "name" : sent[0],
                    "xpos" : self.width/2,
                    "ypos" : self.bHeight + 40,
                    "position": self.currentPosition
                }
        buttons.append(button)

        buttons2 = self.createLayout(sent,self.width/2)
        buttons = buttons + buttons2
        return buttons
        
        

    def findDepth(self, text):
        depth = lambda L: isinstance(L, list) and max(map(depth, L))+1
        return depth(text)

    def DefaultXPos(self, sentence, xPos, buttons):
        #find how many notes are in this depth excluding the head

        #start by checking if the rightmost xposition is clos

        length = len(sentence)-1
        xPositions = []
        #create list of xPositions
        
        if length%2 == 0:

            #find new xpos in respect to the children of previous note
            
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
            mid = []
            mid.append(int(xPos))
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


    def createLayout(self, sentence, xPos, depth=2, buttons=[]):
        
        xPositions = self.DefaultXPos(sentence, xPos, buttons)
        
        for i in range(1,len(sentence)):
            tempPos = self.currentPosition
            tempPos[-1] = i
            if isinstance(sentence[i], list):
                if len(sentence[i]) == 2:
                    if isinstance(sentence[i][0], str) and isinstance(sentence[i][1], str):
                        print("header and leaf", sentence[i])
                        print(i)
                        if i == len(sentence) - 1:
                            print("the goal is heare",sentence[i])
                            self.rightmostX = xPositions[i-1]
                        
                        #HEADER
                        self.increseID()
                        tempPos.append(0)


                        #paint the arrow from parent to child node
                        if self.rightmostX >= xPositions[i-1]:
                            if i != len(sentence)-1:
                                print("yesMOON")
                                print(xPositions[i-1])
                                xPositions[i-1] = self.rightmostX + self.bWidth + 20
                                

                                for i in range(i,len(xPositions)):
                                    xPositions[i] = xPositions[i-1] + (self.bWidth + 20)



                                print(xPositions[i-1])
                        paint = {
                            "pxPos" : self.parentX,
                            "pyPos" : self.parentY,
                            "cxPos" : xPositions[i-1],
                            "cyPos" : (self.bHeight + 40)*depth
                        }
                        self.paintPos.append(paint)

                        

                        header = {
                            "id": self.currentID,
                            "name" : sentence[i][0],
                            "xpos" : xPositions[i-1],
                            "ypos" : (self.bHeight + 40)*depth,
                            "position": tempPos
                        }

                        buttons.append(header)
                        #VALUE
                        self.increseID()

                        tempPos.pop()
                        tempPos.append(1)


                        #paint the arrow from parent to child node
                        paint2 = {
                            "pxPos" : self.parentX,
                            "pyPos" : (self.bHeight + 40)*depth,
                            "cxPos" : xPositions[i-1],
                            "cyPos" : (self.bHeight + 40)*(depth+1)
                        }

                        self.paintPos.append(paint2)

                        value = {
                            "id": self.currentID,
                            "name" : sentence[i][1],
                            "xpos" : xPositions[i-1],
                            "ypos" : (self.bHeight + 40)*(depth+1),
                            "position": tempPos
                        }
                        tempPos.pop()
                        buttons.append(value)


                    else:
                        print("not header and leaf", sentence[i])


                        self.increseID()
                        tempPos.append(0)


                        #paint the arrow from parent to child node
                        paint = {
                            "pxPos" : self.parentX,
                            "pyPos" : self.parentY,
                            "cxPos" : xPositions[i-1],
                            "cyPos" : (self.bHeight + 40)*depth
                        }
                        self.paintPos.append(paint)



                        header = {
                            "id": self.currentID,
                            "name" : sentence[i][0],
                            "xpos" : xPositions[i-1],
                            "ypos" : (self.bHeight + 40)*depth,
                            "position": tempPos
                        }

                        buttons.append(header)
                        #VALUE
                        self.increseID()

                        tempPos.pop()
                        tempPos.append(1)


                        #paint the arrow from parent to child node
                        paint2 = {
                            "pxPos" : self.parentX,
                            "pyPos" : (self.bHeight + 40)*depth,
                            "cxPos" : xPositions[i-1],
                            "cyPos" : (self.bHeight + 40)*(depth+1)
                        }

                        self.paintPos.append(paint2)

                        value = {
                            "id": self.currentID,
                            "name" : sentence[i][1][0],
                            "xpos" : xPositions[i-1],
                            "ypos" : (self.bHeight + 40)*(depth+1),
                            "position": tempPos
                        }
                        tempPos.pop()
                        buttons.append(value)
                        self.createLayout(sentence[i][1], xPositions[i-1], depth+2, buttons)
                else:
                    print("len(sentence) != 2", sentence[i])

                    tempxPos = xPositions[i-1]
                    if isinstance(sentence[i][1], list):
                        if len(sentence[i]) > 2:                            

                            tempxPos = xPositions[i-1] + self.bWidth + 20
                        else:
                            print("<=2")

                    self.increseID()
                    tempPos.append(0)
                    header = {
                        "id" : self.currentID,
                        "name" : sentence[i][0],
                        "xpos" : tempxPos,
                        "ypos" : (self.bHeight + 40)*depth,
                        "position": tempPos
                    }
                    buttons.append(header)


            
            
                    self.createLayout(sentence[i], tempxPos, depth+1, buttons)

            else:
                print("sentence i not list", sentence[i])
                tempxPos = xPositions[i-1]
                value = {
                        "id" : self.currentID,
                        "name" : sentence[i],
                        "xpos" : tempxPos,
                        "ypos" : (self.bHeight + 40)*depth,
                        "position": tempPos
                    }
                buttons.append(value)

        return buttons
            #else:
       







if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App(testVal.tree)
    sys.exit(app.exec_())