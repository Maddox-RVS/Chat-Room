from PrintHelper import printBlue, printGreen, printRed, printError
from ClientHandler import ClientHandler
from colorama import Fore, Style, Back
from threading import Thread
from typing import Union
import socket

HOST: str = '0.0.0.0'
BACKLOG: int = 5
BUFFER_SIZE = 1024

SHUTDOWN: str = 'shutdown'

class ServerTCP():

    def __init__(self, port: int):
        self.port: int = port
        self.serverClients: list[ClientHandler] = []
        self.serverSocket: Union[None, socket.socket] = None
        self.isShutdown: bool = False

    def Shutdown(self):
        printGreen('Shutting down server...')
        printGreen('Disconnecting clients...')
        for i in reversed(range(len(self.serverClients))):
            self.serverClients[i].disconnect()
        self.serverSocket.close()
        self.isShutdown = True
        printGreen('Successfully shutdown!')

    def __announce__(self, message: str):
        for i in range(len(self.serverClients)):
            self.serverClients[i].sendMessage(message)

    def start(self):
        try:
            self.isShutdown = False
            printGreen(f'Starting server on port {self.port}...')
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
                self.serverSocket = serverSocket
                self.serverSocket.bind((HOST, self.port))
                self.serverSocket.listen(BACKLOG)
                boundAddress, boundPort = self.serverSocket.getsockname()
                printGreen(f'Server {boundAddress} listening on port {boundPort} for connections...')

                commandProcessorThread: Thread = Thread(target=self.__runCommandProcessor__, name='commandProcessor')
                commandProcessorThread.start()

                while True:
                    clientSocket, clientAddress = serverSocket.accept()
                    username: str = clientSocket.recv(BUFFER_SIZE).decode('utf-8')
                    printBlue(f'Client {clientAddress} with name {username} has connected to the server!')
                    self.__announce__(Fore.BLUE + f'{username} has joined the server!' + Style.RESET_ALL)
                    clientHandler: ClientHandler = ClientHandler(clientSocket, clientAddress, self.serverClients, username)
                    self.serverClients.append(clientHandler)
                    clientHandler.start()
        except Exception as e: 
            if not self.isShutdown: printGreen('Server shutdown: ' + e)
            else: printGreen('Server shutdown.')
            self.isShutdown = True

    def __runCommandProcessor__(self):
        while True:
            command: str = input(Style.DIM + '[Enter Command] -> ' + Style.RESET_ALL).lower()
            if command == SHUTDOWN:
                self.Shutdown()
                break

if __name__ == '__main__':
    port: int = int(input(Style.DIM + 'Enter a port number: ' + Style.RESET_ALL))
    server: ServerTCP = ServerTCP(port)
    server.start()