# Toon Imager
- This project provides the core system and middleware used by the webserver to request, generate, and recieve back an image of toon based on their DNA string.

## Pseudo-Code
1. POST JSON data containing a key for authentication and the DNA string
2. NodeJS Express server to recieve and parse the JSON
3. Checks if the DNA string is valid
4. Checks if the key is correct
5. Using WebSockets, sends a packet requesting toon data, with a payload containing DNA string
6. Game server recieves and uses DNA string to get the b64 string of the toon snapshot
7. Game server POSTS back a JSON object with the authentication key as well as the large b64 string
8. The NodeJS server parses and reads the b64 string and serves it as the response to the original POST request
9. WebServer serves the Toon Image to the end user

## Setup
 - This requires [Node.js](https://nodejs.org/) v7+ to run.
 - You will need Panda3D 1.10 to run these BAM files
 - (NOTE) The Engine only loads all resources up to Phase_5

Install the dependencies and start the server.

```sh
$ git clone https://github.com/xseano/ToonImager.git ToonImager
$ cd ToonImager/toontown
$ git clone https://github.com/xseano/ToonImagerResources.git resources
$ cd ../server
$ npm install yarn --g
$ yarn install .
$ cd ../toontown
$ ppython -m pip install websocket-client
```

## Running
```sh
$ cd toontown
$ ppython NetworkManager.py
$ cd ../server
$ sudo sh start.sh
```

### Sending Data

Using Postman or Curl, you must post a JSON object with the key and DNA string
```json
{
    "dna": "{DNASTRING}",
    "budge1415fatpackage":"{SECRETKEY}"
}
```

In example:
```json
{
    "dna": "t\\x01\\x01\\x01\\x01\\x56\\x03\\x4b\\x03\\x24\\x1d\\x14\\x00\\x14\\x14",
    "budge1415fatpackage": "lbChFkf0hgGyGE4ltKgElACjBfvot0CrhgxBu65fjgipC56sWGiOkAlX1RqQcmKKntY7D4dFEdazUDmTaVmrYCagmSWgLFEnnCVC"
}
```

### Credits
| Name | Feature |
| ------ | ------ |
| Tessler | Server and Engine Development |
| Liam | Engine Development |
| Judge2020 | Server Development |
