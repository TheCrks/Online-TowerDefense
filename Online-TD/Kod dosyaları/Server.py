import pickle
import socket
from _thread import *

from Game import game
from Game import daireEnemy
from Game import ucgenEnemy
from Game import kareEnemy
from Game import KareDefence
from Game import DaireDefence
from Game import UcgenDefence

server = "10.58.7.131"
port = 5555

sockett = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sockett.bind((server, port))
except socket.error as e:
    str(e)

sockett.listen()
print("Waiting For Connection, Server Started")

connected = set()
games = {}
idCount = 0


def threaded_client(connection, player, gameId):
    global idCount
    connection.send(str.encode(str(player)))

    while True:
        try:
            data = connection.recv(4096).decode()
            try:
                dataList = data.split()
                data = dataList[0]
                pos = [dataList[1], dataList[2]]
            except:
                pass
            if gameId in games:
                game = games[gameId]
                if not data:
                    break
                else:
                    if data == "Kare" and player == 0 and game.summonableEnemy():
                        if game.player0G >= 25:
                            Enemy = kareEnemy(20 * 50, "Kare", 302, 2, (255, 255, 255), 25, 25)
                            game.Enemies.append(Enemy)
                            game.player0G -= 25
                    elif data == "Ucgen" and player == 0 and game.summonableEnemy():
                        if game.player0G >=15:
                            Enemy = ucgenEnemy(10 * 45, "Ucgen", 300, 15, (255, 255, 255))
                            game.Enemies.append(Enemy)
                            game.player0G -= 15
                    elif data == "Daire" and player == 0 and game.summonableEnemy():
                        if game.player0G >= 20:
                            Enemy = daireEnemy(15 * 50, "Daire", 300, 15, (255, 255, 255), 12)
                            game.Enemies.append(Enemy)
                            game.player0G -= 20

                    elif data == "Geri":
                        game.over = True
                        game.manuel = True
                        game.win = int(dataList[1])
                        print(game.over)

                    elif data == "del":
                        game.Enemies.clear()
                        game.Defenders.clear()
                    if data == "KareT" or data == "DaireT" or data == "UcgenT":
                        if data == "KareT" and game.player1G >=25:
                            game.selected = True
                        if data == "DaireT" and game.player1G >=20:
                            game.selected = True
                        if data == "UcgenT" and game.player1G >=15:
                            game.selected = True
                    elif data == "KareD":
                        if game.player1G >=25:
                            Defender = KareDefence(int(pos[0]), int(pos[1]))
                            game.Defenders.append(Defender)
                            game.selected = False
                            game.player1G -= 25
                    elif data == "DaireD":
                        if game.player1G >=20:
                            Defender = DaireDefence(int(pos[0]), int(pos[1]))
                            game.Defenders.append(Defender)
                            game.selected = False
                            game.player1G -= 20
                    elif data == "UcgenD":
                        if game.player1G >=15:
                            Defender = UcgenDefence(int(pos[0]), int(pos[1]))
                            game.Defenders.append(Defender)
                            game.selected = False
                            game.player1G -= 15
                    elif data == "timeSec":
                        if game.counterMin >=8 and game.counterMin <=10 and game.counterSec % 2 == 0:
                            game.player1G += 1
                            game.player0G += 3
                        elif game.counterMin >=6 and game.counterMin <8 and game.counterSec % 2 == 0:
                            game.player1G += 0
                            game.player0G += 6
                        elif game.counterMin >=4 and game.counterMin <6 and game.counterSec % 2 == 0:
                            game.player1G +=0
                            game.player0G +=9
                        elif game.counterMin >=2 and game.counterMin< 4 and game.counterSec % 2 == 0:
                            game.player1G +=0
                            game.player0G +=12
                        elif game.counterMin >=0 and game.counterMin <2 and game.counterSec % 2 == 0:
                            game.player1G +=0
                            game.player0G +=15

                        if game.counterSec > 0:
                            game.counterSec -= 1
                        else:
                            game.counterSec = 59
                        if game.counterSec == 30 or game.counterSec == 0:
                            game.player0H -= 1
                    elif data == "timeMin":
                        game.counterMin -= 1
                    else:
                        if not game.manuel:
                            game.gameOver()
                            game.winner()
                        for i in game.Enemies:
                            i.damage(game)
                            i.move(game)
                            i.die(game)
                        for i in game.Defenders:
                            i.chooseTarget(game)
                            i.d(game)

                    reply = game
                    connection.sendall(pickle.dumps(reply))
            else:
                break
        except:
            break

    print("Lost Connection")

    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    connection.close()


while True:
    connection, address = sockett.accept()
    print("Connected to : ", address)

    idCount += 1
    player = 0
    gameId = (idCount - 1) // 2
    if idCount % 2 == 1:
        games[gameId] = game(gameId)
        print("Creating a new Game ...")
    else:
        games[gameId].ready = True
        player = 1

    start_new_thread(threaded_client, (connection, player, gameId))
