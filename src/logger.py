import logging

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

def get_server_logger() -> logging.Logger:
    logger = logging.getLogger("Broadcast Server")
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler("server.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger


def get_client_logger() -> logging.Logger:
    logger = logging.getLogger("Broadcast Client")
    logger.setLevel(logging.INFO)
    logger.addHandler(console_handler)
    return logger