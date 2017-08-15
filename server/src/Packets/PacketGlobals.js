/*
Each packet must be the maximum packet header size.

Client sends anything that starts with request
Server sends anything that has Data in the name.
*/
class PacketGlobals
{
    constructor()
    {
        this.RequestToonData = "100001";
    }
}

module.exports = PacketGlobals;
