from mss import exception
from gbf_automata.game.gbf import GBFGame
import multiprocessing
import socket
import selectors
import pprint
import types

HOST = "127.0.0.1"
PORT = 65432

sel = selectors.DefaultSelector()


def start_bot():
    print(f"foo: <{multiprocessing.current_process()}>")


def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print(f"Accepted connection from {addr}")
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
        else:
            print(f"Closing connection to {data.addr}")
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print(f"Echoing {data.outb!r} to {data.addr}")
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]


def create_socket():
    slock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    slock.bind((HOST, PORT))
    slock.listen()
    pprint.pprint(f"Listening on {(HOST, PORT)}")

    slock.setblocking(False)
    sel.register(slock, selectors.EVENT_READ, data=None)

    try:
        while True:
            events = sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    accept_wrapper(key.fileobj)
                else:
                    service_connection(key, mask)

    except KeyboardInterrupt:
        pprint.pprint("Caught keyboard interrupt, exiting")

    finally:
        sel.close()


if __name__ == "__main__":
    create_socket()

    # game = GBFGame()
    # game.start()

    # print(f"main: <{threading.get_ident()}>")
    #
    # bot_process = multiprocessing.Process(target=start_bot)
    #
    # bot_process.start()
    # bot_process.is_alive()
    pass
