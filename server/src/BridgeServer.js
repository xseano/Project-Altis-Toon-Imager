const os = require('os');

if (Config.Server.UWS === true)
{
    var WebSocket = require('uws');
}
else
{
    var WebSocket = require('ws');
}

const Connection = require('./Connection');
const gameloop = require('node-gameloop');
const Commands = require('./Commands');

class BridgeServer
{
    /*
    Initializes a new instance of the BridgeServer class
    */

    constructor()
    {
        // Game Variables
        this.id = 0;
        this.clients = [];
        this.players = [];
        this.tick = 0;
        this.extraTick = 0;
        this.token = Config.Server.Token;
        this.maxConn = Config.Server.MaxConnections;
        this.devEnv = Config.Server.DevEnv; // Set this true only in a development setting
        this.wantDebug = Config.Server.WantDebug; // Set to true for packet debugging, etc.

        // Useful
        this.commands = new Commands(this);

        // Other
        Logger.print(`TTPA Image Bridge Server <Build ${Config.Version}>`.green.bold);
    }

    /*
    Starts the Game Server.
    */
    start()
    {
        // perMessageDeflate lags server and is enabled by default, HAS TO BE DISABLED
        var wss = this.wss = new WebSocket.Server({port: Config.Server.Port, perMessageDeflate: false}, this.onOpen.bind(this));

        wss.on('connection', this.onConnect.bind(this));

        // Logger
        Logger.prompt(this.commands.handleCommand.bind(this.commands), Config.Logger.Prompt);

        // Good solution for minimal CPU usage
        this.loop = gameloop.setGameLoop(this.gameLoop.bind(this), Config.Server.Tick);

        // System info debug
        Logger.info(`OS: ${os.platform()}`);
        Logger.info(`CPU: ${os.cpus()[0]["model"]}`);

        Logger.info(`Gameloop running at ${Config.Server.Tick} ms/tick`);
    }

    onOpen()
    {
        Logger.info(`Socket open on port: ${Config.Server.Port}`);
        Logger.info(`Took ${process.uptime()} seconds to start`);
        Logger.info(`Type 'help' or '?' for commands \n`)
    }

    onConnect(socket)
    {
        if (Config.Server.UWS === true)
        {
            var connectionIP = socket._socket.remoteAddress;
        }
        else
        {
            var connectionIP = socket.upgradeReq.connection.remoteAddress;
        }

        if (this.ipQuery(connectionIP) < this.maxConn)
        {
            var id = this.getNextID();
            var conn = new Connection(id, socket, this);
            conn.ip = connectionIP;
            var self = this;

            this.onClose = () =>
            {
                sqlConn.end(
                    function(err)
                    {
                        Logger.warn(`Socket connection disconnected!`);
                    }
                );
            }

            socket.on('message', conn.onMessage.bind(conn));
            socket.on('close', this.onClose);
            socket.on('error', this.onError);

            conn.onOpen();
            this.clients.push(conn);
        }
        else
        {
            socket.close();
            Logger.warn(`${connectionIP} already has ${this.maxConn} existing connection${this.isPlural()}`);
        }
    }

    /* Error Handling */
    onError(err)
    {
        console.log(err);
    }

    /*
    Returns true if the server has more than
    one maximum connections allowed.
    */
    isPlural()
    {
        if (this.maxConn > 1)
        {
            return 's'
        }
        else
        {
            return ''
        }
    }

    gameLoop(delta)
    {
        if (this.tick >= 10)
        {
            this.tick = 0;
        }

        this.tick++;
    }

    /*
    Returns true if there is more than one client
    with the same IP Address.
    */
    ipQuery(ip)
    {
        return (
            this.clients.filter(
                client =>
                    client.ip === ip
            )
        ).length;
    }

    /*
    Returns the next available client ID.
    */
    getNextID()
    {
        if (this.id >= Number.MAX_SAFE_INTEGER - 1)
        {
            this.id = 0;
        }

        return this.id++;
    }
}

module.exports = BridgeServer;
