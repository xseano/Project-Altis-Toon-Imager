import websocket
import thread
import time

def on_message(ws, message):
    # printPacket(message)
    handlePacket(message)

def on_error(ws, error):
    print error

def on_close(ws):
    print "### closed ###"

def on_open(ws):
    print "Sending the server our token"
    ws.send(craftHeader("100001") + craftPayload("{\"token\": \"asdfi809gqwejfd\"}"))
    #ws.close()

def craftHeader(header):
    return header

def craftPayload(payload):
    i = 0
    while i < 250:
        if payload[i] is not None and payload[i] is not "\x00":
            payload += "\x00"
        i+=1
    return payload

def getHeader(data):
    header = ""
    for x in range(0, 6):
        header += data[x]
    return header

def getPayload(data):
    # Read the next 250 bytes after the header, because the max header is 6 bytes and the max payload is 250 bytes
    payload = ""
    for x in range(6, 250 + 6):
        if ord(data[x]) is not 0: # Comparing the ascii code of the data to ascii nul
            payload += str(data[x])
    return payload

def printPacket(packet):
    print getHeader(packet)
    print getPayload(packet)

def handlePacket(packet):
    header = getHeader(packet)
    payload = getPayload(packet)

    if(header == "100002"): # AuthenticationData code
        # do stuff with payload
        print "The server sent back authentication data"
    elif(packet == "100004"): # PirateData code
        # do stuff with payload
        print "The server sent back pirate data"

if __name__ == "__main__":
    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://127.0.0.1:777",
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open

    ws.run_forever()
