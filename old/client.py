#!/usr/bin/env python3
from uuid import getnode as get_mac
import threading
import socket
import os

#TOADD: Two threads, one for sending and one for receiving
#       Sending thread is used by user when typing and sendning messages
#       Receiving thread runs in background and prints messages when the user
#       is not typing, or staright away if urgent

class Client:
    def __init__(self):
        server_addr = (input("Server IP: "), int(input("Server Port: ")))
        #TOADD: add check for buffsize to make sure client and server size is the same
        self.buff_size = 1024

        self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.c.connect(server_addr)

        #send MAC address for client-id
        self.c.send(str(get_mac()).encode("utf-8"))

        init_msg = self.c.recv(self.buff_size).decode("utf-8")
        print(init_msg)

        #data to send to server
        self.to_send = []

        cmd = " "
        while cmd:
            try:
                cmd = input("Command: ").lower()
                self.c.send(cmd.encode("utf-8"))

                if cmd == "exit": break

                reply = self.c.recv(self.buff_size).decode("utf-8")

                if cmd == "ls": self.display_files(reply)
                #elif cmd == "download" or cmd == "upload":
                elif cmd == "download":
                    self.display_files(reply)
                    self.recieve_file()
                else:
                    print(reply)

            except ConnectionError:
                print("[-] Unable to connect to server.")
                break
            except KeyboardInterrupt:
                break
        print("[*] Client Closed.")
        self.c.close()

    def send(self):
        '''Checks every [insert number]seconds if theres anything to be sent and sends it if so'''
        pass

    def recieve_file(self):
        '''Recieves file from server'''
        filename = input("File to Download: ")
        self.c.send(filename.encode("utf-8"))

        reply = self.c.recv(self.buff_size).decode("utf-8")
        if reply == "0":
            segements = []
            seg = self.client.recv("")

        else:
            print("[-] File name {} not found".format(filename))

    def display_files(self, ls_output):
        'displays the ouptput of server ls command correctly'
        #TOADD: make sure ls command doesnt overflow screen
        #       use 'less' command with output
        print(ls_output)

def main():
    os.system("clear")
    Client()

if __name__ == '__main__':
    main()
