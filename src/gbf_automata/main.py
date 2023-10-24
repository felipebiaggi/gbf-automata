import asyncio
import time
from websockets.server import serve
import multiprocessing
import socket
import selectors
import pprint
import types

HOST = "127.0.0.1"
PORT = 65432

sel = selectors.DefaultSelector()
#
#
# def start_bot():
#     
#


# def accept_wrapper(sock):
#     conn, addr = sock.accept()  # Should be ready to read
#     print(f"Accepted connection from {addr}")
#     conn.setblocking(False)
#     data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
#     events = selectors.EVENT_READ | selectors.EVENT_WRITE
#     sel.register(conn, events, data=data)
#
#
# def service_connection(key, mask):
#     sock = key.fileobj
#     data = key.data
#     if mask & selectors.EVENT_READ:
#         recv_data = sock.recv(1024)  # Should be ready to read
#         if recv_data:
#             data.outb += recv_data
#         else:
#             print(f"Closing connection to {data.addr}")
#             sel.unregister(sock)
#             sock.close()
#     if mask & selectors.EVENT_WRITE:
#         if data.outb:
#             print(f"Teste")
#             sent = sock.send()  # Should be ready to write
#             data.outb = data.outb[sent:]
#
#
# def create_tcp_server():
#     slock = socket.socket(socket.AF_, socket.SOCK_STREAM)
#     slock.bind((HOST, PORT))
#     slock.listen()
#     pprint.pprint(f"Listening on {(HOST, PORT)}")
#     slock.setblocking(False)
#     sel.register(slock, selectors.EVENT_READ, data=None)
#
#     try:
#         while True:
#             events = sel.select(timeout=None)
#             for key, mask in events:
#                 if key.data is None:
#                     accept_wrapper(key.fileobj)
#                 else:
#                     service_connection(key, mask)
#
#     except KeyboardInterrupt:
#         pprint.pprint("Caught keyboard interrupt, exiting")
#     finally:
#         sel.close()


# def create_udp_server():
#     socket_lock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     socket_lock.bind((HOST, PORT))
#     pprint.pprint(f"Listening on {(HOST, PORT)}")
#
#     try:
#         while(True):
#             payload, _ = socket_lock.recvfrom(1)
#
#             print(payload)
#
#
#     except KeyboardInterrupt:
#         pprint.pprint("Caught keyboard interrupt, exiting")
#     finally:
#         socket_lock.close()




async def echo(websocket):
    async for message in websocket:
        pprint.pprint(f"Message: {message} - {time.time()}")
        await websocket.send(message)

async def websocket_server():
    pprint.pprint(f"Create Websocket Server: {HOST}:{PORT}")
    async with serve(echo, HOST, PORT):
        await asyncio.Future()


class LoadState(object):
    def __init__(self) -> None:
        self._state = None
        self._lock = multiprocessing.Lock()

    @property
    def state(self):
        with self._lock:
            return self._state

    @state.setter
    def state(self, value):
        with self._lock:
            print("State Change!")
            self._state = value

    @state.getter
    def state(self):
        with self._lock:
            return self._state


def run_websocket_server():
    pprint.pprint(f"Server Process INFO: {multiprocessing.current_process()}")
    asyncio.run(websocket_server())

if __name__ == "__main__":
    
    server_process = multiprocessing.Process(target=run_websocket_server)
    try:
        server_process.start()
    except KeyboardInterrupt:
        pprint.pprint("Caught keyboard interrupt, exiting")

    server_process.join()

    # print(f"main: <{threading.get_ident()}>")
    #
    # bot_process = multiprocessing.Process(target=start_bot)
    #
    # bot_process.start()
    # bot_process.is_alive()
