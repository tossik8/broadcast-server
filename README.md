# Broadcast Server

A simple TCP-based broadcast server and client application written in Python. The server accepts multiple client connections and broadcasts messages from one client to all others. The client connects to the server, sends messages, and receives broadcasted messages from other clients.

## Features

- **Server**:
  - Listens for incoming client connections on a specified port.
  - Broadcasts messages from one client to all other connected clients.
  - Logs connection events to both console and a file (`server.log`).
  - Gracefully handles client disconnections and server shutdown (Ctrl+C).

- **Client**:
  - Connects to the server using a specified host and port.
  - Logs connection events to console.
  - Sends user-input messages to the server.
  - Receives and displays broadcasted messages from other clients.
  - Exits cleanly when the server closes the connection or on user interrupt (Ctrl+C).

- **Command-Line Interface**:
  - Run as a console script (`broadcast-server`) with `start` (server) or `connect` (client) commands.
  - Supports configurable port and host via command-line arguments.

## Requirements

- Python 3.12 or higher
- No external dependencies

## Installation

1. **Clone the Repository** (or download the project):
   ```bash
   git clone https://github.com/tossik8/broadcast-server.git
   cd broadcast-server
   ```

2. **Install the Package**:
   Install the package to enable the `broadcast-server` console script:
   ```bash
   pip install .
   ```

## Usage

The application is run using the `broadcast-server` command with either `start` (to run the server) or `connect` (to run the client).

### Running the Server

Start the server on a specified port:

```bash
broadcast-server start -p <port>
```

- The server listens on `0.0.0.0:<port>` and accepts multiple client connections.
- Press `Ctrl+C` to shut down the server gracefully.

### Running the Client

Connect to a server at a specified host and port:

```bash
broadcast-server connect --host <host> -p <port>
```

- Replace `localhost` with the server’s IP address if running remotely (e.g., `192.168.0.94`).
- Type messages and press Enter to send them to the server.
- Received messages from other clients are displayed in the console.
- The client exits automatically if the server closes the connection or if you press `Ctrl+C`.

## Notes

- The server binds to `0.0.0.0` to accept connections from any network interface.
- The client uses a separate thread to receive messages, allowing simultaneous sending and receiving.
- If the server closes, clients detect the disconnection and exit cleanly using a `SIGINT` signal to interrupt the input prompt.

## Credits

This project was inspired by the [Broadcast Server](https://roadmap.sh/projects/broadcast-server) project idea from roadmap.sh.

## Author

Nikita Toropov
