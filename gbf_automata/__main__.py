import asyncio
import multiprocessing

from gbf_automata.models.gbf_manager import (
    GBFManager,
    StatusManager,
)
from gbf_automata.server.gbf_websocket import GBFAutomataServer
from gbf_automata.services.fsm import StateMachine


def run_fsm(
    message_queue: multiprocessing.Queue,
    status_manager: StatusManager,
):
    fsm = StateMachine(message_queue, status_manager)
    fsm.run()


def main():
    message_queue = multiprocessing.Queue()

    manager = GBFManager()
    manager.start()

    status_manager = manager.StatusManager()

    server = GBFAutomataServer(message_queue, status_manager)

    process = multiprocessing.Process(
        target=run_fsm, args=(message_queue, status_manager)
    )
    process.start()

    try:
        asyncio.run(server.run())
    except KeyboardInterrupt:
        print("\n🛑 Server manually stopped.")
    finally:
        process.terminate()
        process.join()


if __name__ == "__main__":
    main()
