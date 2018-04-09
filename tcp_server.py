import os
import socket
import select
import time

class Tcp_server:
    
    #-------------------------------------------------------------
    def __init__(self):
        self.server = None
        self.data = None

        self.inputs = []
        self.outputs = []
        self.map = []

    #-------------------------------------------------------------
    def run(self, addr):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        self.server.bind(addr)
        self.server.listen(2)

        self.inputs = [self.server]
        self.outputs = []
        self.map = []

        while 1:
            #try:
            readable, writable, exceptional = select.select(
                self.inputs, self.outputs, self.inputs)
            #except:
                #continue

            for s in readable:
                if s is self.server:
                    client, addr = s.accept()
                    if client not in self.inputs:
                        self.inputs.append(client)
                    if client not in self.map:
                        self.map.append(client)
                    
                else:
                    for p in self.inputs:
                        print(p)
                        print('')
                    print('run end')
                    print('')
                    try:
                        self.data = s.recv(1024)
                        if self.data:
                            self.inputs.remove(s)
                            for client in self.map:
                                if client != s:
                                    self.outputs.append(client)
                    except:
                        self.remove_all(s)
            
            for s in writable:
                if self.data:
                    try:
                        s.send(self.data)
                        self.outputs.remove(s)
                    except:
                        self.remove_all(s)
                self.data = None

    #-------------------------------------------------------------
    def remove_all(self, client):
        if client in self.inputs:
            self.inputs.remove(client)
        if client in self.outputs:
            self.outputs.remove(client)
        if client in self.map:
            self.map.remove(client)
        client.close()

if __name__ == '__main__':  
    ip_local = 'localhost'
    ip = 'localhost'
    print('self run')
    tcp_server().run((ip_local,2001))














        
