import struct

def unpackinfo(packedinfo: bytes):
    unp = struct.unpack("<8H", packedinfo)
    ipv, ip = unp[:4] ,""
    for ix in ipv: ip += str(ix) + '.'
    return serverinfo(ip[:-1], unp[4], unp[5], unp[6], unp[7])

class serverinfo:

    def __init__(self, ip: str, tcp_p: int, udp_p: int, pcount: int, state: int):
        self.ip, self.tcp_p, self.udp_p, self.pcount, self.state = ip, tcp_p, udp_p, pcount, state

    def packself(self):
        ipv = list(map(int, self.ip.split('.')))
        return struct.pack("<8H", *ipv, self.tcp_p, self.udp_p, self.pcount, self.state)
    
