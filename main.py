import pyxel
import random
import time

class Node:
    def __init__(self, position, direction):
        self.next = None
        self.position = position
        self.direction = direction

class LinkedList:
    def __init__(self, nodeClass, initPosition=(0,0), initDirection=(0)):
        self.head = nodeClass(initPosition, initDirection)
        self.node = nodeClass

    def insertAtEnd(self, position, direction):
        new_node = self.node(position, direction)  # Create a new node
        last = self.head 
        while last.next:  # traverse the list to find the last node
            last = last.next
        last.next = new_node  # Make the new node the next node of the last node

    def returnPositionList(self):
        list = []
        temp = self.head
        while temp:
            list.append(temp.position)
            temp = temp.next
        return list

    def printList(self):
        temp = self.head # Start from the head of the list
        while temp:
            print(temp.position, temp.direction,end=' | ') # Print the data in the current node
            temp = temp.next # Move to the next node
        print()  # Ensures the output is followed by a new line

class Serpent:
    def __init__(self, bodyClass, nodeClass):
        self.bodyClass = bodyClass
        self.nodeClass = nodeClass
        self.body = self.bodyClass(self.nodeClass)

    def createSegment(self, position, direction):
        self.body.insertAtEnd(position, direction)

    def test(self):
        self.body.printList()

class Fruit:
    def __init__(self, bodyList) -> None:
        self.position = None
        while not self.position:
            tempPos = (random.randint(1,254), random.randint(1,254))
            if(not (tempPos in bodyList.returnPositionList())):
                self.position = tempPos

class Jeu:
    def __init__(self, dimensions):
        self.dimensions = dimensions

    def initGame(self):
        pyxel.init(self.dimensions[0], self.dimensions[1])
        pyxel.load("snake.pyxres")

    def startGame(self):
        pyxel.run(self.update, self.draw)

    def drawWindowPlay(self):
        pyxel.bltm(0,0,0,0,0,256,256)

    def update(self):
        pass

    def draw(self):
        pyxel.cls(0)