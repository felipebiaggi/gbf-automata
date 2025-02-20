import asyncio
import multiprocessing

import websockets

from gbf_automata.models.render_manager import (
    RenderStatus,
    RenderStatusManager,
)


class GBFAutomataServer:
    def __init__(
        self,
        send_queue: multiprocessing.Queue,
        receive_queue: multiprocessing.Queue,
        render_status_manager: RenderStatusManager,
    ) -> None:
        self.send_queue: multiprocessing.Queue = send_queue
        self.receive_queue: multiprocessing.Queue = receive_queue
        self.render_status_manager: RenderStatusManager = render_status_manager
        self.server = None
        self.clients = set()
        self.running = True
        self.stop_event = asyncio.Event()

    async def handler(self, websocket, path):
        client_ip, client_port = websocket.remote_address
        self.clients.add(websocket)
        print(f"[+] New client connected: {client_ip}:{client_port}")
        try:
            async for message in websocket:
                if message == "none":
                    self.render_status_manager.set_status(RenderStatus.RENDERED)

                if message == "block":
                    self.render_status_manager.set_status(RenderStatus.PENDING)

                self.send_queue.put(f"ClientMessage: {message}")
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            print(f"[-] Client disconnected: {client_ip}:{client_port}")
            if websocket in self.clients:
                self.clients.remove(websocket)

    async def start_server(self):
        self.server = await websockets.serve(self.handler, "127.0.0.1", 12000)
        print("[SERVER] WebSocket Server started on ws://127.0.0.1:12000")

    async def process_incoming_messages(self):
        while not self.stop_event.is_set():
            message = await asyncio.to_thread(self.receive_queue.get)

            print(f"FSM Message {message}")

            if message == "STOP":
                print("[!] Stop event detected, shutting down WebSocket Server...")
                self.stop_event.set()

                for client in self.clients:
                    await client.close()

                self.clients.clear()

                if self.server:
                    self.server.close()
                    await self.server.wait_closed()
                break

            if self.clients:
                await asyncio.gather(*[client.send(message) for client in self.clients])

    async def run(self):
        await self.start_server()

        try:
            await asyncio.gather(
                self.stop_event.wait(), self.process_incoming_messages()
            )

        except asyncio.CancelledError:
            pass
        except KeyboardInterrupt:
            print("[!] Shutting down server...")
        finally:
            if self.server:
                self.server.close()
                await self.server.wait_closed()
                print("[X] WebSocket Server closed.")
