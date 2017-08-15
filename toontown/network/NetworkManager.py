import os, sys, time, json, websocket, threading
from direct.showbase import DirectObject
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
import NetworkGlobals

class NetworkManager(DirectObject.DirectObject, threading.Thread):
    notify = DirectNotifyGlobal.directNotify.newCategory('NetworkManager')

    def __init__(self, url):
        threading.Thread.__init__(self)

        self.url = url
        self.lastHeartbeat = 0

        # WebSocket Stuff
        websocket.enableTrace(False)  # We do not want this set to True; it fills up the terminal.
        self.interface = websocket.WebSocketApp(self.url)
        self.interface.on_open = self.on_open
        self.interface.on_message = self.on_message
        self.interface.on_close = self.on_close

        # WS Thread
        self.thread = threading.Thread(target=self.interface.run_forever)
        self.thread.daemon = True

        # Main Thread
        self.start()

    def craft_header(self, header):
        return header

    def craft_payload(self, payload):
        i = len(payload)
        newPayload = payload
        while i < 250:
            if i >= len(payload):
                payload += "\x00"
            else:
                if payload[i] is not "\x00":
                    newPayload += "\x00"
            i += 1
        return payload

    def send_data(self, header, payload):
        print payload
        self.interface.send(self.craft_header(header) + self.craft_payload(str(payload)))

    def get_header(self, data):
        header = ""
        for x in range(0, 6):
            header += data[x]
        return header

    def print_packet(self, packet):
        print ('Header: %s' % (self.get_header(packet)))
        print ('Payload: %s' % (self.get_payload(packet)))

    def get_payload(self, data):
        # Read the next 250 bytes after the header, because the max header is 6 bytes and the max payload is 250 bytes
        payload = ""
        for x in range(6, 250 + 6):
            if ord(data[x]) is not 0:  # Comparing the ascii code of the data to ascii nul
                payload += str(data[x])
        return payload

    def on_message(self, ws, data):
        self.print_packet(data)
        header = self.get_header(data)
        payload = self.get_payload(data)
        self.handle_packet(header, payload)

    def on_error(self, ws, error):
        print error

    def on_close(self, ws):
        self.notify.warning("Disconnected from the server!")
        sys.exit(0)

    def on_open(self, ws):
        self.notify.warning("Connection Opened")

    def connectToLogin(self, serverList, successCallback=None, successArgs=[], failureCallback=None, failureArgs=[]):
        self.successCallback, self.successArgs = successCallback, successArgs
        self.failureCallback, self.failureArgs = failureCallback, failureArgs
        self.notify.warning('Attempting Connection...')
        self.notify.warning("Running forever")
        self.thread.start()

    def handle_packet(self, header, payload):
        if header == NetworkGlobals.RequestToonData:
            print "The server is requesting toon data..."
            print json.loads(payload)
        else:
            print "The server provided invalid or unknown header!"
