import pyxel
import random
import time

width = 256
height = 256








def detection_collision(serpent):
    head_x, head_y = serpent.body.returnPositionList()[0] 

    if head_x < 0 or head_x >= width or head_y < 0 or head_y >= height:
        return True

    body_positions = serpent.body.returnPositionList()[1:]  
    if (head_x, head_y) in body_positions:
        return True

    return False





       
        


class Node:
    def __init__(self, position, direction):
        self.next = None
        self.position = position
        self.direction = direction

class LinkedList:
    def __init__(self, nodeClass, initPosition=(20,20), initDirection=0):
        self.head = nodeClass(initPosition, initDirection)
        self.node = nodeClass
    


    def insertAtBeginning(self,position,direction):
        new_node=self.node(position,direction)
        new_node.next=self.head
        self.head=new_node
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
    
    def sizeList(self):
        if self.head is not None:
            comp=1
            temp=self.head
            while temp:
                comp=comp+1
                temp=temp.next
            return comp
        else:
            return 0
    def deleteAtEnd(self):
        temp=self.head
        while temp.next.next:
            temp=temp.next
        temp.next=None       


class Serpent:
    def __init__(self, bodyClass, nodeClass):
        self.bodyClass = bodyClass
        self.nodeClass = nodeClass
        self.body = self.bodyClass(self.nodeClass)
        self.is_eating=False

    def createSegment(self):
        lastPos = self.body.returnPositionList()[-1]
        lastDir = self.body.returnDirectionList()[-1]
        match self.body.returnDirectionList()[0]:
            case 0:
                self.body.insertAtEnd((lastPos[0], lastPos[1] - 10), lastDir)
            case 1:
                self.body.insertAtEnd((lastPos[0] - 10, lastPos[1]), lastDir)
            case 2: 
                self.body.insertAtEnd((lastPos[0], lastPos[1] +10), lastDir)
            case 3:
                self.body.insertAtEnd((lastPos[0] + 10, lastPos[1]), lastDir)

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

    def updatebodyposition_mypov(self,newDirection):
        self.body.head.direction = newDirection
        
        match newDirection:
            case 0:
                new_position = (self.body.head.position[0], self.body.head.position[1] + 10)
            case 1:
                new_position = (self.body.head.position[0] + 10, self.body.head.position[1])
            case 2:
                new_position = (self.body.head.position[0], self.body.head.position[1] - 10)
            case 3:
                new_position= (self.body.head.position[0] - 10, self.body.head.position[1])
        self.body.insertAtBeginning(new_position,newDirection)
        if not self.is_eating:
            self.body.deleteAtEnd()


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

    def drawFruit(self):
        pyxel.rect(self.position[0],self.position[1],10,10,60)

    def FruitRandomPosition(self,serpent):
            tempPos = (random.randint(1,254), random.randint(1,254))
            if(not (tempPos in serpent.body.returnPositionList())):
                self.position = tempPos

class Jeu:
    def __init__(self, snake, dimensions=(256,256)):
        pyxel.init(dimensions[0], dimensions[1])
        self.snake = snake
        self.fruit=Fruit(self.snake)
        self.direction=0
        self.directions_interdites = { 2: 0, 0: 2, 3: 1, 1: 3}
        self.score=0
        self.ongoing=True
        
    def startGame(self):
        pyxel.run(self.update, self.draw)

    def drawWindowPlay(self):
        pyxel.bltm(0,0,0,0,0,256,256)

    def update(self):

        if self.detection_collision():
            self.ongoing=False
      

        
        if self.detection_collision_fruit():
            self.fruit.FruitRandomPosition(self.snake)
        
        




        self.deplacements()
        time.sleep(0.05)

    def draw(self):
        pyxel.cls(0)
        self.drawWindowPlay()
        if   self.ongoing:
            self.snake.drawSnake()
            self.fruit.drawFruit()
            pyxel.text(5,5, 'SCORE:'+ str(self.score), 7)
        else:
            pyxel.text(50,64, 'GAME OVER', 20)

    def deplacements(self):
        prev_direction=self.direction
        if pyxel.btn(pyxel.KEY_UP):
            self.direction=2
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.direction=1
        if pyxel.btn(pyxel.KEY_DOWN):
            self.direction=0
        if pyxel.btn(pyxel.KEY_LEFT):
            self.direction=3



        if self.direction == self.directions_interdites[prev_direction]:
            self.direction = prev_direction

        self.snake.updatebodyposition_mypov(self.direction)
    def detection_collision_fruit(self):
        
        if self.fruit.position[0]<=self.snake.body.head.position[0]<=self.fruit.position[0]+10:
            if  self.fruit.position[1]<=self.snake.body.head.position[1]<=self.fruit.position[1]+10:
            
         
        if (self.snake.body.head.position[0]< self.fruit.position[0] + 10
             and self.snake.body.head.position[0] + 10 > self.fruit.position[0]
            and self.snake.body.head.position[1]< self.fruit.position[1] + 10 and
             self.snake.body.head.position[1]+ 10 > self.fruit.position[1]):
                self.snake.is_eating=True
                self.score+=1

                return True
        
     
          


        self.snake.is_eating=False        
        return False
    
    def detection_collision(self):
        head_x, head_y = self.snake.body.returnPositionList()[0] 
 
        if head_x < 0 or head_x >= width or head_y < 0 or head_y >= height:
           self.ongoing=False
           return True

        body_positions = self.snake.body.returnPositionList()[1:]  
        if (head_x, head_y) in body_positions:
           self.ongoing=False
           return True
       
        return False




snake = Serpent(LinkedList, Node)
snake.createSegment()
snake.createSegment()
test = Jeu(snake=snake)
test.startGame()
