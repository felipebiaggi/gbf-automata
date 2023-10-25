import functools
import websockets.sync.server

from typing import Dict, Any
from websockets.sync.connection import Connection

from gbf_automata.enums.state import State
from gbf_automata.util.logger import get_logger
from gbf_automata.classes.load_state import LoadState

logger = get_logger(__name__)


HOST = "127.0.0.1"
PORT = 65432

def handler(connection: Connection, **kwargs: Any) -> None:
    connection_id = connection.id
    load_state = kwargs['extra_argument']

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


def create_websocket_server(load_state: LoadState) -> None:

    
    state_handler = functools.partial(handler, extra_argument=load_state)

    with websockets.sync.server.serve(handler=state_handler, host=HOST, port=PORT) as server:
        server.serve_forever()
