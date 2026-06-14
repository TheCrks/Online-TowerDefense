import pygame
from Network import network
pygame.init()
pygame.font.init()

width = 600
height = 730
red = (255, 0, 0)
pathColour = (100, 100, 100)
coordX = width / 2
coordY = 0
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")
coordLists = [[300, 0, 0], [300, 30, 1], [300, 60, 2]]
backgroundColourRed = (255, 50, 50)
backgroundColourBlue = (0, 0, 255)
btnText = ""
backDrawn= False

class Button:
    def __init__(self, text, x, y, colour, buttonWidth, buttonHeight):
        self.text = text
        self.x = x
        self.y = y
        self.colour = colour
        self.width = buttonWidth
        self.height = buttonHeight

    def draw(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 20)
        text = font.render(self.text, True, (255, 255, 255))
        win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                        self.y + round(self.height / 2) - round(text.get_height() / 2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]

        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def redrawWindow(win, game, player, pos):
    global backDrawn
    if not (game.connected()):
        win.fill(backgroundColourBlue)
        font = pygame.font.SysFont("comicsans", 30)
        text = font.render("Oyuncu Bekleniyor...", True, (255, 0, 0), False)
        win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
    else:
        drawBackGround(window,game)
        for i in game.Enemies:
            i.draw(window)
        for i in game.Defenders:
            i.draw(window)
        if game.selected and player == 1:
            if btnText == "Kare":
                pygame.draw.rect(window, (255, 255, 255), pygame.Rect(pos[0], pos[1], 30, 30))
            elif btnText == "Daire":
                pygame.draw.circle(window, (255, 255, 255), pos, 12, 12)
            elif btnText == "Ucgen":
                pygame.draw.polygon(window, (255, 255, 255),
                                    [(pos[0] + 5, pos[1] + 25), (pos[0] + 15, pos[1] + 5), (pos[0] + 25, pos[1] + 25)])

        if player == 0:
            font = pygame.font.SysFont("comicsans", 30)
            text = font.render("Saldıran",False, (255, 0, 0), False)
            health = font.render("HP: "+str(game.player0H),False, (255,0,0))
            win.blit(text, (10, 120))
            win.blit(health,(150, 120))
        elif player ==1:
            font = pygame.font.SysFont("comicsans", 30)
            text = font.render("Savunan", False, (255, 0, 0), False)
            health = font.render("HP: "+str(game.player1H),False, (255,0,0))
            win.blit(text, (10, 120))
            win.blit(health,(150,120))
        font = pygame.font.SysFont("comicsans",20)
        if game.counterSec >=10:
            sec = font.render(str(game.counterSec), True, (200, 200, 200), False)
        else:
            sec = font.render("0"+str(game.counterSec), True, (200, 200, 200), False)
        if game.counterMin >=10:
            min = font.render(str(game.counterMin),True, (200,200,200),False)
        else:
            min = font.render("0"+str(game.counterMin), True, (200, 200, 200), False)
        dot=font.render(".",True,(200,200,200),False)
        win.blit(sec,(40,200))
        win.blit(min,(10,200))
        win.blit(dot,(35,200))
        gold0 = game.player0G
        gold1 = game.player1G
        if player == 0:
            txt = font.render("G: "+str(gold0),False,(0,0,255))
        else:
            txt = font.render("G: "+str(gold1),False,(0,0,255))
        win.blit(txt,(10,150))
        win.blit(font.render("15G",False,(0,0,255)),(525,0))
        win.blit(font.render("25G",False,(0,0,255)),(525,35))
        win.blit(font.render("20G",False,(0,0,255)),(525,70))

        if player ==0:
            if game.win==0:
                win.fill((0,0,0))
                font = pygame.font.SysFont("comicsans", 50)
                text = font.render("Kazandınız!", False, (255, 255, 255), False)
                win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))

            elif game.win==1:
                win.fill((0, 0, 0))
                font = pygame.font.SysFont("comicsans", 50)
                text = font.render("Kaybettiniz!", False, (255, 255, 255), False)
                win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
            else:
                pass
        else:
            if game.win== 0:
                win.fill((0, 0, 0))
                font = pygame.font.SysFont("comicsans", 50)
                text = font.render("Kaybettiniz", False, (255, 255, 255), False)
                win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
            elif game.win == 1:
                win.fill((0, 0, 0))
                font = pygame.font.SysFont("comicsans", 50)
                text = font.render("Kazandınız", False, (255, 255, 255), False)
                win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
            else:
                pass
    pygame.display.update()


button = [Button("Geri", 10, 10, (250, 0, 0), 250, 100), Button("Ucgen", 400, 0, (255, 0, 0), 100, 30),
          Button("Kare", 400, 35, (0, 255, 0), 100, 30), Button("Daire", 400, 70, (0, 0, 255), 100, 30)]#,
          #Button("del", 400, 105, (0, 0, 0), 100, 30)]


def drawBackGround(win, game):
    window.fill((0, 0, 0))
    for i in game.coordLists:
        pygame.draw.rect(window, pathColour, pygame.Rect(i[0], i[1], 30, 30))
    for btn in button:
        btn.draw(win)


def mainLoop():
    global btnText
    loop = True
    clock = pygame.time.Clock()
    n = network()
    player = int(n.getPlayer())
    print("player : ", player)
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    pygame.time.set_timer(pygame.USEREVENT_DROPFILE, 60000)

    while loop:
        clock.tick(60)
        try:
            try:
                pos = pygame.mouse.get_pos()
            except:
                pass
            game = n.sendStr("continue")
        except:
            loop = False
            print("Cant connect")
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in button:
                    if btn.click(pos) and game.connected():
                        if btn.text == "Geri":
                            if player==0:
                                n.sendStr(btn.text + " " + str(1))
                            else:
                                n.sendStr(btn.text+ " " + str(0))
                        else:
                            if player == 1:
                                btnText = btn.text
                                n.sendStr(btn.text + "T")
                            else:
                                n.sendStr(btn.text)
            if event.type == pygame.USEREVENT and player ==1:
                n.sendStr("timeSec")
            if event.type == pygame.USEREVENT_DROPFILE and player ==1:
                n.sendStr("timeMin")
            if game.selected and player == 1:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pos = pygame.mouse.get_pos()
                        data = btnText + "D" + " " + str(pos[0]) + " " + str(pos[1])
                        n.sendStr(data)
            if game.over:
                loop = False
            else:
                pass
        redrawWindow(window, game, player, pos)
        if game.over:
            pygame.time.wait(2000)


def menuScreen(win):
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)
        win.fill(backgroundColourRed)
        font = pygame.font.SysFont("comicsans", 30)
        text = font.render("Oynamak İçin Tılayın!", True, (0, 0, 0))
        win.blit(text, (100, 350))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
            else:
                pass
        pygame.display.update()
    mainLoop()


while True:
    menuScreen(window)
