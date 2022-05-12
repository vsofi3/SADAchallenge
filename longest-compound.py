"""
Sofi Vinas: SADA challenge
5/10/2022
"""
# set up
import sys
import os

# Using a base Node class
class Node:
    def __init__(self, character=None, leaf=False):
        self.character = character
        self.children = {}
        self.leaf = leaf


# defining our Tree class
class Tree:
    def __init__(self):
        # base root is Node
        self.root = Node()
        self.count = {}

    def __contains__(self, baseWord):
        #start at root of tree
        currentNode = self.root
        for character in baseWord:
            if character not in currentNode.children:
                return False
            currentNode = currentNode.children[character]
        #return boolean
        return currentNode.leaf

    # return number of subwords in the entire baseWord
    def dissect(self, baseWord):
        # check for base case
        if not baseWord:
            return 0, []

        # have we traversed this?
        if baseWord in self.count:
            return self.count[baseWord]
        # If not then we need to start traversing the trie
        currentNode = self.root

        # second base case
        # check the letters in the word
        for marker, character in enumerate(baseWord):
            if character not in currentNode.children:
                return 0, []
            currentNode = currentNode.children[character]
            if currentNode.leaf:
                suffix = baseWord[1+marker:]
                # call our dissect function again on the suffix
                numSuffix, listSuffix = self.dissect(suffix)
                self.count[suffix] = numSuffix, listSuffix
                # check if we can dissect this
                if numSuffix:
                    return numSuffix + 1, [baseWord[:1+marker]] + listSuffix
        return currentNode.leaf, [baseWord]


    def returnCompound(self, word):
        #call our dissect function above
        numDissected, dissectedList = self.dissect(word)
        #return with boolean value
        return (1 < numDissected), numDissected, dissectedList


    def insert(self, baseWord):
        # start from the root of the tree
        currentNode = self.root
        for character in baseWord:
            # traverse each letter
            if character not in currentNode.children:
                # create new Node, insert
                currentNode.children[character] = Node(character)
            currentNode = currentNode.children[character]
        #return true
        currentNode.leaf = True


def processFile(inputFile):
    # create new trie data structure
    newTree = Tree()
    # create empty words list to add to
    wordsUsed = []
    # open file to "read"
    with open(inputFile, 'r') as f:
        for line in f:
            # processing input file
            current = line.strip()
            newTree.insert(current)
            wordsUsed.append(current)
    return newTree, wordsUsed


def createList(inputTree, words):
    wordList = []
    for word in words:
        goodToGo, quant, otherList = inputTree.returnCompound(word)
        if goodToGo:
            wordList.append((word, quant, otherList))
    return wordList


def processList(wordList):
    #sort in reverse
    wordList.sort(key=lambda tuple_struct: len(tuple_struct[0]), reverse=True)
    # return the list
    return wordList

# takes from words.txt which contains all possible words we can use
def testProgram(usingFile='words.txt'):
    trie, words = processFile(usingFile)
    # using 2d array
    wordList = processList(createList(trie, words))

    # using 2d array
    longestCompound = wordList[0][0]

    if len(longestCompound):
        print("Longest compound word is: " + longestCompound)
        print("Created from " + str(wordList[0][1]) + " base word(s): " + str(wordList[0][2]))
    else:
        print("Cannot create largest compound word from this list.")

    print("Number of compound words is: " + str(len(wordList)))

    print("\n")
    return trie, words, wordList


def main(argv):
    # run program as "python3 longest-compound.py testDox.txt"
    filename = sys.argv[1]

    # check if valid file path
    if not os.path.isfile(filename):
        print("Error opening file \"" + filename + "\"")
        #exit program completely
        sys.exit()
    testProgram(filename)


# run the program
if __name__ == "__main__":
    main(sys.argv)