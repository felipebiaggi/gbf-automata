import asyncio
import multiprocessing

from gbf_automata.models.render_manager import (
    RenderManager,
    RenderStatusManager,
)
from gbf_automata.server.gbf_websocket import GBFAutomataServer
from gbf_automata.services.fsm import StateMachine


def run_fsm(
    send_queue: multiprocessing.Queue,
    receive_queue: multiprocessing.Queue,
    render_status_manager: RenderStatusManager,
):
    fsm = StateMachine(send_queue, receive_queue, render_status_manager)
    fsm.run()


def main():
    send_queue = multiprocessing.Queue()
    receive_queue = multiprocessing.Queue()

    manager = RenderManager()
    manager.start()

    render_status_manager = manager.RenderStatusManager()

    server = GBFAutomataServer(send_queue, receive_queue, render_status_manager)

    process = multiprocessing.Process(
        target=run_fsm, args=(send_queue, receive_queue, render_status_manager)
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
