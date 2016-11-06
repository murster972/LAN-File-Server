#!/usr/bin/env python3
from uuid import getnode as get_mac
from threading import Thread
import socket
import sys
import os

class Client:
    'Client used to connect to FileServer'
    def __init__(self):
        #TOADD: possibly change var name or class name
        #HARDCODED FOR TESTING ONLY
        server_addr = ("", 1020)
        #server_addr = (input("Server IP: "), int(input("Server Port Number: ")))
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.client.connect(server_addr)
        except socket.error as msg:
            print("[-] Unable to connet to server as the following error occured:\n    {}".format(msg))
            sys.exit(1)
        except ConnectionRefusedError:
            print("[-] Unable to connect to server at the address: {}".format(server_addr))
            sys.exit(1)

        self.segement_size = 1024

        #TOADD: establish encryption protocols when connecting to server
        #send mac-address once connections been established
        self.client.send(str(get_mac()).encode("utf-8"))
        #self.id = self.client.recv(self.segement_size).decode("utf-8")
        welcome_msg = self.client.recv(self.segement_size).decode("utf-8")
        print(welcome_msg)

        self.menu()
        #TOADD: create thread to watch server state

    def menu(self):
        try:
            while True:
                opt = input("command: ").strip()
                self.client.send(opt.encode("utf-8"))
                if opt == "e" or opt == "exit": break
                if opt == "dl" or opt == "ul":
                    filename = input("File to {}: ".format(opt))
                if opt == "dl":
                    self.recieve_file(filename)
                    print("test")
                elif opt == "ul":
                    pass
                else:
                    reply = self.client.recv(self.segement_size).decode("utf-8")
                    print(reply)

        except OSError as err:
            print("[-] The client or server has caused the following error to occur:\n        {}".format(err))
        except KeyboardInterrupt:
            pass
        finally:
            #TOADD: send message to server saying client is closing
            self.client.close()
            print("[*] Client closed.")
            sys.exit(0)

    def send_file(self):
        pass

    def recieve_file(self, filename):
        self.client.send(filename.encode("utf-8"))
        file_exists = self.client.recv(self.segement_size).decode("utf-8")

        if file_exists[0] != "1":
            print("test" + file_exists)
        else:
            segs = []
            i = 0

            #TOADD: progress bar
            #TOADD: Posibly change so that instead of segements its a stream of single
            while True:
                s = self.client.recv(self.segement_size)
                if set(s) == set(b'\0'):
                    break
                segs.append(s)
                i += 1

            #TOADD: let client choose dir to download file to
            f = open("/home/muzza/Documents/programming/python/networking/Test Files received/{}".format(filename), 'wb')
            for i in segs: f.write(i)
            f.close()
            print("[*] The following file has been download: {}".format(filename))

    def watch_server_state(self):
        pass

if __name__ == '__main__':
    os.system("clear")
    Client()
