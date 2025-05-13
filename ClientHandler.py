from threading import Thread
from typing import override
from Console import Console
import socket

BUFFER_SIZE: int = 1024

class ClientHandler(Thread):
    '''
    Handles communication with a single connected client on the server side.
    Runs in its own thread to manage receiving messages and broadcasting them.
    '''

    def __init__(self, clientSocket: socket.socket, clientAddress, serverClients: list['ClientHandler'], console: Console, username: str):
        '''
        Initializes the ClientHandler instance.

        Args:
            clientSocket (socket.socket): The socket for this client.
            clientAddress: The address (IP, port) of the client.
            serverClients (List['ClientHandler']): A list of all connected client handlers on the server.
            console (Console): The shared console object for server logging.
            username (str): The username of this client.
        '''

        super().__init__()
        self.clientSocket: socket.socket = clientSocket
        self.clientAddress = clientAddress
        self.serverClients: list['ClientHandler'] = serverClients 
        self.username: str = username
        self.disconnected: bool = False
        self.console: Console = console

    def sendMessage(self, message: str):
        '''
        Sends a message to the client handled by this instance.

        Args:
            message (str): The message to send.
        '''

        self.clientSocket.sendall(message.encode('utf-8'))

    def disconnect(self):
        '''
        Disconnects the client handled by this instance.
        Closes the socket, removes from server list, and announces departure.
        '''

        self.clientSocket.close()
        self.disconnected = True
        self.serverClients.remove(self)
        self.console.printlnBlue(f'Disconnected {self.clientAddress} with name {self.username}.')
        self.__announce__(f'blue {self.username} has disconnected from the server.')

    def __announce__(self, message: str):
        '''
        Broadcasts a message to all other clients connected to the server.

        Args:
            message (str): The message to announce.
        '''

        for i in range(len(self.serverClients)):
            if self.serverClients[i] is not self:
                self.serverClients[i].sendMessage(message)

    @override
    def run(self):
        '''
        The main execution method for the client handler thread.
        Listens for messages from the client and broadcasts them.
        '''

        try:
            while not self.disconnected:
                data: bytes = self.clientSocket.recv(BUFFER_SIZE)
                if not data:
                    self.disconnect()
                    break
                message = data.decode('utf-8')

                currentLine: str = self.console.getCurrentLineText()
                currentText: str = ''
                if currentLine != '': currentText = self.console.getBackTextToString('[Enter Command] ->', 3, '{Timeout ERROR, current command erased.} -> ')[1:]
                self.console.clearLine()
                self.console.moveFront()
                self.console.println(f'[{self.username}] -> {message}')
                self.console.printDim(f'[Enter Command] -> ')
                self.console.print(currentText)

                self.__announce__(f'[{self.username}] -> {message}') 
        except Exception as e:
            if not self.disconnected: 
                self.console.clearLine()
                self.console.moveFront()
                self.console.printlnError(f'Error handling client {self.clientAddress}!')
        finally:
            if not self.disconnected:
                self.console.printlnBlue(f'Closing connection to {self.clientAddress}...')
                self.disconnect()