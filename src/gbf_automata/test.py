import logging
import websockets.sync.server
from types import FrameType
from multiprocessing import Process
from signal import SIGTERM, signal, Signals
from websockets.sync.connection import Connection
from websockets.sync.server import WebSocketServer

logger = logging.getLogger(__name__)

HOST = "127.0.0.1"
PORT = 65432


def handler(connection: Connection) -> None:
    print(f"Connection open - Client ID: <{connection.id}>")

    try:
        for message in connection:
            print(f"Client message: <{message}>")
    except Exception as err:
        print(f"Genetic error: <{err}>.")

    print(f"Connection close - Client ID: <{connection.id}>.")


class DummyServer:
    def __init__(self) -> None:
        self._server = self.create_server()

    def create_server(self) -> WebSocketServer:
        return websockets.sync.server.serve(handler=handler, host=HOST, port=PORT, close_timeout=1)

    def run(self) -> None:
        print("Server Start.")
        self._server.serve_forever()
        print("Server Stop.")

    def shutdown(self) -> None:
        print("Starting shutdown.")
        self._server.shutdown()

server = DummyServer()


def signal_handler(signal: Signals, frame: FrameType) -> None:
    server.shutdown()


if __name__ == "__main__":
    signal(SIGTERM, handler=signal_handler)

    server.run()


