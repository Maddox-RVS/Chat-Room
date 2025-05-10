from PrintHelper import printBlue, printGreen, printRed, printError
from ClientHandler import ClientHandler
from colorama import Fore, Style, Back
from threading import Thread
from Console import Console
from typing import Union
import socket
import time

HOST: str = '0.0.0.0'
BACKLOG: int = 5
BUFFER_SIZE = 1024

SHUTDOWN: str = '/shutdown'
ANNOUNCE: str = '/announce'

class ServerTCP():

    def __init__(self, port: int):
        self.port: int = port
        self.serverClients: list[ClientHandler] = []
        self.serverSocket: Union[None, socket.socket] = None
        self.isShutdown: bool = False
        self.console: Console = Console()

    def Shutdown(self):
        # printGreen('Shutting down server...')
        self.console.printlnGreen('Shutting down server...')
        # printGreen('Disconnecting clients...')
        self.console.printlnGreen('Disconnnecting clients...')
        for i in reversed(range(len(self.serverClients))):
            self.serverClients[i].disconnect()
        self.serverSocket.close()
        self.isShutdown = True
        # printGreen('Successfully shutdown!')
        self.console.printlnGreen('Successfully shutdown!')

    def __announce__(self, message: str):
        for i in range(len(self.serverClients)):
            self.serverClients[i].sendMessage(message)

    def start(self):
        try:
            self.isShutdown = False
            # printGreen(f'Starting server on port {self.port}...')
            self.console.printlnGreen(f'Starting server on port {self.port}...')
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
                self.serverSocket = serverSocket
                self.serverSocket.bind((HOST, self.port))
                self.serverSocket.listen(BACKLOG)
                boundAddress, boundPort = self.serverSocket.getsockname()
                # printGreen(f'Server {boundAddress} listening on port {boundPort} for connections...')
                self.console.printlnGreen(f'Server {boundAddress} listening on port {boundPort} for connections...')

                commandProcessorThread: Thread = Thread(target=self.__runCommandProcessor__, name='commandProcessor')
                commandProcessorThread.start()

                while True:
                    clientSocket, clientAddress = serverSocket.accept()
                    username: str = clientSocket.recv(BUFFER_SIZE).decode('utf-8')
                    # printBlue(f'Client {clientAddress} with name {username} has connected to the server!')
                    self.console.clearLine()
                    self.console.moveFront()
                    self.console.printlnBlue(f'Client {clientAddress} with name {username} has connected to the server!')
                    self.console.printDim('[Enter Command] -> ')
                    self.__announce__(Fore.BLUE + f'{username} has joined the server!' + Style.RESET_ALL)
                    clientHandler: ClientHandler = ClientHandler(clientSocket, clientAddress, self.serverClients, self.console, username)
                    self.serverClients.append(clientHandler)
                    clientHandler.start()
        except Exception as e: 
            if not self.isShutdown: 
                # printGreen('Server shutdown: ' + e)
                self.console.printlnGreen('Server shutdown: ' + e)
            else: 
                # printGreen('Server shutdown.')
                self.console.printlnGreen('Server shutdown.')
            self.isShutdown = True

    def __runCommandProcessor__(self):
        while True:
            # command: str = input(Style.DIM + '[Enter Command] -> ' + Style.RESET_ALL).lower()
            self.console.printDim('[Enter Command] -> ')
            command: str = self.console.input().lower().split()

            if command[0] == SHUTDOWN:
                self.Shutdown()
                break
            elif command[0] == ANNOUNCE:
                words: list[str] = command[1:]
                message: str = ' '.join(words)
                self.__announce__(f'*[SERVER]* -> {message}')
                self.console.println(f'*[SERVER]* -> {message}')
            else:
                self.console.printlnError(f'Unknown command -> {command}')

if __name__ == '__main__':
    port: int = int(input(Style.DIM + 'Enter a port number: ' + Style.RESET_ALL))
    server: ServerTCP = ServerTCP(port)
    server.start()
    time.sleep(2)