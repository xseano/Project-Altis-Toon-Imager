from NetworkManager import NetworkManager

class NetworkBase():

    def __init__(self):

        # Server to connect to - Node Server
        self.networkManager = NetworkManager('ws://127.0.0.1:777/', wantTrace=False, runForever=True, threadingDaemon=True)
