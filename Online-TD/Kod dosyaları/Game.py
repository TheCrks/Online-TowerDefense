from random import randint
import pygame
pygame.font.init()


class kareEnemy:
    def __init__(self, health, name, x, y, color, width, height):
        self.name = name
        self.health = health
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height
        self.pos = 0
        self.rect = pygame.Rect(self.x + 2, self.y + 2, self.width, self.height)
        self.text = str(self.health)
        self.speed = 1
        self.cost = 25

    def draw(self, window):
        self.text = str(int(self.health / 50))
        pygame.draw.rect(window, self.color, self.rect)
        font = pygame.font.SysFont("comicsans", 10)
        text = font.render(self.text, True, (0, 0, 0))
        window.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                           self.y + round(self.height / 2) - round(text.get_height() / 2)))

    def move(self, game):
        if game.coordLists[self.pos][0] + 2 > self.x and game.coordLists[self.pos][2] == "Left":
            self.pos += 1
        elif game.coordLists[self.pos][0] + 2 < self.x and game.coordLists[self.pos][2] == "Right":
            self.pos += 1
        elif game.coordLists[self.pos][1] + 2 < self.y and game.coordLists[self.pos][2] == "Down":
            self.pos += 1
        else:
            pass

        if game.coordLists[self.pos][2] == "Down":
            self.rect.y += self.speed
        elif game.coordLists[self.pos][2] == "Left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
        self.x = self.rect.x
        self.y = self.rect.y

    def die(self, game):
        if (self.health <= 0):
            game.Enemies.remove(self)
            game.player1G += 7

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def damage(self, game):
        if self.y >= 730:
            game.removeEnemy(self)
            game.player1H -= 3
            game.player0G += 10


class ucgenEnemy:
    def __init__(self, health, name, x, y, color):
        self.name = name
        self.health = health
        self.x = x
        self.y = y
        self.color = color
        self.pos = 0
        self.text = str(self.health)
        self.speed = 2
        self.cost = 15

    def draw(self, window):
        self.text = str(int(self.health / 50))
        pygame.draw.polygon(window, self.color,
                            [(self.x + 5, self.y + 25), (self.x + 15, self.y + 5), (self.x + 25, self.y + 25)])
        font = pygame.font.SysFont("comicsans", 10)
        text = font.render(self.text, True, (0, 0, 0))
        window.blit(text, (round(self.x + 10), round(self.y + 10)))

    def move(self, game):
        if game.coordLists[self.pos][0] + 2 > self.x and game.coordLists[self.pos][2] == "Left":
            self.pos += 1
        elif game.coordLists[self.pos][0] + 2 < self.x and game.coordLists[self.pos][2] == "Right":
            self.pos += 1
        elif game.coordLists[self.pos][1] + 2 < self.y and game.coordLists[self.pos][2] == "Down":
            self.pos += 1
        else:
            pass

        if game.coordLists[self.pos][2] == "Down":
            self.y += self.speed
        elif game.coordLists[self.pos][2] == "Left":
            self.x -= self.speed
        else:
            self.x += self.speed

    def die(self, game):
        if (self.health <= 0):
            game.Enemies.remove(self)
            game.player1G += 5

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def damage(self, game):
        if self.y >= 730:
            game.removeEnemy(self)
            game.player1H -= 2
            game.player0G = 8


class daireEnemy:
    def __init__(self, health, name, x, y, color, radius):
        self.name = name
        self.health = health
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.pos = 0
        self.text = str(self.health)
        self.speed = 1
        self.cost = 20

    def draw(self, window):
        self.text = str(int(self.health / 50))
        pygame.draw.circle(window, self.color, (self.x + 15, self.y + 15), self.radius, self.radius)
        font = pygame.font.SysFont("comicsans", 10)
        text = font.render(self.text, True, (0, 0, 0))
        window.blit(text, (round(self.x + 8), round(self.y + 6)))

    def move(self, game):
        if game.coordLists[self.pos][0] >= self.x and game.coordLists[self.pos][2] == "Left":
            self.pos += 1
        elif game.coordLists[self.pos][0] <= self.x and game.coordLists[self.pos][2] == "Right":
            self.pos += 1
        elif game.coordLists[self.pos][1] <= self.y and game.coordLists[self.pos][2] == "Down":
            self.pos += 1
        else:
            pass

        if game.coordLists[self.pos][2] == "Down":
            self.y += self.speed
        elif game.coordLists[self.pos][2] == "Left":
            self.x -= self.speed
        else:
            self.x += self.speed

    def die(self, game):
        if (self.health <= 0):
            game.Enemies.remove(self)

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def damage(self, game):
        if self.y >= 730:
            game.removeEnemy(self)
            game.player1H -= 1
            game.player0G += 9

