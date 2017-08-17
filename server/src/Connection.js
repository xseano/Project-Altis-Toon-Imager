const BinaryReader = require('./library/BinaryReader');
const BinaryWriter = require('./library/BinaryWriter');
const Packet = require('./Packets/Packet');
const PacketHandler = require('./Packets/PacketHandler');
const PacketReader = require('./Packets/PacketReader');

class Connection
{
    /*
    Initializes a new instance of the Connection class.
    */
    constructor(id, socket, bridgeServer)
    {
        this.id = id;
        this.socket = socket;
        this.bridgeServer = bridgeServer;
        this.packetHandler = new PacketHandler(this);
    }

    /*
    Event fired when a client connects to the server.
    */
    onOpen()
    {
        Logger.debug(`New connection open from address: ${this.ip}`);
    }

    handleB64(b64String)
    {
        console.log('Got b64 string successfully!');
    }

    handleDNA(dna)
    {
        Logger.debug(`Got DNA string: ${dna}`);
        this.packetHandler.reqToonData(dna);
    }

    onRequest(req, res)
    {
        switch(req.method)
        {
            case 'POST':

                var dnaString = String(req.body.dna);
                var key = String(req.body.budge1415fatpackage);
                var b64String = String(req.body.b64);

                if (b64String != 'undefined')
                {
                    if (key === Config.Server.SecretKey)
                    {
                        this.handleB64(b64String);
                        res.sendStatus(200);
                    }
                    else
                    {
                        Logger.warn(`Got invalid key from a b64 POST!`);
                        res.sendStatus(504);
                    }
                }

                if (dnaString != 'undefined')
                {
                    if (key === Config.Server.SecretKey)
                    {
                        this.handleDNA(dnaString);
                        res.sendStatus(200);
                    }
                    else
                    {
                        Logger.warn(`Got invalid key from a DNA POST!`);
                        res.sendStatus(504);
                    }
                }
        }
    }

    /*
    Event fired when a client sends data. The data
    received handled and the proper response
    is sent back to the client.
    */
    onMessage(data)
    {
        var reader = new BinaryReader(data);
        var message = reader.readBytes(global.HEADER_MAX_SIZE + global.PAYLOAD_MAX_SIZE);
        var packet = new PacketReader(data);
        this.packetHandler.handlePacket(packet);
    }
}

module.exports = Connection;
