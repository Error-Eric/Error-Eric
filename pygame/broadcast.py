# udp_gb_server.py

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

PORT = 1060

network = '<broadcast>'
s.sendto('cute dnn'.encode('utf-8'), (network, PORT))