import socket
import threading


class UDPReceiver(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.is_running = True
        self.udp_ip = ""
        self.udp_port = 5005
        self.microphones = []

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
                if data.decode() == "Start":
                    self.microphones.append(addr[0])
                elif data.decode() == "Stop":
                    self.remove_microphone(addr[0])
        except KeyboardInterrupt:
            print("You pressed Ctrl+C")
        finally:
            sock.close()

    def shutdown(self):
        self.is_running = False
        message = "Shutdown"
        sock = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_DGRAM)  # UDP
        sock.sendto(message.encode(), (self.udp_ip, self.udp_port))

    def get_microphones(self):
        return self.microphones

    def remove_microphone(self, ip):
        try:
            self.microphones.remove(ip)
        except ValueError:
            print("There is no {} in list".format(ip))
