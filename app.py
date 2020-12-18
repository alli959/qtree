# coding=utf-8
import tkinter as tk
from tkinter import filedialog, Text
import os
import re
import json
import nltk
from nltk.corpus import treebank
import tree



 


root = tk.Tk()
apps = []

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



print(testData)

sentarr = []
sentences = testData.split('\n\n')
tree = tree.Tree(sentences,0)
'''
for i in sentences:
    tree,ind = readTree(i, 0)
    sentarr.append(tree)'''

print(tree.tree)

'''
def drawTree(tree, ind):
    for i in tree:
        temp = i[0] + drawTree(i[1:], 0)
        print(temp)'''



def addApp():
    filename = filedialog.askopenfilename(initialdir="/", title="Select File", filetypes=(("psd files", "*.psd"), ("all files", "*.*")))
    apps.append(filename)
    print(filename)

canvas = tk.Canvas(root, height=700, width=700, bg="#263D42")
canvas.pack()




frame = tk.Frame(root, bg="white")
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

def test():
    print("yes")
testlab = tk.Label(master=frame, bg="#ffffff", text="test")
testlab.grid(row=2)




openFile = tk.Button(root, text="Open File", padx=10, pady=5, fg="white", bg="#263D42", command=addApp)
openFile.pack()
runApps = tk.Button(root, text="Run Apps", padx=10, pady=5, fg="white", bg="#263D42")

runApps.pack()

print(root.winfo_width)

root.mainloop()