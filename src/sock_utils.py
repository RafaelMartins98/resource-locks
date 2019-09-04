#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket as s

def create_tcp_server_socket(address, port, queue_size):
    '''
        :param address: IP Address associated to the server side
        :param port: Address port the server will use to communicate
        :param queue_size: Maximum queue size
        :return: server socket
    '''
    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
    sock.bind((address, port))
    sock.listen(queue_size)

    return sock

def create_tcp_client_socket(address, port):
    '''
        :param address: IP Address associated to the client side
        :param port: Address port the client will use to communicate
        :return: client socket
    '''

    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    sock.connect((address, port))

    return sock

def receive_all(socket, length):
    '''
        :param socket: buffer for readings
        :param length: Maximum size of bytes that can be read and sent
        :return:
    '''
    try:
        return socket.recv(length)
    except s.timeout:
        print("Timeout Error\n")
    except s.error:
        print("Error while fetching data\n")