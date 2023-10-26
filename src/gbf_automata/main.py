import functools
from multiprocessing import Process
from signal import SIGINT, Signals, signal, SIGTERM
from types import FrameType
from typing import List
from gbf_automata.classes.load_state import get_state
from gbf_automata.server.websocket import GbfAutomataServer
from gbf_automata.util.logger import get_logger

load_state = get_state()
server = GbfAutomataServer(load_state)
logger = get_logger(__name__)



def signal_hander(signal: Signals, frame: FrameType, processes: List):
    server.shutdown()
    
    for process in processes:
        process.join()
        process.close()

if __name__ == "__main__":

    processes = []  

    processes.append(Process(target=server.run))

    partial_handler = functools.partial(signal_hander, processes=processes)
    signal(SIGTERM, partial_handler)
    signal(SIGINT, partial_handler)

    for process in processes:
        process.start()

    for process in processes:
        process.join()


    logger.info("GBFAutomata finished.")
