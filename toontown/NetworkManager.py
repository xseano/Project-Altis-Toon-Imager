import websocket, time, sys, requests, json, base64
import NetworkGlobals
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
    print (payload)
    ws.send(craft_header(header) + craft_payload(str(payload)))

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
    print (error)

def on_close(ws):
    print ("Disconnected from the server!")
    sys.exit(0)

def on_open(ws):
    print ("Connection Opened")

def handle_packet(header, payload):
    if header == NetworkGlobals.RequestToonData:
        print ("The server is requesting toon data...")

        Toon = ToonView(base64.b64decode(payload))
        Toon.run()

        if Toon.b64String:
            sendToonData(Toon.b64String)
    else:
        print ("The server provided invalid or unknown header!")

def sendToonData(b64String):
    url = "http://localhost:2052"
    b64 = str(b64String)
    payload = { "b64" : b64, "budge1415fatpackage": NetworkGlobals.SecretKey }
    requests.post(url, json=payload)

if __name__ == "__main__":
    ws = websocket.WebSocketApp("ws://127.0.0.1:2052",
                                on_open = on_open,
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)

    websocket.enableTrace(True)

    ws.run_forever()
