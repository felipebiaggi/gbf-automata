import asyncio

import websockets


class GBFAutomataServer:
    def __init__(self, send_queue, receive_queue) -> None:
        self.send_queue = send_queue
        self.receive_queue = receive_queue
        self.server = None
        self.clients = set()
        self.running = True

    async def handler(self, websocket, path):
        """Gerencia conexões WebSocket"""
        client_ip, client_port = websocket.remote_address
        self.clients.add(websocket)

        self.send_queue.put(f"Client {client_ip}:{client_port} connected")

        try:
            async for message in websocket:
                self.send_queue.put(
                    f"ClientMessage: {message}"
                )  # Envia mensagem ao processo pesado
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            print(f"❌ Client disconnected: {client_ip}:{client_port}")
            self.clients.remove(websocket)  # Remove cliente da lista

    async def start_server(self):
        self.server = await websockets.serve(self.handler, "127.0.0.1", 12666)
        print("🚀 WebSocket Server started on ws://127.0.0.1:12666")

    async def process_incoming_messages(self):
        """Escuta mensagens do processo pesado e as envia para os clientes"""
        while True:
            message = self.receive_queue.get()  # Bloqueia até receber uma mensagem
            print(f"⚙️ Heavy CPU process sent: {message}")

            # Envia mensagem para todos os clientes conectados
            if self.clients:
                await asyncio.gather(*[client.send(message) for client in self.clients])

    async def run(self):
        await self.start_server()

        try:
            await asyncio.Future()

            # await asyncio.gather(
            #     self.process_incoming_messages(),
            #     asyncio.Future(),  # Mantém o servidor rodando
            # )
        except asyncio.CancelledError:
            pass
        except KeyboardInterrupt:
            print("🔴 Shutting down server...")
        finally:
            if self.server:
                self.server.close()
                await self.server.wait_closed()
                print("🛑 WebSocket Server closed.")
