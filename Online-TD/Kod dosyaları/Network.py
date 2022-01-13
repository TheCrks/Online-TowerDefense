import socket
import pickle


class network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "10.58.7.131"
        self.port = 5555
        self.address = (self.server, self.port)
        self.player = self.connect()

    def getPlayer(self):
        return self.player

    def connect(self):
        try:
            self.client.connect(self.address)
            return self.client.recv(2048 * 1000).decode()
        except:
            pass

    def sendStr(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048 * 2048))
        except socket.error as e:
            print(e)

