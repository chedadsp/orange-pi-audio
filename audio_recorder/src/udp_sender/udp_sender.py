"""
Created on Jan 10, 2019

@author: Nebojsa
"""
import socket
from uuid import getnode
from time import sleep
import threading


class UDPSender(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.is_running = True
        self.server_ip = "255.255.255.255"
        # On windows (depend on local network)
        # self.server_ip = "local.network.number.255"
        self.udp_port = 5005
        self.mac_address = ':'.join(("%012X" % getnode())[i:i+2] for i in range(0, 12, 2))

    def run(self):
        try:
            while self.is_running:
                print("Sending message...")
                self.starting_server_message()
                sleep(1)
        except KeyboardInterrupt:
            print("You pressed Ctrl+C")

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
        self.is_running = False
