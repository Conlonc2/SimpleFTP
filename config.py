'''
File used by the server/client_config.py to read in the
configurations set
'''


class Configure:
    # Headers specific to creating connections
    server_port = 'SERVER_PORT'
    shared_direcotry = "PATH"
    server_ip = "SERVER"
    client_port = "CLIENT_PORT"
    download_path = "DOWNLOAD"
    serverConfig = "server.config"
    clientConfig = "client.config"

    def __init__(self):
        pass  # skip init

    def server_config(self):
        try:
            with open(self.serverConfig, 'r') as f:
                serPort = 0
                sharedPAth = ""
                for line in f:
                    sub = line.strip().split('=')
                    if(sub[0] == self.server_port):
                        serPort = int(sub[1])
                    elif(sub[0] == self.shared_direcotry):
                        sharedPath = sub[1]
                    else:
                        pass
                f.close()
                return serPort, sharedPath
        except Exception as e:
            print(e)

    def client_config(self):
        try:
            with open(self.clientConfig, 'r') as f:
                serPort = 0
                serName = ""
                clientPort = 0
                downPath = ""
                for l in f:
                    sub = l.strip().split("=")
                    if(sub[0] == self.server_ip):
                        serName = sub[1]
                    elif(sub[0] == self.server_port):
                        serPort = int(sub[1])
                    elif(sub[0] == self.client_port):
                        clientPort = sub[1]
                    elif(sub[0] == self.download_path):
                        downPath = sub[1]
                    else:
                        pass
                return serName, serPort, clientPort, downPath
        except Exception as e:
            print(e)


def test():
    conf = configure()
    client = conf.client_config()
    server = conf.server_config()
    print(client)
    print(server)


if (__name__ == "__main__"):
    test()
