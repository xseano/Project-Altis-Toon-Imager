const PacketGlobals = require('./PacketGlobals');
const PacketWriter = require('./PacketWriter');
const PacketReader = require('./PacketReader');
class PacketHandler
{
    /*
    Initializes a new instance of the PacketHandler class.
    */
    constructor(parentConnection)
    {
        this.id = parentConnection.id;
        this.socket = parentConnection.socket;
        this.bridgeServer = parentConnection.bridgeServer;
        this.isAuthenticated = false;
        this.packetGlobals = new PacketGlobals();
    }

    handlePacket(packet)
    {
        if(this.bridgeServer.wantDebug == true)
        {
            TTLogger.debugPacket(this.unm, packet.header, packet.payload);
        }

        if (packet.header === this.packetGlobals.RecieveToonData)
        {
            var payload = this.cleanPayload(packet.payload)
            var b64String = payload;

            console.log(JSON.parse(payload))

            //Logger.debug(`Got b64 string: ${tpeb64String}`)
        }

    }

    /*
    Removes null bytes from a payload.
    Returns payload free of null bytes.
    */
    cleanPayload(payload)
    {
        return payload.replace(/\u0000/g, '');
    }

    ping()
    {
      this.sendPacket('dCUCAgEAGwIbEBtxcXFxcXHhP1FRUVFRUdE/ExMTExMTsz8AAAAAAADwPwAAAAAAAPA/AAAAAAAA8D9xcXFxcXHhP1FRUVFRUdE/ExMTExMTsz9xcXFxcXHhP1FRUVFRUdE/ExMTExMTsz8=');
    }

    /* Requests Toon Data */
    reqToonData(dnaString)
    {
        this.sendPacket(dnaString);
    }

    /*
    Sends a packet to the current socket connection.
    */
    sendPacket(packet)
    {
        if (this.socket && this.socket.readyState == 1)
        {
            this.socket.send(packet);
        }
    }
}

module.exports = PacketHandler;
