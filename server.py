#!/usr/bin/env/python3
from random import randint
from hashlib import sha1
from threading import Thread
import socket
import sys
import os

class FileServer:
    'File server used by clients'
    #list of all clients connected to server and all operations currently between server and clients
    client_list = {}
    current_operations = {}
    segement_size = 1024
    #state of server, checked by client handlers, if 1 server is running if 0 server is closeed/closing
    server_state = 0
    root_folder = "/home/muzza/Documents/programming/python/networking/Test Files"

    def __init__(self):
        #TOADD: add error checking for server address
        try:
            #self.server_addr = (input("Server IP: "), int(input("Server Port Number: ")))
            #HARDCODED FOR TESTING ONLY
            self.server_addr = ("", 1020)
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind(self.server_addr)
            self.server.listen(5)

        except KeyboardInterrupt:
            #prints newline and exits
            print("")
            sys.exit(0)

        except ValueError:
            print("[-] Invalid server port number")
            sys.exit(1)

        except OSError as err:
            print("[-] Server unable to bind to address {}\n    As the following error occured:\n        {}".format(server_addr, err))
            sys.exit(1)

        FileServer.server_state = 1

        self.listen_clients()

    def listen_clients(self):
        'Listens for new clients, and performs steps allowing them to connect to server'
        print("[*] Server listening for clients at: {}".format(self.server_addr))
        try:
            while True:
                client_sock, client_addr = self.server.accept()

                new_client = Thread(target=ClientHandler, args=[client_sock], daemon=True)
                new_client.start()

        except OSError as err:
            print("[-] The following error has occured:        {}".format(err))

        except KeyboardInterrupt:
            #TOADD: if any operations are happening ask if they should be finished before closing server
            pass

        finally:
            #TOADD: Send message to all clients saying server is closing
            self.server_state = 0
            print("[*] Server closed.")
            self.server.close()

class ClientHandler(FileServer):
    'Handles all clients connected to server, including client requests and '
    def __init__(self, client_sock):
        #TOADD: establish encryption protocols when connecting to client
        #TOADD: check server and client seg size are the same
        #get client mac-address to create client-id
        self.client_sock = client_sock

        client_mac = int(self.client_sock.recv(FileServer.segement_size).decode("utf-8"))
        self.client_id = sha1(str(client_mac * randint(1000, 9999)).encode("utf-8")).hexdigest()
        FileServer.client_list[self.client_id] = self.client_sock

        print("[*] Client {} has connected to the server".format(self.client_id))

        #self.client_sock.send(self.client_id.encode("utf-8"))
        self.client_sock.send("[+] Connected to server, you client-id is: {}".format(self.client_id).encode("utf-8"))

        #two threads, one two listen for client requests and one to watch for a change in server state
        c_cmds = Thread(target=self.client_commands, daemon=1)
        c_cmds.start()
        #watch_server = Thread(target=self.watch_server_state, daemon=1)
        #watch_server.start()

    def client_commands(self):
        'listens for and handles all client commands'
        try:
            while True:
                cmd = self.client_sock.recv(FileServer.segement_size).decode("utf-8")
                print("[*] {} - {}".format(self.client_id, cmd))
                if cmd == "dl":
                    filename = self.client_sock.recv(FileServer.segement_size).decode("utf-8")
                    file_exists = os.popen('find "{}" -maxdepth 1 -name "{}"'.format(FileServer.root_folder, filename)).read()
                    if not file_exists:
                        self.client_sock.send("[-] The following file does not exist: {}".format(filename).encode("utf-8"))
                        continue
                    else:
                        self.client_sock.send("1".encode("utf-8"))
                        self.send_file(filename)
                        continue
                elif cmd == "ul":
                    pass
                elif cmd == "ls":
                    reply = os.popen("ls '{}'".format(FileServer.root_folder)).read()
                elif cmd == "hp" or cmd == "?":
                    reply = "[*] The following commands are avaible:\n        dl - download file\n        ul - upload file\n        ls - list files\n        hp or ? - show avaible files\n        e or exit - exit\n"
                else:
                    reply = "[-] The following command was not recognised: {}\n    Use the command 'help' or '?' to see avaible commands".format(cmd)
                self.client_sock.send(reply.encode("utf-8"))

        except (ConnectionError, BrokenPipeError) as err:
            print("[-] Unable to connect to client {}".format(self.client_id))
        finally:
            #TOADD: check if any operations and tell client servers closing
            self.client_sock.close()
            print("[*] Client {} closed".format(self.client_id))

    def send_file(self, filename):
        print("[*] {} - Sending the following file to this client: {}".format(self.client_id, filename))

        segs = self.get_segements(filename)
        for i in segs:
            self.client_sock.send(i)
        end = b''.ljust(FileServer.segement_size, b'\0')
        self.client_sock.send(end)
        print("[*] Client {} has downloaded the following file: {}".format(file))

    def recieve_file(self):
        pass

    def watch_server_state(self):
        pass

    def get_segements(self, filename):
        'splits file into segements'
        segs = []

        with open("{}/{}".format(FileServer.root_folder, filename), 'rb') as f:
            while True:
                s = f.read(FileServer.segement_size)
                if not s: break
                segs.append(s)

        #add padding to last segment
        if len(segs[::-1][0]) < FileServer.segement_size:
            segs[len(segs) - 1] = segs[len(segs) - 1].ljust(FileServer.segement_size)
        return segs

def main():
    #checks if script is being ran with sudo or by root
    if os.getuid() == 0:
        os.system("clear")
        FileServer()
    else:
        print("[*] The server may not work correctly if not ran as root.")
        try:
            #Bug: Python 2.x doesnt interp input as string unless quotes are round
            #     e.g. 2.x interps the input Yes as as var name instead of a string
            opt = input("Would you like to try run the server as root? [y/n]: ")
            if opt == "y" or opt == "Y":
                #TOADD: allow use to specify server.py location
                print("[*] Trying to run as root")
                os.system("sudo python3 server.py")
            else:
                os.system("clear")
                print("[*] Running without root")
                FileServer()
        except KeyboardInterrupt:
            print("")
            sys.exit(0)

if __name__ == '__main__':
    main()
