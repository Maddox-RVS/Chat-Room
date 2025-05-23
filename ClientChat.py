from threading import Thread
from Console import Console
from typing import Union
import threading
import socket
import time
import sys

BUFFER_SIZE: int = 1024
QUIT: str = '/quit'

class ClientTCP():
    '''
    Represents a TCP client for the chat application.
    Handles connection to the server, sending and receiving messages.
    '''

    def __init__(self, host: str, port: int, username: str):
        '''
        Initializes the ClientTCP instance.

        Args:
            host (str): The server's hostname or IP address.
            port (int): The server's port number.
            username (str): The username for the client.
        '''

        self.host: str = host
        self.port: int = port
        self.username: str = username
        self.clientSocket: Union[None, socket.socket] = None
        self.disconnected: bool = True
        self.stopEvent: Union[None, threading.Event] = None
        self.console: Console = Console()

    def __sendMessage__(self, message: str):
        '''
        Sends a message to the connected server.

        Args:
            message (str): The message string to send.
        '''

        try: self.clientSocket.sendall(message.encode('utf-8'))
        except Exception as e: 
            self.console.printlnError('Cound\'t send message. Make sure client is connected properly!')
            self.disconnect()

    def disconnect(self):
        '''
        Disconnects the client from the server.
        Closes the socket and sets the stop event for threads.
        '''

        self.console.printlnGreen('Disconnecting from server...')
        self.clientSocket.close()
        self.stopEvent.set()
        self.disconnected = True
        self.console.printlnGreen('Disconnected.')

    def connect(self):
        '''
        Establishes a connection to the server and starts communication.
        It creates a socket, connects, starts a message sender thread,
        sends the username, and then enters a loop to receive messages.
        '''

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
            try:
                self.clientSocket = clientSocket
                self.clientSocket.connect((self.host, self.port))
                self.disconnected = False

                self.stopEvent: threading.Event = threading.Event()
                messageSenderThread: Thread = Thread(target=self.__runMessageSender__, name='messageSender', args=(self.stopEvent,))
                messageSenderThread.start()

                self.__sendMessage__(self.username)

                while True:
                    data: bytes = self.clientSocket.recv(BUFFER_SIZE)
                    currentText: str = self.console.getBackTextToString('[Send Message] ->', 3, '{Timeout ERROR, current message erased.} -> ')[1:]
                    self.console.clearLine()
                    self.console.moveFront()

                    message: str = data.decode('utf-8').split()
                    if message[0] == 'blue': self.console.printlnBlue(' '.join(message[1:]))
                    elif message[0] == 'green': self.console.printlnGreen(' '.join(message[1:]))
                    else: self.console.println(' '.join(message))

                    self.console.printDim(f'[Send Message] -> ')
                    self.console.print(currentText)
            except ConnectionRefusedError:
                self.console.printlnError('Connection refused!')
            except Exception as e:
                self.console.println('')
                self.console.printlnError('Issue connecting to server!')
                if not self.disconnected: self.disconnect()

    def __runMessageSender__(self, stopEvent):
        '''
        Runs in a separate thread to handle sending user input as messages.

        Args:
            stopEvent (threading.Event): Event used to signal the thread to stop.
        '''
        
        while not self.stopEvent.is_set():
            self.console.printDim('[Send Message] -> ')
            message: str = self.console.input()

            linesCovered: int = self.console.getLinesCovered(f'[Send Message] -> {message}')                                                    
            for i in range(linesCovered):
                self.console.clearLine()
                self.console.moveUp()
            self.console.moveFront()
            self.console.println(f'[{self.username}] -> {message}')

            if self.disconnected: break
            elif message.lower() == QUIT:            
                self.disconnect()
            else: self.__sendMessage__(message)

if __name__ == '__main__':
    host: str = ''
    port: int = 0
    username: str = ''

    if not (len(sys.argv) == 1 or len(sys.argv) == 4):
        print('Usage: python ClientChat.py [server address] [server port] [username]')
        exit(0)

    if len(sys.argv) == 1:
        tempConsole: Console = Console()
        tempConsole.printDim('Enter the server address: ')
        host = tempConsole.input()
        tempConsole.printDim('Enter the server port: ')
        port = int(tempConsole.input())
        tempConsole.printDim('Enter a username: ')
        username = tempConsole.input()
        tempConsole.close()
    else:
        host = sys.argv[1]
        port = int(sys.argv[2])
        username = sys.argv[3]

    client: ClientTCP = ClientTCP(host, port, username)
    client.connect()

    time.sleep(2)