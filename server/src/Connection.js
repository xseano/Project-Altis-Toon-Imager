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
        this.dnaResp.status(200).send(b64String);
        console.log('Got b64 string successfully!');
    }

    handleDNA(dna)
    {
        Logger.debug(`Got DNA string: ${dna}`);
        this.packetHandler.reqToonData(dna);
    }

    onDNARequest(req, res)
    {
        switch(req.method)
        {
            case 'OPTIONS':

              var headers = {};
              headers["Access-Control-Allow-Origin"] = "*";
              headers["Access-Control-Allow-Methods"] = "POST, GET, PUT, DELETE, OPTIONS";
              headers["Access-Control-Allow-Credentials"] = false;
              headers["Access-Control-Max-Age"] = '86400'; // 24 hours
              headers["Access-Control-Allow-Headers"] = "X-Requested-With, X-HTTP-Method-Override, Content-Type, Accept";
              res.writeHead(200, headers);
              res.end();
              break;

            case 'POST':

              var dnas = String(req.body.dna);

              if (dnas != 'undefined')
              {
                this.handleDNA(dnas);
                this.dnaResp = res;
              }

              break;

            default:
              break;
        }
    }

    onB64Request(req, res)
    {
        switch(req.method)
        {
            case 'OPTIONS':

              var headers = {};
              headers["Access-Control-Allow-Origin"] = "*";
              headers["Access-Control-Allow-Methods"] = "POST, GET, PUT, DELETE, OPTIONS";
              headers["Access-Control-Allow-Credentials"] = false;
              headers["Access-Control-Max-Age"] = '86400'; // 24 hours
              headers["Access-Control-Allow-Headers"] = "X-Requested-With, X-HTTP-Method-Override, Content-Type, Accept";
              res.writeHead(200, headers);
              res.end();
              break;

            case 'POST':

              var b64s = String(req.body.b64);

              if (b64s != 'undefined')
              {
                this.handleB64(b64s);
              }

              break;

            default:
              break;
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
