import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QButtonGroup
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
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
        self.currentID = 1
        self.buttongroup = QButtonGroup()
        self.title = 'PyQt5 button - pythonspot.com'
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

        

        button = {
                    "id": self.currentID,
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


    def createLayout(self, sentence, xPos, depth=2, buttons=[]):
        
        #find the rightmost x in respect to the current y value

        




        #find how many notes are in this depth excluding the head
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




            


        
        for i in range(1,len(sentence)):
            if isinstance(sentence[i], list):
                if len(sentence[i]) == 2 and isinstance(sentence[i][0], str) and isinstance(sentence[i][1], str):
                    #HEADER
                    self.increseID()
                    header = {
                        "id": self.currentID,
                        "name" : sentence[i][0],
                        "xpos" : xPositions[i-1],
                        "ypos" : (self.bHeight + 20)*depth
                    }

                    buttons.append(header)

                    #VALUE
                    self.increseID()


                    value = {
                        "id": self.currentID,
                        "name" : sentence[i][1],
                        "xpos" : xPositions[i-1],
                        "ypos" : (self.bHeight + 20)*(depth+1)
                    }
                    buttons.append(value)
                else:
                    tempxPos = xPositions[i-1]
                    if isinstance(sentence[i][1], list):
                        if len(sentence[i]) > 2:
                            

                            tempxPos = xPositions[i-1] + self.bWidth + 20

                    self.increseID()
                    header = {
                        "id" : self.currentID,
                        "name" : sentence[i][0],
                        "xpos" : tempxPos,
                        "ypos" : (self.bHeight + 20)*depth
                    }

                    buttons.append(header)


                    self.createLayout(sentence[i], tempxPos, depth+1, buttons)

        return buttons
            #else:







if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App(testVal.tree)
    sys.exit(app.exec_())