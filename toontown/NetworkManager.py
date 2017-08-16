import websocket
import thread
import time
import sys
import NetworkGlobals
import ast
from Base import ToonView

def craft_header(header):
    return header

def craft_payload(payload):
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

def send_data(header, payload):
    print payload
    interface.send(craft_header(header) + craft_payload(str(payload)))

def get_header(data):
    header = ""
    for x in range(0, 6):
        header += data[x]
    return header

def print_packet(packet):
    print ('Header: %s' % (get_header(packet)))
    print ('Payload: %s' % (get_payload(packet)))

def get_payload(data):
    # Read the next 250 bytes after the header, because the max header is 6 bytes and the max payload is 250 bytes
    payload = ""
    for x in range(6, 250 + 6):
        if ord(data[x]) is not 0:  # Comparing the ascii code of the data to ascii nul
            payload += str(data[x])
    return payload

def on_message(ws, data):
    print_packet(data)
    header = get_header(data)
    payload = get_payload(data)
    handle_packet(header, payload)

def on_error(ws, error):
    print error

def on_close(ws):
    print ("Disconnected from the server!")
    sys.exit(0)

def on_open(ws):
    print ("Connection Opened")

def startConnection(self):
    print ('Attempting Connection...')
    print ("Running forever")
    thread.start()

def handle_packet(header, payload):
    if header == NetworkGlobals.RequestToonData:
        print "The server is requesting toon data..."

        str = payload[1:]
        dnaString = "t"
        for x in str.split("\\x"):
            if x != '':
                dnaString += chr(int(x, 16))

        Toon = ToonView()
        Toon.loadModels()
        Toon.displayDNA(dnaString)
        Toon.run()
        Toon.kill()



    else:
        print "The server provided invalid or unknown header!"

if __name__ == "__main__":
    ws = websocket.WebSocketApp("ws://127.0.0.1:777",
                                on_open = on_open,
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)

    websocket.enableTrace(True)

    ws.run_forever()
