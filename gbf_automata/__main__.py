import functools
from multiprocessing import Process
from multiprocessing.managers import BaseManager
from multiprocessing.process import BaseProcess
from signal import SIGINT, Signals, signal, SIGTERM
from types import FrameType
from gbf_automata.classes.load_state import LoadState, get_state
from gbf_automata.game.gbf import GBFGame
from gbf_automata.server.websocket import GBFAutomataServer
from gbf_automata.util.logger import get_logger


load_state = get_state()
logger = get_logger(__name__)


# def signal_hander(
#     signal: Signals, frame: FrameType, server_process: BaseProcess
# ) -> None:
#     logger.debug(f"Signal: <{signal}>  - Frame: <{frame}>")
#     server.shutdown()
#     server_process.terminate()


if __name__ == "__main__":
    # # BaseManager.register("LoadState", LoadState)
    # manager = BaseManager()
    # manager.start()
    # load_state_manager = manager.LoadState()  # type: ignore
    #
    # game = GBFGame(load_state_manager)
    # server = GBFAutomataServer(load_state_manager)
    #
    # server_process = Process(target=server.run)
    #
    # game_process = Process(target=game.run)
    #
    # partial_handler = functools.partial(signal_hander, server_process=server_process)
    # signal(SIGTERM, partial_handler)
    # signal(SIGINT, partial_handler)
    #
    # game_process.start()
    # server_process.start()
    #
    # game_process.join()
    # server_process.join()
    #
    # logger.info("GBFAutomata finished.")
