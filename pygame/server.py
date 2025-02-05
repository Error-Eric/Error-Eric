import socket
import time
import datetime
import struct
import lan_util

class player:
    def validIp(argip : str) -> bool:
        fourpart = argip.split('.')
        if len(fourpart) != 4: return False
        try:
            for part in fourpart: 
                if not(0 <= int(part) <= 255) : 
                    return False
        except: return False
        return True

    def __init__(self, ip : str, pid : int, ishost = False):
        try:
            if not player.validIp(ip) : raise ValueError(f"Invalid IP address({ip}).")
            if not 1000 <= pid <= 9999: raise ValueError(f"Invalid pid({pid}), not in [1000, 9999].")
            if type(ishost) != bool: raise TypeError
        except (TypeError, AttributeError): 
            raise TypeError(f"Bad type when initializing the server{type(ip), type(pid)}.")
        
        self.ip, self.pid, self.ishost = ip, pid, ishost


"""
Server class
--------
A server class consists of three sockets. One TCP socket (self.gamesocktcp) to handle communication with client, one UDP socket for real-time communication, one UDP socket for boardcasting. The former two ports can be allocated by the OS. (Most instances I found on the internet use a port assigned by the programmer, I'm not sure if it is a good idea.) 

"""
class server:
    """Deafult BROADCAST PORT"""
    BROADCASTPORT = 4321

    """TCP or UDP. Not this method does not provide full exception check. Use it carefully."""
    def newsocket(kind = "TCP", ip = '', port = 0):
        sty = socket.SOCK_STREAM if kind == "TCP" else socket.SOCK_DGRAM
        ret = socket.socket(socket.AF_INET, sty)
        try: ret.bind((ip, port))
        except: ret.bind((ip, 0)); print("???")
        ip, port = ret.getsockname()
        print(f"New {kind} created on {ip},{port}.")
        return ret

    """ Create a server with three sockets. 0 for an ephemeral port. If no port is provided, make sure port 4321 is not occupied."""
    def __init__(self, bport = BROADCASTPORT, gtport = 0, guport = 0):
        self.plist = [] # player list is initially empty
        self.cond = "Waiting"

        self.broadcs = server.newsocket("UDP", port = bport)
        self.tcps = server.newsocket("TCP", port = gtport)
        self.udps = server.newsocket("UDP", port = guport)
        
        self.ip = socket.gethostbyname(socket.gethostname())
        self.info = lan_util.serverinfo(self.ip, self.tcps.getsockname()[1], 
                                        self.udps.getsockname()[1], len(self.plist), 0)

        self.broadcs.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST, 1)

    def __del__(self):
        self.broadcs.close()
        self.tcps.close()
        self.udps.close()
        print(f"Server is closed.")

    """Tell every other listening socket on the LAN where an server socket is open."""
    def broadcastserver(self):
        print("boardcasting")
        self.broadcs.sendto(self.info.packself(), ('<broadcast>',4322))

if __name__ == "__main__":
    curserver = server()

    while True:
        time.sleep(2)
        try: curserver.broadcastserver()
        except KeyboardInterrupt: break