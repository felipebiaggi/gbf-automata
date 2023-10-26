import sys
import functools
import websockets.sync.server

from typing import Any
from types import FrameType
from socket import SHUT_RDWR
from signal import Signals, SIGTERM, signal
from websockets.sync.connection import Connection
from gbf_automata.enums.state import State
from gbf_automata.util.logger import get_logger
from gbf_automata.classes.load_state import LoadState

logger = get_logger(__name__)


HOST = "127.0.0.1"
PORT = 65432


class GbfAutomataServer:
    def __init__(self, state: LoadState) -> None:
        self._state = state
        self._server = self.create_connection()

        self.setup_signal()

    def create_connection(self) -> websockets.sync.server.WebSocketServer:
        state_handler = functools.partial(handler, extra_argument=self._state)
        return websockets.sync.server.serve(handler=state_handler, host=HOST, port=PORT)

    def run(self) -> None:
        self._server.serve_forever()
        logger.info("Server Stop.")

    def shutdown(self) -> None:
        logger.info("Socket Shutdown.")
        self._server.socket.shutdown(SHUT_RDWR)
        
        logger.info("Shutdown Close.")
        self._server.shutdown()


    def setup_signal(self) -> None:
        partial_handler = functools.partial(signal_handler, server=self)
        signal(SIGTERM, partial_handler)


def handler(connection: Connection, **kwargs: Any) -> None:
    connection_id = connection.id
    load_state = kwargs["extra_argument"]

    if not isinstance(load_state, LoadState):
        raise Exception

    logger.info(f"Connection open - Client ID: <{connection_id}>")

    try:
        for (
            message
        ) in connection:  # Se a conexão é fechada o iterator levante um exception.
            if message == "none":
                load_state.state = State.NONE

            if message == "block":
                load_state.state = State.BLOCK

    except websockets.ConnectionClosedError as err:
        logger.error(f"Connection error: <{err}>.")
    except (
        Exception
    ) as err:  # Caso a exception não sejá tratada, capturamos o que chegar aqui.
        logger.error(f"Genetic error: <{err}>.")

    logger.info(f"Connection close - Client ID: <{connection_id}>.")


def signal_handler(
    signal: Signals, frame: FrameType, server: GbfAutomataServer
) -> None:
    logger.info(f"Signals: <{signal}> \n FrameType: <{frame}>")
    logger.info("Child SIGTERM")
    server.shutdown()
