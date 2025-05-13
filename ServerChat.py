from ClientHandler import ClientHandler
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
    '''
    Represents the TCP chat server.
    Handles incoming client connections, manages clients, and processes server commands.
    '''

    def __init__(self, port: int):
        '''
        Initializes the ServerTCP instance.

        Args:
            port (int): The port number for the server to listen on.
        '''

        self.port: int = port
        self.serverClients: list[ClientHandler] = []
        self.serverSocket: Union[None, socket.socket] = None
        self.isShutdown: bool = False
        self.console: Console = Console()

    def Shutdown(self):
        '''
        Shuts down the server gracefully.
        Disconnects all clients and closes the server socket.
        '''

        self.console.printlnGreen('Shutting down server...')
        self.console.printlnGreen('Disconnnecting clients...')
        for i in reversed(range(len(self.serverClients))):
            self.serverClients[i].disconnect()
        self.serverSocket.close()
        self.isShutdown = True
        self.console.printlnGreen('Successfully shutdown!')

    def __announce__(self, message: str):
        '''
        Sends a message to all currently connected clients.

        Args:
            message (str): The message string to broadcast.
        '''

        for i in range(len(self.serverClients)):
            self.serverClients[i].sendMessage(message)

    def start(self):
        '''
        Starts the server, listens for connections, and handles them.
        Binds the socket, starts a command processor thread, and accepts client connections.
        '''

        try:
            self.isShutdown = False
            self.console.printlnGreen(f'Starting server on port {self.port}...')
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverSocket:
                self.serverSocket = serverSocket
                self.serverSocket.bind((HOST, self.port))
                self.serverSocket.listen(BACKLOG)
                boundAddress, boundPort = self.serverSocket.getsockname()
                self.console.printlnGreen(f'Server {boundAddress} listening on port {boundPort} for connections...')

                commandProcessorThread: Thread = Thread(target=self.__runCommandProcessor__, name='commandProcessor')
                commandProcessorThread.start()

                while True:
                    clientSocket, clientAddress = serverSocket.accept()
                    username: str = clientSocket.recv(BUFFER_SIZE).decode('utf-8')
                    self.console.clearLine()
                    self.console.moveFront()
                    self.console.printlnBlue(f'Client {clientAddress} with name {username} has connected to the server!')
                    self.console.printDim('[Enter Command] -> ')
                    self.__announce__(f'blue {username} has joined the server!')
                    clientHandler: ClientHandler = ClientHandler(clientSocket, clientAddress, self.serverClients, self.console, username)
                    self.serverClients.append(clientHandler)
                    clientHandler.start()
        except Exception: 
            if not self.isShutdown: self.console.printlnGreen('Server shutdown: ')
            else: self.console.printlnGreen('Server shutdown.')
            self.isShutdown = True

    def __runCommandProcessor__(self):
        '''
        Runs in a separate thread to handle server administrator commands.
        Processes commands like '/shutdown' and '/announce'.
        '''
        
        while True:
            self.console.printDim('[Enter Command] -> ')
            command: str = self.console.input().lower().split()

            if command[0] == SHUTDOWN:
                self.Shutdown()
                break
            elif command[0] == ANNOUNCE:
                words: list[str] = command[1:]
                message: str = ' '.join(words)
                self.__announce__(f'green *[SERVER]* -> {message}')
                self.console.printlnGreen(f'*[SERVER]* -> {message}')
            else:
                self.console.printlnError(f'Unknown command -> {' '.join(command)}')

if __name__ == '__main__':
    tempConsole: Console = Console()

    tempConsole.printDim('Enter a port number: ')
    port: str = int(tempConsole.input())
    tempConsole.close()

    server: ServerTCP = ServerTCP(port)
    server.start()

    time.sleep(2)