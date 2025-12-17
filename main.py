import pyxel
import random
import time

class Node:
    def __init__(self, position, direction):
        self.next = None
        self.position = position
        self.direction = direction

class LinkedList:
    def __init__(self, nodeClass, initPosition=(20,20), initDirection=(0)):
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
    
    def returnDirectionList(self):
        list = []
        temp = self.head
        while temp:
            list.append(temp.direction)
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

    def createSegment(self):
        lastPos = self.body.returnPositionList()[-1]
        lastDir = self.body.returnDirectionList()[-1]
        match self.body.returnDirectionList()[0]:
            case 0:
                self.body.insertAtEnd((lastPos[0], lastPos[1] + 10), lastDir)
            case 1:
                self.body.insertAtEnd((lastPos[0] + 10, lastPos[1]), lastDir)
            case 2: 
                self.body.insertAtEnd((lastPos[0], lastPos[1] -10), lastDir)
            case 3:
                self.body.insertAtEnd((lastPos[0] - 10, lastPos[1]), lastDir)

    def test(self):
        self.body.printList()

    def drawSnake(self):
        snakePosition = self.body.returnPositionList()
        for i in range(len(snakePosition)):
            pyxel.rect(snakePosition[i][0], snakePosition[i][1], 10, 10, 13)

class Fruit:
    def __init__(self, serpent):
        self.position = None
        while not self.position:
            tempPos = (random.randint(1,254), random.randint(1,254))
            if(not (tempPos in serpent.body.returnPositionList())):
                self.position = tempPos

class Jeu:
    def __init__(self, dimensions):
        self.dimensions = dimensions

    def initGame(self):
        pyxel.init(self.dimensions[0], self.dimensions[1])
        pyxel.load("snake.pyxres")
        self.snake = snake

    def startGame(self):
        pyxel.run(self.update, self.draw)

    def drawWindowPlay(self):
        pyxel.bltm(0,0,0,0,0,256,256)

    def update(self,bodyClass):
        if self.detection_collision():
            self.x_carre=60
            self.y_carre=60
        
        self.x_carre,self.y_carre=self.deplacement_carre(self.x_carre,self.y_carre)



    def deplacement(self):
        if pyxel.btn(pyxel.KEY_RIGHT) :
            
            self.x_carre += 1
        if pyxel.btn(pyxel.KEY_LEFT) :
            if self.x>0:
                self.x_carre += -1
        if  pyxel.btn(pyxel.KEY_UP):
            if self.y>0:
                self.y-=1
        
        if pyxel.btn(pyxel.KEY_DOWN):
            if self.y<120:
                self.y+=1

    def detection_collision(self):
        if Fruit.position[0]<self.x_carre<Fruit.position[0]+8:
            if  Fruit.position[1]<self.y_carre<Fruit.position[1]+8:
                return True
          
        return False
        

        

    def draw(self):
        pyxel.cls(0)