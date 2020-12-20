# coding=utf-8
import tkinter as tk
from tkinter import filedialog, Text
import os
import numpy as np
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import re
import json
import tree



class App(QWidget):

    def __init__(self, text):
        super().__init__()
        self.title = 'PyQt5 button - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 700
        self.height = 700

        self.initUI(text)
    
    def initUI(self, text):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        buttons = []

        self.createButtons(text)
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
        test = np.array(text)
        print(test)








testData = '''(  (IP-MAT
    (NP-SBJ (NPR-N Steinunn))
    (VBDI seldi)
    (NP-OB2 (NPR-D Mirko))
    (NP-OB1 (ADJ-A tæknilega) (N-A fjarstýringu))))

(  (IP-MAT
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




sentarr = []
sentences = testData.split('\n\n')
tree = tree.Tree(sentences,0)
'''
for i in sentences:
    tree,ind = readTree(i, 0)
    sentarr.append(tree)'''





'''
def drawTree(tree, ind):
    for i in tree:
        temp = i[0] + drawTree(i[1:], 0)
        print(temp)'''



def addApp():
    filename = filedialog.askopenfilename(initialdir="/", title="Select File", filetypes=(("psd files", "*.psd"), ("all files", "*.*")))
    apps.append(filename)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App(tree.tree)
    sys.exit(app.exec_())