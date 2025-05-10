from PrintHelper import printBlue, printGreen, printRed, printError, printOverwriteLine, printDim, printOverwrite
from colorama import Fore, Style, Back
from threading import Thread
from Console import Console
from typing import Union
import threading
import colorama
import socket
import time

BUFFER_SIZE: int = 1024
QUIT: str = '/quit'

class ClientTCP():
    def __init__(self, host: str, port: int, username: str):
        self.host: str = host
        self.port: int = port
        self.username: str = username
        self.clientSocket: Union[None, socket.socket] = None
        self.disconnected: bool = True
        self.stopEvent: Union[None, threading.Event] = None
        self.console: Console = Console()

    def __sendMessage__(self, message: str):
        try: self.clientSocket.sendall(message.encode('utf-8'))
        except Exception as e: 
            self.console.printlnError('Cound\'t send message. Make sure client is connected properly!')
            self.disconnect()

    def disconnect(self):
        self.console.printlnGreen('Disconnecting from server...')
        self.clientSocket.close()
        self.stopEvent.set()
        self.disconnected = True
        self.console.printlnGreen('Disconnected.')

    def connect(self):
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
                    self.console.println()

                    self.console.printDim(f'[Send Message] -> ')
                    self.console.print(currentText)
            except ConnectionRefusedError:
                self.console.printlnError('Connection refused!')
            except Exception as e:
                self.console.println('')
                self.console.printlnError('Issue connecting to server!')
                if not self.disconnected: self.disconnect()

    def __runMessageSender__(self, stopEvent):
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
    colorama.init()

    tempConsole: Console = Console()

    tempConsole.printDim('Enter the server address: ')
    host: str = tempConsole.input()
    tempConsole.printDim('Enter the server port: ')
    port: str = int(tempConsole.input())
    tempConsole.printDim('Enter a username: ')
    username: str = tempConsole.input()
    tempConsole.close()

    client: ClientTCP = ClientTCP(host, port, username)
    client.connect()

    colorama.deinit()

    time.sleep(2)