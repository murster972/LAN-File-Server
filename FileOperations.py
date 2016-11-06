#!/usr/bin/env python3
import os

"""
TODO: check filename doesnt allow client to traverse backwards through directories,
      i.e. old/../../../../../../../../
      from this dir would travers back to the root dir
"""

class FileOperations:
    '''Mehtods for file operations used by the client and server'''
    def __init__(self, sock, segement_size):
        ''':param sock: sock used to send/recieve a file
           :param segement_size: size of segements in Bytes'''
        self.sock = sock
        self.segement_size = segement_size

    def send_file(self, filename):
        '''sends file using socket
           :param filename: name of file being sent'''
        pass

    def recieve_file(self, filename):
        ''' recieves segements of a file through socket,
            then reassembles segements and writes data to file
            :param filename: name of file being uploaded'''
        pass

    def segement_file(self, filename):
        '''Segements a file into bytes of size segement_size'''
        segs = []

        with open("{}".format(filename), 'rb') as f:
            while True:
                s = f.read(self.segement_size)
                if not s: break
                segs.append(s)

        segs[len(segs) - 1] = segs[len(segs) - 1].ljust(self.segement_size)
        return segs

    def avaiable_files(self, dirname):
        '''returns the files at the directory passed as an arg
           :param dirname: directory to search'''
        return os.popen('ls "{}" 2>/dev/null'.format(dirname)).read()

    def file_exists(self, filename):
        '''returns True if file exists else False
           :param filename: file to check'''
        return os.system('ls "{}" 2>/dev/null'.format(filename)) == 0

#checking inheritance will work for client and server classes
class testClass(FileOperations):
    def __init__(self):
        self.server_sock = "test"
        self.segement_size = 2048
        super().__init__(self.server_sock, self.segement_size)

if __name__ == '__main__':
    f = testClass()
    print(f.sock)
    print(f.segement_size)
    print(f.avaiable_files("."))
