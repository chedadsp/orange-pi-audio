import socket


class UDPSender(object):

    def __init__(self):
        self.server_ip = "255.255.255.255"
        self.udp_port = 5005

    def starting_server_message(self):
        self.send_message("Start")

    def send_message(self, message):
        sock = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(message.encode(), (self.server_ip, self.udp_port))
        sock.close()

    def stopping_server_message(self):
        self.send_message("Stop")
