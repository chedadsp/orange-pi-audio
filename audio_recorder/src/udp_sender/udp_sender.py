"""
Created on Jan 10, 2019

@author: Nebojsa
"""
import socket
from uuid import getnode


class UDPSender(object):

    def __init__(self):
        self.server_ip = "255.255.255.255"
        # On windows (depend on local network)
        # self.server_ip = "local.network.number.255"
        self.udp_port = 5005
        self.mac_address = ':'.join(("%012X" % getnode())[i:i+2] for i in range(0, 12, 2))

    def send_message(self, message):
        sock = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(message.encode(), (self.server_ip, self.udp_port))
        sock.close()

    def starting_server_message(self):
        self.send_message("Start {}".format(self.mac_address))

    def stopping_server_message(self):
        self.send_message("Stop {}".format(self.mac_address))
