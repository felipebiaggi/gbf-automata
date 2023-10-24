import websockets.sync.server
from gbf_automata.util.logger import get_logger
from websockets.sync.connection import Connection

from gbf_automata.util.logger import get_logger

logger = get_logger(__name__)


HOST = "127.0.0.1"
PORT = 65432


def handler(connection: Connection) -> None:
    connection_id = connection.id

    logger.info(f"Connection open - Client ID: <{connection_id}>")

    try:
        for (
            message
        ) in connection:  # Se a conexão é fechada o iterator levante um exception.
            logger.info(message)
    except websockets.ConnectionClosedError as err:
        logger.error(f"Connection error: <{err}>.")
    except (
        Exception
    ) as err:  # Caso a exception não sejá tratada, capturamos o que chegar aqui.
        logger.error(f"Genetic error: <{err}>.")

    logger.info(f"Connection close - Client ID: <{connection_id}>.")


def create_websocket_server() -> None:
    with websockets.sync.server.serve(handler=handler, host=HOST, port=PORT) as server:
        server.serve_forever()


if __name__ == "__main__":
    create_websocket_server()
