# udp_gb_client.py

import socket
import lan_util
import select

class client:

    PORT = 4322
    BPORT = 4321

    def newsocket(kind = "TCP", ip = '', port = 0):
        sty = socket.SOCK_STREAM if kind == "TCP" else socket.SOCK_DGRAM
        ret = socket.socket(socket.AF_INET, sty)
        try: ret.bind((ip, port))
        except: ret.bind((ip, 0)); print("???")
        ip, port = ret.getsockname()
        print(f"New {kind} created on {ip},{port}.")
        return ret

    def __init__(self):
        self.decsock = client.newsocket("UDP", port= client.PORT)
        self.tcp = None
        self.udp = client.newsocket("UDP")
        self.available = []
    
    def listen(self):
        while True:
            data, addr = self.decsock.recvfrom(65535)
            sinfo = lan_util.unpackinfo(data)
            print(sinfo)
            return sinfo
            
    def connect_server(self, tcpport : int, udpport : int, ip = "localhost"):
        print(f"connecting {ip}({tcpport},{udpport})...")
        try:
            self.s_tcpaddr = (ip, tcpport)
            self.s_udpaddr = (ip, udpport)
            self.tcp = socket.create_connection(ip, tcpport)
        except:
            print("Connection failed!")
    
    def __del__(self):
        try: self.tcp.close() ; print("TCP closed")
        except: print("TCP already closed.")
        try: self.udp.close() ; print("UDP closed")
        except: print("UDP already closed.")
        try: self.decsock.close() ; print("Decsock closed")
        except: print("Decsock already closed.")

if __name__ == "__main__":
    curclient = client()
    print(curclient.listen())


"""         
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

PORT = 4322

s.bind(('', PORT))
print('Listening for broadcast at ', s.getsockname())

while True:
    data, address = s.recvfrom(65535)
    data = data.decode().split('::')
    
    print('Server received from {}:{}'.format(address, data))
"""