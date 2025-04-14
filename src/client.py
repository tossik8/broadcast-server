import socket
import os
import signal
from .logger import get_client_logger
import argparse
from threading import Thread, main_thread

logger = get_client_logger()


def _receive_messages(client: socket.socket) -> None:
    while True:
        data = client.recv(1024)
        if not data:
            break
        print(data.decode())
    if main_thread().is_alive():
        os.kill(os.getpid(), signal.SIGINT)


def start_client(args: argparse.Namespace) -> None:
    with socket.socket() as client:
        try:
            client.connect((args.host, args.port))
        except:
            logger.error(f"Could not connect to {args.host}:{args.port}.")
            return
        logger.info(f"Listening on {client.getsockname()}.")
        logger.info(f"Connected with {args.host}:{args.port}.")
        receive_message_thread = Thread(target=_receive_messages, args=[client])
        receive_message_thread.start()
        while True:
            try:
                user_input = input("Enter your message\n")
            except KeyboardInterrupt:
                client.shutdown(socket.SHUT_RDWR)
                client.close()
                break
            client.sendall(user_input.encode())
    logger.info(f"Connection closed with {args.host}:{args.port}.")

