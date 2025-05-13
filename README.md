# Python Terminal Chat Application

[![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) A simple, terminal-based chat application built with Python using sockets for networking and the `curses` library for an enhanced console interface.

## Table of Contents

* [Features](#features)
* [Project Structure](#project-structure)
* [Prerequisites](#prerequisites)
* [Installation](#installation)
* [Usage](#usage)
    * [Running the Server](#running-the-server)
    * [Running the Client](#running-the-client)
* [Commands](#commands)
    * [Server Commands](#server-commands)
    * [Client Commands](#client-commands)
* [Dependencies](#dependencies)

## Features

* **Real-time Chat:** Send and receive messages instantly between multiple clients connected to a central server.
* **Server Administration:** Server console allows for administrative commands like announcements and shutdown.
* **Colored Output:** Uses the `curses` library to provide colored text for different types of messages (e.g., server announcements, user joins/leaves, errors).
* **Dynamic Console UI:** Enhanced console interaction for message input and display, handling line wrapping and clearing.
* **Multi-threaded:** Server handles multiple clients concurrently using threading. Client uses threads for sending and receiving messages simultaneously.

## Project Structure

├── ServerChat.py       # Main script to run the chat server    
├── ClientChat.py       # Main script to run the chat client    
├── ClientHandler.py    # Handles individual client connections on the server   
├── Console.py          # Utility class for enhanced console I/O using curses   
└── requirements.txt    # Lists project dependencies    
## Prerequisites

* **Python 3.x (3.13.2 recommended):** Ensure you have a compatible Python version installed.
* **pip:** Python's package installer, usually included with Python.
* **Terminal that supports `curses`:** The `curses` library is used for the console interface.
    * **Linux/macOS:** Typically supported out-of-the-box.
    * **Windows:** Requires the `windows-curses` package (included in `requirements.txt`). You might need a compatible terminal emulator like Windows Terminal or Git Bash.

## Installation

1.  **Clone the repository (or download the files):**
    ```bash
    # If using Git
    git clone https://github.com/Maddox-RVS/Chat-Room.git
    cd https://github.com/Maddox-RVS/Chat-Room.git
    ```
    Or simply place all the `.py` files in the same directory.

2.  **Install dependencies:**
    Navigate to the project directory in your terminal and run:
    ```bash
    pip install -r requirements.txt
    ```
    This command installs all the necessary packages listed in the `requirements.txt` file.

## Usage

### Running the Server

1.  Open your terminal.
2.  Navigate to the directory containing the project files.
3.  Run the server script:
    ```bash
    python ServerChat.py
    ```
4.  The script will prompt you to enter a port number for the server to listen on. Choose an available port (e.g., `5000`, `8080`).
5.  The server will start and display messages indicating it's listening for connections. You can now enter server commands.

### Running the Client

1.  Open a **new** terminal window for each client you want to connect.
2.  Navigate to the directory containing the project files.
3.  Run the client script using one of the following methods:

    * **Method 1: Command-line arguments:**
        ```bash
        python ClientChat.py <server_address> <server_port> <username>
        ```
        * Replace `<server_address>` with the IP address or hostname of the machine running the server (use `127.0.0.1` or `localhost` if running on the same machine).
        * Replace `<server_port>` with the port number the server is listening on.
        * Replace `<username>` with your desired chat nickname.

        **Example:**
        ```bash
        python ClientChat.py 127.0.0.1 5000 Alice
        ```

    * **Method 2: Interactive prompts:**
        ```bash
        python ClientChat.py
        ```
        The script will prompt you to enter the server address, server port, and username interactively.

4.  Once connected, you can start sending messages by typing them and pressing Enter. Incoming messages from other users and the server will be displayed.

## Commands

### Server Commands

Enter these commands in the terminal window where the `ServerChat.py` script is running:

* `/announce <message>`: Sends a message prefixed with `*[SERVER]*` to all connected clients. The message will be displayed in green.
    * Example: `/announce Server maintenance in 5 minutes.`
* `/shutdown`: Disconnects all clients gracefully and shuts down the server.

### Client Commands

Enter these commands in the terminal window where the `ClientChat.py` script is running:

* `/quit`: Disconnects the client from the server and exits the client application.

## Dependencies

> **This project relies on the following Python packages:**     
>
> ansicon==1.89.0     
> colorama==0.4.6     
> cursor==1.3.5       
> jinxed==1.3.0   
> PySimpleValidate==0.2.12      
> stdiomask==0.0.6    
> wcwidth==0.2.13     
> wheel==0.45.1       
> windows-curses==2.4.1  # Required for curses support on Windows     
> These can be installed using the `requirements.txt` file as described in the [Installation](#installation) section.