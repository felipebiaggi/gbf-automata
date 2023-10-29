import sys
import functools
import websockets.sync.server

from types import FrameType
from socket import SHUT_RDWR
from signal import Signals, SIGTERM, signal
from websockets.sync.connection import Connection
from gbf_automata.enums.state import State
from gbf_automata.util.logger import get_logger
from gbf_automata.util.settings import settings
from gbf_automata.classes.load_state import LoadState

logger = get_logger(__name__)


class GBFAutomataServer:
    def __init__(self, load_state: LoadState) -> None:
        self._load_state = load_state
        self._server = self.create_connection()

    def create_connection(self) -> websockets.sync.server.WebSocketServer:
        state_handler = functools.partial(handler, load_state=self._load_state)
        return websockets.sync.server.serve(
            handler=state_handler, host=settings.host, port=settings.port
        )

    def run(self) -> None:
        self._server.serve_forever()
        logger.info("Server Stop.")

    def shutdown(self) -> None:
        logger.info("Socket Shutdown.")
        self._server.socket.shutdown(SHUT_RDWR)

        logger.info("Shutdown Close.")
        self._server.shutdown()

        logger.info("Os Exit")
        sys.exit(0)

    def setup_signal(self) -> None:
        partial_handler = functools.partial(signal_handler, server=self)
        signal(SIGTERM, partial_handler)


def handler(connection: Connection, load_state: LoadState) -> None:
    logger.info(f"Connection open - Client ID: <{connection.id}>")

    try:
        for (
            message
        ) in connection:  # Se a conexão é fechada o iterator levante um exception.
            if message == "none":
                load_state.set_state(State.NONE)

            if message == "block":
                load_state.set_state(State.BLOCK)

    except websockets.ConnectionClosedError as err:
        logger.error(f"Connection error: <{err}>.")
    except (
        Exception
    ) as err:  # Caso a exception não sejá tratada, capturamos o que chegar aqui.
        logger.error(f"Genetic error: <{err}>.")

    logger.info(f"Connection close - Client ID: <{connection.id}>.")


def signal_handler(
    signal: Signals, frame: FrameType, server: GBFAutomataServer
) -> None:
    logger.info(f"Signals: <{signal}> \n FrameType: <{frame}>")
    server.shutdown()
