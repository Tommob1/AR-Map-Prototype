import asyncio
import websockets

async def server(websocket, path):
    async for message in websocket:
        print(f"Received compass data: {message}")

start_server = websockets.serve(server, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()