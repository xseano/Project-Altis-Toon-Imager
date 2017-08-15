const Packet = require('./Packet');

class PacketReader extends Packet
{

    /*
    Initializes a new instance of the PacketReader class.
    */
    constructor(data)
    {
        var header = "";
        var payload = "";

        for(var i = 0; i < global.HEADER_MAX_SIZE; i++)
        {
            header += data[i];
        }

        for(var i = global.HEADER_MAX_SIZE; i < global.HEADER_MAX_SIZE + global.PAYLOAD_MAX_SIZE; i++)
        {
            payload += data[i];
        }

        super(header, payload);
    }
}

module.exports = PacketReader;
