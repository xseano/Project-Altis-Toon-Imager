#!/usr/bin/env python

from direct.stdpy import threading
from multiprocessing import Process
import asyncio
import websockets, base64
from Base import ToonView
Toon = ToonView()

async def hello():
    async with websockets.connect('ws://localhost:777') as websocket:

        greeting = await websocket.recv()
        print("< {}".format(greeting))
        payload = base64.b64decode(greeting)
        #Toon.run()
        Toon.s(payload)
        #Toon.sb.run()
        #Toon.sb.restart()
        #Toon.sb.destroy()
        #p = Process(target=Toon.s, args=(payload,))
        #p.start()
        #t = threading.Thread(target=Toon.s(payload))
        #t.start()
        #t.stop()


asyncio.get_event_loop().run_until_complete(hello())
#asyncio.get_event_loop().run_forever()
