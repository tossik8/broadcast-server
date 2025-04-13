import argparse
from .server import start_server
from .client import start_client


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(required=True)
    start_parser = subparsers.add_parser("start", help="Start a broadcast server")
    start_parser.add_argument("-p", "--port", type=int, required=True)
    start_parser.set_defaults(func=start_server)
    connect_parser = subparsers.add_parser("connect", help="Connect to a broadcast server")
    connect_parser.add_argument("--host", default="localhost")
    connect_parser.add_argument("-p", "--port", type=int, required=True)
    connect_parser.set_defaults(func=start_client)
    args = parser.parse_args()
    try:
        args.func(args)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