class KareDefence:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (255, 255, 255)
        self.damage = 5
        self.coolDown = 1
        self.width = 30
        self.height = 30
        self.target = None
        self.range = 70
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)

    def setPos(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def chooseTarget(self, game):
        if len(game.Enemies) >= 2:
            a = 0
            try:
                if len(game.Enemies) >= 1:
                    distanceclosest = (self.x - game.Enemies[0].getX()) ** 2 + (self.y - game.Enemies[0].getY()) ** 2
                    for i in range(0, len(game.Enemies)):
                        distance1 = (self.x - game.Enemies[i].getX()) ** 2 + (self.y - game.Enemies[i].getY()) ** 2
                        if distance1 < distanceclosest:
                            distanceclosest = distance1
                            a = i
                    distanceClosest = (self.x - game.Enemies[a].getX()) ** 2 + (self.y - game.Enemies[a].getY()) ** 2
                    if distanceClosest <= self.range * self.range:
                        self.target = game.Enemies[a]
                    else:
                        self.target = None
                else:
                    self.target = None
            except:
                pass
        elif len(game.Enemies) == 0:
            a = None
            self.target = None
        else:
            a = 0
            distance = (self.x - game.Enemies[0].getX()) ** 2 + (self.y - game.Enemies[0].getY()) ** 2
            if self.range * self.range >= distance:
                self.target = game.Enemies[0]
            else:
                self.target = None

        return a

    def d(self, game):
        if self.target is not None:
            a = self.chooseTarget(game)
            game.Enemies[a].health -= self.damage


class UcgenDefence:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (255, 255, 255)
        self.damage = 3
        self.coolDown = 1
        self.target = None
        self.range = 70

    def draw(self, window):
        pygame.draw.polygon(window, self.color,
                            [(self.x + 5, self.y + 25), (self.x + 15, self.y + 5), (self.x + 25, self.y + 25)])

    def setPos(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def chooseTarget(self, game):
        if len(game.Enemies) >= 2:
            a = 0
            try:
                if len(game.Enemies) >= 1:
                    distanceclosest = (self.x - game.Enemies[0].getX()) ** 2 + (self.y - game.Enemies[0].getY()) ** 2
                    for i in range(0, len(game.Enemies)):
                        distance1 = (self.x - game.Enemies[i].getX()) ** 2 + (self.y - game.Enemies[i].getY()) ** 2
                        if distance1 < distanceclosest:
                            distanceclosest = distance1
                            a = i
                    distanceClosest = (self.x - game.Enemies[a].getX()) ** 2 + (self.y - game.Enemies[a].getY()) ** 2
                    if distanceClosest <= self.range * self.range:
                        self.target = game.Enemies[a]
                    else:
                        self.target = None
                else:
                    self.target = None
            except:
                pass
        elif len(game.Enemies) == 0:
            a = None
            self.target = None
        else:
            a = 0
            distance = (self.x - game.Enemies[0].getX()) ** 2 + (self.y - game.Enemies[0].getY()) ** 2
            if self.range * self.range >= distance:
                self.target = game.Enemies[0]
            else:
                self.target = None

        return a


    def d(self, game):
        if self.target is not None:
            a = self.chooseTarget(game)
            game.Enemies[a].health -= self.damage


class DaireDefence:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (255, 255, 255)
        self.damage = 4
        self.coolDown = 1
        self.radius = 12
        self.target = None
        self.range = 70

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius, self.radius)

    def setPos(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def chooseTarget(self, game):
        if len(game.Enemies) >= 2:
            a = 0
            try:
                if len(game.Enemies) >= 1:
                    distanceclosest = (self.x - game.Enemies[0].getX()) ** 2 + (self.y - game.Enemies[0].getY()) ** 2
                    for i in range(0, len(game.Enemies)):
                        distance1 = (self.x - game.Enemies[i].getX()) ** 2 + (self.y - game.Enemies[i].getY()) ** 2
                        if distance1 < distanceclosest:
                            distanceclosest = distance1
                            a = i
                    distanceClosest = (self.x - game.Enemies[a].getX()) ** 2 + (self.y - game.Enemies[a].getY()) ** 2
                    if distanceClosest <= self.range * self.range:
                        self.target = game.Enemies[a]
                    else:
                        self.target = None
                else:
                    self.target = None
            except:
                pass
        elif len(game.Enemies) == 0:
            a = None
            self.target = None
        else:
            a = 0
            distance = (self.x - game.Enemies[0].getX()) ** 2 + (self.y - game.Enemies[0].getY()) ** 2
            if self.range * self.range >= distance:
                self.target = game.Enemies[0]
            else:
                self.target = None
        return a

    def d(self, game):
        if self.target is not None:
            a = self.chooseTarget(game)
            game.Enemies[a].health -= self.damage


class game:
    def __init__(self, id):
        self.id = id
        self.ready = False
        self.coordLists = [[300, 0, "Down"], [300, 30, "Down"], [300, 60, "Down"], [300, 90, "Down"],
                           [300, 120, "Down"]]
        self.coordX = 300
        self.coordY = 120
        self.drawPath()
        self.Enemies = []
        self.Defenders = []
        self.player0H = 20
        self.player1H = 20
        self.selected = False
        self.counterSec = 60
        self.counterMin = 9
        self.player0G = 30
        self.player1G = 30
        self.over = False
        self.win = 42
        self.manuel = False


    def addEnemy(self, Enemy):
        self.Enemies.append(Enemy)

    def removeEnemy(self, Enemy):
        self.Enemies.remove(Enemy)

    def connected(self):
        return self.ready

    def summonableEnemy(self):
        out = True
        for i in self.Enemies:
            if i.y < 30:
                out = False
        return out

    def indexof(self, List, index):
        out = False
        for i in range(0, len(List)):
            if index == List[i]:
                out = True
        return out

    def drawPathDown(self):
        self.coordY += 30
        self.coordLists.append([self.coordX, self.coordY, "Down"])

    def direction(self):
        if self.coordLists[len(self.coordLists) - 1][0] == self.coordLists[len(self.coordLists) - 2][0]:
            return "Down"
        else:
            if self.coordLists[len(self.coordLists) - 1][0] > self.coordLists[len(self.coordLists) - 2][0]:
                return "Right"
            else:
                return "Left"

    def drawPathRight(self):
        self.coordX += 30
        self.coordLists.append([self.coordX, self.coordY, "Right"])

    def drawPathLeft(self):
        self.coordX -= 30
        self.coordLists.append([self.coordX, self.coordY, "Left"])

    def turnChance(self, percent):
        number = randint(0, 100)
        randomList = []
        for i in range(0, percent):
            randomList.append(randint(0, 100))
        if self.indexof(randomList, number):
            return True
        else:
            return False

    def turnDown(self):
        turn = False
        if self.coordLists[len(self.coordLists) - 1][0] <= 120 or self.coordLists[len(self.coordLists) - 1][
            0] >= 600 - 120:
            turn = True
        if self.coordLists[len(self.coordLists) - 1][1] == self.coordLists[len(self.coordLists) - 2][1] == \
                self.coordLists[len(self.coordLists) - 3][1]:
            turn = self.turnChance(60)
        elif self.coordLists[len(self.coordLists) - 1][1] == self.coordLists[len(self.coordLists) - 2][1] != \
                self.coordLists[len(self.coordLists) - 3][1]:
            turn = self.turnChance(30)
        else:
            turn = False
        return turn

    def turnRL(self):
        turn = False
        if self.coordLists[len(self.coordLists) - 1][0] == self.coordLists[len(self.coordLists) - 2][0] == \
                self.coordLists[len(self.coordLists) - 3][0] == \
                self.coordLists[len(self.coordLists) - 4][0]:
            turn = self.turnChance(50)
        elif self.coordLists[len(self.coordLists) - 1][0] == self.coordLists[len(self.coordLists) - 2][0] == \
                self.coordLists[len(self.coordLists) - 3][
                    0] != self.coordLists[len(self.coordLists) - 4][0]:
            turn = self.turnChance(20)
        else:
            turn = False
        return turn

    def drawPath(self):
        counter = 3
        run = True
        self.drawPathDown()
        while run:
            if self.direction() == "Down":
                if self.turnRL():
                    if self.coordLists[len(self.coordLists) - 1][0] >= 600 - 240:
                        if self.turnChance(60):
                            self.drawPathLeft()
                        else:
                            self.drawPathRight()
                    elif self.coordLists[len(self.coordLists) - 1][0] >= 600 - 120:
                        if self.turnChance(80):
                            self.drawPathLeft()
                        else:
                            self.drawPathRight()
                    elif self.coordLists[len(self.coordLists) - 1][0] >= 600 - 90:
                        if self.turnChance(90):
                            self.drawPathLeft()
                        else:
                            self.drawPathRight()
                    elif self.coordLists[len(self.coordLists) - 1][0] <= 240:
                        if self.turnChance(60):
                            self.drawPathLeft()
                        else:
                            self.drawPathRight()
                    elif self.coordLists[len(self.coordLists) - 1][0] <= 120:
                        if self.turnChance(80):
                            self.drawPathLeft()
                        else:
                            self.drawPathRight()
                    elif self.coordLists[len(self.coordLists) - 1][0] <= 90:
                        if self.turnChance(90):
                            self.drawPathLeft()
                        else:
                            self.drawPathRight()
                    else:
                        if self.turnChance(50):
                            self.drawPathLeft()
                        else:
                            self.drawPathRight()
                else:
                    self.drawPathDown()
            elif self.direction() == "Left":
                if self.coordLists[len(self.coordLists) - 1][0] <= 90:
                    self.drawPathDown()
                else:
                    if self.turnDown():
                        self.drawPathDown()
                    else:
                        self.drawPathLeft()

            else:
                if self.coordLists[len(self.coordLists) - 1][0] >= 600 - 90:
                    self.drawPathDown()
                else:
                    if self.turnDown():
                        self.drawPathDown()
                    else:
                        self.drawPathRight()
            counter += 1
            if self.coordLists[counter][1] >= 730:
                run = False

    def winner(self):
        if self.over and self.player0H <= 0 :
            self.win = 1
            return 1
        elif self.over and self.player1H <=0 :
            self.win = 0
            return 0
        else:
            self.win = 42
            return 42

    def gameOver(self):
        if (self.player1H <=0 or self.player0H <=0) and not self.manuel:
            self.over = True
            print(self.over)
            return True
        else :
            self.over = False
            return False
