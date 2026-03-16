import asyncio
import json
import websockets

connected_clients = set()

async def handler(websocket):
    print("Client connected")
    connected_clients.add(websocket)

    try:
        async for message in websocket:
            print("Received:", message)

            # Broadcast message to all other clients
            for client in connected_clients:
                if client != websocket:
                    await client.send(message)

    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

    finally:
        connected_clients.remove(websocket)

async def main():
    print("Signaling server running on ws://0.0.0.0:8080")
    async with websockets.serve(handler, "0.0.0.0", 8080):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
