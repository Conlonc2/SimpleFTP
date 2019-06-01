'''
server for FTP
'''

from config import Configure
import protocol
import os
from socket import *
import threading


class Server:
    threads = []

    def __init__(self):
        self.port, self.path = Configure().server_config()
        self.run = True

    def getList(self):
        return os.listdir(self.path)

    def sendList(self, socket):
        socket.send(protocol.prep_list(protocol.SEND_LIST, self.getList()))

    def sendFile(self, socket, fName):
        f = open(fName, 'rb')
        l = f.read(1024)
        while l:
            socket.send(l)
            l = f.read(1024)

    def start(self):
        port = self.port
        serverSocket = socket(AF_INET, SOCK_STREAM)
        serverSocket.bind(('0.0.0.0', port))
        serverSocket.listen(20)
        print("Server listening on port {}... Ready to receive".format(port))
        while self.run:
            connectionSocket, addr = serverSocket.accept()
            if(connectionSocket and addr):
                print(addr)
                t = threading.Thread(target=self.request_handler, args=[
                                     connectionSocket, addr])
                Server().threads.append(t)
                t.start()
        for x in Server().threads:
            x.join()
            break

    def stop(self):
        self.run = False

    def request_handler(self, connectionSocket, addr):

        dataRec = connectionSocket.recv(1024)
        header, msg = protocol.decode_incoming(dataRec.decode())
        if(header == protocol.REQ_LIST):
            self.sendList(connectionSocket)
        elif(header == protocol.REQ_FILE):
            self.sendFile(connectionSocket, self.path+"/"+msg)
        elif(header == protocol.KILL_SERVER):
            print("Server is going down!")
            self.stop()
        else:
            connectionSocket.send(protocol.prep_send(
                protocol.ERR, "Invalid Message"))
        connectionSocket.close()


def main():
    s = Server()
    s.start()


main()
