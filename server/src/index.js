// Global Deps
global.Config   = require('./config.json');
global.readline = require('readline');
global.rl       = readline.createInterface({
    input:  process.stdin,
    output: process.stdout
});

global.Logger   = require('./library/Logger');
global.Colors   = require('colors');
global.HEADER_MAX_SIZE = 6;
global.PAYLOAD_MAX_SIZE = 250;

const tLogger = require('./library/TTLogger')
global.TTLogger = new tLogger();
Logger.print("Loading Dependencies...".green.dim);

// Start deps
Logger.start();

// Main Game Server
var BridgeServer = require('./BridgeServer')
var server = new BridgeServer();
server.start();

// Error handling
process.on('uncaughtException', (error) => Logger.error(error));
