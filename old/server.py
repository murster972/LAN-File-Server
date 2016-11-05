#!/usr/bin/env python3
from hashlib import sha1
from random import randint
import threading
import socket
import sys
import os

#USE INHERITANCE NOT GLOBAL VARIABLES
all_client_ids = {}

class Server:
    def __init__(self):
        #sets up server
        s_addr = (input("IP: "), int(input("Port: ")))
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(s_addr)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.listen(5)

        self.BUFF_SIZE = 1024

        self.new_clients()

    def new_clients(self):
        client_numb = 0

        try:
            while True:
                print("[*] Waiting for a new client to connect")
                client, client_addr = self.s.accept()

                #gets client MAC address to create user-id
                #TOADD: make client_id 48-bits
                client_mac = int(client.recv(self.BUFF_SIZE).decode("utf-8"))
                client_id = str(client_mac * randint(1, client_mac)).encode("utf-8")
                client_id_hash = sha1(client_id).hexdigest()
                all_client_ids[client_id_hash] = client

                #add two threads, one for sending, one for receiving
                print("[*] Client connected, id: {}".format(client_id_hash))
                #self.clients[client_numb] = client
                c_thread = threading.Thread(target=ClientHandler, args=[client, client_addr, self. BUFF_SIZE, client_id_hash], daemon=True)
                c_thread.start()
                #client_numb += 1

        except (KeyboardInterrupt, OSError):
            #TOADD: send message to all clients that server is closing
            #TOADD: Wait for all operations to complete first or ask if they wish to force close
            print("[-] An error has occured.")

        finally:
            self.s.close()
            print("[*] Server Closed.")

class ClientHandler(Server):
    'Handles clients'
    def __init__(self, client, client_addr, buff_size, client_id):
        self.client = client
        self.client_addr = client_addr
        self.buff_size = buff_size
        self.client_id = client_id

        self.client.send("[*] SERVER: Connected to server, your client-id is {}".format(self.client_id).encode("utf-8"))

        cmd = " "
        try:
            while cmd:
                cmd = self.client.recv(self.buff_size).decode("utf-8")
                if cmd == "exit": break
                if cmd == "ls": self.list_files()
                elif cmd == "download": self.send_file()
                elif cmd == "upload": self.client.send("[*] Upload is not avaible yet".encode("utf-8"))
                elif cmd == "help" or cmd == "?":
                    reply = "Commands\nls - show avaible files\ndownload - download file\nupload - upload file\nhelp - show commands\nexit - close client\n"
                    self.client.send(reply.encode("utf-8"))
                else:
                    self.client.send("[-] Unrecongized command: {}".format(cmd).encode("utf-8"))

                print("[+] Client {}: {}".format(self.client_id, cmd))
        except (ConnectionError, BrokenPipeError):
            print("[-] An error occured with the socket.")
        finally:
            self.client.close()
            del all_client_ids[self.client_id]
            print("[*] Client {} closed".format(self.client_id))

    def send_file(self):
        'sends file to client'
        self.list_files()
        filename = self.client.recv(self.buff_size).decode("utf-8")

        try:
            to_send = open("Test Files/{}".format(filename), 'rb')
            self.client.send("0".encode("utf-8"))
            try:
                pass
            finally:
                pass

        except FileNotFoundError:
            self.client.send("-1".encode("utf-8"))

    def recieve_file(self):
        pass

    def list_files(self):
        #TOADD: Allow user to pick directories
        files = os.popen("ls 'Test Files'").read().encode("utf-8")
        self.client.send(files)

    def display_help(self):
        pass

def main():
    os.system("clear")
    #checks script is running with sudo rights
    if os.getuid() != 0:
        print("Script should be ran with 'sudo' or root")
        opt = input("Try to run script with sudo[y/n]: ")
        if opt == "Y" or opt == "y":
            #TOADD: check if user is in correct dir to run server script
            os.system("sudo python3 server.py")
            sys.exit(0)
        else:
            print("Ending script.")
            sys.exit(1)
    else:
        Server()

if __name__ == '__main__':
    main()
