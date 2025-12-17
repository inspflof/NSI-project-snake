import pyxel
import random
import time

width = 128
height = 128




pyxel.init(width, height, title="SNAKE", fps=60, display_scale=None)




def init():
    global x_carre, y_carre
    x_carre = 60
    y_carre = 60
    pyxel.run(update, draw)




def detection_collision(x, y):
    if x >= 120 or x< 3 or y >= 118 or y < 4:
        return True
    return False 
            


  


    

def update():
    global x_carre, y_carre
    x_carre, y_carre = deplacement_carre(x_carre, y_carre)
    if detection_collision(x_carre, y_carre):
        x_carre, y_carre = 60, 60 


       

def draw():
    pyxel.cls(1)
    pyxel.rect(x_carre, y_carre, 8, 8, 13)
    pyxel.rect(0, 125, 160, 3, 5)
    pyxel.rect(0, 0, 160, 3, 5)
    pyxel.rect(0, 0, 3, 160, 5)
    pyxel.rect(125,0,3,160,5)
        





def deplacement_carre(x, y):
    
   if pyxel.btn(pyxel.KEY_UP):
      if y > 0:
         y = y - 1
   if pyxel.btn(pyxel.KEY_DOWN):
      if y < 120:
         y = y + 1
   if pyxel.btn(pyxel.KEY_LEFT):
      if x > 0:
         x = x - 1
   if pyxel.btn(pyxel.KEY_RIGHT):
      if x < 120:
         x = x + 1
   return x, y






class Node:
    def __init__(self, position, direction):
        self.next = None
        self.position = position
        self.direction = direction

class LinkedList:
    def __init__(self, nodeClass, initPosition=(20,20), initDirection=0):
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

    def changeDirPosHead(self, newDirection):
        self.body.head.direction = newDirection
        match newDirection:
            case 0:
                self.body.head.position = (self.body.head.position[0], self.body.head.position[1] + 10)
            case 1:
                self.body.head.position = (self.body.head.position[0] + 10, self.body.head.position[1])
            case 2:
                self.body.head.position = (self.body.head.position[0], self.body.head.position[1] - 10)
            case 3:
                self.body.head.position = (self.body.head.position[0] - 10, self.body.head.position[1])

    def updateBodyPosition(self):
        temp = self.body.head.next  # Start from the second segment, not the head
        prev_position = self.body.head.position  # Store the head's position
        prev_direction = self.body.head.direction  # Store the head's direction
        while temp:
            current_position = temp.position  # Store the current segment's position
            current_direction = temp.direction  # Store the current segment's direction
            temp.position = prev_position  # Update the current segment's position to the previous segment's position
            temp.direction = prev_direction  # Update the current segment's direction to the previous segment's direction
            prev_position = current_position  # Update the previous position for the next segment
            prev_direction = current_direction  # Update the previous direction for the next segment
            temp = temp.next

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
        self.snake = snake

    def startGame(self):
        pyxel.run(self.update, self.draw)

    def drawWindowPlay(self):
        pyxel.bltm(0,0,0,0,0,256,256)

    def update(self):
        self.deplacements()
        snake.updateBodyPosition()
        time.sleep(0.1)

    def draw(self):
        pyxel.cls(0)
        self.drawWindowPlay()
        self.snake.drawSnake()

    def deplacements(self):
        if pyxel.btn(pyxel.KEY_UP):
            self.snake.changeDirPosHead(2)
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.snake.changeDirPosHead(1)
        if pyxel.btn(pyxel.KEY_DOWN):
            self.snake.changeDirPosHead(0)
        if pyxel.btn(pyxel.KEY_LEFT):
            self.snake.changeDirPosHead(3)


snake = Serpent(LinkedList, Node)
snake.createSegment()
snake.createSegment()
test = Jeu(snake=snake)
test.startGame()

