import asyncio
import multiprocessing

from gbf_automata.server.gbf_websocket import GBFAutomataServer


def run_fsm(send_queue, receive_queue):
    """Simula uma tarefa CPU-bound rodando separada do event loop"""

    while True:
        try:
            message = send_queue.get()
            print(f"  Finite State Machine message recv: <{message}>")
        except KeyboardInterrupt:
            print("  Finite State Machine closed")
            break


def main():
    send_queue = multiprocessing.Queue()  # Para enviar mensagens ao processo pesado
    receive_queue = multiprocessing.Queue()  # Para receber mensagens do processo pesado

    server = GBFAutomataServer(send_queue, receive_queue)

    process = multiprocessing.Process(target=run_fsm, args=(send_queue, receive_queue))
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

# if __name__ == "__main__":
#     BaseManager.register("LoadState", LoadState)
#     manager = BaseManager()
#     manager.start()
#     load_state_manager = manager.LoadState()  # type: ignore
#
#     server = GBFAutomataServer(load_state_manager)
#     server_process = Process(target=server.run)
#
#     server = GBFAutomataServer(load_state_manager)
