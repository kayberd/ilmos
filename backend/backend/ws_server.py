import websockets
import asyncio
import json

async def handler(ws):
    """
    while True:
        try:
            data = await ws.recv()
        except websockets.ConnectionClosedOK:
            break
        print(data)
    """
    async for msg in ws:
        print(msg)
        data = json.loads(msg)

        if data.__contains__("fetch_db"):
            if data["fetch_db"] is True:
                print("Database fetched from server")
async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    asyncio.run(main())
