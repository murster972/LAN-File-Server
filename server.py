#!/usr/bin/env/python3
from FileOperations import FileOperations as FileOps
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
    root_folder = ""

    def __init__(self):
        try:
            ip = input("Sever IP: ")
            port = int(input("Server Port Number: "))

            if not self.valid_ip_addr(ip):
                print("[-] Invalid Ip address")
                sys.exit(1)

            FileServer.root_folder = input("Server root directory: ")
            if os.system("ls {}".format(FileServer.root_folder)):
                print("[-] Root directory not found: {}".format(FileServer.root_folder))
                sys.exit(1)

            self.server_addr = (ip, port)
            #HARDCODED FOR TESTING ONLY
            #self.server_addr = ("", 1020)
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

    def valid_ip_addr(self, ip):
        'checks that the user has entered a valid ip address'
        quads = ip.split(".")

        try:
            a = int("".join(quads))
            if len(quads) == 4:
                for i in quads:
                    if int(i) > 255 or int(i) < 0:
                        return False
                return True
            else:
                return False
        except ValueError:
            return False

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
                    #TOADD: send filesize to client so they can check they have room
                    filename = self.client_sock.recv(FileServer.segement_size).decode("utf-8")
                    if filename == " ":
                        continue
                    #TOADD: change os.popen() so command filename is checked before input as it could allow command injection
                    file_exists = os.popen('find "{}" -maxdepth 1 -name "{}" 2>/dev/null'.format(FileServer.root_folder, filename)).read()
                    #file_exists = 1
                    if not file_exists:
                        self.client_sock.send("[-] The following file does not exist: {}".format(filename).encode("utf-8"))
                        continue
                    else:
                        self.client_sock.send("1".encode("utf-8"))
                        FileOps.send_file("{}/{}".format(FileServer.root_folder, filename), self.client_sock, self.segement_size)
                        print("[+] Client-{} has downloaded the following file: {}".format(self.client_id, filename))
                        continue
                elif cmd == "ul":
                    #TOADD: get filesize from client so can check there's enough room
                    filename = self.client_sock.recv(FileServer.segement_size).decode("utf-8")
                    if set(filename) != set(" "):
                        FileOps.recieve_file("{}/{}".format(FileServer.root_folder, filename), self.client_sock, FileServer.segement_size)
                        print("[+] Client-{} successfully uploaded the following file: {}".format(self.client_id, filename))
                    else:
                        print("[-] Client-{} failed to upload an unkown file".format(self.client_id))
                    continue
                elif cmd == "ls":
                    #BUG: Server hangs if an empty dir is passed with 'ls'
                    reply = os.popen("ls '{}'".format(FileServer.root_folder)).read()
                    if not reply:
                        reply = "[-] No Files avaiable for client to download"
                elif cmd == "hp" or cmd == "?":
                    reply = "[*] The following commands are avaible:\n        dl - download file\n        ul - upload file\n        ls - list files\n        cl - clear screen\n        hp or ? - show avaible commands\n        e or exit - exit\n"
                else:
                    reply = "[-] The following command was not recognised: {}\n    Use the command 'help' or '?' to see avaible commands".format(cmd)
                self.client_sock.send(reply.encode("utf-8"))

        except (ConnectionError, BrokenPipeError) as err:
            print("[-] Unable to connect to client {}".format(self.client_id))
        finally:
            #TOADD: check if any operations and tell client servers closing
            self.client_sock.close()
            print("[*] Client {} closed".format(self.client_id))

def main():
    #checks if script is being ran with sudo or by root
    if os.getuid() == 0:
        os.system("clear")
        FileServer()
    else:
        print("[*] The server may not work correctly if not ran as root.")
        try:
            opt = input("Would you like to try run the server as root? [y/n]: ")
            if opt == "y" or opt == "Y":
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
