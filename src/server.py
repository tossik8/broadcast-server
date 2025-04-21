import socket
import argparse
from .logger import get_server_logger
from threading import Thread, Lock

HOST = "0.0.0.0"

logger = get_server_logger()
connections_by_group: dict[str, set[socket.socket]] = { "general": set() }
lock = Lock()


def _broadcast(group: str, data: str, sender) -> None:
    with lock:
        copy = connections_by_group[group].copy()
    for conn in copy:
        try:
            if conn.getpeername() == sender:
                continue
        except socket.error:
            logger.debug("Could not get peer name. Connection had been terminated before.")
            continue
        message = f"From {sender}: {data}".encode()
        try:
            conn.sendall(message)
        except socket.error:
            logger.warning("Could not broadcast.")


def _shutdown_server() -> None:
    logger.info("Shutting down server...")
    with lock:
        for connections in connections_by_group.values():
            for conn in connections:
                logger.info(f"Closing connection with {conn.getpeername()}...")
                conn.shutdown(socket.SHUT_RDWR)
                conn.close()
    logger.info("Server shut down.")


def _change_groups(group: str, data: str, conn: socket.socket) -> str:
    new_group = data[7:]
    if len(new_group) == 0:
        raise ValueError("Group name cannot be empty.")
    if new_group == group:
        raise ValueError("Group name must be different from the currently active group.")
    with lock:
        connections_by_group[group].remove(conn)
        if new_group in connections_by_group:
            connections_by_group[new_group].add(conn)
        else:
            connections_by_group[new_group] = set([conn])
    return new_group


def _handle_group_change(group: str, data: str, conn: socket.socket, address) -> str:
    try:
        group = _change_groups(group, data, conn)
    except ValueError as e:
        logger.warning(e)
        try:
            conn.sendall(f"From {conn.getsockname()}: {str(e)}".encode())
        except socket.error:
            logger.warning(f"Could not send the reason for group change failure to {address}.")
    else:
        try:
            conn.sendall(f"From {conn.getsockname()}: You switched to group '{group}'".encode())
        except socket.error:
            logger.warning(f"Could not send group change confirmation to {address}.")
        else:
            logger.info(f"{address} switched to group '{group}'.")
    return group


def _receive_messages(conn: socket.socket, address) -> None:
    group = "general"
    with conn:
        while True:
            try:
                data = conn.recv(1024)
            except socket.error:
                logger.debug(f"Could not receive data from {address}. Connection had been terminated before.")
                break
            if not data:
                break
            data = data.decode()
            if data.startswith("GROUP: "):
                group = _handle_group_change(group, data, conn, address)
            else:
                _broadcast(group, data, address)
        with lock:
            connections_by_group[group].remove(conn)
    logger.info(f"Connection closed with {address}.")


def start_server(args: argparse.Namespace) -> None:
    logger.info("Starting server...")
    with socket.socket() as server:
        try:
            server.bind((HOST, args.port))
        except OSError:
            logger.error(f"Could not start server on {HOST}:{args.port}.")
            return
        server.listen()
        logger.info(f"Listening on {HOST}:{args.port}.")
        try:
            while True:
                conn, address = server.accept()
                thread = Thread(target=_receive_messages, args=[conn, address], name=str(address))
                with lock:
                    connections_by_group["general"].add(conn)
                thread.start()
                logger.info(f"Connected with {address}.")
        except KeyboardInterrupt:
            _shutdown_server()

