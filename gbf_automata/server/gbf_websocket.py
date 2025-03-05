import asyncio
import multiprocessing

import websockets

from gbf_automata.models.gbf_manager import (
    CombatStatus,
    ConnectionStatus,
    RenderStatus,
    StatusManager,
)
from gbf_automata.models.message import Message, MessageAction, MessageType


class GBFAutomataServer:
    def __init__(
        self,
        message_queue: multiprocessing.Queue,
        render_status_manager: StatusManager,
    ) -> None:
        self.message_queue: multiprocessing.Queue = message_queue
        self.status_manager: StatusManager = render_status_manager
        self.server = None
        self.clients = set()
        self.running = True
        self.stop_event = asyncio.Event()

    async def handler(self, websocket, path):
        client_ip, client_port = websocket.remote_address
        self.clients.add(websocket)
        print(f"[+] New client connected: {client_ip}:{client_port}")

        self.status_manager.set_connection_status(ConnectionStatus.CONNECTED)

        try:
            async for message in websocket:
                print(message)
                if message == "none":
                    self.status_manager.set_render_status(RenderStatus.RENDERED)

                if message == "block":
                    self.status_manager.set_render_status(RenderStatus.PENDING)

                if message == "display-on":
                    self.status_manager.set_combat_status(CombatStatus.STOPPED)

                if message == "display-off":
                    self.status_manager.set_combat_status(CombatStatus.STARTED)

                if message == "end-battle":
                    self.status_manager.set_combat_status(CombatStatus.ENDED)

        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            print(f"[-] Client disconnected: {client_ip}:{client_port}")
            if websocket in self.clients:
                self.clients.remove(websocket)

    async def start_server(self):
        self.server = await websockets.serve(self.handler, "127.0.0.1", 12000)
        print("[SERVER] WebSocket Server started on ws://127.0.0.1:12000")

    async def fsm_incoming_messages(self):
        while not self.stop_event.is_set():
            message: Message = await asyncio.to_thread(self.message_queue.get)

            print(f"FSM Message {message}")

            if (
                message.message_type == MessageType.INTERNAL
                and message.message_action == MessageAction.STOP
            ):
                print("[!] Stop event detected, shutting down WebSocket Server...")
                self.stop_event.set()

                for client in self.clients:
                    await client.close()

                self.clients.clear()

                if self.server:
                    self.server.close()
                    await self.server.wait_closed()
                break

            if message.message_type == MessageType.EXTERNAL:
                if self.clients:
                    await asyncio.gather(
                        *[
                            client.send(message.model_dump_json())
                            for client in self.clients
                        ]
                    )

    async def run(self):
        await self.start_server()

        try:
            await asyncio.gather(self.stop_event.wait(), self.fsm_incoming_messages())

        except asyncio.CancelledError:
            pass
        except KeyboardInterrupt:
            print("[!] Shutting down server...")
        finally:
            if self.server:
                self.server.close()
                await self.server.wait_closed()
                print("[X] WebSocket Server closed.")
