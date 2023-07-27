from matplotlib import pprint
from gbf_automata.wrapper.x11 import get_position, set_position

if __name__ == "__main__":
    pprint.pprint(get_position())

    set_position(0, 0)
