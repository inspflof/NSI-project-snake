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
        self.tilemap_snake=[]

    def createSegment(self):
        lastPos = self.body.returnPositionList()[-1]
        lastDir = self.body.returnDirectionList()[-1]
        newPos = None
        match lastDir:
            case 0:
                newPos = (lastPos[0], lastPos[1] - 8)
            case 1:
                newPos = (lastPos[0] - 8, lastPos[1])
            case 2:
                newPos = (lastPos[0], lastPos[1] + 8)
            case 3:
                newPos = (lastPos[0] + 8, lastPos[1])

        self.body.insertAtEnd(newPos, lastDir)

    def updatebodyposition(self, direction):
        self.body.head.direction = direction

        x, y = self.body.head.position
        newPos = None
        match direction:
            case 0:
                newPos = (x, y + 8)
            case 1:
                newPos = (x + 8, y)
            case 2:
                newPos = (x, y - 8)
            case 3:
                newPos = (x - 8, y)

        self.body.insertAtBeginning(newPos, direction)

        if not self.is_eating:
            self.body.deleteAtEnd()

    def drawSnake(self):
        for x, y in self.body.returnPositionList():
            pyxel.rect(x, y, 10, 10, 13)
    
    def select_snake_tilemap(self):
        snakePosition=self.body.returnPositionList()
        self.tilemap_snake=[]
        match self.body.head.direction:
            case 0:
                self.tilemap_snake.append((0,32))

            case 1:
                self.tilemap_snake.append((0,24))
                    
            case 2:
                self.tilemap_snake.append((0,16))
                    
            case 3:
                self.tilemap_snake.append((0,40))

        dictionary_turn={((8,0),(0,-8)):(24,16),
                             ((0,8),(-8,0)):(24,16),

                             ((-8,0),(0,-8)):(24,24),
                             ((0,8),(8,0)):(24,24),

                             ((8,0),(0,8)):(24,32),
                             ((0,-8),(-8,0)):(24,32),

                             ((-8,0),(0,8)):(24,40),
                             ((0,-8),(8,0)): (24,40)
                                      }
        dictionary_queue={(8,0):(8,24),
                          (-8,0):(8,40),
                          (0,8):(8,32),
                          (0,-8):(8,16)}

        dictionary_body_straight={(8,0):(16,24),
                                 (-8,0):(16,24),
                                 (0,8):(16,16),
                                 (0,-8):(16,16)}
        
        dx_after = 0
        dy_after = 0
        for i in range(1,len(snakePosition)-1):
           
            x_prev,y_prev=snakePosition[i-1]
            x_after,y_after=snakePosition[i+1]
            x_curr,y_curr=snakePosition[i]
            dx_curr=x_prev-x_curr
            dy_curr=y_prev-y_curr
            dx_after=x_curr-x_after
            dy_after=y_curr-y_after
            if (dx_curr,dy_curr)==(dx_after,dy_after):
                self.tilemap_snake.append(dictionary_body_straight[(dx_curr,dy_curr)])
            else:
                self.tilemap_snake.append(dictionary_turn[((dx_after,dy_after),(dx_curr,dy_curr))])
        self.tilemap_snake.append(dictionary_queue[(dx_after,dy_after)])

    def drawsnake_bis(self):
        snakePosition=self.body.returnPositionList()
        for i in range(len(snakePosition)):
            x,y=snakePosition[i]
            pyxel.blt(x,y, 0, self.tilemap_snake[i][0],self.tilemap_snake[i][1],8,8, 0)
            
    def returntilemap_snake(self):
        return self.tilemap_snake
        
class Fruit:
    def __init__(self, serpent):
        self.position = self.randomPos(serpent)

    def randomPos(self, serpent):
        while True:
            pos = (
                random.randrange(8, 248, 8),
                random.randrange(8, 248, 8)
            )
            if pos not in serpent.body.returnPositionList():
                return pos

    def respawn(self, serpent):
        self.position = self.randomPos(serpent)

    def drawFruit(self):
        pyxel.blt(self.position[0], self.position[1], 0, 16,8 , 8, 8, 0)

class Jeu:
    def __init__(self, snake):
        pyxel.init(width, height)
        pyxel.load("snake.pyxres")
        self.snake = snake
        self.fruit = Fruit(snake)
        self.direction = 0
        self.interdit = {0: 2, 2: 0, 1: 3, 3: 1}
        self.score = 0
        self.highscore = self.load_highscore()
        self.ongoing = True
        self.speed = 2 
        self.paused = False
    def load_highscore(self):
        try:
           with open("highscore.txt", "r") as f:
             return int(f.read())
        except:
            return 0
        
    def save_highscore(self):
       with open("highscore.txt", "w") as f:
           f.write(str(self.highscore))

    def startGame(self):
        pyxel.run(self.update, self.draw)

    def update(self):

        if pyxel.btnp(pyxel.KEY_SPACE):
            self.paused = not self.paused

        if self.paused:
            return

        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btn(pyxel.KEY_A):
            self.snake.createSegment()

        if not self.ongoing:
            return
         
        if pyxel.frame_count % self.speed != 0:
            return

        self.handleInput()
        self.snake.updatebodyposition(self.direction)

        if self.collisionMur() or self.collisionCorps():
            self.ongoing = False
            if self.score > self.highscore:
                self.highscore = self.score
                self.save_highscore()

        if self.collisionFruit():
            self.snake.is_eating = True
            self.score += 1
            self.fruit.respawn(self.snake)
        else:
            self.snake.is_eating = False

    def draw(self):
        pyxel.cls(0)
        pyxel.bltm(0,0,0,0,0,256,256,0)

        if self.ongoing:
            self.snake.select_snake_tilemap()
            self.snake.drawsnake_bis()
            self.fruit.drawFruit()
            pyxel.text(5, 5, f"SCORE : {self.score}", 7)
            pyxel.text(5, 15, f"HIGHSCORE : {self.highscore}", 6)

        else:
            pyxel.text(90, 120, "GAME OVER", 8)
            pyxel.text(75, 140, f"HIGHSCORE : {self.highscore}", 7)

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
        return x <= 8 or x+8 >= 248 or y <=8  or y+8 >= 248

    def collisionCorps(self):
        head = self.snake.body.head.position
        return head in self.snake.body.returnPositionList()[1:]

    def collisionFruit(self):
        hx, hy = self.snake.body.head.position
        fx, fy = self.fruit.position

        return (
            hx < fx + 8 and
            hx + 8 > fx and
            hy < fy + 8 and
            hy + 8 > fy
        )

def startGame(serpentClass, gameClass, bodyClass, nodeClass):
    snake = serpentClass(bodyClass, nodeClass)
    snake.createSegment()
    snake.createSegment()

    game = gameClass(snake)
    game.startGame()

startGame(Serpent, Jeu, LinkedList, Node)