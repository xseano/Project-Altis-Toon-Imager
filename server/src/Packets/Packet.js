const BinaryWriter = require ('../library/BinaryWriter');

class Packet
{
    /*
    Initializes a new instance of the Packet class.
    */
    constructor(header, payload)
    {
        this.header = header;
        this.payload = payload;
        if(this.header.length > global.HEADER_MAX_SIZE)
        {
            Logger.warn(`The length of the header must be less than ${global.HEADER_MAX_SIZE}`)
        }

        if(this.payload.length > global.PAYLOAD_MAX_SIZE)
        {
            Logger.warn(`The length of the payload must be less than ${global.PAYLOAD_MAX_SIZE}`)
        }
    }

    /*
    Returns this packet instance into a byte array.
    */
    toByteArray()
    {
        var byteArr = this.toCharArray();
        for(var i = 0; i < byteArr.length; i++)
        {
            byteArr[i] = writer.writeUint8(byteArr[i]);
        }

        while(byteArr.length < global.PAYLOAD_MAX_SIZE)
        {
                byteArr.push('\u0000');
        }
        return byteArr;
    }

    /*
    Returns this packet instance into a char array.
    */
    toCharArray()
    {
        var charArr = [];
        var writer = new BinaryWriter();

        for(var i = 0; i < this.header.length; i++)
        {
            charArr.push(header.charCodeAt(i));
        }

        for(var i = 0; i < this.payload.length; i++)
        {
            charArr.push(payload.charCodeAt(i));
        }

        return charArr;
    }

    /*
    Returns this packet instance into a string
    */
    toString()
    {
        return this.header + this.payload;
    }

    /*
    Prints this packet as a byte array.
    */
    printByteArray()
    {
        Logger.debug(toByteArray().toString());
    }

    /*
    Prints this packet as a char array.
    */
    printCharArray()
    {
        Logger.debug(toCharArray().toString());
    }

    /*
    Adds null bytes to the end of the payload if necessary
    */
    fillPayload()
    {
        for(var i = 0; i < global.PAYLOAD_MAX_SIZE; i++)
        {
            if (this.payload.charCodeAt(i) != "\u0000")
            {
                this.payload += "\u0000"
            }
        }
    }
}

module.exports = Packet;
