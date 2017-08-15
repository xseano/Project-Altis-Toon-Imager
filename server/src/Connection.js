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
    Connects to the MySQL server, and sends the client their PID.
    */
    onOpen()
    {
        var self = this;
        this.bridgeServer.app.all('*',
            function(req, res)
            {
                res.header('Access-Control-Allow-Origin', '*');
                res.header('Access-Control-Allow-Methods', 'POST');
                res.header('Access-Control-Allow-Headers', 'Content-type');

                switch(req.method)
                {
                    case 'POST':
                        var dnaString = String(req.body.dna);

                        if (dnaString)
                        {
                            res.sendStatus(200);
                            Logger.debug(`Got DNA string: ${dnaString}`);
                            self.packetHandler.reqToonData(dnaString);
                        }

                }
            }
        );
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
