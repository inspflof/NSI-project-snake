import pyxel
import random

width = 256
height = 256


class Node:
    def __init__(self, position, direction):
        self.next = None
        self.position = position
        self.direction = direction


class LinkedList:
    def __init__(self, nodeClass, initPosition=(20, 20), initDirection=0):
        self.head = nodeClass(initPosition, initDirection)
        self.node = nodeClass

    def insertAtBeginning(self, position, direction):
        new_node = self.node(position, direction)
        new_node.next = self.head
        self.head = new_node

    def insertAtEnd(self, position, direction):
        new_node = self.node(position, direction)
        temp = self.head
        while temp.next:
            temp = temp.next
        temp.next = new_node

    def deleteAtEnd(self):
        if not self.head.next:
            return
        temp = self.head
        while temp.next.next:
            temp = temp.next
        temp.next = None

    def returnPositionList(self):
        res = []
        temp = self.head
        while temp:
            res.append(temp.position)
            temp = temp.next
        return res

    def returnDirectionList(self):
        res = []
        temp = self.head
        while temp:
            res.append(temp.direction)
            temp = temp.next
        return res


class Serpent:
    def __init__(self, bodyClass, nodeClass):
        self.body = bodyClass(nodeClass)
        self.is_eating = False

    def createSegment(self):
        lastPos = self.body.returnPositionList()[-1]
        lastDir = self.body.returnDirectionList()[-1]

        match lastDir:
            case 0:
                newPos = (lastPos[0], lastPos[1] - 10)
            case 1:
                newPos = (lastPos[0] - 10, lastPos[1])
            case 2:
                newPos = (lastPos[0], lastPos[1] + 10)
            case 3:
                newPos = (lastPos[0] + 10, lastPos[1])

        self.body.insertAtEnd(newPos, lastDir)

    def updatebodyposition(self, direction):
        self.body.head.direction = direction

        x, y = self.body.head.position
        match direction:
            case 0:
                newPos = (x, y + 10)
            case 1:
                newPos = (x + 10, y)
            case 2:
                newPos = (x, y - 10)
            case 3:
                newPos = (x - 10, y)

        self.body.insertAtBeginning(newPos, direction)

        if not self.is_eating:
            self.body.deleteAtEnd()

    def drawSnake(self):
        for x, y in self.body.returnPositionList():
            pyxel.rect(x, y, 10, 10, 13)


class Fruit:
    def __init__(self, serpent):
        self.position = self.randomPos(serpent)

    def randomPos(self, serpent):
        while True:
            pos = (
                random.randrange(0, 256, 10),
                random.randrange(0, 256, 10)
            )
            if pos not in serpent.body.returnPositionList():
                return pos

    def respawn(self, serpent):
        self.position = self.randomPos(serpent)

    def drawFruit(self):
        pyxel.rect(self.position[0], self.position[1], 10, 10, 8)


class Jeu:
    def __init__(self, snake):
        pyxel.init(width, height)
        self.snake = snake
        self.fruit = Fruit(snake)
        self.direction = 0
        self.interdit = {0: 2, 2: 0, 1: 3, 3: 1}
        self.score = 0
        self.ongoing = True
        self.speed = 2


    def startGame(self):
        pyxel.run(self.update, self.draw)

    def update(self):
    
        if not self.ongoing:
            return
        if pyxel.frame_count % self.speed != 0:
            return

        self.handleInput()
        self.snake.updatebodyposition(self.direction)

        if self.collisionMur() or self.collisionCorps():
            self.ongoing = False

        if self.collisionFruit():
            self.snake.is_eating = True
            self.score += 1
            self.fruit.respawn(self.snake)
        else:
            self.snake.is_eating = False





    def draw(self):
        pyxel.cls(0)

        if self.ongoing:
            self.snake.drawSnake()
            self.fruit.drawFruit()
            pyxel.text(5, 5, f"SCORE : {self.score}", 7)
        else:
            pyxel.text(90, 120, "GAME OVER", 8)


    def handleInput(self):
        prev = self.direction

        if pyxel.btn(pyxel.KEY_UP):
            self.direction = 2
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.direction = 1
        elif pyxel.btn(pyxel.KEY_DOWN):
            self.direction = 0
        elif pyxel.btn(pyxel.KEY_LEFT):
            self.direction = 3

        if self.direction == self.interdit[prev]:
            self.direction = prev

    def collisionMur(self):
        x, y = self.snake.body.head.position
        return x < 0 or x >= width or y < 0 or y >= height

    def collisionCorps(self):
        head = self.snake.body.head.position
        return head in self.snake.body.returnPositionList()[1:]

    def collisionFruit(self):
        hx, hy = self.snake.body.head.position
        fx, fy = self.fruit.position

        return (
            hx < fx + 10 and
            hx + 10 > fx and
            hy < fy + 10 and
            hy + 10 > fy
        )


snake = Serpent(LinkedList, Node)
snake.createSegment()
snake.createSegment()

game = Jeu(snake)
game.startGame()
