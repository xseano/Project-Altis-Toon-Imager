const Packet = require('./Packet');

class PacketWriter extends Packet
{
    constructor(header, payload)
    {
        super(header, payload);
        this.fillPayload();
    }
}

module.exports = PacketWriter;
