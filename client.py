#!/usr/bin/env python3
from FileOperations import FileOperations as FileOps
from uuid import getnode as get_mac
from threading import Thread
from random import randint
import socket
import sys
import os


class Client:
    'Client used to connect to FileServery'
    def __init__(self):
        #TOADD: possibly change var name or class name
        #HARDCODED FOR TESTING ONLY
        server_addr = ("", 1020)
        #server_addr = (input("Server IP: "), int(input("Server Port Number: ")))
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        #for testing only, user will choose what dir to save to
        self.SAVETO = "/home/muzza/Documents/programming/python/networking/Test Files received"
        #android save
        #self.SAVETO = "sdcard"

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
                if opt == "cl":
                    os.system("clear")
                    continue
                self.client.send(opt.encode("utf-8"))
                if opt == "e" or opt == "exit": break
                if opt == "dl" or opt == "ul":
                    filename = input("File to {}: ".format(opt))
                if opt == "dl":
                    self.client.send(filename.encode("utf-8"))
                    file_exists = self.client.recv(self.segement_size).decode("utf-8")
                    if file_exists == "1":
                        FileOps.recieve_file("{}/{}".format(self.SAVETO, filename), self.client, self.segement_size)
                        print("[+] File downloaded successfully")
                    else:
                        print(file_exists)
                    continue
                elif opt == "ul":
                    if FileOps.file_exists(filename):
                        self.client.send(filename.encode("utf-8"))
                        FileOps.send_file(filename, self.client, self.segement_size)
                        print("[+] File uploaded successfully")
                    else:
                        self.client.send(" ".encode("utf-8"))
                        print("[-] Unable to upload as the file could not be found: {}".format(filename))
                    #self.client.send(filename.encode("utf-8"))
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

if __name__ == '__main__':
    os.system("clear")
    Client()
