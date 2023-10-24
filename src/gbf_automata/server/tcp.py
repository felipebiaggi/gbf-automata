import types
import socket
import selectors

from gbf_automata.util.logger import get_logger

logger = get_logger(__name__)
sel = selectors.DevpollSelector()


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
            logger.info(f"Closing connection to {data.addr}")
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            logger.info(f"Echoing {data.outb!r} to {data.addr}")
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]


def create_tcp_server(host: str, port: int):
    slock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    slock.bind((host, port))
    slock.listen()
    logger.info(f"Listening on {(host, port)}")

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
        logger.error("Caught keyboard interrupt, exiting")

    finally:
        sel.close()
