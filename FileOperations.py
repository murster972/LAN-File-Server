#!/usr/bin/env python3
import socket
import os

"""
TODO: check filename doesnt allow client to traverse backwards through directories,
      i.e. old/../../../../../../../../
      from this dir would travers back to the root dir
"""

class FileOperations:
    '''Methods used for file operations, used by the client and server'''
    def send_file(filename, sock, segement_size):
        '''sends file using socket
           :param filename: name of file being sent
           :param sock: sock used to send a file
           :param segement_size: size of segements in Bytes'''
        segs = FileOperations.segement_file(filename, segement_size)

        for i in segs:
            sock.send(i)
        sock.send(b'\0'.ljust(segement_size, b'\0'))

    def recieve_file(filename, sock, segement_size):
        ''' recieves segements of a file through socket,
            then reassembles segements and writes data to file
            :param filename: name of file being uploaded
            :param sock: sock used to recieve a file
            :param segement_size: size of segements in Bytes'''
        segs = []

        while True:
            s = sock.recv(segement_size)
            if set(s) == set(b'\0'): break
            segs.append(s)

        #TOADD: ask user if they want to overwrite of file already exists
        f = open(filename, "wb")
        for i in segs: f.write(i)
        f.close()

    def segement_file(filename, segement_size):
        '''Segements a file into bytes of size segement_size'''
        segs = []

        with open("{}".format(filename), 'rb') as f:
            while True:
                s = f.read(segement_size)
                if not s: break
                segs.append(s)

        segs[len(segs) - 1] = segs[len(segs) - 1].ljust(segement_size)
        return segs

    def avaiable_files(dirname):
        '''returns the files at the directory passed as an arg
           :param dirname: directory to search'''
        return os.popen('ls "{}" 2>/dev/null'.format(dirname)).read()

    def file_exists(filename):
        '''returns True if file exists else False
           :param filename: file to check'''
        return os.system('ls "{}" 2>/dev/null'.format(filename)) == 0

if __name__ == '__main__':
    s = testServer()
