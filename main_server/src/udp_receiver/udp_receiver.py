"""
Created on Jan 10, 2019

@author: Nebojsa
"""
import socket
import threading


class UDPReceiver(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.is_running = True
        self.udp_ip = ""
        self.udp_port = 5005
        self.microphones = {}

    def run(self):
        print("Listener started.")
        self.receive_message()
        print("Listener shutting down.")

    def receive_message(self):

        sock = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP
        sock.bind((self.udp_ip, self.udp_port))
        try:
            while self.is_running:
                data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
                print("received message:", data)
                print("from address:", addr)
                message = data.decode()
                if message == "Shutdown":
                    break
                split_message = message.split(" ")
                if len(split_message) == 2:

                    if split_message[0] == "Start":
                        if self.microphones.get(addr[0]) != split_message[1]:
                            print("New microphone added with address: {} and mac: {}".format(addr[0], split_message[1]))
                            self.microphones[addr[0]] = split_message[1]
                    elif split_message[0] == "Stop":
                        print("Removing microphone with address: {} and mac: {}".format(addr[0], split_message[1]))
                        self.remove_microphone(addr[0])
                    else:
                        self.unknown_message(message)
                else:
                    self.unknown_message(message)

        except KeyboardInterrupt:
            print("You pressed Ctrl+C")
        finally:
            sock.close()

    def shutdown(self):
        self.is_running = False
        message = "Shutdown"
        sock = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP
        sock.sendto(message.encode(), ("127.0.0.1", self.udp_port))

    def get_microphones(self):
        return self.microphones

    def remove_microphone(self, ip):
        try:
            self.microphones.pop(ip)
        except KeyError:
            print("There is no {} in map".format(ip))

    def unknown_message(self, message):
        print("Receive unknown message: {}".format(message))
