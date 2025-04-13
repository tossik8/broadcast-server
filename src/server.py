import socket
import argparse
from .logger import get_server_logger
from threading import Thread, Lock

HOST = "0.0.0.0"

logger = get_server_logger()
connections: list[socket.socket] = []
lock = Lock()


def _broadcast(data: bytes, sender) -> None:
    with lock:
        copy = connections.copy()
    for conn in copy:
        if conn.getpeername() == sender:
            continue
        message = f"From {sender}: {data.decode()}"
        try:
            conn.sendall(message.encode())
        except socket.error:
            logger.warning("Could not broadcast")


def _shutdown_server() -> None:
    with lock:
        for conn in connections:
            conn.shutdown(socket.SHUT_RDWR)
            conn.close()
        connections.clear()


def _receive_messages(conn: socket.socket, address) -> None:
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            _broadcast(data, address)
        try:
            with lock:
                connections.remove(conn)
        except ValueError:
            logger.debug(f"{address} had been removed from connections before")
    logger.info(f"Connection closed with {address}")


def start_server(args: argparse.Namespace) -> None:
    with socket.socket() as server:
        try:
            server.bind((HOST, args.port))
        except OSError:
            logger.error(f"Could not start server on {HOST}:{args.port}")
            return
        server.listen()
        logger.info(f"Server is listening on {HOST}:{args.port}")
        try:
            while True:
                conn, address = server.accept()
                thread = Thread(target=_receive_messages, args=[conn, address])
                with lock:
                    connections.append(conn)
                thread.start()
                logger.info(f"Connected with {address}")
        except KeyboardInterrupt:
            _shutdown_server()
            logger.info("Server closed")

