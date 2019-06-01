'''
client for  FTP
'''

import protocol
from config import Configure
from socket import *
import os


class Client:

    # a list to store file list from server so we don't need to request it everytime
    files = []

    def __init__(self):
        self.serverName, self.serverPort, self.clientPort, self.downloadPath = Configure().client_config()

    def menu(self):
        print("\nWelcome to simple file sharing system!")
        print("Please select operations from menu")
        print("--------------------------------------")
        print("1. Review the List of Available Files")
        print("2. Download File")
        print("3. Quit\n")

    def selection(self):
        resp = 0
        while resp < 1 or 3 < resp:
            self.menu()
            try:
                resp = int(input("Enter Your Selection: "))
                if(resp == -1):
                    return resp
            except:
                resp = 0
            if(resp > 0 and 4 > resp):
                return resp
            print("Invalid selection!")

    def connect(self):
        serverName = self.serverName
        serverPort = self.serverPort
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName, serverPort))
        return clientSocket

    def requestList(self):
        # connect to server and request a list
        socket = self.connect()
        socket.send(protocol.prep_send(protocol.REQ_LIST, " "))
        header, data = protocol.decode_incoming(socket.recv(1024).decode())
        socket.close()
        # list recived now it needs to be formated to clients list
        print(header, protocol.SEND_LIST)
        if (header == protocol.SEND_LIST):
            files = data.split(',')
            self.files = []
            for f in files:
                self.files.append(f)
        else:
            print("Error: Can't get file list")

    def printList(self):
        count = 1  # this will be used for user to select from the list
        for f in self.files:
            print('{:<3d}{}'.format(count, f))
            count += 1

    def fileSelect(self):
        if(len(self.files) == 0):
            self.requestList()
        resp = -1
        while resp < 0 or resp > len(self.files)+1:
            self.printList()
            try:
                resp = int(input('Enter the number of the file you want: '))
            except:
                resp = -1
            if (resp > 0 and resp < len(self.files)+1):
                return(self.files[resp-1])
            print('Invalid')

    def download(self, fileName):
        socket = self.connect()
        socket.send(protocol.prep_send(protocol.REQ_FILE, fileName))
        with open(self.downloadPath+"/"+fileName, 'wb') as f:
            print('File Opened')
            while True:
                data = socket.recv(1024)
                if not data:
                    break
                f.write(data)
        print(fileName + " has been downloaded to " + self.downloadPath)
        f.close()
        socket.close()

    def start(self):
        option = 0
        while option != 3:
            option = self.selection()
            if(option == 1):
                if(len(self.files) == 0):
                    self.requestList()
                self.printList()
            elif option == 2:
                self.download(self.fileSelect())
            elif option == -1:
                self.connect().send(protocol.prep_send(protocol.KILL_SERVER, " "))
                print("Server went down now I am too!")
                break
            else:
                pass


def main():
    c = Client()
    c.start()


main()
