import select
import psycopg2
import psycopg2.extensions
import websockets
import asyncio
import json

async def signal():
    async with websockets.connect("ws://localhost:8001") as websocket:
        signal = {"fetch_db": True}
        await websocket.send(json.dumps(signal))
        
conn = psycopg2.connect(dbname="main", user="ilmos", password="ilmos3131")
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

curs = conn.cursor()
curs.execute("LISTEN test;")

print("Waiting for notifications on channel 'test'")
while True:
    if select.select([conn],[],[],5) == ([],[],[]):
        print("Timeout")
    else:
        conn.poll()
        while conn.notifies:
            notify = conn.notifies.pop(0)
            # asyncio.run(signal())
            print("Got NOTIFY:", notify.pid, notify.channel, notify.payload)
