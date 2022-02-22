# Simple Python Sniffer (Raw) for Single Packet

import socket
import os

# Define lhost.
HOST = '[IP ADDRESS HERE]'

def main():
    # Create raw socket, bind to public interface
    if os.name == 'nt':
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP

    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    sniffer.bind((HOST, 0))

    # Include IP header in capture w/ IP_HDRINCL and receive single packet
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    
# Uncomment next two lines if Win environment.
    # If Windows, send IOCTL to NIC driver to enable promiscuity.
    #if os.name == 'nt':
        #sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    # Print entire raw packet.
    print(sniffer.recvfrom(65565)) 

    # If Win, turn off promiscuous mode.
    #if os.name == 'nt':
        #sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

if __name__ == '__main__':
    main()