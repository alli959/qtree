#-----TREE------

#Attributes:

    #text - array of all sentences
    #tree - array of sentences in the form of ['' [IP-MAT [NP-SBJ [N-N bar]]]]

class Tree:
    def __init__(self, text, ind):
        self.text = text
        tree = []
        indTemp = []
        sentencenr = 0
        for i in text:
            a,b = self.createTree(i, 0, sentencenr)
            tree.append(a)
            indTemp.append(b)
            sentencenr += 1
        self.tree = tree
        self.ind = indTemp



    def createTree(self, text, ind, sentencenr, verbose=False):
        """The basic idea here is to represent the file contents as a long string
        and iterate through it character-by-character (the 'ind' variable
        points to the current character). Whenever we get to a new tree,
        we call the function again (recursively) to read it in."""
                
        if verbose:
            print("Reading new subtree", text[ind:][:10])

        # consume any spaces before the tree
        while text[ind].isspace():
            ind += 1

        if text[ind] == "(":
            if verbose:
                print("Found open paren")
            tree = []
            ind += 1

            # record the label after the paren
            label = ""
            while not text[ind].isspace() and text[ind] != "(":
                label += text[ind]
                ind += 1
            if label != '':

                tree.append(label)
            else:
                tree.append("sentence Nr. " + str(sentencenr))
            if verbose:
                print("Read in label:", label)

            # read in all subtrees until right paren
            subtree = True
            while subtree:
                # if this call finds only the right paren it'll return False
                subtree, ind = self.createTree(text, ind, sentencenr, verbose=verbose)
                if subtree:
                    tree.append(subtree)

            # consume the right paren itself
            ind += 1
            assert(text[ind] == ")")
            ind += 1

            if verbose:
                print("End of tree", tree)

            return tree, ind

        elif text[ind] == ")":
            # there is no subtree here; this is the end paren of the parent tree
            # which we should not consume
            ind -= 1
            return False, ind

        else:
            # the subtree is just a terminal (a word)
            word = ""
            while not text[ind].isspace() and text[ind] != ")":
                word += text[ind]
                ind += 1

            if verbose:
                print("Read in word:", word)

            return word, ind
        
    #add leaf to the tree

    def addLeaf(self, positions, label, value):
        sentence = self.tree
        print(sentence)
        string = "sentence"
        for i in positions:
            string = string + '[' + str(i) + ']'
        string = string + ".append([{},".format(label)
        string = string + "{}])".format(value)
        exec(string)
        self.updateTree(sentence)

    def removeLeaf(self, positions):
        sentence = self.tree
        string = "del sentence"
        for i in positions:
            string = string + '[' + str(i) + ']'
        self.updateTree(sentence)
    
        
    
    def updateTree(self, newTree):
        self.tree = newTree

    

    


            


        