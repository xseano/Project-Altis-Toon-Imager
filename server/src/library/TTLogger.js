class TTLogger
{
    constructor()
    {

    }

    debugPacket(client, header, payload)
    {
        Logger.debug(`Client ${client} sent a packet:`);
        Logger.debug(`\tHeader: ${header}`);
        Logger.debug(`\tPayload: ${payload}`);
    }
}

module.exports = TTLogger;
