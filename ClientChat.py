from PrintHelper import printBlue, printGreen, printRed, printError, printOverwriteLine, printDim, printOverwrite
from colorama import Fore, Style, Back
from threading import Thread
from typing import Optional
from typing import Union
import threading
import colorama
import curses
import socket
import sys
import os

BUFFER_SIZE: int = 1024
QUIT: str = 'quit'

class ClientTCP():
    def __init__(self, host: str, port: int, username: str):
        self.host: str = host
        self.port: int = port
        self.username: str = username
        self.clientSocket: Union[None, socket.socket] = None
        self.disconnected: bool = False
        self.stopEvent: Union[None, threading.Event] = None

    def __sendMessage__(self, message: str):
        try: self.clientSocket.sendall(message.encode('utf-8'))
        except Exception as e: 
            printError('Cound\'t send message. Make sure client is connected properly!')
            self.disconnect()

    def disconnect(self):
        printGreen('Disconnecting from server...')
        self.clientSocket.close()
        self.stopEvent.set()
        self.disconnected = True
        printGreen('Disconnected.')

    def connect(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
            try:
                self.clientSocket = clientSocket
                self.clientSocket.connect((self.host, self.port))

                self.stopEvent: threading.Event = threading.Event()
                messageSenderThread: Thread = Thread(target=self.__runMessageSender__, name='messageSender', args=(self.stopEvent,))
                messageSenderThread.start()

                self.__sendMessage__(self.username)

                while True:
                    data: bytes = self.clientSocket.recv(BUFFER_SIZE)
                    printOverwriteLine(data.decode('utf-8'))
                    print(Style.DIM + f'\n[Send Message] -> ' + Style.RESET_ALL, end='')
            except ConnectionRefusedError:
                printError('Connection refused!')
            except Exception as e:
                if not self.disconnected: 
                    printError('Issue connecting to server!')
                    self.disconnect()

    def __runMessageSender__(self, stopEvent):
        while not self.stopEvent.is_set():
            message: str = input(Style.DIM + '[Send Message] -> ' + Style.RESET_ALL)
            # sys.stdout.write('\033[1A') # Move the cursor up 1 line
            # printOverwriteLine(f'[{self.username}] -> {message}' + os.linesep)
            printOverwrite(f'[Send Message] -> {message}', f'[{self.username}] -> {message}')
            if self.disconnected: break
            elif message.lower() == QUIT:
                self.disconnect()
            else: self.__sendMessage__(message)

if __name__ == '__main__':
    colorama.init()

    host: str = input(Style.DIM + 'Enter the server address: ' + Style.RESET_ALL)
    port: int = int(input(Style.DIM + 'Enter the server port: ' + Style.RESET_ALL))
    username: str = input(Style.DIM + 'Enter a username: ' + Style.RESET_ALL)
    client: ClientTCP = ClientTCP(host, port, username)
    client.connect()

    colorama.deinit()