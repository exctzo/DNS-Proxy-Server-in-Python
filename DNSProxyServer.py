import socket
import sys
import struct
from binascii import hexlify
from threading import Thread

# send a TCP DNS query to the upstream DNS server
def sendTCP(DNSserverIP, query):
    server = (DNSserverIP, 53)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server)

    # convert the UDP DNS query to the TCP DNS query
    pay = chr(len(query))
    tcp_query = b'\x00' + pay.encode() + query

    sock.send(tcp_query)  	
    data = sock.recv(1024)
    return data

# a new thread to handle the UPD DNS request to TCP DNS request
def handler(data, addr, socket, DNSserverIP):
    TCPanswer = sendTCP(DNSserverIP, data)
    UDPanswer = TCPanswer[2:]
    socket.sendto(UDPanswer, addr)


if __name__ == '__main__':
    DNSserverIP = sys.argv[1]
    port = int(sys.argv[2])
    host = ''
    try:
        # setup a UDP server to get the UDP DNS request
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((host, port))
        
        while True:
            data, addr = sock.recvfrom(1024)
            th = Thread(target=handler, args=(data, addr, sock, DNSserverIP))
            th.start()
    except Exception as err:
        print(err)
        sock.close()
