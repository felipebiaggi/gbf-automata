import time

from multiprocessing import Process

from gbf_automata.classes.load_state import get_state
from gbf_automata.enums.state import State
from gbf_automata.server.websocket import create_websocket_server


load_state = get_state()

if __name__ == "__main__":

    server_process = Process(
        target=create_websocket_server,
        args=(load_state,)
    )


    server_process.start()
    server_process.join()

    # server_process.start()
    #
    # while True:
    #     if server_process.is_alive() is False:
    #         break
    #     else:
    #         time.sleep(1.0)
    #
    # server_process.terminate()

