import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from collections.abc import Sequence
from itertools import chain, count
import numpy as np
import tree

testData = '''(  (IP-MAT
    (NP-SBJ (NPR-N Steinunn))
    (VBDI seldi)
    (NP-OB2 (NPR-D Mirko))))'''




testVal = tree.Tree([testData], 0)

print(testVal)

class App(QWidget):

    def __init__(self, text):
        super().__init__()
        self.title = 'PyQt5 button - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 700
        self.height = 700
        self.depth = self.findDepth(text)
        self.initUI(text)
    
    def initUI(self, text):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        buttons = self.createButtons(text)

        button1 = QPushButton('PyQt5 button', self)
        button2 = QPushButton('PyQt5 button', self)

        button1.setToolTip('This is an example button')
        button1.move(90,70)
        button2.move(30,30)

        button1.clicked.connect(self.on_click)
        button2.clicked.connect(self.on_click)
        
        self.show()

    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')

    def createButtons(self,text):
        print(text[0][1])
        yPos = 10
        #below is temp, change later
        sent = text[0][1]
        depth = self.findDepth(sent)
        maxHeight = self.height // depth
        print(maxHeight)


        print(maxHeight)
        return []
        
        

    def findDepth(self, text):
        depth = lambda L: isinstance(L, list) and max(map(depth, L))+1
        return depth(text)


    def createLayout(self, sentence, depth=1):
        buttons = []
        for i in range(len(sentence)):
            if isinstance(sentence[i], list):
                createLayout(sentence[i], depth+1)
            else:
                button = {
                    name : "",
                    xpos : 0,
                    ypos : 0
                }
                if isinstance(sentence[i+1],list):
                    button.name = sentence[i]
                    button.xpos = self.width / 2
                    button.ypos = depth * (self.height // """tempVal""" 3)
                buttons.append(button)
                else:
                    for j in sentence[i]:
                    
        #QPushButton('PyQt5 button', self)






if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App(testVal.tree)
    sys.exit(app.exec_())