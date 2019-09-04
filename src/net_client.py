#!/usr/bin/python
# -*- coding: utf-8 -*-

import sock_utils as su
import pickle as p
import struct

class server:
    
    def __init__(self, address, port):
        self._address = address
        self._port = port
        self._sock = None

        
    def connect(self):
        """
            Creates the server socket
        """
        self._sock = su.create_tcp_client_socket(self._address, self._port)

    def send_receive(self, data):
        """
            It sends the data through the connection socket, and returns 
            the answer received by the endpoint.
        """
        mens = p.dumps(data, -1)
        size_mens = struct.pack("!i", len(mens))
        self._sock.sendall(size_mens)
        self._sock.sendall(mens)

        size_bytes = su.receive_all(self._sock, 4)
        size = struct.unpack("!i", size_bytes)[0]

        msg = su.receive_all(self._sock, size)
        obj = p.loads(msg)

        return list(obj)
    
    def close(self):
        """
            Closes the communication
        """
        self._sock.close()


