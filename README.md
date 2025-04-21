# Broadcast Server

A simple TCP-based broadcast server and client application written in Python. The server accepts multiple client connections, allows clients to join different groups, and broadcasts messages from one client to all others within the same group. The client connects to the server, sends messages, and receives broadcasted messages from other clients in the same group.

## Features

- **Server**:

  - Listens for incoming client connections on a specified port.
  - Manages multiple groups, with clients able to switch between groups.
  - Broadcasts messages from one client to all other clients in the same group.
  - Logs connection events, group changes, and errors to both console and a file (`server.log`).
  - Gracefully handles client disconnections and server shutdown (Ctrl+C).

- **Client**:

  - Connects to the server using a specified host and port.
  - Logs connection events to console.
  - Sends user-input messages to the server.
  - Receives and displays broadcasted messages from other clients in the same group.
  - Can switch to a different group by sending a message starting with "GROUP: " followed by the group name.
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

2. **Install the Package**: Install the package to enable the `broadcast-server` console script:

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
- Clients are initially placed in the "general" group.
- Press `Ctrl+C` to shut down the server gracefully.

### Running the Client

Connect to a server at a specified host and port:

```bash
broadcast-server connect --host <host> -p <port>
```

- Replace `localhost` with the server’s IP address if running remotely (e.g., `192.168.0.94`).
- Type messages and press Enter to send them to the server.
- To change groups, send a message starting with "GROUP: " followed by the desired group name (e.g., "GROUP: lobby").
- Received messages from other clients in the same group are displayed in the console.
- The client exits automatically if the server closes the connection or if you press `Ctrl+C`.

### Group Changing

- Clients can switch to a different group by sending a message that starts with "GROUP: " followed by the group name.
- If the group does not exist, the server will create it.
- Clients cannot switch to a group with an empty name or to the same group they are already in.
- Upon successful group change, the client receives a confirmation message.
- If an error occurs (e.g., trying to switch to the same group), the client is notified of the error.

## Notes

- The server binds to `0.0.0.0` to accept connections from any network interface.
- The client uses a separate thread to receive messages, allowing simultaneous sending and receiving.
- If the server closes, clients detect the disconnection and exit cleanly using a `SIGINT` signal to interrupt the input prompt.
- Messages are only broadcasted to clients within the same group, excluding the sender.

## Credits

This project was inspired by the [Broadcast Server](https://roadmap.sh/projects/broadcast-server) project idea from roadmap.sh.

## Author

Nikita Toropov
