import asyncio
import websockets
import base64





async def hello():
    uri = "ws://localhost:9093"
    async with websockets.connect(uri) as websocket:

        await websocket.send("hello world")

        greeting = await websocket.recv()
        print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())