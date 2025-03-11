import asyncio
import multiprocessing

import websockets

from gbf_automata.models.gbf_manager import (
    CombatStatus,
    ConnectionStatus,
    RenderStatus,
    ResultStatus,
    StatusManager,
)
from gbf_automata.models.message import Message, MessageAction, MessageType
from gbf_automata.util.logger import get_logger
from gbf_automata.util.settings import settings

logger = get_logger()


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
        logger.info(f"[SERVER] New client connected: {client_ip}:{client_port}")

        self.status_manager.set_connection_status(ConnectionStatus.CONNECTED)

        try:
            async for message in websocket:
                logger.debug(f"[SERVER] Client message: {message}")

                if message == "none":
                    self.status_manager.set_render_status(RenderStatus.PENDING)

                if message == "block":
                    self.status_manager.set_render_status(RenderStatus.RENDERED)

                if message == "display-on":
                    self.status_manager.set_combat_status(CombatStatus.STOPPED)

                if message == "display-off":
                    self.status_manager.set_combat_status(CombatStatus.STARTED)

                if message == "end-battle":
                    self.status_manager.set_combat_status(CombatStatus.ENDED)

                if message == "content-result":
                    self.status_manager.set_result_status(ResultStatus.AVAILABLE)

        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            logger.info(f"[SERVER] Client disconnected: {client_ip}:{client_port}")
            if websocket in self.clients:
                self.clients.remove(websocket)

    async def start_server(self):
        self.server = await websockets.serve(
            self.handler, settings.server.host, settings.server.port
        )
        logger.info(
            f"[SERVER] WebSocket Server started on ws://{settings.server.host}:{settings.server.port}"
        )

    async def fsm_incoming_messages(self):
        while not self.stop_event.is_set():
            message: Message = await asyncio.to_thread(self.message_queue.get)

            logger.debug(f"[SERVER] Queue message: {message}")

            if (
                message.message_type == MessageType.INTERNAL
                and message.message_action == MessageAction.STOP
            ):
                logger.info(
                    "[SERVER] Stop event detected, shutting down WebSocket Server..."
                )
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
            logger.info("[SERVER] Shutting down server...")
        finally:
            self.stop_event.set()
            if self.server:
                self.server.close()
                await self.server.wait_closed()
                logger.info("[SERVER] WebSocket Server closed.")
