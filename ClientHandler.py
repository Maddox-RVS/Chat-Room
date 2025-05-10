from PrintHelper import printBlue, printGreen, printRed, printError
from colorama import Fore, Back, Style
from threading import Thread
from typing import override
from Console import Console
import socket

BUFFER_SIZE: int = 1024

class ClientHandler(Thread):
    def __init__(self, clientSocket: socket.socket, clientAddress, serverClients: list['ClientHandler'], console: Console, username: str):
        super().__init__()
        self.clientSocket: socket.socket = clientSocket
        self.clientAddress = clientAddress
        self.serverClients: list['ClientHandler'] = serverClients 
        self.username: str = username
        self.disconnected: bool = False
        self.console: Console = console

    def sendMessage(self, message: str):
        self.clientSocket.sendall(message.encode('utf-8'))

    def disconnect(self):
        self.clientSocket.close()
        self.disconnected = True
        self.serverClients.remove(self)
        # printBlue(f'Disconnected {self.clientAddress} with name {self.username}.')
        self.console.printlnBlue(f'Disconnected {self.clientAddress} with name {self.username}.')
        self.__announce__(Fore.BLUE + f'{self.username} has disconnected from the server.' + Style.RESET_ALL)

    def __announce__(self, message: str):
        for i in range(len(self.serverClients)):
            if self.serverClients[i] is not self:
                self.serverClients[i].sendMessage(message)

    @override
    def run(self):
        try:
            while True:
                data: bytes = self.clientSocket.recv(BUFFER_SIZE)
                if not data:
                    self.disconnect()
                    break
                message = data.decode('utf-8')
                # print(f'[{self.username}] -> {message}')

                currentText: str = self.console.getBackTextToString('[Enter Command] ->', 3, '{Timeout ERROR, current command erased.} -> ')[1:]
                self.console.clearLine()
                self.console.moveFront()
                self.console.println(f'[{self.username}] -> {message}')
                self.console.printDim(f'[Enter Command] -> ')
                self.console.print(currentText)

                self.__announce__(f'[{self.username}] -> {message}') 
        except Exception as e:
            if not self.disconnected: 
                # printError(f'Error handling client {self.clientAddress}!')
                self.console.clearLine()
                self.console.moveFront()
                self.console.printlnError(f'Error handling client {self.clientAddress}!')
        finally:
            if not self.disconnected:
                # printBlue(f'Closing connection to {self.clientAddress}...')
                self.console.printlnBlue(f'Closing connection to {self.clientAddress}...')
                self.disconnect()