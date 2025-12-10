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

snake = Serpent(LinkedList, Node)
snake.createSegment((0,1), 1)
snake.test()